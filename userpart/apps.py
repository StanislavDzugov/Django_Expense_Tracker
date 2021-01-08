from django.apps import AppConfig


class UserpartConfig(AppConfig):
    name = 'userpart'

    def ready(self):
        import userpart.signals