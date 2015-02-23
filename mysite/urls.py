from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from django.conf import settings

urlpatterns = patterns('',
    # set the root as homepage app
    url(r'^$', include('homepage.urls', namespace="homepage")),
    # filebrowser access/browse (TO DO: required for filebrowser to function?)
    url(r'^admin/filebrowser/', include(site.urls)),
    # grappelli URLS
    url(r'^grappelli/', include('grappelli.urls')),
    # set url of admin site
    url(r'^admin/', include(admin.site.urls)),
    # restricted access to ckeditor upload/browse (required for ckeditor availability)
    url(r'^ckeditor/', include('ckeditor.urls')),
)

# NOTE THAT PRODUCTION SERVER WILL NEED TO BE DIFFERENT
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))