from django.contrib.auth.models import User
from django.db import models

from .app_settings import DISTRICT_CHOICES


class TrinityUserProfile(models.Model):
    """User profile fields specific to Trinity Education
    """
    user = models.ForeignKey(User, db_index=True, related_name="trinitypreferences")
    district = models.CharField(verbose_name='School District', blank=True, 
    	                        max_length=6, choices=DISTRICT_CHOICES)
	