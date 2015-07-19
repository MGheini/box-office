 
from django.contrib import admin

from .models import Event, Feedback, Ticket, Order

admin.site.register(Event)
admin.site.register(Feedback)
admin.site.register(Ticket)
admin.site.register(Order)