from django.test import TestCase
from django.core.urlresolvers import reverse

from mock import patch
from expecter import expect

from django_outbox.outbox import Outbox, Mail


class OutboxTemplateViewTest(TestCase):
    mails = (
        Mail('20101010', 'Foo', 'foo@example.com', 'baz@example.com', 
            'Sat, 26 Oct 2013 17:15:32 -0000', 'Foo content'), 
        Mail('20101010', 'Bar', 'bar@example.com', 'baz@example.com', 
            'Sat, 26 Oct 2013 17:15:32 -0000', 'Bar content'))

    @patch('django_outbox.views.Outbox', spec=Outbox)
    def test_get(self, outbox_class):
        outbox_class.return_value.all.return_value = self.mails
        response = self.client.get(self._reverse())

        expect(response.status_code) == 200
        expect(response.context['mails']) == self.mails

    def _reverse(self):
        return reverse('outbox')


class EmailTemplateViewTest(TestCase):
    id = '20101010'
    mail = Mail(id, 'Foo', 'foo@example.com', 'baz@example.com', 
            'Sat, 26 Oct 2013 17:15:32 -0000', 'Foo content')

    @patch('django_outbox.views.Outbox', spec=Outbox)
    def test_get(self, outbox_class):
        outbox_class.return_value.get.return_value = self.mail

        response = self.client.get(self._reverse())

        expect(response.status_code) == 200
        expect(response.context['mail']) == self.mail

    def _reverse(self):
        return reverse('mail', kwargs=dict(id=self.id))
