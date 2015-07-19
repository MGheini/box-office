 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import MemberRegModelForm, OrganizerRegModelForm

def register(request):
	member_form = MemberRegModelForm()
	organizer_form = OrganizerRegModelForm()
	return render(request, 'register.html', {'member_form': member_form, 'organizer_form': organizer_form})

def our_logout(request):
	return HttpResponseRedirect('/')