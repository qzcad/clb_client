from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'client'

    def ready(self):
        import signals
