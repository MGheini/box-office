 
from django.shortcuts import render
from django.http import HttpResponse

from . import models
from users.models import Member
from users.forms import LoginForm
from services.forms import EventModelForm


def get_layout():
	categories = models.Category.objects.all()
	most_populars = models.Event.objects.order_by('event_avg_rate')[:5]
	newest = models.Event.objects.order_by('submit_date')[:5]

	return {'categories': categories, 'newest': newest, 'most_populars': most_populars}

def home(request):
	layout = get_layout()
	form = LoginForm()

	# felan hameye event ha ra dar nazar darim, ba'dan bayad available haa neshun dade beshe
	available_events = models.Event.objects.all()

	return render(request, 'home.html',
		{'form': form,
		'home': True,
		'visitor': True,
		'member': False,
		'organizer': False,
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