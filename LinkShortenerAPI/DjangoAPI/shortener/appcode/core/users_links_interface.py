class UsersLinksInterface:
    def add_link(self, user_token, shortlink, longlink, password):
        pass

    def delete_link(self, user_token, shortlink):
        pass

    def modify_shortlink(self, user_token, old_shortlink, new_shortlink):
        pass

    def modify_longlink(self, user_token, shortlink, new_longlik):
        pass

    def modify_password(self, user_token, shortlink, new_password):
        pass

    def change_user_email(self, token, new_email):
        pass

    def get_user_shotlinks_table(self, token):
        pass
