from shortener.appcode.django_db_interfaces.django_links_interface import AccessToDjangoLinksDB
from shortener.appcode.django_db_interfaces.django_users_interface import AccessToDjangoUsersDB
from shortener.appcode.django_db_interfaces.django_users_links_interface import AccessToDjangoUsersLinksDB

from shortener.appcode.core.users_handle import UsersActions
from shortener.appcode.core.links_handle import LinksActions
from shortener.appcode.core.users_links_handle import UsersLinksActions
from shortener.appcode.core.db_errors import *

# from shortener.appcode.core.shortlink_data import ShortlinkData
# from shortener.appcode.core.shortlinks_table import ShortlinksTable

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


class MissedParameters(Exception): pass


def bool_to_str(variable):
    return str(int(variable))


def check_request_for_missed_parameters(request, *parameters):
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


class DjangoRequestReceiver:
    @staticmethod
    def get_links_interface():
        return LinksActions(AccessToDjangoLinksDB())

    @staticmethod
    def get_users_interface():
        return UsersActions(AccessToDjangoUsersDB())

    @staticmethod
    def get_users_links_interface():
        return UsersLinksActions(AccessToDjangoUsersLinksDB())

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
            if action == 'createuser':
                return DjangoRequestReceiver.handle_action_create_user(request)
            if action == 'loguserin':
                return DjangoRequestReceiver.handle_action_log_user_in(request)
            if action == 'loguserout':
                return DjangoRequestReceiver.handle_action_log_user_out(request)
            if action == 'deleteuser':
                return DjangoRequestReceiver.handle_action_delete_user(request)
            if action == 'changeuserpassword':
                return DjangoRequestReceiver.handle_action_change_user_password(request)
            if action == 'changeuseremail':
                return DjangoRequestReceiver.handle_action_change_user_email(request)
            if action == 'createshortlink':
                return DjangoRequestReceiver.handle_action_create_link(request)
            if action == 'deleteshortlink':
                return DjangoRequestReceiver.handle_action_delete_link(request)
            if action == 'modifyshortlink':
                return DjangoRequestReceiver.handle_action_modify_shortlink(request)
            if action == 'modifylonglink':
                return DjangoRequestReceiver.handle_action_modify_longlink(request)
            if action == 'modifypassword':
                return DjangoRequestReceiver.handle_action_modify_shortlink_password(request)
            if action == 'translate':
                return DjangoRequestReceiver.handle_action_translate(request)
            if action == 'checklink':
                return DjangoRequestReceiver.handle_action_check_link(request)
            if action == 'getuserlinks':
                return DjangoRequestReceiver.handle_action_get_user_links(request)
            # if action == '':
            #     return DjangoRequestReceiver.handle_action_(request)
        except MissedParameters as error:
            return error.response
        except BaseException as error:
            return HttpResponse(status=500, reason='Internal Server Error')  # TODO add log saving

        return HttpResponse(status=405, reason="Action '%s' is not supported" % action)

    @staticmethod
    def handle_action_create_user(request):
        check_request_for_missed_parameters(request, 'email', 'password')
        email = request.POST['email']
        password = request.POST['password']

        users_interface = DjangoRequestReceiver.get_users_interface()

        try:
            users_interface.create_user(email, password)
            return HttpResponse(status=201, reason='User succesfully created')
        except EmailAlreadyTaken:
            return HttpResponse(status=400, reason='Email(%s) is already taken' % email)
        except ValidationError:
            return HttpResponse(status=400, reason='password does not meet requirements')

    @staticmethod
    def handle_action_log_user_in(request):
        check_request_for_missed_parameters(request, 'email', 'password')
        email = request.POST['email']
        password = request.POST['password']

        users_interface = DjangoRequestReceiver.get_users_interface()

        try:
            token = users_interface.log_user_in(email, password)
            return HttpResponse(status=200, reason='User succesfully logged in', content=token)
        except WrongPassword:
            return HttpResponse(status=401, reason='Incorrect password for user')
        except UserNotExists:
            return HttpResponse(status=404, reason='User not found')

    @staticmethod
    def handle_action_log_user_out(request):
        check_request_for_missed_parameters(request, 'token')
        token = request.POST['token']

        users_interface = DjangoRequestReceiver.get_users_interface()

        try:
            users_interface.log_user_out(token)
            return HttpResponse(status=200, reason='User succesfully logged out')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')

    @staticmethod
    def handle_action_delete_user(request):
        check_request_for_missed_parameters(request, 'token')
        token = request.POST['token']

        users_interface = DjangoRequestReceiver.get_users_interface()

        try:
            users_interface.delete_user(token)
            return HttpResponse(status=200, reason='User succesfully deleted')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_change_user_password(request):
        check_request_for_missed_parameters(request, 'token', 'newPassword')
        token = request.POST['token']
        new_password = request.POST['newPassword']

        users_interface = DjangoRequestReceiver.get_users_interface()

        try:
            users_interface.change_user_password(token, new_password)
            return HttpResponse(status=200, reason='Password succesfully changed')
        except ValidationError:
            return HttpResponse(status=400, reason='password does not meet requirements')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_change_user_email(request):
        check_request_for_missed_parameters(request, 'token', 'newEmail')
        token = request.POST['token']
        new_email = request.POST['newEmail']

        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            users_links_interface.change_user_email(token, new_email)
            return HttpResponse(status=200, reason='Email succesfully changed')
        except EmailAlreadyTaken:
            return HttpResponse(status=400, reason='Email(%s) is already taken' % new_email)
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_create_link(request):
        check_request_for_missed_parameters(request, 'longLink')
        shortlink = request.POST.get('shortLink', '')
        longlink = request.POST['longLink']
        link_password = request.POST.get('linkPassword', '')
        token = request.POST.get('token', '')

        try:
            if token == '':
                return DjangoRequestReceiver.create_anonymous_link(longlink, link_password)
            else:
                return DjangoRequestReceiver.create_link_for_user(shortlink, longlink, link_password, token)
        except ValidationError:
            return HttpResponse(status=400, reason='shortlink, longlink or password does not meet requirements')

    @staticmethod
    def handle_action_delete_link(request):
        check_request_for_missed_parameters(request, 'token', 'shortLink')
        token = request.POST['token']
        shortlink = request.POST['shortLink']

        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            users_links_interface.delete_link(token, shortlink)
            return HttpResponse(status=200, reason='Shortlink succesfully deleted')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except ShortLinkNotExists:
            return HttpResponse(status=404, reason='Shortlink not found')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_modify_shortlink(request):
        check_request_for_missed_parameters(request, 'token', 'shortLink', 'newShortLink')
        token = request.POST['token']
        shortlink = request.POST['shortLink']
        new_shortlink = request.POST['newShortLink']

        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            users_links_interface.modify_shortlink(token, shortlink, new_shortlink)
            return HttpResponse(status=200, reason='Shortlink succesfully modified')
        except ValidationError:
            return HttpResponse(status=400, reason='shortlink does not meet requirements')
        except ShortLinkAlreadyTaken:
            return HttpResponse(status=400, reason='Shortlink(%s) is already taken' % new_shortlink)
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except ShortLinkNotExists:
            return HttpResponse(status=404, reason='Shortlink not found')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_modify_longlink(request):
        check_request_for_missed_parameters(request, 'token', 'shortLink', 'newLongLink')
        token = request.POST['token']
        shortlink = request.POST['shortLink']
        new_longlink = request.POST['newLongLink']

        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            users_links_interface.modify_longlink(token, shortlink, new_longlink)
            return HttpResponse(status=200, reason='Longlink succesfully modified')
        except ValidationError:
            return HttpResponse(status=400, reason='longlink does not meet requirements')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except ShortLinkNotExists:
            return HttpResponse(status=404, reason='Shortlink not found')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_modify_shortlink_password(request):
        check_request_for_missed_parameters(request, 'token', 'shortLink', 'newPassword')
        token = request.POST['token']
        shortlink = request.POST['shortLink']
        new_password = request.POST['newPassword']

        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            users_links_interface.modify_password(token, shortlink, new_password)
            return HttpResponse(status=200, reason='Password succesfully modified')
        except ValidationError:
            return HttpResponse(status=400, reason='password does not meet requirements')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except ShortLinkNotExists:
            return HttpResponse(status=404, reason='Shortlink not found')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    @staticmethod
    def handle_action_translate(request):
        check_request_for_missed_parameters(request, 'shortLink')
        shorlink = request.POST['shortLink']
        password = request.POST.get('linkPassword', '')

        links_interface = DjangoRequestReceiver.get_links_interface()

        try:
            longlink = links_interface.get_longlink_from_shortlink(shorlink, password)
            return HttpResponse(content=longlink, status=200,
                                reason='Successful translation to longlink')
        except IncorrectPasswordForShortLink:
            return HttpResponse(status=401, reason='Incorrect password for shortlink')
        except ShortLinkNotExists:
            return HttpResponse(status=404, reason='Shortlink not found')

    @staticmethod
    def handle_action_check_link(request):
        check_request_for_missed_parameters(request, 'shortLink')
        shorlink = request.POST['shortLink']

        links_interface = DjangoRequestReceiver.get_links_interface()

        shorlink_data = links_interface.get_shortlink_data(shorlink)
        content = 'exists: ' + bool_to_str(shorlink_data.exists()) + \
                  '; needsPassword: ' + bool_to_str(shorlink_data.does_need_password()) + \
                  '; belongsToUser: ' + bool_to_str(shorlink_data.does_belong_to_user()) + \
                  '; expirationDate: ' + str(shorlink_data.get_expiration_date())

        return HttpResponse(content=content, status=200, reason='Request done')

    @staticmethod
    def handle_action_get_user_links(request):
        check_request_for_missed_parameters(request, 'token')
        token = request.POST['token']

        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            shortlinks_table = users_links_interface.get_user_shortlinks_table(token)
            return HttpResponse(content=str(shortlinks_table), status=200,
                                reason='Links returned', content_type='application/json')
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')

    # @staticmethod
    # def handle_action_(request):
    #     pass

    @staticmethod
    def create_anonymous_link(longlink, link_password):
        links_interface = DjangoRequestReceiver.get_links_interface()

        shortlink = links_interface.add_anonymous_shortlink(longlink, link_password)
        return HttpResponse(content=shortlink, status=201, reason='Shortlink succesfully added')

    @staticmethod
    def create_link_for_user(shortlink, longlink, link_password, user_token):
        users_links_interface = DjangoRequestReceiver.get_users_links_interface()

        try:
            if shortlink == '':
                shortlink = users_links_interface.add_random_link(user_token, longlink, link_password)
            else:
                users_links_interface.add_link(user_token, shortlink, longlink, link_password)
            return HttpResponse(content=shortlink, status=201, reason='Shortlink succesfully added')
        except ShortLinkAlreadyTaken:
            return HttpResponse(status=400, reason='Shortlink(%s) is already taken' % shortlink)
        except InvalidToken:
            return HttpResponse(status=401, reason='Invalid token')
        except TokenExpired:
            return HttpResponse(status=408, reason='Token expired')
