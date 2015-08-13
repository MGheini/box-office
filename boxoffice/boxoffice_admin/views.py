
from datetime import datetime
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, get_user, logout

from users.forms import LoginForm
from users.models import Organizer
from services.models import Event, Category, SubCategory, Order
from .forms import EventEditModelForm, CategoryEditModelForm, SubCategoryEditModelForm
from services.forms import EventModelFormAdmin, CategoryModelForm , SubCategoryModelForm, TicketFormSet

class TemplateUser():

	def __init__(self, user):
		self.user = user
		if user.is_superuser:
			self.type = 'مدیر'
		elif Organizer.objects.filter(user=user).count() > 0:
			self.type = 'برگزار‌کننده'
			self.has_permission = Organizer.objects.get(user=user).has_permission_to_create_category
			self.checkbox_activity = True
		else:
			self.type = 'مشتری'

def admin_home(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
		
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_superuser:
					login(request, user)
					return render(request, 'admin-layout.html', {})
				return render(request, 'admin-login.html', {'form': form, 'not_admin': True})
			return render(request, 'admin-login.html', {'form': form, 'bad_login': True})
		return render(request, 'admin-login.html', {'form': form, 'bad_login': True})
	form = LoginForm()
	if request.user.is_authenticated():
		return render(request, 'admin-layout.html', {}) # Agar admin az home biad
	return render(request, 'admin-login.html', {'form': form})

def show_orders_all(request):
    orders = Order.objects.all()

    return render(request, 'show-all-orders.html', {'orders': orders})

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

def search_orders_all(request):
    if request.method == "GET":
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        error = ''

        orders = []
        if start and end:
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')

            if start < end:
                orders = list(Order.objects.filter(order_date__range=(start, end)))
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

        if len(orders) == 0 and error is '':
            error = 'هیچ سفارشی برای نمایش وجود ندارد.'

        return render(request, 'show-all-orders.html', {'orders': orders, 'error': error})


def search_orders_summary(request):
    if request.method == "GET":
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        error = ''

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

        if len(orders) == 0 and error is '':
            error = 'هیچ سفارشی برای نمایش وجود ندارد.'

        return render(request, 'show-orders-summary.html', {'template_orders': template_orders, 'error': error})

def show_orders_summary(request):
    orders = Event.objects.all()

    template_orders = []
    for order in orders:
        template_orders += [TemplateOrder(order)]

    return render(request, 'show-orders-summary.html', {'template_orders': template_orders})

def delete_multiple_events(request):
	events = Event.objects.order_by('-submit_date').all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		Event.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	if 'successfulEdit' in request.GET:
		return render(request, 'manage-events.html', {'events': events, 'successful_edit': True})

	return render(request, 'manage-events.html', {'events': events})

def delete_event(request, event_id):
	todel = Event.objects.get(id=event_id).delete()
	return HttpResponseRedirect('/bo-admin/events/')

class EditEventView(CreateView):
	template_name = 'edit-event.html'
	form_class = EventEditModelForm
	success_url = '/bo-admin/events/?successfulEdit=true'

	def get_form_kwargs(self, **kwargs):
		form_kwargs = super(EditEventView, self).get_form_kwargs(**kwargs)
		form_kwargs['event'] = Event.objects.get(id=self.kwargs['event_id'])
		return form_kwargs

	def get(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form(self.form_class)
		return self.render_to_response(
			self.get_context_data(form=form,
								  event=Event.objects.get(id=self.kwargs['event_id']),
								  formset=TicketFormSet()))

	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		formset = TicketFormSet(request.POST)
		if (form.is_valid() and formset.is_valid()):
			return self.form_valid(form, formset)
		else:
			return self.form_invalid(form, formset)

	def form_valid(self, form, formset):
		self.object = Event.objects.get(id=self.kwargs['event_id'])
		event_title = form.cleaned_data['event_title']
		if event_title != '':
			self.object.event_title = event_title
		category = form.cleaned_data['category']
		if category is not None:
			self.object.category = category
		subcategory = form.cleaned_data['subcategory']
		if subcategory is not None:
			self.object.subcategory = subcategory
		event_place = form.cleaned_data['event_place']
		if event_place != '':
			self.object.event_place = event_place
		event_date = form.cleaned_data['event_date']
		if event_date is not None:
			self.object.event_date = event_date
		event_time = form.cleaned_data['event_time']
		if event_time is not None:
			self.object.event_time = event_time
		event_description = form.cleaned_data['event_description']
		if event_description != '':
			self.object.event_description = event_description
		event_deadline_date = form.cleaned_data['event_deadline_date']
		if event_deadline_date is not None:
			self.object.event_deadline_date = event_deadline_date
		event_deadline_time = form.cleaned_data['event_deadline_time']
		if event_deadline_time is not None:
			self.object.event_deadline_time = event_deadline_time
		organizer = form.cleaned_data['organizer']
		if organizer is not None:
			self.object.organizer = organizer
		if self.request.FILES:
			self.object.event_image = self.request.FILES['event_image']
		todel = self.request.POST.getlist('todelete')
		self.object.ticket_set.all().filter(id__in=todel).delete()
		self.object.save()
		formset.instance = self.object
		formset.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, formset):
		return self.render_to_response(
			self.get_context_data(form=form,
								  event=Event.objects.get(id=self.kwargs['event_id']),
								  formset=formset))

class AddEventView(CreateView):
    template_name = 'add-new-event.html'
    form_class = EventModelFormAdmin

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


def delete_multiple_categories(request):
	categories = Category.objects.all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		Category.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	if 'successfulEdit' in request.GET:
		return render(request, 'manage-categories.html', {'categories': categories, 'successful_edit': True})

	return render(request, 'manage-categories.html', {'categories': categories})

def delete_category(request, category_id):
	todel = Category.objects.get(id=category_id).delete()
	return HttpResponseRedirect('/bo-admin/categories/')

def edit_category(request, category_id):
	if request.method == 'POST':
		category = Category.objects.get(id=category_id)
		form = CategoryEditModelForm(category, request.POST)
		if form.is_valid():
			category_name = form.cleaned_data['category_name']
			if category_name!='':
				category.category_name = category_name
			category_glyphicon = form.cleaned_data['category_glyphicon']
			if category_glyphicon!='':
				category.category_glyphicon = category_glyphicon
			category.save()
		return HttpResponseRedirect('/bo-admin/categories/?successfulEdit=true')
	else:
		form = CategoryEditModelForm(Category.objects.get(id=category_id))
		return render(request, 'edit-category.html', {'form': form, 'category_id':category_id})

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

	if 'successfulEdit' in request.GET:
		return render(request, 'manage-subcategories.html', {'subcategories': subcategories, 'successful_edit': True})

	return render(request, 'manage-subcategories.html', {'subcategories': subcategories})

def delete_subcategory(request, sub_category_id):
	todel = SubCategory.objects.get(id=sub_category_id).delete()
	return HttpResponseRedirect('/bo-admin/subcategories/')

def edit_subcategory(request, subcategory_id):
	if request.method == 'POST':
		subcategory = SubCategory.objects.get(id=subcategory_id)
		form = SubCategoryEditModelForm(subcategory, request.POST)
		if form.is_valid():
			subcategory_name = form.cleaned_data['subcategory_name']
			if subcategory_name!='':
				subcategory.subcategory_name = subcategory_name
			category = form.cleaned_data['category']
			if category is not None:
				subcategory.category = category
			subcategory.save()
		return HttpResponseRedirect('/bo-admin/subcategories/?successfulEdit=true')
	else:
		form = SubCategoryEditModelForm(SubCategory.objects.get(id=subcategory_id))
		return render(request, 'edit-subcategory.html', {'form': form, 'subcategory_id':subcategory_id})

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

def manage_users(request):
	users = User.objects.all()
	template_users = []

	for user in users:
		template_users += [TemplateUser(user)]

	if request.method == 'POST':
		tobepermitted = request.POST.getlist('permitted')
		organizers = Organizer.objects.all()
		print(tobepermitted)

		for organizer in organizers:
			if str(organizer.user.id) in tobepermitted: # Ey str() ...
				organizer.has_permission_to_create_category = True
				organizer.save()
			else:
				organizer.has_permission_to_create_category = False
				organizer.save()
		return HttpResponseRedirect('')
	
	return render(request, 'manage-users.html', {'users': template_users})

def our_logout(request):
	logout(request)
	return render(request, 'logout-admin.html', {})