
from django import forms
from django.db.models import F
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

class EventModelFormAdmin(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['submit_date']
		fields = ['event_title', 'category', 'subcategory', 'event_image', 'event_place', 'event_date', 'event_time', 'event_description', 'event_deadline_date', 'event_deadline_time', 'organizer']
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
			'organizer': 'برگزارکننده',
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

	def clean(self):
		cleaned_data = super(EventModelFormAdmin, self).clean()
		event_date = cleaned_data.get('event_date')
		event_time = cleaned_data.get('event_time')
		event_deadline_date = cleaned_data.get('event_deadline_date')
		event_deadline_time = cleaned_data.get('event_deadline_time')
		if event_deadline_date and event_date and event_deadline_time and event_time:
			if event_deadline_date > event_date:
				self.add_error('event_deadline_date', forms.ValidationError('مهلت خرید بلیت باید قبل از برگزاری رویداد به پایان برسد.'))
			elif event_deadline_date == event_date:
				if event_deadline_time >= event_time:
					self.add_error('event_deadline_time', forms.ValidationError('مهلت خرید بلیت باید قبل از برگزاری رویداد به پایان برسد.'))

class EventModelFormOrganizer(forms.ModelForm):
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

	def clean(self):
		cleaned_data = super(EventModelFormOrganizer, self).clean()
		event_date = cleaned_data.get('event_date')
		event_time = cleaned_data.get('event_time')
		event_deadline_date = cleaned_data.get('event_deadline_date')
		event_deadline_time = cleaned_data.get('event_deadline_time')
		if event_deadline_date and event_date and event_deadline_time and event_time:
			if event_deadline_date > event_date:
				self.add_error('event_deadline_date', forms.ValidationError('مهلت خرید بلیت باید قبل از برگزاری رویداد به پایان برسد.'))
			elif event_deadline_date == event_date:
				if event_deadline_time >= event_time:
					self.add_error('event_deadline_time', forms.ValidationError('مهلت خرید بلیت باید قبل از برگزاری رویداد به پایان برسد.'))

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
	min_num=1,
	validate_min=True,
	extra=1,
	widgets={'ticket_type': forms.TextInput(attrs={'placeholder': 'نوع'}),
		'ticket_price': forms.TextInput(attrs={'placeholder': 'قیمت'}),
		'total_capacity': forms.TextInput(attrs={'placeholder': 'ظرفیت'}),})

class PurchaseChooseForm(forms.Form):
	tickets = forms.ModelChoiceField(queryset=Ticket.objects.none(), widget=forms.RadioSelect(attrs={'class': 'radio', 'style': 'display: inline; cursor: pointer;'}), empty_label=None)
	num = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'تعداد', 'value': '1', 'min': '1'}),)

	def __init__(self, event_id, *args, **kwargs):
		super(PurchaseChooseForm, self).__init__(*args, **kwargs)
		self.fields['tickets'].queryset = Ticket.objects.filter(event__id=event_id).filter(total_capacity__gt=F('purchased_num'))

	def clean_num(self):
		if self.cleaned_data['num'] <= 0 or self.cleaned_data['num'] == '':
			raise forms.ValidationError('تعداد بلیت‌هایتان را مشخص فرمایید.')

		return self.cleaned_data['num']

	def clean(self):
		cleaned_data = super(PurchaseChooseForm, self).clean()
		num = self.cleaned_data.get('num')
		tickets = self.cleaned_data.get('tickets')

		if tickets != None and num > (tickets.total_capacity - tickets.purchased_num):
			self.add_error('num', forms.ValidationError('تعداد بلیت موجود کافی نیست.'))

		return self.cleaned_data

class BankPaymentForm(forms.Form):
	card_number_1 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'xxxx', 'maxlength': '4', 'tabindex': '1003'}),)
	card_number_2 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'xxxx', 'maxlength': '4', 'tabindex': '1002'}),)
	card_number_3 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'xxxx', 'maxlength': '4', 'tabindex': '1001'}),)
	card_number_4 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'xxxx', 'maxlength': '4', 'tabindex': '1000'}),)
	cvv2 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'xxx', 'maxlength': '3', 'tabindex': '1004'}),)
	password = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '****', 'type': 'password', 'maxlength': '6', 'tabindex': '1005'}),)

	ticket_id = forms.CharField(max_length=10)
	num = forms.CharField(max_length=10)

	def clean(self):
		cleaned_data = super(BankPaymentForm, self).clean()
		card_number_1 = self.cleaned_data.get('card_number_1')
		card_number_2 = self.cleaned_data.get('card_number_2')
		card_number_3 = self.cleaned_data.get('card_number_3')
		card_number_4 = self.cleaned_data.get('card_number_4')

		if card_number_1 != 1234 or card_number_2 != 1234 or card_number_3 != 1234 or card_number_4 != 1234:
			self.add_error('card_number_1', forms.ValidationError('رمز کارت اشتباه وارد شده است.'))

		return self.cleaned_data
