from shortener.appcode.django_db.django_links_model import AccessToDjangoLinksDB

from shortener.appcode.core.short_to_long import ShortToLongLinkTranslator
from shortener.appcode.core.anon_shortlink_save import ShortlinkSaverForAnonymousUsers
from shortener.appcode.core.db_errors import *

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


class DjangoRequestReceiver:
    @staticmethod
    def handle_request(request):
        if request.method != "POST":
            return HttpResponse(status=400, reason='Request must be send by POST method')

        try:
            action = request.POST['action']
        except MultiValueDictKeyError:
            return HttpResponse(status=406, reason='Not given \'action\' parameter')
        action = action.lower()

        if action == 'translate':
            return DjangoRequestReceiver.handle_action_translate(request)
        if action == 'checklink':
            return DjangoRequestReceiver.handle_action_checklink(request)
        if action == 'anoncreatelink':
            return DjangoRequestReceiver.handle_action_anoncreatelink(request)
        # if action.lower() == '':
            # return DjangoRequestReceiver.handle_action_(request)

        return HttpResponse(status=405, reason="Method '%s' not supported" % action)

    @staticmethod
    def handle_action_translate(request):
        db_access = AccessToDjangoLinksDB()
        translator = ShortToLongLinkTranslator(db_access)

        try:
            shortlink = request.POST['shortlink']
        except MultiValueDictKeyError:
            return HttpResponse(status=406, reason='Not given required parameters for this action: shortlink')

        password = request.POST.get('linkPassword', '')

        try:
            longlink = translator.translate_shortlink_to_longlink(shortlink, password)
        except ShortLinkNotExists:
            return HttpResponse(status=404, reason='Shortlink not found')
        except IncorrectPasswordForShortLink:
            return HttpResponse(status=401, reason='Incorrect password for shortlink')
        except BaseException:
            return HttpResponse(status=500, reason='Internal Server Error')
            # return HttpResponse(status=, reason=)

        return HttpResponse(content='longlink: %s' % longlink, status=200, reason='Successful translation to longlink')

    @staticmethod
    def handle_action_checklink(request):
        db_access = AccessToDjangoLinksDB()
        # checker = (db_access)

        try:
            shortlink = request.POST['shortlink']
        except MultiValueDictKeyError:
            return HttpResponse(status=406, reason='Not given required parameters for this action: shortlink')

    @staticmethod
    def handle_action_anoncreatelink(request):
        pass

    # @staticmethod
    # def handle_action_(request):
    #     pass
