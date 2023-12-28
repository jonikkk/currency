from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView

from currency.forms import SourceForm, RateForm, ContactUsForm
from currency.models import Rate, ContactUs, Source
from django.core.mail import send_mail


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class RateListView(ListView):
    queryset = Rate.objects.all().select_related('source')
    template_name = 'rate_list.html'


class RateCreateView(CreateView):
    form_class = RateForm
    template_name = 'rate_create.html'
    success_url = reverse_lazy('currency:rate-list')


class RateUpdateView(UserPassesTestMixin, UpdateView):
    model = Rate
    form_class = RateForm
    template_name = 'rate_update.html'
    success_url = reverse_lazy('currency:rate-list')

    def test_func(self):
        return self.request.user.is_superuser


class RateDeleteView(UserPassesTestMixin, DeleteView):
    model = Rate
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate-list')

    def test_func(self):
        return self.request.user.is_superuser


class RateDetailsView(LoginRequiredMixin, DetailView):
    model = Rate
    template_name = 'rate_details.html'
    success_url = reverse_lazy('currency:rate-list')


class ContactUsListView(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contactUs.html'


class ContactUsCreateView(CreateView):
    form_class = ContactUsForm
    template_name = 'contactus_create.html'
    success_url = reverse_lazy('currency:contactus-list')

    def _send_email(self):
        recipient = settings.EMAIL_HOST_USER
        subject = self.object.subject
        message = self.object.message
        email_from = self.object.email_from
        send_mail(
            subject,
            message,
            email_from,
            [recipient],
            fail_silently=False,
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_email()
        return redirect


class ContactUsUpdateView(UpdateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'contactus_update.html'
    success_url = reverse_lazy('currency:contactus-list')


class ContactUsDeleteView(DeleteView):
    model = ContactUs
    template_name = 'contactus_delete.html'
    success_url = reverse_lazy('currency:contactus-list')


class ContactUsDetailsView(DetailView):
    model = ContactUs
    template_name = 'contactus_details.html'
    success_url = reverse_lazy('currency:contactus-list')


class SourceCreateView(CreateView):
    model = Source
    form_class = SourceForm
    template_name = 'source_create.html'
    success_url = reverse_lazy('currency:source-list')


class SourceUpdateView(UpdateView):
    model = Source
    form_class = SourceForm
    template_name = 'source_update.html'
    success_url = reverse_lazy('currency:source-list')


class SourceDeleteView(DeleteView):
    model = Source
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source-list')


class SourceDetailsView(DetailView):
    model = Source
    template_name = 'source_details.html'
    success_url = reverse_lazy('currency:source-list')


class SourceListView(ListView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'
