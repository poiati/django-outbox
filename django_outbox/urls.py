from django.conf.urls import patterns, include, url

from .views import OutboxTemplateView, MailTemplateView


urlpatterns = patterns('',
    url(r'^$', OutboxTemplateView.as_view(), name='outbox'),
    url(r'^(?P<id>.+)/$', MailTemplateView.as_view(), name='mail'),
)
