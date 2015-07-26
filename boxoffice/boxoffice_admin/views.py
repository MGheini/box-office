from django.shortcuts import render
from .boxoffice_admin import models

# Create your views here.
def delete_multiple_events(request):
	events = models.Event.objects.all()

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		models.Event.objects.filter(id__in=todel).delete()
		return HttpResponseRedirect('')

	return render(request, 'delete-mutiple-events.html', {'events': events})