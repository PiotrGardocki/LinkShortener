from shortener.django_receive import DjangoRequestReceiver

from django.http import HttpResponse


def index(request):
    # return HttpResponse('Port: ' + request.META['SERVER_PORT'])
    return DjangoRequestReceiver.handle_request(request)
