 
from django.shortcuts import render
from django.http import HttpResponse


def register(request):
	return HttpResponse('register')

def our_logout(request):
	return HttpResponse('logout')
