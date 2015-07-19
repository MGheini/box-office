
from django.db import models

from users.models import Member, Organizer

class Event(models.Model):
	event_title = models.CharField(max_length=255)
	event_category = models.CharField(max_length=255)
	event_subcategory = models.CharField(max_length=255)
	event_image = models.ImageField(upload_to='media/', blank="True")
	event_place = models.CharField(max_length=255)
	event_date = models.DateField()
	event_description = models.TextField()
	event_deadline = models.DateField()
	submit_date = models.DateField()
	organizer = models.ForeignKey(Organizer)

	def __str__(self):
		return self.event_title

class Feedback(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	rate = models.PositiveSmallIntegerField()
	post = models.TextField()

	class Meta:
		unique_together = ("member", "event")

	def __str__(self):
		return self.member.user.username + " on " + self.event.event_title

class Ticket(models.Model):
	event = models.ForeignKey(Event)
	ticket_type = models.CharField(max_length=255)
	total_num = models.PositiveSmallIntegerField()
	purchased_num = models.PositiveSmallIntegerField()
	ticket_price = models.PositiveIntegerField()

	class Meta:
		unique_together = ("event", "ticket_type")

	def __str__(self):
		return self.ticket_type + " ticket for " + self.event.event_title

class Order(models.Model):
	member = models.ForeignKey(Member)
	ticket = models.ForeignKey(Ticket)
	num = models.PositiveSmallIntegerField()
	total_price = models.PositiveIntegerField()
	order_date = models.DateField()

	def __str__(self):
		return self.member.user.username + " purchased tickets of " + self.ticket.event.event_title