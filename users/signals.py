from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Profile


def create_profile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile(
            user=user,
            user_name=user.username,
            name=user.first_name,
            email=user.email
        )
        profile.save()
        subject = 'Welcome To BlogEx'
        message= 'Thank You For Signing Up'
        recipient_list =[profile.email,]

        send_mail(
            subject=subject,
            message=message,
            from_email='contact.echeckup@gmail.com',
            recipient_list=recipient_list,
            fail_silently=False
        )


def update_profile(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user

    if created is False:
        user.username = profile.user_name
        user.first_name = profile.name
        user.email = profile.email
        user.save()


post_save.connect(create_profile,sender=User)
post_save.connect(update_profile,sender=Profile)


@receiver(post_delete,sender=Profile)
def delete_user(sender,instance,**kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
