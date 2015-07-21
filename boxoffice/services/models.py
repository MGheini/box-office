
from django.db import models
from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey

from users.models import Member, Organizer

class Category(models.Model):
	category_name = models.CharField(max_length=100)

	def __str__(self):
		return self.category_name

class SubCategory(models.Model):
	category = models.ForeignKey(Category)
	subcategory_name = models.CharField(max_length=100)

	def __str__(self):
		return self.subcategory_name

# All categories we have
# سینما
# 	اکشن
# 	کمدی
# 	مستند
# 	درام
# 	ترسناک
# 	معمایی
# 	علمی-تخیلی
# تئاتر
# 	درام
# 	موزیکال
# 	کمدی
# 	تراژدی
# نمایشگاه
# 	نقاشی
# 	عکاسی
# 	مجسمه سازی
# ورزش
# 	فوتبال
# 	والیبال
# 	بسکتبال
# 	تنیس
# موسیقی
# 	سنتی
# 	پاپ
# 	راک

class Event(models.Model):
	category = models.ForeignKey(Category)
	subcategory = ChainedForeignKey(SubCategory,
		chained_field="category",
		chained_model_field="category",
		show_all=False,
        auto_choose=True,
        null=True)
	ticket = models.ForeignKey(Ticket, null=True)
	event_title = models.CharField(max_length=255, blank="True")
	event_image = models.ImageField(upload_to='media/', blank="True")
	event_place = models.CharField(max_length=255, blank="True")
	event_description = models.TextField(blank="True")
	event_date = models.DateTimeField(blank=True)
	event_deadline = models.DateTimeField(blank=True)
	submit_date = models.DateTimeField(default=datetime.now, blank=True)
	organizer = models.ForeignKey(Organizer)

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

	def __str__(self):
		return self.ticket_type + " ticket for " + self.event.event_title

class Feedback(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	rate = models.PositiveSmallIntegerField()
	post = models.TextField()

	class Meta:
		unique_together = ("member", "event")

	def __str__(self):
		return self.member.user.username + " on " + self.event.event_title

class Order(models.Model):
	member = models.ForeignKey(Member)
	ticket = models.ForeignKey(Ticket)
	num = models.PositiveSmallIntegerField()
	total_price = models.PositiveIntegerField()
	order_date = models.DateField()

	def __str__(self):
		return self.member.user.username + " purchased tickets of " + self.ticket.event.event_title
