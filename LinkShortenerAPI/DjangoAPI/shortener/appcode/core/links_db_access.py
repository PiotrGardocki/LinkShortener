class LinksDBInterface:
    def get_longlink_from_shortlink(self, shortlink, password=''): pass

    def check_if_shortlink_is_in_db(self, shortlink): pass

    def check_if_shortlink_has_password(self, shortlink): pass

# methods for inserting links
    def save_longlink_and_generate_shortlink(self, longlink, password=''): pass

    def save_shortlink_and_longlink(self, shortlink, longlink, password=''): pass

# methods for modyfying links
    def change_shortlink(self, old_shortlink, new_shortlink): pass

    def change_longlink(self, shortlink, old_longlink, new_longlink): pass

    def change_password(self, shortlink, old_password, new_password): pass
