from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.contrib.auth.models import User
from django.dispatch import receiver

from django.db.models.signals import (pre_save,
                                      post_save,
                                      pre_delete,
                                      post_delete
                                      )
from .models import Profile


def login_success(sender, request, user, **kwargs):
    print("-------")
    print(
        "loged in signal...Run intro:",
    )
    print("sender:", sender)
    print("request:", request)
    print("user:", user)
    print("user password:", user.password)
    print(f"kwags: {kwargs}")


user_logged_in.connect(login_success, sender=User)


def logout_success(sender, request, user, **kwargs):
    print("-------")
    print(
        "loged out in signal...Run intro:",
    )
    print("sender:", sender)
    print("request:", request)
    print("user:", user)
    print(f"kwags: {kwargs}")


@receiver(user_login_failed)
def login_fail(sender, request, credentials, **kwargs):
    print("-------")
    print(
        "login fail signal...Run intro:",
    )
    print("sender:", sender)
    print("request:", request)
    print("cred:", credentials)
    print(f"kwags: {kwargs}")


# user_logged_out.connect(logout_success, sender=User)


# models signals views
# pre_save()
@receiver(pre_save, sender=User)
def begining_save(sender, instance, **kwargs):
    print("-------")
    print(
        "pre save begining...Run intro:",
    )
    print("sender:", sender)
    print("instance:", instance)
    print(f"kwags: {kwargs}")
# pre_save.connect(begining_save, sender=User)

# post_save()
@receiver(post_save, sender=User)
def end_of_save(sender, instance, created, **kwargs):
    print("-------")
    print(
        "post save end of save...Run intro:",
    )

    if created:  # new record created
        print("sender:", sender)
        print("created:", created)
        print("instance:", instance)
        print(f"kwags: {kwargs}")
    else:  # update
        print(f"{instance.username} is update")
# pre_save.connect(end_of_save, sender=User)

# pre_delete()


@receiver(pre_delete, sender=User)
def begining_delete(sender, instance, **kwargs):
    print("-------")
    print(
        "pre delete begining...Run intro:",
    )
    print("sender:", sender)
    print("instance:", instance)
    print(f"kwags: {kwargs}")
# pre_delete.connect(begining_delete, sender=User)

# post_delete()


@receiver(post_delete, sender=User)
def end_of_delete(sender, instance, **kwargs):
    print("-------")
    print(
        "post delete ...Run intro:",
    )

    print("sender:", sender)
    print("instance:", instance)
    print(f"kwags: {kwargs}")
# post_delete.connect(end_of_delete, sender=User)


# Q1.create a user profile if user created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile when a new user is saved.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver function to save the user profile when the user is saved.
    """
    instance.profile.save()


# Q2.if use profile model is_active fields is updated to false create a
# signals to send message

# @receiver(pre_save, sender=Profile)
def pre_notify_when_user_active_turn_to_false(sender, instance, **kwargs):
    """
    Signal receiver function to print a message when the is_active 
    field is updated to False.
    """
    if instance.is_active is False:
        print("pre save -- User is turning inactive. Send a notification.")


# q2 same using post save


@receiver(post_save, sender=Profile)
def post_notify_when_user_active_turn_to_false(
    sender, instance, created, update_fields, **kwargs
):
    """
    Signal receiver function to print a message when the is_active
    field is updated to False.
    """
    if not created and "is_active" in update_fields and \
            instance.is_active is False:

        user = instance.user
        message = (
            f"Post-save: User {user.username} ({user.email}) and their "
            "profile are deactivated."
        )
        print(message)
        # Add your logic for sending a notification here
