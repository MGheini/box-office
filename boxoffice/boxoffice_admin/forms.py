
from django import forms

from services.models import Event, Category, SubCategory

class EventEditModelForm(forms.ModelForm):

	class Meta:
		model = Event
		exclude = ['submit_date', 'event_avg_rate']
		fields = ['event_title', 'category', 'subcategory', 'event_image', 'event_place', 'event_date', 'event_description', 'event_deadline', 'organizer']
		labels = {
			'event_title': 'عنوان رویداد',
			'category': 'دسته',
			'subcategory': 'زیردسته',
			'event_image': 'تصویر',
			'event_place': 'محل برگزاری',
			'event_date': 'زمان برگزاری',
			'event_description': 'توضیحات تکمیلی',
			'event_deadline': 'آخرین مهلت خرید بلیت',
			'organizer': 'برگزارکننده'
		}

	def __init__(self, event, *args, **kwargs):
		super(EventEditModelForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
		self.fields['event_title'].widget = forms.TextInput(attrs={'placeholder': event.event_title})
		self.fields['event_place'].widget = forms.TextInput(attrs={'placeholder': event.event_place})
		self.fields['event_date'].widget = forms.TextInput(attrs={'placeholder': event.event_date})
		self.fields['event_description'].widget = forms.Textarea(attrs={'rows': 4, 'placeholder': event.event_description})
		self.fields['event_deadline'].widget = forms.TextInput(attrs={'placeholder': event.event_deadline})

	def clean(self):
		cleaned_data = super(EventEditModelForm, self).clean()
		category = cleaned_data.get('category')
		subcategory = cleaned_data.get('subcategory')
		if  category and not subcategory:
			self.add_error('subcategory', forms.ValidationError('متناسب دسته انتخاب شده، زیر دسته جدید انتخاب کنید.'))

class CategoryEditModelForm(forms.ModelForm):

	class Meta:
		model = Category
		exclude = []
		labels = {
			'category_name': 'عنوان دسته',
			'category_glyphicon': 'آیکن دسته'
		}

	def __init__(self, category, *args, **kwargs):
		super(CategoryEditModelForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
		self.fields['category_name'].widget = forms.TextInput(attrs={'placeholder': category.category_name})
		self.fields['category_glyphicon'].widget = forms.TextInput(attrs={'placeholder': 'توجه داشته باشید که باید یکی از آیکن‌های موجود در بوت استرپ ۳ باشد.'})

class SubCategoryEditModelForm(forms.ModelForm):

	class Meta:
		model = SubCategory
		fields = ['subcategory_name', 'category']
		labels = {
			'subcategory_name': 'عنوان زیردسته',
			'category': 'دسته'
		}

	def __init__(self, subcategory, *args, **kwargs):
		super(SubCategoryEditModelForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
		self.fields['subcategory_name'].widget = forms.TextInput(attrs={'placeholder': subcategory.subcategory_name})