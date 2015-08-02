
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout

from users.models import Organizer
from boxoffice_admin.models import MyAdmin
from services.forms import EventModelForm, TicketFormSet
from services.models import Event, Category, SubCategory,Ticket,Order
from services.forms import EventModelForm, CategoryModelForm , SubCategoryModelForm
from django.db.models import Q

from datetime import datetime

def admin_home(request):
	return render(request, 'admin-layout.html', {})
	
	
def search_form(request):
    return render(request, 'search-form.html')

def search(request):
    if 'q' in request.POST:
        q = request.POST['q']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        try:
            events = Event.objects.get(Q(event_title=q) & Q(event_date__contains=startDate) & Q(event_deadline__contains=endDate))

        except Event.DoesNotExist:
            return render(request,'output-table.html',{'query' : q,'success' : False})

        tickets = events.ticket_set
        number = tickets.count()
        try:
            orders = Order.objects.filter(ticket__event=events)
        except Order.DoesNotExist:
            return render(request, 'output-table.html',
                        {'events' : events,'success' : True , 'query' : q , 'ticketNum' : number , 'price': 0 , 'order' : False})
        total = sum([order.total_price for order in orders])
        return render(request, 'output-table.html',
                        {'events' : events,'success' : True , 'query' : q , 'ticketNum' : number , 'price': total ,'order' : True})

def search_by_time(request):
    return render(request, 'search-orders-by-time.html')

def search_by_time_result(request):
    if 'startDate' in request.POST and 'endDate' in request.POST:
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        try:
            events = Event.objects.filter(Q(event_date__contains=startDate) & Q(event_deadline__contains=endDate))

        except Event.DoesNotExist:
            return render(request,'search-by-time-result.html',{'success' : False})
        try:
            orders = Order.objects.filter(ticket__event=events)
        except Order.DoesNotExist:
            return render(request, 'search-by-time-result.html',
                        {'events' : events,'success' : True  , 'price': 0 , 'order' : False})
        total = sum([order.total_price for order in orders])
        return render(request, 'search-by-time-result.html',
                        {'events' : events,'success' : True , 'price': total ,'order' : True})

def all_orders(request):
    try:
        orders = Order.objects.all()
    except Order.DoesNotExist:
        return render(request,'all-orders.html',{'success' : False})
    if orders.count() == 0:
        return render(request,'all-orders.html',{'success' : False})
    return render(request, 'all-orders.html' ,{'success' : True , 'orders' : orders})

class TemplateOrder():

    def __init__(self, event):
        self.event = event
        
        num = 0
        income = 0
        for ticket in event.ticket_set.all():
            num += ticket.purchased_num
            income += ticket.ticket_price * ticket.purchased_num
        self.sold_ticket_num = num
        self.total_income = income

def search_orders(request):
    if request.method == "GET":
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        error = None

        orders = []
        if start and end:
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')

            if start < end:
                orders = list(Event.objects.filter(event_date__range=(start, end)))
            else:
                orders = []
                error = 'زمان شروع باید قبل از زمان پایان باشد.'
        elif start:
            orders = []
            error = 'زمان پایان را مشخص کنید.'
        elif end:
            orders = []
            error = 'زمان شروع را مشخص کنید.'
        else:
            orders = []
            error = 'زمان شروع و پایان را مشخص کنید.'

        template_orders = []
        for order in orders:
            template_orders += [TemplateOrder(order)]

        return render(request, 'show-orders-summary.html', {'template_orders': template_orders, 'error': error})

def show_orders(request):
    orders = Event.objects.all()

    template_orders = []
    for order in orders:
        template_orders += [TemplateOrder(order)]

    return render(request, 'show-orders-summary.html', {'template_orders': template_orders})


def show_all_events(request):
    events = Event.objects.all()
    ticketNum=[]
    total=[]
    for event in events:
        tickets = event.ticket_set
        ticketNum.append(tickets.count())
        try:
            orders = Order.objects.filter(ticket__event=events)
        except Order.DoesNotExist:
            return render(request, 'all-events.html',
                        {'events' : events,'success' : False , 'ticketNum' : ticketNum , 'price': 0 , 'order' : False})
        total.append(sum([order.total_price for order in orders]))

    list = zip(events,ticketNum,total)
    return render(request, 'all-events.html',
                        {'success' : True ,'order' : True , 'list' : list})	

def delete_multiple_events(request):
	events = Event.objects.order_by('-submit_date').all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		Event.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	return render(request, 'manage-events.html', {'events': events})

def delete_event(request, event_id):
	todel = Event.objects.get(id=event_id).delete()
	return HttpResponseRedirect('/bo-admin/events/')

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
            self.object.organizer = Organizer.objects.get(user=self.request.user)
            self.object.save()
            formset.instance = self.object
            formset.save()
            success = True
            return render(self.request, 'add-new-event.html', {'success': success})
        else:
            return render(self.request, 'add-new-event.html', {'form': form})


def delete_multiple_categories(request):
	categories = Category.objects.all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		Category.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	return render(request, 'manage-categories.html', {'categories': categories})

def delete_category(request, category_id):
	todel = Category.objects.get(id=category_id).delete()
	return HttpResponseRedirect('/bo-admin/categories/')

def add_category(request):
	category_form = CategoryModelForm()

	if(request.method == 'POST'):
		category_form = CategoryModelForm(request.POST)

		if category_form.is_valid():
			category = category_form.save(commit=False)
			category.save()
			success = True
			return render(request, 'add-new-category.html', {'success': success})

		return render(request, 'add-new-category.html', {'category_form': category_form})

	else:
		category_form = CategoryModelForm()

	return render(request, 'add-new-category.html', {'category_form': category_form})


def delete_multiple_subcategories(request):
	subcategories = SubCategory.objects.all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		SubCategory.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	return render(request, 'manage-subcategories.html', {'subcategories': subcategories})

def delete_subcategory(request, sub_category_id):
	todel = SubCategory.objects.get(id=sub_category_id).delete()
	return HttpResponseRedirect('/bo-admin/subcategories/')

def add_subcategory(request):
	subcategory_form = SubCategoryModelForm()

	if(request.method == 'POST'):
		subcategory_form = SubCategoryModelForm(request.POST)

		if subcategory_form.is_valid():
			subcategory = subcategory_form.save(commit=False)
			subcategory.save()
			success = True
			return render(request, 'add-new-subcategory.html', {'success': success})

		return render(request, 'add-new-subcategory.html', {'subcategory_form': subcategory_form})

	else:
		subcategory_form = SubCategoryModelForm()

	return render(request, 'add-new-subcategory.html', {'subcategory_form': subcategory_form})

def our_logout(request):
	logout(request)
	return render(request, 'logout-admin.html', {})
