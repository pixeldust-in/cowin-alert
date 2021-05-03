# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from src.core.models import CowinSession


# @receiver(post_save, sender=CowinSession)
# def save_session(sender, instance, **kwargs):
#     from .tasks import handle_session_create  # noqa

#     handle_session_create.delay(instance.id)
