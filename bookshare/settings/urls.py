from django.contrib import admin
from django.contrib import auth
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('website.views',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    # url(r'^bookshare/', include('bookshare.foo.urls')),

    # home page
    url(r'^$', 'index', name = 'homepage'),

    # product page
    url(r'^product/(?P<slug>[^\.]+)', 'product', name = 'productpage'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)