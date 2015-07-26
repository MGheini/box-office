from django.shortcuts import render, HttpResponseRedirect
from boxoffice_admin.models import MyAdmin
from services.models import Event

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