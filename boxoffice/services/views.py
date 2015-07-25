 
from django.shortcuts import render
from django.http import HttpResponse

from . import models
from users.models import Member
from users.forms import LoginForm
from services.forms import EventModelForm


def get_layout():
	categories = models.Category.objects.all()

	return {'categories': categories}

def home(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'home.html',
		{'form': form,
		'home': True,
		'visitor': True,
		'member': False,
		'organizer': False,
		'categories': layout['categories']})

def answer(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'FAQ.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories']})

def about_us(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'Gisheh.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories']})

def event_details(request, event_id):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-event-details.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories']})

def purchase(request, event_id):
	layout = get_layout()
	return render(request, 'buy-ticket.html',
		{'member': True,
		'categories': layout['categories']})

def rate(request, event_id):
	return HttpResponse('rate')

def post(request, event_id):
	return HttpResponse('post')

def category(request, category):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-category-events.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories']})

def subcategory(request, category, subcategory):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-sub-category-events.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories']})

def submit(request):
	layout = get_layout()
	event_form = EventModelForm()
	return render(request, 'submit-new-event.html',
		{'event_form': event_form,
		'organizer': True,
		'categories': layout['categories']})


def receipt(request, order_id):
	layout = get_layout()
	return render(request, 'view-receipt.html',
		{'member': True,
		'categories': layout['categories']})

def history(request):
	layout = get_layout()
	return render(request, 'purchase-history.html',
		{'member': True,
		'categories': layout['categories']})