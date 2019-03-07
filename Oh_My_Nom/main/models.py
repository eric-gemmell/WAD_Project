from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	#Users need to contain the following attributes:
		#-A userName and Password
		#-An address so that we know where find their restaurants
		
	#on_delete = models.Cascade means that upon deleteing the profile, the user model that had been created
	# and that is associated here by a one to one relationship will be deleted as well.
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	address = models.CharField(max_length=128)
	
	def __str__():
		return self.user.username
	
