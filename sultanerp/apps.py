from django.apps import AppConfig


class SultanErpConfig(AppConfig):
    name = 'sultanerp'

    def ready(self):
        print("AppConfig ready method called")
        import sultanerp.signals
