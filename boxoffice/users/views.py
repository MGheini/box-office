 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from . import models
from services.models import Category, Event
from .forms import MemberRegModelForm, OrganizerRegModelForm, LoginForm

def get_layout():
	categories = Category.objects.all()
	most_populars = Event.objects.order_by('-event_avg_rate')[:4]
	newest = Event.objects.order_by('-submit_date')[:4]

	return {'categories': categories, 'newest': newest, 'most_populars': most_populars}

def our_login(request):
	layout = get_layout()
	available_events = Event.objects.all()

	form = LoginForm(request.POST)

	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if models.Member.objects.filter(user=user).count() == 1:
				request.session['user_type'] = 'member'
			elif models.Organizer.objects.filter(user=user).count() == 1:
				request.session['user_type'] = 'organizer'
			else:
				request.session['user_type'] = 'admin'
			request.method = 'GET'
			return HttpResponseRedirect('/')
		return render(request, 'home.html', {'form': form,
											'home': True,
											'visitor': True,
											'bad_login': True,
											'categories': layout['categories'],
											'available_events': available_events,
											'newest': layout['newest'],
											'most_populars': layout['most_populars']})
	return render(request, 'home.html', {'form': form,
										'home': True,
										'visitor': True,
										'bad_login': True,
										'categories': layout['categories'],
										'available_events': available_events,
										'newest': layout['newest'],
										'most_populars': layout['most_populars']})

def register(request):
	layout = get_layout()

	if request.method == 'POST':
		if 'member-reg-btn' in request.POST:
			form = MemberRegModelForm(request.POST)

			if form.is_valid():
				username = form.cleaned_data['member_username']
				password = form.cleaned_data['member_password']
				email = form.cleaned_data['member_email']
				member = form.save(commit=False)
				user = User.objects.create_user(username=username, email=email, password=password)
				user.first_name = form.cleaned_data['member_first_name']
				user.last_name = form.cleaned_data['member_last_name']
				user.save()
				member.user = user
				member.save()

				user = authenticate(username=username, password=password)
				login(request, user)

				request.session['user_type'] = 'member'
				request.method = 'GET'
				return HttpResponseRedirect('/')
			else:
				organizer_form = OrganizerRegModelForm()
				login_form = LoginForm()
				return render(request, 'register.html', {'member_form': form,
														 'organizer_form': organizer_form,
														 'form': login_form,
														 'visitor': True,
														 'categories': layout['categories'],
														 'newest': layout['newest'],
														 'most_populars': layout['most_populars']})
		else:
			form = OrganizerRegModelForm(request.POST)

			if form.is_valid():
				username = form.cleaned_data['organizer_username']
				password = form.cleaned_data['organizer_password']
				email = form.cleaned_data['organizer_email']
				organizer = form.save(commit=False)
				user = User.objects.create_user(username=username, email=email, password=password)
				user.first_name = form.cleaned_data['organizer_first_name']
				user.last_name = form.cleaned_data['organizer_last_name']
				user.save()
				organizer.user = user
				organizer.save()

				user = authenticate(username=username, password=password)
				login(request, user)

				request.session['user_type'] = 'organizer'
				request.method = 'GET'
				return HttpResponseRedirect('/')
			else:
				member_form = MemberRegModelForm()
				login_form = LoginForm()
				return render(request, 'register.html', {'member_form': member_form,
														 'organizer_form': form,
														 'form': login_form,
														 'visitor': True,
														 'categories': layout['categories'],
														 'newest': layout['newest'],
														 'most_populars': layout['most_populars']})
	else:
		member_form = MemberRegModelForm()
		organizer_form = OrganizerRegModelForm()
		form = LoginForm()
		return render(request, 'register.html', {'member_form': member_form,
												'organizer_form': organizer_form,
												'form': form,
												'visitor': True,
												'categories': layout['categories'],
												'newest': layout['newest'],
												'most_populars': layout['most_populars']})

def our_logout(request):
	logout(request)
	return HttpResponseRedirect('/')