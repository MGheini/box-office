 
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	return render(request, 'home.html', {})

def answer(request):
	return HttpResponse('FAQ')

def about_us(request):
	return HttpResponse('Gisheh')

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
	return render(request, 'purchase-history.html', {})
