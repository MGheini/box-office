
from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', 'services.views.home'),
    url(r'^FAQ/$', 'services.views.answer'),
    url(r'^Gisheh/$', 'services.views.about_us'),
    url(r'^register/$', 'users.views.register'),
    url(r'^events/', include([
    	url(r'^(?P<event_id>[\d]+)/', include([
    		url(r'^$', 'services.views.event_details'),
			url(r'^purchase/$', 'services.views.purchase'),
			url(r'^rate/$', 'services.views.rate'),
			url(r'^post/$', 'services.views.post'),    		
    	])),
    	url(r'^(?P<category>[\w ]+)/', include([
    		url(r'^$', 'services.views.category'),
    		url(r'^(?P<subcategory>[\w ]+)/$', 'services.views.subcategory'),
    	])),
    ])),
    url(r'^submit/$', 'services.views.submit'),
    url(r'^orders/(?P<order_id>[\d]+)/receipt/$', 'services.views.receipt'),
    url(r'^history/$', 'services.views.history'),
    url(r'^logout/$', 'users.views.our_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]