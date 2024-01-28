from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django_filters.views import FilterView

from currency.filters import RateFilter, ContactUsFilter, SourceFilter
from currency.forms import SourceForm, RateForm, ContactUsForm
from currency.models import Rate, ContactUs, Source

from currency.tasks import send_email_in_background


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class RateListView(FilterView):
    queryset = Rate.objects.all().select_related('source').order_by('-created')
    template_name = 'rate_list.html'
    paginate_by = 25
    filterset_class = RateFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_params'] = '&'.join(
            f'{key}={value}' for key, value in self.request.GET.items() if key != 'page'
        )
        return context


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


class ContactUsListView(FilterView):
    queryset = ContactUs.objects.all()
    template_name = 'contactUs.html'
    filterset_class = ContactUsFilter
    paginate_by = 25


class ContactUsCreateView(CreateView):
    form_class = ContactUsForm
    template_name = 'contactus_create.html'
    success_url = reverse_lazy('currency:contactus-list')

    def _send_email(self):
        subject = self.object.subject
        message = self.object.message
        email_from = self.object.email_from

        send_email_in_background.apply_async(
            kwargs={
                "subject": subject,
                "message": message,
                "email_from": email_from
            },
            countdown=10,
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


class SourceListView(FilterView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'
    filterset_class = SourceFilter
    paginate_by = 25
