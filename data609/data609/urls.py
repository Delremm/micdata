from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from dbproxy.views import ProfileView, ManageView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'data609.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    (r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/$', TemplateView.as_view(
        template_name="src/index.html"), name="dashboard"),
    url(r'^api/', include('dbproxy.api', namespace='api')),
    url(r'^profile/$', ProfileView.as_view(), name="profile"),
    url(r'^manage/$', ManageView.as_view(), name="manage"),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
