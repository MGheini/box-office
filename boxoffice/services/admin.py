 
from django.contrib import admin

from .models import Event, Feedback, Ticket, Order, Category, SubCategory

admin.site.register(Event)
admin.site.register(Feedback)
admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(SubCategory)