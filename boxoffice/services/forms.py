
from django import forms
from django.forms.models import inlineformset_factory

from .models import Event, Ticket, Category, SubCategory

class TicketModelForm(forms.ModelForm):

	class Meta:
		model = Ticket
		fields = ['ticket_type', 'ticket_price', 'total_capacity']
		labels = {
			'ticket_type': 'نوع بلیت',
			'ticket_price': 'قیمت بلیت',
			'total_capacity': 'ظرفیت',
		}

class EventModelForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['submit_date', 'organizer']
		fields = ['event_title', 'category', 'subcategory', 'event_image', 'event_place', 'event_date', 'event_time', 'event_description', 'event_deadline_date', 'event_deadline_time']
		labels = {
			'event_title': 'عنوان رویداد',
			'category': 'دسته',
			'subcategory': 'زیردسته',
			'event_image': 'تصویر',
			'event_place': 'محل برگزاری',
			'event_description': 'توضیحات تکمیلی',
			'event_deadline_date': 'آخرین مهلت خرید بلیت',
			'event_deadline_time': 'زمان مهلت خرید بلیت',
			'event_date': 'تاریخ برگزاری',
			'event_time': 'زمان برگزاری',
			'ticket': 'بلیت‌ها',
		}
		widgets = {
          		'event_description': forms.Textarea(attrs={'rows':4, 'maxlength': 255, 'placeholder': ' مثلا: نیم ساعت قبل از شروع برنامه در سالن حضور داشته باشید.'}),
			'event_deadline_date': forms.TextInput(attrs={'type': 'date'}),
			'event_deadline_time': forms.TextInput(attrs={'type': 'time'}),
			'event_date': forms.TextInput(attrs={'type': 'date'}),
			'event_time': forms.TextInput(attrs={'type': 'time'}),
			'event_place': forms.TextInput(attrs={'placeholder': ' استادیوم آزادی'}),
			'event_title': forms.TextInput(attrs={'placeholder': ' مسابقه والیبال ایران-آمریکا'}),
        	}

class CategoryModelForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['category_name', 'category_glyphicon']
		labels = {
			'category_name': 'عنوان دسته',
			'category_glyphicon': 'آیکن دسته',
		}
		widgets = {
			'category_name': forms.TextInput(attrs={'placeholder': ' مثلا: نمایشگاه'}),
			'category_glyphicon': forms.TextInput(attrs={'placeholder': ' مثلا: eye-close'}),
        	}

class SubCategoryModelForm(forms.ModelForm):
	class Meta:
		model = SubCategory
		fields = ['subcategory_name', 'category']
		labels = {
			'subcategory_name': 'عنوان زیردسته',
			'category': 'دسته',
		}
		widgets = {
			'subcategory_name': forms.TextInput(attrs={'placeholder': ' مثلا: مجسمه سازی'}),
        	}

TicketFormSet = inlineformset_factory(
	Event,
	Ticket,
	fields=('ticket_type','ticket_price', 'total_capacity'),
	extra=1,
	widgets={'ticket_type': forms.TextInput(attrs={'placeholder': 'نوع'}),
		'ticket_price': forms.TextInput(attrs={'placeholder': 'قیمت'}),
		'total_capacity': forms.TextInput(attrs={'placeholder': 'ظرفیت'}),})
