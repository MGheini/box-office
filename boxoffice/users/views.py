 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def register(request):
	return render(request, 'register.html', {})

def our_logout(request):
	return HttpResponseRedirect('/')
