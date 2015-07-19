
from django import forms

from .models import Member, Organizer

class MemberRegModelForm(forms.ModelForm):
	member_first_name = forms.CharField(required=True, label='نام')
	member_last_name = forms.CharField(required=True, label='نام خانوادگی')
	member_username = forms.CharField(required=True, label='نام کاربری')
	member_password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput)
	member_password2 = forms.CharField(required=True, label='تکرار رمز عبور', widget=forms.PasswordInput)
	member_email = forms.EmailField(required=True, label='رایانامه')

	class Meta:
		model = Member
		fields = ['member_first_name', 'member_last_name', 'gender', 'member_username', 'member_password', 'member_password2', 'member_email', 'pre_phone_number', 'phone_number']
		labels = {
			'gender': 'جنسیت',
			'pre_phone_number': 'پیش شماره',
			'phone_number': 'شماره تلفن',
		}

class OrganizerRegModelForm(forms.ModelForm):
	organizer_first_name = forms.CharField(required=True, label='نام')
	organizer_last_name = forms.CharField(required=True, label='نام خانوادگی')
	organizer_username = forms.CharField(required=True, label='نام کاربری')
	organizer_password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput)
	organizer_password2 = forms.CharField(required=True, label='تکرار رمز عبور', widget=forms.PasswordInput)
	organizer_email = forms.EmailField(required=True, label='رایانامه')

	class Meta:
		model = Organizer
		fields = ['organizer_first_name', 'organizer_last_name', 'organization_name', 'organization_reg_num', 'organizer_username', 'organizer_password', 'organizer_password2', 'organizer_email']
		labels = {
			'organization_name': 'نام مؤسسه',
			'organization_reg_num': 'شماره ثبت مؤسسه',
		}

class LoginForm(forms.Form):
	username = forms.CharField(required=True, label='نام کاربری')
	password = forms.CharField(required=True, label='رمز عبور', widget=forms.PasswordInput)