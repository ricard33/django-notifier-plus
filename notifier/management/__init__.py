###############################################################################
## Imports
###############################################################################
# Python
from importlib import import_module

# Django
from django.conf import settings

# User
import notifier
from notifier.models import Backend
from notifier import settings as notifier_settings


###############################################################################
## Code
###############################################################################
def create_backends(app, **kwargs):
    """
    Creates/Updates Backend objects based on NOTIFIER_BACKENDS settings.

    All values except `enabled` are derived from the Backend class and
    not suppossed to be modified by user. They will be over-written on restart.
    """

    for klass in notifier_settings.BACKEND_CLASSES:
        try:
            backend = Backend.objects.get(name=klass.name)
        except Backend.DoesNotExist:
            backend = Backend()
            backend.enabled = True
        finally:
            backend.display_name = klass.display_name
            backend.name = klass.name
            backend.description = klass.description
            backend.klass = ('.'.join([klass.__module__, klass.__name__]))
            backend.save()


def create_notifications(app, **kwargs):
    """
    Creates all the notifications specified in notifiers.py for all apps
    in INSTALLED_APPS
    """

    for installed_app in settings.INSTALLED_APPS:
        try:
            import_module(installed_app + '.notifications')
        except ImportError:
            pass



# post_syncdb.connect(
#     create_backends,
#     dispatch_uid="notifier.management.create_backends",
#     sender=notifier.models
# )
# post_syncdb.connect(
#     create_notifications,
#     dispatch_uid="notifier.management.create_notifications",
#     sender=notifier.models
# )
