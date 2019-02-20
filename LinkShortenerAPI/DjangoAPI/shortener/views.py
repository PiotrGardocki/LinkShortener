from shortener.django_receive import DjangoRequestReceiver

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    try:
        response = DjangoRequestReceiver.handle_request(request)
    except BaseException:
        response = HttpResponse(status=500, reason='Another server error occured')

    if not isinstance(response, HttpResponse):
        response = HttpResponse(status=500, reason='Another server error occured')

    response["Access-Control-Allow-Origin"] = "*"
    return response
