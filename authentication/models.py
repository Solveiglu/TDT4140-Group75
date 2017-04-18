from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.backends import ModelBackend

#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    bio = models.TextField(max_length=500, blank=True)
#    firstName = models.CharField(max_length=30, blank=True)
#    lastName = models.CharField(max_length=30, blank=True)
#    birthDate = models.DateField(null=True, blank=True)

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)#

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

