
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

GENDER_CHOICES = (
    ('M', 'مرد'),
    ('F', 'زن'),
)

class Member(models.Model):
	user = models.OneToOneField(User)
	# Inside User:
	# username, password, first_name, last_name
	# email, date_joined, last_login

	pre_phone_regex = RegexValidator(regex=r'^\d{3}$', message="پیش‌شماره متشکل از سه رقم است.")
	pre_phone_number = models.CharField(max_length=3, validators=[pre_phone_regex], blank=True) # validators should be a list

	phone_regex = RegexValidator(regex=r'^\d{6,10}$', message="بین ۶ تا ۱۰ رقم وارد کنید.")
	phone_number = models.CharField(max_length=10, validators=[phone_regex], blank=True) # validators should be a list

	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank="False")

	def __str__(self):
		return self.user.first_name + " (" + self.user.username + ")"

class Organizer(models.Model):
	user = models.OneToOneField(User)
	# Inside User:
	# username, password, first_name, last_name
	# email, date_joined, last_login
	
	organization_name = models.CharField(max_length=255)
	organization_reg_num = models.CharField(max_length=255)

	def __str__(self):
		return self.user.first_name + " from " + self.organization_name + " (" + self.user.username + ")"