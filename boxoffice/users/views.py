 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import MemberRegModelForm, OrganizerRegModelForm, LoginForm

def register(request):
	member_form = MemberRegModelForm()
	organizer_form = OrganizerRegModelForm()
	form = LoginForm()
	return render(request, 'register.html', {'member_form': member_form, 'organizer_form': organizer_form, 'form': form, 'visitor': True})

def our_logout(request):
	return HttpResponseRedirect('/')