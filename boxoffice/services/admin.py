 
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

from .models import Event, Feedback, Ticket, Order, Category, SubCategory

class EventAdmin(admin.ModelAdmin):
	list_filter = ['submit_date', ('submit_date', DateRangeFilter)]
	list_display = ('organizer_fa', 'event_title_fa', 'event_place_fa', 'event_date_fa', 'event_deadline_fa', 'event_description_fa', 'submit_date_fa', 'category_fa', 'subcategory_fa')

	def organizer_fa(self, obj):
		return obj.organizer
	organizer_fa.short_description = 'برگزارکننده'

	def event_title_fa(self, obj):
		return obj.event_title
	event_title_fa.short_description = 'عنوان اصلی رویداد'

	def event_place_fa(Self, obj):
		return obj.event_place
	event_place_fa.short_description = 'محل برگزاری رویداد'

	def event_date_fa(Self, obj):
		return obj.event_date
	event_date_fa.short_description = 'زمان برگزاری رویداد'

	def event_deadline_fa(Self, obj):
		return obj.event_deadline
	event_deadline_fa.short_description = 'مهلت خرید بلیت'

	def event_description_fa(Self, obj):
		return obj.event_description
	event_description_fa.short_description = 'توضیحات تکمیلی'

	def submit_date_fa(Self, obj):
		return obj.submit_date
	submit_date_fa.short_description = 'زمان ثبت رویداد'

	def category_fa(Self, obj):
		return obj.category
	category_fa.short_description = 'دسته'

	def subcategory_fa(Self, obj):
		return obj.subcategory
	subcategory_fa.short_description = 'زیردسته'


class OrderAdmin(admin.ModelAdmin):
	list_filter = ['order_date', ('order_date', DateRangeFilter)]
	list_display = ('member_fa', 'ticket_fa', 'num_fa', 'total_price_fa', 'order_date_fa')

	def member_fa(self, obj):
		return obj.member
	member_fa.short_description = 'کاربر خریدار'

	def ticket_fa(Self, obj):
		return obj.ticket
	ticket_fa.short_description = 'بلیت'

	def num_fa(Self, obj):
		return obj.num
	num_fa.short_description = 'تعداد خریداری شده'

	def total_price_fa(Self, obj):
		return obj.total_price
	total_price_fa.short_description = 'قیمت کل'

	def order_date_fa(Self, obj):
		return obj.order_date
	order_date_fa.short_description = 'تاریخ خرید'


class TicketAdmin(admin.ModelAdmin):
	list_display = ('event_fa', 'ticket_type_fa', 'total_capacity_fa', 'purchased_num_fa')

	def event_fa(self, obj):
		return obj.event
	event_fa.short_description = 'رویداد مربوطه'

	def ticket_type_fa(Self, obj):
		return obj.ticket_type
	ticket_type_fa.short_description = 'نوع بلیت'

	def total_capacity_fa(Self, obj):
		return obj.total_capacity
	total_capacity_fa.short_description = 'ظرفیت'

	def purchased_num_fa(Self, obj):
		return obj.purchased_num
	purchased_num_fa.short_description = 'تعداد سفارش داده شده'


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('member_fa', 'event_fa', 'rate_fa', 'post_fa')

	def member_fa(Self, obj):
		return obj.member
	member_fa.short_description = 'کاربر'

	def event_fa(Self, obj):
		return obj.event
	event_fa.short_description = 'رویداد'

	def rate_fa(Self, obj):
		return obj.rate
	rate_fa.short_description = 'امتیاز داده شده'

	def post_fa(Self, obj):
		return obj.post
	post_fa.short_description = 'نظر داده شده'

admin.site.register(Event, EventAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)