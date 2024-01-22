from django.contrib.auth.models import BaseUserManager


class CustomManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None, **kwargs):
        user_instance = self.model(
            email=email, first_name=first_name, last_name=last_name, **kwargs
        )
        user_instance.set_password(password)
        user_instance.save()
        return user_instance

    def create_superuser(self, email, first_name, last_name, password=None):
        others_params = {"is_superuser": True, "is_staff": True}
        return self.create_user(email, first_name, last_name, password, **others_params)