class UsersInterface:
    def create_user(self, email, password):
        pass

    def delete_user(self, email, password):
        pass

    def change_user_password(self, email, old_password, new_password):
        pass

    def change_user_email(self, old_email, new_email, password):
        pass

    def get_user_shotlinks_table(self, email, password):
        pass

    # def validate_user(self, email, password):
    #     pass
