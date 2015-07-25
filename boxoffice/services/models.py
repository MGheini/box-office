
from django.db import models
from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey

from users.models import Member, Organizer

class Category(models.Model):
	category_name = models.CharField(max_length=100)
	category_glyphicon = models.CharField(max_length=30, null=True)

	class Meta:
		verbose_name_plural = "دسته‌ها"
		verbose_name = "دسته"

	def __str__(self):
		return self.category_name

class SubCategory(models.Model):
	category = models.ForeignKey(Category)
	subcategory_name = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "زیردسته‌ها"
		verbose_name = "زیردسته"

	def __str__(self):
		return self.subcategory_name + " (" + self.category.category_name + ")"

class Event(models.Model):
	category = models.ForeignKey(Category)
	subcategory = ChainedForeignKey(SubCategory,
		chained_field="category",
		chained_model_field="category",
		show_all=False,
        auto_choose=True,
        null=True)

	event_title = models.CharField(max_length=255, blank=False)
	event_image = models.ImageField(upload_to='media/', blank=True, default="media/noimage.png")
	event_place = models.CharField(max_length=255, blank=False)
	event_description = models.TextField(blank=True)
	event_date = models.DateTimeField(blank=False)
	event_deadline = models.DateTimeField(blank=False)
	submit_date = models.DateTimeField(default=datetime.now)
	organizer = models.ForeignKey(Organizer)
	event_avg_rate = models.FloatField(default=0.0)

	class Meta:
		verbose_name_plural = "رویدادها"
		verbose_name = "رویداد"

	def __str__(self):
		return self.event_title

class Ticket(models.Model):
	event = models.ForeignKey(Event, null=True)
	ticket_type = models.CharField(max_length=255)
	ticket_price = models.PositiveIntegerField()
	total_capacity = models.PositiveSmallIntegerField()
	purchased_num = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ("event", "ticket_type")
		verbose_name_plural = "بلیت‌ها"
		verbose_name = "بلیت"

	def __str__(self):
		return self.ticket_type + " (" + self.event.event_title +")"

class Comment(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	comment_text = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "نظرها"
		verbose_name = "نظر"

	def __str__(self):
		return self.comment_text

class Rate(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	rate = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ("member", "event")
		verbose_name_plural = "امتیازها"
		verbose_name = "امتیاز"

	def __str__(self):
		return self.rate

class Order(models.Model):
	member = models.ForeignKey(Member)
	ticket = models.ForeignKey(Ticket)
	num = models.PositiveSmallIntegerField(blank=False)
	total_price = models.PositiveIntegerField(blank=False)
	order_date = models.DateField(blank=False)

	class Meta:
		verbose_name_plural = "سفارش‌ها"
		verbose_name = "سفارش"

	def __str__(self):
		return self.member.user.username + " (" + self.ticket.event.event_title + ")"