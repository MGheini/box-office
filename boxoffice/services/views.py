 
from django.shortcuts import render
from django.http import HttpResponse

from users.forms import LoginForm

def home(request):
	form = LoginForm()
	return render(request, 'home.html', {'form': form, 'home': True, 'visitor': True, 'member': False, 'organizer': False})

def answer(request):
	form = LoginForm()
	return render(request, 'FAQ.html', {'form': form, 'visitor': True})

def about_us(request):
	form = LoginForm()
	return render(request, 'Gisheh.html', {'form': form, 'visitor': True})

def event_details(request, event_id):
	return render(request, 'view-event-details.html', {})

def purchase(request, event_id):
	return render(request, 'buy-ticket.html', {})

def rate(request, event_id):
	return HttpResponse('rate')

def post(request, event_id):
	return HttpResponse('post')

def category(request, category):
	return render(request, 'view-category-events.html', {})

def subcategory(request, category, subcategory):
	return render(request, 'view-category-events.html', {})

def submit(request):
	return render(request, 'submit-new-event.html', {})

def receipt(request, order_id):
	return render(request, 'view-receipt.html', {})

def history(request):
	return render(request, 'purchase-history.html', {'member': True})