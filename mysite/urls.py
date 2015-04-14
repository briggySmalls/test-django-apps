from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from django.conf import settings
# from fbfeed.feeds import FacebookGroupPosts


# initialise fbfeed
# GROUP_ID = '501953199923737'
# ACCESS_TOKEN = '812176038862023|neR_lhZIyH-CpvT9IPnFrZmLHxY'
# REQUEST_URL_SKEL = 'https://graph.facebook.com/{0}/feed?access_token={1}'
# LINK_SKEL = 'https://www.facebook.com/groups/{}'
# kwargs = {
#     'title': 'Skin Deep Group Posts',
#     'link': LINK_SKEL.format(GROUP_ID),
#     'request_url': REQUEST_URL_SKEL.format(GROUP_ID, ACCESS_TOKEN),
#     'author_name': 'Skin Deep',
# }

urlpatterns = patterns(
    '',
    # set the root as homepage app
    url(r'^$', include('homepage.urls', namespace="homepage")),
    # filebrowser access/browse (TO DO: required for filebrowser to function?)
    url(r'^admin/filebrowser/', include(site.urls)),
    # grappelli URLs
    url(r'^grappelli/', include('grappelli.urls')),
    # set URL of admin site
    url(r'^admin/', include(admin.site.urls)),
    # restricted access to ckeditor upload/browse
    url(r'^ckeditor/', include('ckeditor.urls')),
    # fbfeed URLs
    #   url(r'^feed/', FacebookGroupPosts(**kwargs))
)

# NOTE THAT PRODUCTION SERVER WILL NEED TO BE DIFFERENT
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}))
