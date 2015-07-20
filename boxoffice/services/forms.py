from django import forms
from .models import Event

class EventModelForm(forms.ModelForm):
	
	class Meta:
		model = Event
		exclude = ['submit_date', 'organizer']
		fields = ['event_title', 'category', 'subcategory', 'event_image', 'event_place', 'event_date', 'event_description', 'event_deadline']
		labels = {
			'event_title': 'عنوان رویداد',
			'category': 'دسته',
			'subcategory': 'زیردسته',
			'event_image': 'تصویر',
			'event_place': 'محل برگزاری',
			'event_description': 'توضیحات تکمیلی',
			'event_deadline': 'آخرین مهلت خرید بلیت',
			'event_date': 'زمان برگزاری',
		}