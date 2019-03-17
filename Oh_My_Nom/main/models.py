from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=128)

	def __str__(self):
		return self.user.username + "; location: "+ self.location
