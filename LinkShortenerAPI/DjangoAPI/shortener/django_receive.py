from shortener.appcode.django_db.django_model import AccessToDjangoLinksDB

from shortener.appcode.core.anon_shortlink_save import ShortlinkSaverForAnonymousUsers
from shortener.appcode.core.short_to_long import ShortToLongLinkTranslator
from shortener.appcode.core.db_errors import *

from django.http import HttpResponse


class DjangoRequestReceiver:
    @staticmethod
    def handle_request(request):
        pass

    @staticmethod
    def handle_translation(request):
        pass

    @staticmethod
    def handle_anonymous_link_creation(request):
        pass
