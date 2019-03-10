class LinksInterface:
    def add_link(self, longlink, link_password='', shortlink=None, user_token=None, expiration_date=None):
        pass

    def delete_link(self, user_token, shortlink):
        pass

    def modify_shortlink(self, user_token, old_shortlink, new_shortlink):
        pass

    def modify_longlink(self, user_token, shortlink, new_longlink):
        pass

    def modify_link_password(self, user_token, shortlink, new_password):
        pass

    def get_longlink_from_shortlink(self, shortlink, password=''):
        pass

    def get_shortlink_data(self, shortlink):
        pass

    def get_user_shortlinks_table(self, user_token):
        pass
