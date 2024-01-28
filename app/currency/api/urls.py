
from rest_framework import routers

from currency.api.views import RateViewSet, ContactUsViewSet, SourceView

router = routers.SimpleRouter(trailing_slash=True)
router.register('rates', RateViewSet, basename='rate')
router.register('contactus', ContactUsViewSet, basename='contact-us')
router.register('source', SourceView, basename='source')

app_name = 'currency_api'
urlpatterns = router.urls
