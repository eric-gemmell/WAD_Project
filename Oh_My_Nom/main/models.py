from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=128)

	def __str__(self):
		return self.user.username + "; location: "+ self.location

class Restaurant(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	place_id = models.CharField(max_length=200)

	def __str__(self):
		return "User '{}' saved restaurant: {}".format(self.user.username,self.place_id)
