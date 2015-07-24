 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from . import models
from .forms import MemberRegModelForm, OrganizerRegModelForm, LoginForm

def our_login(request):
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
		return render(request, 'home.html', {'form': form, 'home': True, 'visitor': True, 'bad_login': True})
	return render(request, 'home.html', {'form': form, 'home': True, 'visitor': True, 'bad_login': True})

def register(request):
	member_form = MemberRegModelForm()
	organizer_form = OrganizerRegModelForm()
	form = LoginForm()
	return render(request, 'register.html', {'member_form': member_form, 'organizer_form': organizer_form, 'form': form, 'visitor': True})

def our_logout(request):
	return HttpResponseRedirect('/')