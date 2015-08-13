 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from . import models
from users.forms import LoginForm
from users.views import our_login
from users.models import Member, Organizer
from .forms import EventModelForm, CategoryModelForm, SubCategoryModelForm

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

def event_details(request, event_id):
	layout = get_layout()
	form = LoginForm()
	return render(request, 'view-event-details.html',
		{'form': form,
		'visitor': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def purchase(request, event_id):
	layout = get_layout()
	return render(request, 'buy-ticket.html',
		{'member': True,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

def rate(request, event_id):
	return HttpResponse('rate')

def comment(request, event_id):
	return HttpResponse('post')

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

def submit(request):
	layout = get_layout()
	event_form = EventModelForm()
	return render(request, 'submit-new-event.html',
		{'event_form': event_form,
		'organizer': True,
		'permitted': False,
		'categories': layout['categories'],
		'newest': layout['newest'],
		'most_populars': layout['most_populars']})

class AddEventView(CreateView):
    template_name = 'add-new-event.html'
    form_class = EventModelForm

    def get_context_data(self, **kwargs):
        context = super(AddEventView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TicketFormSet(self.request.POST)
        else:
            context['formset'] = TicketFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            # self.object.organizer = Organizer.objects.all()[0] #Organizer.objects.get(user=get_user(self.request))
            self.object.save()
            formset.instance = self.object
            formset.save()
            success = True
            return render(self.request, 'add-new-event.html', {'success': success})
        else:
            return render(self.request, 'add-new-event.html', {'form': form})

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