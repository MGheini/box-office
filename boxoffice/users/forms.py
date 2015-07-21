
from django import forms

from .models import Member, Organizer

GENDER_CHOICES = (
    ('M', 'مرد'),
    ('F', 'زن'),
)

class MemberRegModelForm(forms.ModelForm):
	member_first_name = forms.CharField(required=True, label='نام', widget=forms.TextInput(attrs={'placeholder': ' مثلا: مژده'}))
	member_last_name = forms.CharField(required=True, label='نام خانوادگی', widget=forms.TextInput(attrs={'placeholder': ' مثلا: پاشاخانلو'}))
	member_username = forms.CharField(required=True, label='نام کاربری', widget=forms.TextInput(attrs={'placeholder': ' مثلا: mozhpar'}))
	member_password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' گذرواژتان را فاش نکنید.'}))
	member_password2 = forms.CharField(required=True, label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' گذرواژتان را تکرار کنید.'}))
	member_email = forms.EmailField(required=True, label='رایانامه', widget=forms.EmailInput(attrs={'placeholder': ' مثلا: mozhpar@gisheh.ir'}))
	gender = forms.ChoiceField(required=True, label='جنسیت', widget=forms.RadioSelect, choices=GENDER_CHOICES)

	class Meta:
		model = Member
		fields = ['member_first_name', 'member_last_name', 'gender', 'member_username', 'member_password', 'member_password2', 'member_email', 'pre_phone_number', 'phone_number']
		labels = {
			'gender': 'جنسیت',
			'pre_phone_number': 'پیش شماره',
			'phone_number': 'شماره تلفن',
		}
		widgets = {
			'pre_phone_number': forms.TextInput(attrs={'placeholder': ' مثلا: 021'}),
			'phone_number': forms.TextInput(attrs={'placeholder': ' مثلا: 22001133'}),
        }

class OrganizerRegModelForm(forms.ModelForm):
	organizer_first_name = forms.CharField(required=True, label='نام', widget=forms.TextInput(attrs={'placeholder': ' مثلا: پردیس'}))
	organizer_last_name = forms.CharField(required=True, label='نام خانوادگی', widget=forms.TextInput(attrs={'placeholder': ' مثلا: قینی'}))
	organizer_username = forms.CharField(required=True, label='نام کاربری', widget=forms.TextInput(attrs={'placeholder': ' مثلا: mozhpar'}))
	organizer_password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' گذرواژتان را فاش نکنید.'}))
	organizer_password2 = forms.CharField(required=True, label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': ' گذرواژتان را تکرار کنید.'}))
	organizer_email = forms.EmailField(required=True, label='رایانامه', widget=forms.EmailInput(attrs={'placeholder': ' مثلا: mozhpar@gisheh.ir'}))

	class Meta:
		model = Organizer
		fields = ['organizer_first_name', 'organizer_last_name', 'organization_name', 'organization_reg_num', 'organizer_username', 'organizer_password', 'organizer_password2', 'organizer_email']
		labels = {
			'organization_name': 'نام مؤسسه',
			'organization_reg_num': 'شماره ثبت مؤسسه',
		}
		widgets = {
			'organization_name': forms.TextInput(attrs={'placeholder': ' مثلا: گیشه‌سازان سبز شریف'}),
			'organization_reg_num': forms.TextInput(attrs={'placeholder': ' مثلا: 123456'}),
        }

class LoginForm(forms.Form):
	username = forms.CharField(required=True, label='نام کاربری')
	password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput)