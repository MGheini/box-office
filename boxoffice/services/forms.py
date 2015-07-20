from django import forms
from .models import Event, Ticket

class TicketModelForm(forms.ModelForm):

	class Meta:
		model = Ticket
		fields = ['ticket_type', 'ticket_price', 'total_capacity']

class EventModelForm(forms.ModelForm):
	# ticket = forms.CharField(required=True, label='ربلیت‌ها', widget=forms.Select)
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
			'ticket': 'بلیت‌ها',
		}
		widgets = {
          		'event_description': forms.Textarea(attrs={'rows':4, 'maxlength': 255, 'placeholder': ' مثلا: نیم ساعت قبل از شروع برنامه در سالن حضور داشته باشید.'}),
			'event_deadline': forms.TextInput(attrs={'id':'date_input', 'placeholder': '2015-07-06 22:54'}),
			'event_date': forms.TextInput(attrs={'id':'date_input_2', 'placeholder': '2015-07-06 22:54'}),
			'event_place': forms.TextInput(attrs={'placeholder': ' استادیوم آزادی'}),
			'event_title': forms.TextInput(attrs={'placeholder': ' مسابقه والیبال ایران-آمریکا'}),
        	}
