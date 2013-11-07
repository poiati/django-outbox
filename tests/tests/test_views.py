from django.test import TestCase
from django.core.urlresolvers import reverse

from mock import patch
from expecter import expect

from django_outbox.outbox import Outbox, Mail


class OutboxTemplateViewTest(TestCase):
    mails = (
        Mail('20101010', 'Foo', 'foo@example.com', 'baz@example.com', 
            'Sat, 26 Oct 2013 17:15:32 -0000', 'text/plain',
            {'text/plain': 'Foo content'}), 
        Mail('20101010', 'Bar', 'bar@example.com', 'baz@example.com', 
            'Sat, 26 Oct 2013 17:15:32 -0000', 'text/plain',
            {'text/plain': 'Foo content'}))

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
    html_content = '<b>Example</b>'
    text_content = 'Foo content'
    mail = Mail(id, 'Foo', 'foo@example.com', 'baz@example.com', 
            'Sat, 26 Oct 2013 17:15:32 -0000', 
            'multipart/alternative',
            {'text/plain': text_content, 'text/html': html_content})

    @patch('django_outbox.views.Outbox', spec=Outbox)
    def test_get_text_plain(self, outbox_class):
        outbox_class.return_value.get.return_value = self.mail

        response = self.client.get(
                self._reverse(), 
                {'content_type': 'text/plain'})

        expect(response.status_code) == 200
        expect(response.context['mail']) == self.mail
        self.assertContains(response, self.text_content)

    @patch('django_outbox.views.Outbox', spec=Outbox)
    def test_get_text_html(self, outbox_class):
        outbox_class.return_value.get.return_value = self.mail

        response = self.client.get(
                self._reverse(), 
                {'content_type': 'text/html'})

        expect(response.status_code) == 200
        self.assertContains(response, self.html_content)

    def _reverse(self):
        return reverse('mail', kwargs=dict(id=self.id))
