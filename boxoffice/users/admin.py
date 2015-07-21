
from django.contrib import admin
from .models import Member, Organizer

class MemberAdmin(admin.ModelAdmin):

	list_display = ['username', 'gender_fa', 'email', 'date_joined', 'pre_phone_number', 'phone_number']

	def pre_phone_number(self, obj):
		return obj.pre_phone_number
	pre_phone_number.short_description = 'پیش‌شماره'

	def phone_number(self, obj):
		return obj.phone_number
	phone_number.short_description = 'شماره تلفن'

	def gender_fa(self, obj):
		return obj.gender
	gender_fa.short_description = 'جنسیت'

	def username(self, obj):
		return obj.user.username
	username.short_description = 'نام کاربری'
    
	def first_name(self, obj):
		return obj.user.first_name
	first_name.short_description = 'نام'

	def last_name(self, obj):
		return obj.user.last_name
	last_name.short_description = 'نام خانوادگی'

	def email(self, obj):
		return obj.user.email
	email.short_description = 'رایانامه'

	def date_joined(self, obj):
		return obj.user.date_joined
	date_joined.short_description = 'زمان عضویت'


class OrganizerAdmin(admin.ModelAdmin):

	list_display = ['username', 'date_joined', 'organization_name_fa', 'organization_reg_num_fa']

	def organization_name_fa(self, obj):
		return obj.organization_name
	organization_name_fa.short_description = 'نام موسسه'

	def organization_reg_num_fa(self, obj):
		return obj.organization_reg_num
	organization_reg_num_fa.short_description = 'شماره ثبت'

	def username(self, obj):
		return obj.user.username
	username.short_description = 'نام کاربری'
    
	def date_joined(self, obj):
		return obj.user.date_joined
	date_joined.short_description = 'زمان عضویت'

admin.site.register(Member, MemberAdmin)
admin.site.register(Organizer, OrganizerAdmin)
