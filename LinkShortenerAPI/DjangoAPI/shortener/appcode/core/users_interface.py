class UsersInterface:
    def create_user(self, email, password):
        pass

    def delete_user(self, token):
        pass

    def change_user_password(self, token, new_password):
        pass

    def log_user_in(self, email, password):
        pass

    def log_user_out(self, token):
        pass

    def extend_token(self, token):
        pass

    def expire_token(self, token):
        pass

    def get_user_for_token(self, token):
        pass

    def validate_token(self, token):
        pass

    @staticmethod
    def generate_token_for_user():
        pass
