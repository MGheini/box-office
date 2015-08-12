
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from boxoffice_admin.views import AddEventView, EditEventView

urlpatterns = [
    url(r'^$', 'services.views.home'),
    url(r'^FAQ/$', 'services.views.answer'),
    url(r'^Gisheh/$', 'services.views.about_us'),
    url(r'^register/$', 'users.views.register'),
    url(r'^events/', include([
    	url(r'^(?P<event_id>[\d]+)/', include([
    		url(r'^$', 'services.views.event_details'),
			url(r'^purchase/$', 'services.views.purchase'),
            url(r'^pay/$', 'services.views.pay'),
			url(r'^rate/$', 'services.views.rate'),
			url(r'^comment/$', 'services.views.comment'),   # /events/5/comment/?comment_text=loremipsums
            url(r'^comment/like/$', 'services.views.like_unlike'),   # /events/{{event.id}}/comment/{{comment.id}}/like/
    	])),
    	url(r'^(?P<category>[\w ]+)/', include([
    		url(r'^$', 'services.views.category'),
    		url(r'^(?P<subcategory>[\w ]+)/$', 'services.views.subcategory'),
    	])),
    ])),
    url(r'^submit/$', 'services.views.submit_event'),
    url(r'^submitcategory/$', 'services.views.submit_category'),
    url(r'^orders/(?P<order_id>[\d]+)/receipt/$', 'services.views.receipt'),
    url(r'^history/$', 'services.views.history'),
    url(r'^logout/$', 'users.views.our_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

    # admin related urls
    url(r'^bo-admin/$', 'boxoffice_admin.views.admin_home'),

    url(r'^bo-admin/users/$', 'boxoffice_admin.views.manage_users'),
    
    url(r'^bo-admin/events/$', 'boxoffice_admin.views.delete_multiple_events'),
    url(r'^bo-admin/events/(?P<event_id>[\d]+)/delete/$', 'boxoffice_admin.views.delete_event'),
    url(r'^bo-admin/events/(?P<event_id>[\d]+)/edit/$', EditEventView.as_view()),
    url(r'^bo-admin/events/add/$', AddEventView.as_view()),

    url(r'^bo-admin/categories/$', 'boxoffice_admin.views.delete_multiple_categories'),
    url(r'^bo-admin/categories/(?P<category_id>[\d]+)/delete/$', 'boxoffice_admin.views.delete_category'),
    url(r'^bo-admin/categories/(?P<category_id>[\d]+)/edit/$', 'boxoffice_admin.views.edit_category'),
    url(r'^bo-admin/categories/add/$', 'boxoffice_admin.views.add_category'),

    url(r'^bo-admin/subcategories/$', 'boxoffice_admin.views.delete_multiple_subcategories'),
    url(r'^bo-admin/subcategories/(?P<sub_category_id>[\d]+)/delete/$', 'boxoffice_admin.views.delete_subcategory'),
    url(r'^bo-admin/subcategories/(?P<subcategory_id>[\d]+)/edit/$', 'boxoffice_admin.views.edit_subcategory'),
    url(r'^bo-admin/subcategories/add/$', 'boxoffice_admin.views.add_subcategory'),
    
    url(r'^bo-admin/report/orders/summary/search/$', 'boxoffice_admin.views.search_orders_summary'),
    url(r'^bo-admin/report/orders/all/search/$', 'boxoffice_admin.views.search_orders_all'),

    url(r'^bo-admin/report/orders/summary/$', 'boxoffice_admin.views.show_orders_summary'),
    url(r'^bo-admin/report/orders/all/$', 'boxoffice_admin.views.show_orders_all'),

    url(r'^bo-admin/logout/$', 'boxoffice_admin.views.our_logout'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)