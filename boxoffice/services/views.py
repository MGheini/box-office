
import datetime

from django.shortcuts import render
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from . import models
from users.models import Member
from users.forms import LoginForm
from users.views import our_login
from .forms import CategoryModelForm , SubCategoryModelForm, PurchaseChooseForm, BankPaymentForm, EventModelFormOrganizer, TicketFormSet

def get_layout():
	categories = models.Category.objects.all()
	most_populars = models.Event.objects.order_by('-event_avg_rate')[:4]
	newest = models.Event.objects.order_by('-submit_date')[:4]

	return {'categories': categories, 'newest': newest, 'most_populars': most_populars}

def home(request):
	layout = get_layout()

	# felan hameye event ha ra dar nazar darim, ba'dan bayad available haa neshun dade beshe
	available_events = models.Event.objects.all()

	if request.method == 'POST':
		return our_login(request) # don't forget to return!
	elif request.user.is_authenticated():
		if 'user_type' in request.session:
			if request.session['user_type'] == 'member':
				return render(request, 'home.html',
					{'home': True,
					'member': True,
					'categories': layout['categories'],
					'available_events': available_events,
					'newest': layout['newest'],
					'most_populars': layout['most_populars']})
			elif request.session['user_type'] == 'organizer':
				return render(request, 'home.html',
					{'home': True,
					'organizer': True,
					# 'permitted': request.user.has_permission_to_create_category,
					'categories': layout['categories'],
					'available_events': available_events,
					'newest': layout['newest'],
					'most_populars': layout['most_populars']})
			else:
				return HttpResponseRedirect('/bo-admin')
		else:
			return HttpResponseRedirect('/bo-admin')
	else:
		form = LoginForm()
		return render(request, 'home.html',
			{'form': form,
			'home': True,
			'visitor': True,
			'categories': layout['categories'],
			'available_events': available_events,
			'newest': layout['newest'],
			'most_populars': layout['most_populars']})

