
from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
	user = models.OneToOneField(User)

	def __str__(self):
		return self.user.first_name + " (" + self.user.username + ")"

class Organizer(models.Model):
	user = models.OneToOneField(User)
	organization_name = models.CharField(max_length=255)
	organization_reg_num = models.CharField(max_length=255)

	def __str__(self):
		return self.user.first_name + " from " + self.organization_name + " (" + self.user.username + ")"