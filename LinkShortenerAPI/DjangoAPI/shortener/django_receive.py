from shortener.appcode.django_db.django_links_model import AccessToDjangoLinksDB
from shortener.appcode.django_db.django_users_model import AccessToDjangoUsersDB

from shortener.appcode.core.short_to_long import ShortToLongLinkTranslator
from shortener.appcode.core.anon_shortlink_save import ShortlinkSaverForAnonymousUsers
from shortener.appcode.core.users_handle import UsersActions
from shortener.appcode.core.db_errors import *

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


class MissedParameters(Exception): pass


class DjangoRequestReceiver:
    @staticmethod
    def check_for_missed_parameters(request, *parameters):
        not_given_parameters = []
        for param_name in parameters:
            if request.POST.get(param_name, None) is None:
                not_given_parameters.append(param_name)

        if len(not_given_parameters) > 0:
            response = HttpResponse(status=406, reason='Not given required parameters for this action: ' +
                                                       ';'.join(not_given_parameters))
            error = MissedParameters('Missed POST variables')
            error.response = response
            raise error

    @staticmethod
    def handle_request(request):
        if request.method != 'POST':
            return HttpResponse(status=400, reason='Request must be send by POST method')

        try:
            action = request.POST['action']
        except MultiValueDictKeyError:
            return HttpResponse(status=406, reason="Not given 'action' parameter")
        action = action.lower()

        try:
            if action == 'translate':
                return DjangoRequestReceiver.handle_action_translate(request)
            if action == 'checklink':
                return DjangoRequestReceiver.handle_action_check_link(request)
            if action == 'anoncreatelink':
                return DjangoRequestReceiver.handle_action_anon_create_link(request)
            if action == 'createuser':
                return DjangoRequestReceiver.handle_action_create_user(request)
            if action == 'loginuserin':
                return DjangoRequestReceiver.handle_action_log_user_in(request)
            if action == 'loginuserout':
                return DjangoRequestReceiver.handle_action_log_user_out(request)
            if action == 'deleteuser':
                return DjangoRequestReceiver.handle_action_delete_user(request)
            if action == 'changeuserpassword':
                return DjangoRequestReceiver.handle_action_change_user_password(request)
            if action == 'changeuseremail':
                return DjangoRequestReceiver.handle_action_change_user_email(request)
            # if action == '':
            #     return DjangoRequestReceiver.handle_action_(request)
        except MissedParameters as error:
            return error.response
        except BaseException as error:
            return HttpResponse(status=500, reason='Internal Server Error(%s)' % str(error)) # TODO add log saving

        return HttpResponse(status=405, reason="Action '%s' is not supported" % action)

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
    def handle_action_check_link(request):
        db_access = AccessToDjangoLinksDB()
        # checker = (db_access)

        try:
            shortlink = request.POST['shortlink']
        except MultiValueDictKeyError:
            return HttpResponse(status=406, reason='Not given required parameters for this action: shortlink')

    @staticmethod
    def handle_action_anon_create_link(request):
        pass

    @staticmethod
    def handle_action_create_user(request):
        DjangoRequestReceiver.check_for_missed_parameters(request, 'email', 'password')

        db_access = AccessToDjangoUsersDB()
        users_handler = UsersActions(db_access)

        email = request.POST['email']
        password = request.POST['password']

        try:
            users_handler.create_user(email, password)
            return HttpResponse(status=201, reason='User succesfully created')
        except EmailAlreadyTaken:
            return HttpResponse(status=400, reason='Email(%s) is already taken' % email)

    @staticmethod
    def handle_action_log_user_in(request):
        DjangoRequestReceiver.check_for_missed_parameters(request, 'email', 'password')

        db_access = AccessToDjangoUsersDB()
        users_handler = UsersActions(db_access)

        email = request.POST['email']
        password = request.POST['password']

        try:
            token = users_handler.log_user_in(email, password)
            return HttpResponse(status=200, reason='User succesfully logged in', content='token: ' + token)
        except WrongPassword:
            return HttpResponse(status=401, reason='Incorrect password for user')
        except UserNotExists:
            return HttpResponse(status=404, reason='User not found')

    @staticmethod
    def handle_action_log_user_out(request):
        DjangoRequestReceiver.check_for_missed_parameters(request, 'token')

        db_access = AccessToDjangoUsersDB()
        users_handler = UsersActions(db_access)

        token = request.POST['token']

        try:
            users_handler.log_user_out(token)
            return HttpResponse(status=200, reason='User succesfully logged out')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_delete_user(request):
        DjangoRequestReceiver.check_for_missed_parameters(request, 'token')

        db_access = AccessToDjangoUsersDB()
        users_handler = UsersActions(db_access)

        token = request.POST['token']

        try:
            users_handler.delete_user(token)
            return HttpResponse(status=200, reason='User succesfully deleted')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_change_user_password(request):
        DjangoRequestReceiver.check_for_missed_parameters(request, 'token', 'newPassword')

        db_access = AccessToDjangoUsersDB()
        users_handler = UsersActions(db_access)

        token = request.POST['token']
        new_password = request.POST['newPassword']

        try:
            users_handler.change_user_password(token, new_password)
            return HttpResponse(status=200, reason='Password succesfully changed')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_change_user_email(request):
        DjangoRequestReceiver.check_for_missed_parameters(request, 'token', 'newEmail')

        db_access = AccessToDjangoUsersDB()
        users_handler = UsersActions(db_access)

        token = request.POST['token']
        new_email = request.POST['newEmail']

        try:
            users_handler.change_user_email(token, new_email)
            return HttpResponse(status=200, reason='Email succesfully changed')
        except EmailAlreadyTaken:
            return HttpResponse(status=400, reason='Email(%s) is already taken' % new_email)
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')


    # @staticmethod
    # def handle_action_(request):
    #     pass
