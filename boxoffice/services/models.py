
import datetime

from django.db import models
from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey

from users.models import Member, Organizer

class Category(models.Model):
	category_name = models.CharField(max_length=100)
	category_glyphicon = models.CharField(max_length=30, null=True, blank=True)

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
		return self.subcategory_name

class Event(models.Model):
	category = models.ForeignKey(Category)
	subcategory = ChainedForeignKey(SubCategory,
		chained_field="category",
		chained_model_field="category",
		show_all=False,
        auto_choose=True)

	event_title = models.CharField(max_length=255)
	event_image = models.ImageField(upload_to='media/', blank=True, default="media/noimage.png")
	event_place = models.CharField(max_length=255)
	event_description = models.TextField(blank=True)
	event_date = models.DateField()
	event_time = models.TimeField()
	event_deadline_date = models.DateField()
	event_deadline_time = models.TimeField()
	submit_date = models.DateTimeField(default=datetime.now)
	organizer = models.ForeignKey(Organizer)
	event_avg_rate = models.FloatField(default=0.0)

	empty_chair_offset = models.PositiveIntegerField(default=1)

	class Meta:
		verbose_name_plural = "رویدادها"
		verbose_name = "رویداد"

	def __str__(self):
		return self.event_title

class Ticket(models.Model):
	event = models.ForeignKey(Event)
	ticket_type = models.CharField(max_length=20)
	ticket_price = models.PositiveIntegerField()
	total_capacity = models.PositiveSmallIntegerField()
	purchased_num = models.PositiveSmallIntegerField(default=0)

	class Meta:
		unique_together = ("event", "ticket_type")
		verbose_name_plural = "بلیت‌ها"
		verbose_name = "بلیت"

	def __str__(self):
		return self.ticket_type + ' (' + str(self.ticket_price) + ' تومان)'

class Comment(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	comment_text = models.CharField(max_length=200)
	datetime = models.DateTimeField(default=datetime.now)
	like_num = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = "نظرها"
		verbose_name = "نظر"

	def __str__(self):
		return self.comment_text

class LikeComment(models.Model):
	member = models.ForeignKey(Member)
	comment = models.ForeignKey(Comment)

	def __str__(self):
		return member.user.username + ' (' + comment.comment_text + ')'

class Rate(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	rate = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ("member", "event")
		verbose_name_plural = "امتیازها"
		verbose_name = "امتیاز"

	def __str__(self):
		return str(self.rate)

class Order(models.Model):
	member = models.ForeignKey(Member)
	ticket = models.ForeignKey(Ticket)
	event = models.ForeignKey(Event)
	num_purchased = models.PositiveSmallIntegerField()
	total_price = models.PositiveIntegerField()
	order_date = models.DateTimeField(default=datetime.now)
	purchase_code = models.PositiveIntegerField()
	first_chair_offset = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = "سفارش‌ها"
		verbose_name = "سفارش"

	def __str__(self):
		return self.member.user.username + ' (' + self.ticket.event.event_title + ')'
