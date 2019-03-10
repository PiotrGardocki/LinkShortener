class UsersInterface:
    def create_user(self, email, password):
        pass

    def log_user_in(self, email, password):
        pass

    def log_user_out(self, token):
        pass

    def delete_user(self, token):
        pass

    def change_user_password(self, token, new_password):
        pass

    def change_user_email(self, token, new_email):
        pass

    def validate_token(self, token):
        pass

    def refresh_token(self, token):
        pass
