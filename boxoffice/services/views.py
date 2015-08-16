import datetime

from django.shortcuts import render
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from . import forms
from . import models
from users.forms import LoginForm
from users.views import our_login
from users.models import Member, Organizer

def get_layout():
	categories = models.Category.objects.all()
	most_populars = models.Event.objects.exclude(event_deadline_date__lt=datetime.datetime.now().date(), event_deadline_time__lt=datetime.datetime.now().time()).order_by('-event_avg_rate')[:5]
	newest = models.Event.objects.exclude(event_deadline_date__lt=datetime.datetime.now().date(), event_deadline_time__lt=datetime.datetime.now().time()).order_by('-submit_date')[:5]

	return {'categories': categories, 'newest': newest, 'most_populars': most_populars}

def get_users_template_variables(request):
	if request.user.is_authenticated():
		if request.session['user_type'] == 'member':
			member = Member.objects.get(user=request.user)
			organizer = None
			permitted = False
			visitor = False
		else:
			organizer = True
			permitted = Organizer.objects.get(user=request.user).has_permission_to_create_category
			member = None
			visitor = False
	else:
		member = None
		organizer = None
		permitted = False
		visitor = True

	return {'member': member, 'organizer': organizer, 'permitted': permitted, visitor: 'visitor'}

def home(request):
	layout = get_layout()

	# az unaaE ke mohlate kharid daaran, random chantaa ro bede!
	available_events = models.Event.objects.exclude(event_deadline_date__lt=datetime.datetime.now().date(), event_deadline_time__lt=datetime.datetime.now().time()).order_by('?')[:5]

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
				permitted = Organizer.objects.get(user=request.user).has_permission_to_create_category
				return render(request, 'home.html',
					{'home': True,
					'organizer': True,
					'permitted': permitted,
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

	users_template_variables = get_users_template_variables(request)

	return render(request, 'FAQ.html',
		{'form': form,
		'visitor': users_template_variables['visitor'],
		'member': users_template_variables['member'],
		'organizer': users_template_variables['organizer'],
		'permitted': users_template_variables['permitted'],
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def about_us(request):
	layout = get_layout()
	form = LoginForm()

	users_template_variables = get_users_template_variables(request)

	return render(request, 'FAQ.html',
		{'form': form,
		'visitor': users_template_variables['visitor'],
		'member': users_template_variables['member'],
		'organizer': users_template_variables['organizer'],
		'permitted': users_template_variables['permitted'],
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

class TicketWithAvailableCapacity():

	def __init__(self, ticket):
		self.ticket = ticket
		self.ticket_available_capacity = ticket.total_capacity - ticket.purchased_num

def event_details(request, event_id):
	layout = get_layout()
	form = LoginForm()
	event = models.Event.objects.get(id=event_id)		

	if request.user.is_authenticated():
		if request.session['user_type'] == 'member':
			member = Member.objects.get(user=request.user)
			if models.Rate.objects.filter(member=member, event=event).count() > 0:
				rate = models.Rate.objects.get(member=member, event=event).rate
			else:
				rate = None
			organizer = None
			permitted = False
			visitor = False
		else:
			organizer = True
			permitted = Organizer.objects.get(user=request.user).has_permission_to_create_category
			member = None
			rate = None
			visitor = False
	else:
		member = None
		rate = None
		organizer = None
		permitted = False
		visitor = True

	tickets = []
	for ticket in event.ticket_set.all():
		tickets += [TicketWithAvailableCapacity(ticket)]

	like_comments = models.LikeComment.objects.filter(comment__event__id=event_id)

	is_available = False
	for t in event.ticket_set.all():
		if t.total_capacity > t.purchased_num:
			is_available = True
			break

	# event_deadline_date = models.DateField()
	# event_deadline_time = models.TimeField()
	event_deadline_has_passed = False
	if event.event_deadline_date < datetime.datetime.now().date():
		if event.event_deadline_time < datetime.datetime.now().time():
			event_deadline_has_passed = True

	return render(request, 'view-event-details.html',
		{'form': form,
		'visitor': visitor,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars'],
		'event': event,
		'member': member,
		'organizer': organizer,
		'permitted': permitted,
		'rate': rate,
		'tickets': tickets,
		'like_comments': like_comments,
		'avg_rate': event.event_avg_rate,
		'is_available': is_available,
		'event_deadline_has_passed': event_deadline_has_passed,})

def purchase(request, event_id):
	event = models.Event.objects.get(id=event_id)
	layout = get_layout()
	form = LoginForm()

	if request.user.is_authenticated():
		if request.method == 'POST':
			ticket_form = forms.PurchaseChooseForm(event_id, request.POST)
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
					'total_price': total_price,})
		else:
			ticket_form = forms.PurchaseChooseForm(event_id)

		return render(request, 'buy-ticket-step-1.html',
			{'ticket_form': ticket_form,
			'categories': layout['categories'],
			'newest': layout['newest'],
			'most_populars': layout['most_populars'],
			'ticket_form': ticket_form,
			'event': event,
			})

def pay(request, event_id):
	event = models.Event.objects.get(id=event_id)
	layout = get_layout()
	form = LoginForm()

	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		if request.method == "GET":
			payment_form = forms.BankPaymentForm(request.GET)
			
			ticket_id = request.GET['tid']
			num = request.GET['n']
			
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
					'event_id': event.id,
					'num': num,
					'ticket_id': ticket.id,})
		elif request.method == "POST":
			payment_form = forms.BankPaymentForm(request.POST)
			
			ticket_id = request.POST['ticket_id']
			event_id = request.POST['event_id']
			num = request.POST['num']
			total_price = int(num) * models.Ticket.objects.get(id=ticket_id).ticket_price

			event = models.Event.objects.get(id=event_id)
			ticket = models.Ticket.objects.get(id=ticket_id)

			if payment_form.is_valid():
				
				if ticket.total_capacity - ticket.purchased_num >= int(num):
					# save the order...
					order = models.Order()
					order.member = member
					order.ticket = ticket
					order.event = event
					order.num_purchased = int(num)
					order.total_price = order.num_purchased * order.ticket.ticket_price
					# order.order_date = datetime.datetime.now() --> DEFAULT WILL SET IT
					order.purchase_code = int(order.member.id + (order.order_date - datetime.datetime(1970, 1, 1)).total_seconds())

					order.first_chair_offset = order.event.empty_chair_offset()
					order.event.save()

					order.ticket.purchased_num += int(num)
					order.ticket.save()

					order.save()

					chairs = []
					for i in range(order.num_purchased):
						chairs += [i+order.first_chair_offset]

					return render(request, 'buy-ticket-step-3.html',
						{'member': member,
						'categories': layout['categories'],
						'newest': layout['newest'],
						'most_populars': layout['most_populars'],
						'paid': True,
						'order': order,
						'chairs': chairs,})
				else:
					return render(request, 'buy-ticket-failed.html',
						{'member': member,
						'categories': layout['categories'],
						'newest': layout['newest'],
						'most_populars': layout['most_populars'],
						'ticket': ticket,})

			payment_form = forms.BankPaymentForm(event_id)
			return render(request, 'buy-ticket-step-3.html',
				{'member': member,
				'categories': layout['categories'],
				'newest': layout['newest'],
				'most_populars': layout['most_populars'],
				'total_price': total_price,
				'payment_form': payment_form,
				'event_id': event.id,
				'num': num,
				'ticket_id': ticket_id,})

def rate(request, event_id):
	member = Member.objects.get(user=request.user)
	event = models.Event.objects.get(id=event_id)
	rate = int(request.GET['rate'])
	if models.Rate.objects.filter(member=member, event=event).count() > 0:
		rating = models.Rate.objects.get(member=member, event=event)
		old_rate = rating.rate
		rating.rate = rate
		rating.save()
		total_raters = models.Rate.objects.filter(event=event).count()
		event.event_avg_rate = ((total_raters) * event.event_avg_rate - old_rate + rate) / total_raters
		event.save()
	else:
		new_rating = models.Rate()
		new_rating.member = member
		new_rating.event = event
		new_rating.rate = rate
		new_rating.save()
		total_raters = models.Rate.objects.filter(event=event).count()
		event.event_avg_rate = ((total_raters - 1) * event.event_avg_rate + rate) / total_raters
		event.save()
	return HttpResponse(event.event_avg_rate, status=200)

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
	
	events = models.Event.objects.filter(category__category_name=category).exclude(event_deadline_date__lt=datetime.datetime.now().date(), event_deadline_time__lt=datetime.datetime.now().time())
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

	events = models.Event.objects.filter(subcategory__subcategory_name=subcategory).exclude(event_deadline_date__lt=datetime.datetime.now().date(), event_deadline_time__lt=datetime.datetime.now().time())
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
	form_class = forms.EventModelFormOrganizer
	layout = get_layout()
	
	def get_context_data(self, **kwargs):
		context = super(AddEventView, self).get_context_data(**kwargs)
		layout = get_layout()
		if self.request.POST:
			context['formset'] = forms.TicketFormSet(self.request.POST)
		else:
			context['formset'] = forms.TicketFormSet()
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
			self.object.organizer = Organizer.objects.get(user=self.request.user)
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

	if request.user.is_authenticated() and request.session['user_type'] == 'organizer':
		permitted = models.Organizer.objects.get(user=request.user).has_permission_to_create_category
		if permitted:
			if request.method == 'POST':
				if 'category-submit-btn' in request.POST:
					form = forms.CategoryModelForm(request.POST)

					if form.is_valid():
						form.save()

						subcategory_submit_form = forms.SubCategoryModelForm
						return render(request, 'submit-new-category.html',
							{'organizer': True,
							'permitted': True,
							'category_success': True,
							'subcategory_submit_form': subcategory_submit_form,
							'categories': layout['categories'],
							'newest': layout['newest'],
							'most_populars': layout['most_populars']})
					else:
						subcategory_submit_form = forms.SubCategoryModelForm
						return render(request, 'submit-new-category.html',
							{'organizer': True,
							'permitted': True,
							'category_submit_form': form,
							'subcategory_submit_form': subcategory_submit_form,
							'categories': layout['categories'],
							'newest': layout['newest'],
							'most_populars': layout['most_populars']})
				else:
					form = forms.SubCategoryModelForm(request.POST)

					if form.is_valid():
						form.save()

						category_submit_form = forms.CategoryModelForm
						return render(request, 'submit-new-category.html',
							{'organizer': True,
							'permitted': True,
							'subcategory_success': True,
							'category_submit_form': category_submit_form,
							'categories': layout['categories'],
							'newest': layout['newest'],
							'most_populars': layout['most_populars']})
					else:
						category_submit_form = forms.CategoryModelForm
						return render(request, 'submit-new-category.html',
							{'organizer': True,
							'permitted': True,
							'category_submit_form': category_submit_form,
							'subcategory_submit_form': form,
							'categories': layout['categories'],
							'newest': layout['newest'],
							'most_populars': layout['most_populars']})
			else:
				category_submit_form = forms.CategoryModelForm()
				subcategory_submit_form = forms.SubCategoryModelForm()
				return render(request, 'submit-new-category.html',
					{'organizer': True,
					'permitted': True,
					'category_submit_form': category_submit_form,
					'subcategory_submit_form': subcategory_submit_form,
					'categories': layout['categories'],
					'newest': layout['newest'],
					'most_populars': layout['most_populars']})
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

def receipt(request, order_id):
	layout = get_layout()
	order = models.Order.objects.get(id=order_id)
	member = Member.objects.get(user=request.user)
	
	chairs = []
	for i in range(order.num_purchased):
		chairs += [i + order.first_chair_offset]

	return render(request, 'view-receipt.html',
		{'member': member,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars'],
		'order': order,
		'chairs': chairs})

def history(request):
	layout = get_layout()

	if request.user.is_authenticated() and request.session['user_type'] == 'member':
		orders = {}
		categories = models.Category.objects.all()
		
		for category in categories:
			orders[category.category_name] = list(models.Order.objects.filter(member__user=request.user, event__category__category_name=category.category_name))

		return render(request, 'purchase-history.html',
			{'member': True,
			 'orders': orders,
			'categories': layout['categories'],
			'newest': layout['newest'],
			'most_populars': layout['most_populars']})
	else:
		return HttpResponseRedirect('/')

def search_by_code(request):
	layout = get_layout()
	if request.user.is_authenticated() and request.session['user_type'] == 'member':
		if request.method == 'GET':
			purchase_code = request.GET['code']

			try:
			    order = models.Order.objects.get(purchase_code=purchase_code)
			except models.Order.DoesNotExist:
			    order = None

			if order and (order in member.order_set.all()):
				return receipt(request, order.id)
			else:
				orders = {}
				categories = models.Category.objects.all()
				
				for category in categories:
					orders[category.category_name] = list(models.Order.objects.filter(member__user=request.user, event__category__category_name=category.category_name))

				error = 'شما خریدی با کد رهگیری وارد شده نداشته‌اید.'

				return render(request, 'purchase-history.html',
					{'member': True,
					 'orders': orders,
					'categories': layout['categories'],
					'newest': layout['newest'],
					'most_populars': layout['most_populars'],
					'error': error})

	else:
		return HttpResponseRedirect('/')
