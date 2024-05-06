from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile
# Signals 
# this post_save signals 
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print('created')
    if created:
        UserProfile.objects.create(user=instance)
        print('created the user profile')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('user is updated')
        except:
            # create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print('Profile was not exist, but i created one')
        print('User is Updated')


# this pre-save signal
@receiver(pre_save, sender=User)
def pre_save_profile_recevier(sender, instance, **kwargs):
    print(instance.username,'this is user is being saved')