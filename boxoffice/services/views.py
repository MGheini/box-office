 
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	return HttpResponse('home')

def answer(request):
	return HttpResponse('FAQ')

def about_us(request):
	return HttpResponse('Gisheh')

def event_details(request, event_id):
	return HttpResponse('event details')

def purchase(request, event_id):
	return HttpResponse('purchse')

def rate(request, event_id):
	return HttpResponse('rate')

def post(request, event_id):
	return HttpResponse('post')

def category(request, category):
	return HttpResponse('category')

def subcategory(request, category, subcategory):
	return HttpResponse('subcategory')

def submit(request):
	return HttpResponse('submit')

def receipt(request, order_id):
	return HttpResponse('receipt')

def history(request):
	return HttpResponse('history')
