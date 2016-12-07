from django.db import models

# Create your models here.
class Users(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	def __unicode__(self):
		return self.username


