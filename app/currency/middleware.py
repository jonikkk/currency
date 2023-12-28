import time

from currency.models import RequestResponseTimeMiddlewareModel


class RequestResponseTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        model = RequestResponseTimeMiddlewareModel()
        model.path = request.path
        model.request_method = request.method
        model.execute_time = end_time - start_time
        model.save()

        return response
