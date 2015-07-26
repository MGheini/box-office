from django.shortcuts import render, HttpResponseRedirect
from boxoffice_admin.models import MyAdmin
from services.models import Event, Category, SubCategory
from users.models import Organizer
from services.forms import EventModelForm, CategoryModelForm , SubCategoryModelForm

# Create your views here.
def delete_multiple_events(request):
	events = Event.objects.all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		Event.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	return render(request, 'manage-events.html', {'events': events})

def delete_event(request, event_id):
	todel = Event.objects.get(id=event_id).delete()
	return HttpResponseRedirect('/bo-admin/events/')

# MUST ADD TICKETS to this
def add_event(request):
	event_form = EventModelForm()
	if(request.method == 'POST'):
		event_form = EventModelForm(request.POST)

		if event_form.is_valid():
			event = event_form.save(commit=False)
			organizer = Organizer.objects.get(user=request.user)
			event.organizer = organizer
			event.save()
			success = True
			return render(request, 'add-new-event.html', {'success': success})

		return render(request, 'add-new-event.html', {'event_form': event_form})

	else:
		event_form = EventModelForm()
		return render(request, 'add-new-event.html', {'event_form': event_form})

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