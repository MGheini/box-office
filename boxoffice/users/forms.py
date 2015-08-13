
from django import forms
from django.contrib.auth.models import User

from .models import Member, Organizer

GENDER_CHOICES = (
    ('M', 'مرد'),
    ('F', 'زن'),
)

class MemberRegModelForm(forms.ModelForm):
	member_first_name = forms.CharField(required=True, label='نام', widget=forms.TextInput(attrs={'placeholder': ' مثال: پردیس', 'class': 'required'}))
	member_last_name = forms.CharField(required=True, label='نام خانوادگی', widget=forms.TextInput(attrs={'placeholder': ' مثال: قینی', 'class': 'required'}))
	member_username = forms.CharField(required=True, label='نام کاربری', widget=forms.TextInput(attrs={'placeholder': ' مثال: mozhpar', 'class': 'required'}))
	member_password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' هیچگاه گذرواژتان را فاش نکنید.', 'class': 'required'}))
	member_password2 = forms.CharField(required=True, label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' تکرار گذرواژه', 'class': 'required'}))
	member_email = forms.EmailField(required=True, label='رایانامه', widget=forms.TextInput(attrs={'placeholder': ' مثال: mozhpar@gisheh.ir', 'class': 'required'}))
	gender = forms.ChoiceField(required=True, label='جنسیت', widget=forms.RadioSelect, choices=GENDER_CHOICES)

	class Meta:
		model = Member
		fields = ['member_first_name', 'member_last_name', 'gender', 'member_username', 'member_password', 'member_password2', 'member_email', 'pre_phone_number', 'phone_number']
		labels = {
			'pre_phone_number': 'پیش شماره',
			'phone_number': 'شماره تلفن',
		}
		widgets = {
			'pre_phone_number': forms.TextInput(attrs={'placeholder': ' مثال: 021'}),
			'phone_number': forms.TextInput(attrs={'placeholder': ' مثال: 2200112277'}),
		}

	def clean_member_username(self):
		if User.objects.filter(username=self.cleaned_data['member_username']).count() > 0:
			raise forms.ValidationError('نام کاربری انتخاب شده تکراری است.')

		return self.cleaned_data['member_username']

	def clean_member_email(self):
		if User.objects.filter(email=self.cleaned_data['member_email']).count() > 0:
			raise forms.ValidationError('رایانامه انتخاب شده تکراری است.')

		return self.cleaned_data['member_email']

	def clean_member_password(self):
		if len(self.cleaned_data['member_password']) < 6:
			raise forms.ValidationError('رمز عبور باید حداقل ۶ نویسه باشد.')

		return self.cleaned_data['member_password']

	def clean(self):
		cleaned_data = super(MemberRegModelForm, self).clean()
		password = cleaned_data.get('member_password')
		password2 = cleaned_data.get('member_password2')
		if password and password2 and password != password2:
			self.add_error('member_password2', forms.ValidationError('رمز عبورها یکسان نیستند.'))

class OrganizerRegModelForm(forms.ModelForm):
	organizer_first_name = forms.CharField(required=True, label='نام', widget=forms.TextInput(attrs={'placeholder': ' مثال: مژده', 'class': 'required'}))
	organizer_last_name = forms.CharField(required=True, label='نام خانوادگی', widget=forms.TextInput(attrs={'placeholder': ' مثال: پاشاخانلو', 'class': 'required'}))
	organizer_username = forms.CharField(required=True, label='نام کاربری', widget=forms.TextInput(attrs={'placeholder': ' مثال: mozhpar', 'class': 'required'}))
	organizer_password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' هیچگاه گذرواژتان را فاش نکنید.', 'class': 'required'}))
	organizer_password2 = forms.CharField(required=True, label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' تکرار گذرواژه', 'class': 'required'}))
	organizer_email = forms.EmailField(required=True, label='رایانامه', widget=forms.TextInput(attrs={'placeholder': ' مثال: mozhpar@gisheh.ir', 'class': 'required'}))
	organization_name = forms.CharField(required=True, label='نام مؤسسه', widget=forms.TextInput(attrs={'placeholder': ' مثال: گیشه‌سازان سبز شریف', 'class': 'required'}))
	organization_reg_num = forms.CharField(required=True, label='شماره ثبت مؤسسه', widget=forms.TextInput(attrs={'placeholder': ' مثال: 123456', 'class': 'required'}))

	class Meta:
		model = Organizer
		fields = ['organizer_first_name', 'organizer_last_name', 'organization_name', 'organization_reg_num', 'organizer_username', 'organizer_password', 'organizer_password2', 'organizer_email']

	def clean_organizer_username(self):
		if User.objects.filter(username=self.cleaned_data['organizer_username']).count() > 0:
			raise forms.ValidationError('نام کاربری انتخاب شده تکراری است.')

		return self.cleaned_data['organizer_username']

	def clean_organizer_email(self):
		if User.objects.filter(email=self.cleaned_data['organizer_email']).count() > 0:
			raise forms.ValidationError('رایانامه انتخاب شده تکراری است.')

		return self.cleaned_data['organizer_email']

	def clean_organizer_password(self):
		if len(self.cleaned_data['organizer_password']) < 6:
			raise forms.ValidationError('رمز عبور باید حداقل ۶ نویسه باشد.')

		return self.cleaned_data['organizer_password']

	def clean(self):
		cleaned_data = super(OrganizerRegModelForm, self).clean()
		password = cleaned_data.get('organizer_password')
		password2 = cleaned_data.get('organizer_password2')
		if password and password2 and password != password2:
			self.add_error('organizer_password2', forms.ValidationError('رمز عبورها یکسان نیستند.'))

class LoginForm(forms.Form):
	username = forms.CharField(required=True, label='نام کاربری')
	password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput)