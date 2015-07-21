 
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from .models import Event, Feedback, Ticket, Order, Category, SubCategory

class EventAdmin(admin.ModelAdmin):
	list_filter = ('category', 'subcategory', 'organizer')

class OrderAdmin(admin.ModelAdmin):
	list_filter = ('order_date', ('order_date', DateRangeFilter))
	

admin.site.register(Event, EventAdmin)
admin.site.register(Feedback)
admin.site.register(Ticket)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
