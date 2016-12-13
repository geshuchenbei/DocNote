from django.db import models

# Create your models here.
class Users(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	def __unicode__(self):
		return self.username

class SortTree(models.Model):
	parendid = models.IntegerField()
	key = models.CharField(max_length=300)
	level = models.IntegerField()
	owner = models.IntegerField()
	value = models.CharField(max_length=300)
	pathvalue = models.CharField(max_length=300)

class Docs(models.Model):
	docname = models.CharField(max_length=200)
	readstatus = models.CharField(max_length=50)
	docurl = models.CharField(max_length=300)
	readlog = models.TextField()
	usernote = models.TextField() 
	treenodeid = models.IntegerField()
	owner = models.IntegerField()
	docfile = models.FileField(upload_to="uploads/",null=True)
