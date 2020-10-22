from django.apps import AppConfig

from django_oso import Oso

class SocialConfig(AppConfig):
    name = 'social'

    def ready(self):
        from django.contrib.auth.models import Group
        Oso.register_class(Group, name="django::contrib::auth::Group")
        Oso.register_constant(None, name="None")
