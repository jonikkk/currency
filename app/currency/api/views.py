from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import filters

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from currency.api.paginators import RatePagination
from currency.api.serializers import RateSerializer, ContactUsSerializer, SourceSerializer
from currency.api.throtling import RateThrottle
from currency.filters import RateFilter, ContactUsFilter
from currency.models import Rate, ContactUs, Source


class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all().order_by('-created')
    serializer_class = RateSerializer
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = ('buy', 'sell', 'created')
    throttle_classes = (RateThrottle,)


class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    filterset_class = ContactUsFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ('email_from', 'subject')
    search_fields = ('email_from', 'subject')


class SourceView(ReadOnlyModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
