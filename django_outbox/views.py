from django.views.generic import TemplateView

from .outbox import Outbox


class OutboxTemplateView(TemplateView):
    template_name = 'django_outbox/outbox.html'

    def get_context_data(self, **kwargs):
        context = super(OutboxTemplateView, self).get_context_data(**kwargs)
        context['mails'] = Outbox().all()
        return context


class MailTemplateView(TemplateView):
    template_name = 'django_outbox/mail.html'

    def get_context_data(self, id, **kwargs):
        context = super(MailTemplateView, self).get_context_data(**kwargs)
        context['mail'] = Outbox().get(id)
        return context
