from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

# makes Django load signal so it works.
    def ready(self):
        from . import signals
