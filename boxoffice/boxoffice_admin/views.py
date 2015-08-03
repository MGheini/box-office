
from django.contrib.auth import logout, get_user
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.shortcuts import render, HttpResponseRedirect

from users.forms import LoginForm
from users.models import Organizer
from boxoffice_admin.models import MyAdmin
from services.models import Event, Category, SubCategory
from .forms import EventEditModelForm, CategoryEditModelForm, SubCategoryEditModelForm
from services.forms import EventModelForm, CategoryModelForm , SubCategoryModelForm, TicketFormSet

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
	form = LoginForm()
	return render(request, 'admin-login.html', {'form': form})

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
		event_description = form.cleaned_data['event_description']
		if event_description != '':
			self.object.event_description = event_description
		event_deadline = form.cleaned_data['event_deadline']
		if event_deadline is not None:
			self.object.event_deadline = event_deadline
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
            self.object.organizer = Organizer.objects.get(user=get_user(self.request))
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
			if category!='':
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