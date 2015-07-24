 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from users.forms import LoginForm
from users.views import our_login
from services.forms import EventModelForm

def home(request):
	if request.method == 'POST':
		return our_login(request) # don't forget to return!
	elif request.user.is_authenticated():
		if request.session['user_type'] == 'member':
			return render(request, 'home.html', {'home': True, 'member': True})
		elif request.session['user_type'] == 'organizer':
			return render(request, 'home.html', {'home': True, 'organizer': True})
		else:
			return HttpResponseRedirect('/admin')
	else:
		form = LoginForm()
		return render(request, 'home.html', {'form': form, 'home': True, 'visitor': True})

def answer(request):
	form = LoginForm()
	return render(request, 'FAQ.html', {'form': form, 'visitor': True})

def about_us(request):
	form = LoginForm()
	return render(request, 'Gisheh.html', {'form': form, 'visitor': True})

def event_details(request, event_id):
	form = LoginForm()
	return render(request, 'view-event-details.html', {'form': form, 'visitor': True})

def purchase(request, event_id):
	return render(request, 'buy-ticket.html', {'member': True})

def rate(request, event_id):
	return HttpResponse('rate')

def post(request, event_id):
	return HttpResponse('post')

def category(request, category):
	form = LoginForm()
	return render(request, 'view-category-events.html', {'form': form, 'visitor': True})

def subcategory(request, category, subcategory):
	form = LoginForm()
	return render(request, 'view-sub-category-events.html', {'form': form, 'visitor': True})

def submit(request):
	event_form = EventModelForm()
	return render(request, 'submit-new-event.html', {'event_form': event_form, 'organizer': True})


def receipt(request, order_id):
	return render(request, 'view-receipt.html', {'member': True})

def history(request):
	return render(request, 'purchase-history.html', {'member': True})