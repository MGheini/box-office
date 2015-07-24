 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from . import models
from users.models import Member
from users.forms import LoginForm
from users.views import our_login
from services.forms import EventModelForm


def get_layout():
	categories = models.Category.objects.all()
	most_populars = models.Event.objects.order_by('event_avg_rate')[:5]
	newest = models.Event.objects.order_by('submit_date')[:5]

	return {'categories': categories, 'newest': newest, 'most_populars': most_populars}

def home(request):
	layout = get_layout()

	# felan hameye event ha ra dar nazar darim, ba'dan bayad available haa neshun dade beshe
	available_events = models.Event.objects.all()

	if request.method == 'POST':
		return our_login(request) # don't forget to return!
	elif request.user.is_authenticated():
		if request.session['user_type'] == 'member':
			return render(request, 'home.html',
				{'home': True,
				'member': True,
				'categories': layout['categories'],
				'available_events': available_events,
				'newest': layout['newest'],
				'most_populars': layout['most_populars']})
		elif request.session['user_type'] == 'organizer':
			return render(request, 'home.html',
				{'home': True,
				'organizer': True,
				'categories': layout['categories'],
				'available_events': available_events,
				'newest': layout['newest'],
				'most_populars': layout['most_populars']})
		else:
			return HttpResponseRedirect('/admin')
	else:
		form = LoginForm()
		return render(request, 'home.html',
			{'from': form,
			'home': True,
			'visitor': True,
			'categories': layout['categories'],
			'available_events': available_events,
			'newest': layout['newest'],
			'most_populars': layout['most_populars']})

def answer(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'FAQ.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def about_us(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'Gisheh.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def event_details(request, event_id):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-event-details.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def purchase(request, event_id):
	layout = get_layout()
	return render(request, 'buy-ticket.html',
		{'member': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def rate(request, event_id):
	return HttpResponse('rate')

def comment(request, event_id):
	return HttpResponse('post')

def category(request, category):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-category-events.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def subcategory(request, category, subcategory):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-sub-category-events.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def submit(request):
	layout = get_layout()
	event_form = EventModelForm()
	return render(request, 'submit-new-event.html',
		{'event_form': event_form,
		'organizer': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})


def receipt(request, order_id):
	layout = get_layout()
	return render(request, 'view-receipt.html',
		{'member': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def history(request):
	layout = get_layout()
	return render(request, 'purchase-history.html',
		{'member': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})