def answer(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'FAQ.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def about_us(request):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'Gisheh.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

class TicketWithAvailableCapacity():

	def __init__(self, ticket):
		self.ticket = ticket
		self.ticket_available_capacity = ticket.total_capacity - ticket.purchased_num

class EnhancedComment():

	def __init__(self, comment, member):
		self.comment = comment

		if models.LikeComment.objects.filter(comment=comment, member=member) > 0:
			self.do_i_like = True
		else:
			self.do_i_like = False

def event_details(request, event_id):
	layout = get_layout()
	form = LoginForm()
	event = models.Event.objects.get(id=event_id)		

	if request.user.is_authenticated():
		member = models.Member.objects.get(user=request.user)
		visitor = False
	else:
		member = None
		visitor = True

	tickets = []
	for ticket in event.ticket_set.all():
		tickets += [TicketWithAvailableCapacity(ticket)]

	like_comments = models.LikeComment.objects.filter(comment__event__id=event_id)

	return render(request, 'view-event-details.html',
		{'form': form,
		'visitor': visitor,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars'],
		'event': event,
		'member': member,
		'tickets': tickets,
		'like_comments': like_comments,
		'avg_rate': int(event.event_avg_rate),
		'c_avg_rate': (5 - int(event.event_avg_rate)),})

def purchase(request, event_id):
	event = models.Event.objects.get(id=event_id)
	layout = get_layout()
	form = LoginForm()

	if request.user.is_authenticated():
		if request.method == 'POST':
			ticket_form = PurchaseChooseForm(event_id, request.POST)
			if ticket_form.is_valid():
				num = ticket_form.cleaned_data['num']
				ticket = ticket_form.cleaned_data['tickets']
				total_price = int(num) * ticket.ticket_price
				
				return render(request, 'buy-ticket-step-2.html',
					{'form': form,
					'categories': layout['categories'],
					'newest': layout['newest'],
					'most_populars': layout['most_populars'],
					'num': num,
					'ticket': ticket,
					'total_price': total_price,
					})
		else:
			ticket_form = PurchaseChooseForm(event_id)

		return render(request, 'buy-ticket-step-1.html',
			{'ticket_form': ticket_form,
			'categories': layout['categories'],
			'newest': layout['newest'],
			'most_populars': layout['most_populars'],
			'ticket_form': ticket_form,
			'event': event,
			})

# todo
def pay(request, event_id):
	event = models.Event.objects.get(id=event_id)
	layout = get_layout()
	form = LoginForm()

	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		if request.method == "GET":
			payment_form = BankPaymentForm(request.GET)
			
			ticket_id = request.GET['ticket_id']
			num = request.GET['num']
			
			if ticket_id and num:
				ticket = models.Ticket.objects.get(id=ticket_id)
				total_price = int(num) * ticket.ticket_price

				return render(request, 'buy-ticket-step-3.html',
					{'member': member,
					'categories': layout['categories'],
					'newest': layout['newest'],
					'most_populars': layout['most_populars'],
					'total_price': total_price,
					'payment_form': payment_form,
					'event': event,})
				# for order:
				# member = models.ForeignKey(Member)
				# ticket = models.ForeignKey(Ticket)
				# event = models.ForeignKey(Event, null=True)
				# num_purchased = models.PositiveSmallIntegerField(blank=False)
				# total_price = models.PositiveIntegerField(blank=False)
				# order_date = models.DateTimeField(default=datetime.now, blank=False)
				# purchase_code = models.PositiveIntegerField(blank=False)
		elif request.method == "POST":
			payment_form = BankPaymentForm(request.POST)
			if payment_form.is_valid():
				

				# save the order...
				success = True
				return render(request, 'buy-ticket-step-3.html',
					{'member': member,
					'categories': layout['categories'],
					'newest': layout['newest'],
					'most_populars': layout['most_populars'],
					'success': success,
					'order': order,})
		else:
			payment_form = BankPaymentForm(event_id)

def rate(request, event_id):
	return HttpResponse('rate')

def like_unlike(request, event_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		comment_id = request.GET.get('comment_id')
		if not comment_id:
			return HttpResponse("Not enough information.", status=400)
		comment = models.Comment.objects.get(id=comment_id)
		
		for like in models.LikeComment.objects.all():
			if like.comment.id == comment.id and like.member.id == member.id:
				comment.like_num -= 1
				comment.save()
				like.delete() # unlike it.
				return HttpResponse('unliked', status=200)

		# like it.
		new_like = models.LikeComment()
		new_like.member = member
		new_like.comment = comment
		comment.like_num += 1
		comment.save()
		new_like.save()
		return HttpResponse('liked', status=200)

def comment(request, event_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		if request.method == "GET":
			comment_text = request.GET.get('comment_text')

			if not (comment_text):
				return HttpResponse("Not enough information.", status=400)

			new_comment = models.Comment()
			new_comment.member = member
			new_comment.event = models.Event.objects.get(id=event_id)
			new_comment.comment_text = comment_text
			new_comment.datetime = datetime.datetime.now()
			new_comment.liked_members = []
			new_comment.save()

			return HttpResponse(new_comment.id, status=200)

class TemplateEvent():
	def __init__(self, event):
		self.event = event
		self.ticket_available = False

		event_tickets = self.event.ticket_set.all()
		for ticket in event_tickets:
			if ticket.total_capacity - ticket.purchased_num > 0:
				self.ticket_available = True;
				break

def category(request, category):
	layout = get_layout()
	form = LoginForm()
	
	events = models.Event.objects.filter(category__category_name=category)
	template_events = []
	for event in events:
		template_events += [TemplateEvent(event)]

	return render(request, 'view-category-events.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars'],
		'events': template_events,
		'category': category})

def subcategory(request, category, subcategory):
	layout = get_layout()
	form = LoginForm()

	events = models.Event.objects.filter(subcategory__subcategory_name=subcategory)
	template_events = []
	for event in events:
		template_events += [TemplateEvent(event)]

	return render(request, 'view-sub-category-events.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars'],
		'events': template_events,
		'category': category,
		'subcategory': subcategory})

class AddEventView(CreateView):
	template_name = 'submit-new-event.html'
	form_class = EventModelFormOrganizer
	layout = get_layout()
	
	def get_context_data(self, **kwargs):
		context = super(AddEventView, self).get_context_data(**kwargs)
		layout = get_layout()
		if self.request.POST:
			context['formset'] = TicketFormSet(self.request.POST)
		else:
			context['formset'] = TicketFormSet()
		context['organizer'] = True
		context['categories'] = layout['categories']
		context['newest'] = layout['newest']
		context['most_populars'] = layout['most_populars']
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		layout = get_layout()

		if formset.is_valid():
			self.object = form.save(commit=False)
			self.object.organizer = models.Organizer.objects.get(user=self.request.user)
			self.object.save()
			formset.instance = self.object
			formset.save()
			success = True
			return render(self.request, 'submit-new-event.html',
				{'success': success,
				'organizer': True,
				'categories': layout['categories'],
				'newest': layout['newest'],
				'most_populars': layout['most_populars']})
		else:
			return render(self.request, 'submit-new-event.html',
				{'form': form,
				'organizer': True,
				'categories': layout['categories'],
				'newest': layout['newest'],
				'most_populars': layout['most_populars']})

def submit_category(request):
	layout = get_layout()
	category_submit_form = CategoryModelForm()
	subcategory_submit_form = SubCategoryModelForm()
	return render(request, 'submit-new-category.html',
		{'organizer': True,
		'permitted': True,
		'category_submit_form': category_submit_form,
		'subcategory_submit_form': SubCategoryModelForm,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def receipt(request, order_id):
	layout = get_layout()
	return render(request, 'view-receipt.html',
		{'member': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def history(request):
	layout = get_layout()
	return render(request, 'purchase-history.html',
		{'member': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})