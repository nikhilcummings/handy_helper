from django.db import models
import re
import pytz
from django.utils import timezone

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors={}
        errors['fName'] =''
        errors['lName'] =''
        errors['email'] =''
        errors['pw'] =''
        errors['cpw'] =''
        
        if len(postData['first_name'])<2:
            errors['fName'] = 'First name should be at least 2 characters'
        elif not LETTER_REGEX.match(postData['first_name']):
            errors['fName'] = 'First name should consist entirely of letters'
        if len(postData['last_name'])<2:
            errors['lName'] = 'Last name should be at least 2 characters'
        elif not LETTER_REGEX.match(postData['last_name']):
            errors['lName'] = 'Last name should consist entirely of letters'
        if len(postData['email'])<5:
            errors['email'] = 'Email address should be at least 5 characters'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please enter a valid email address'
        if len(postData['pw'])<8:
            errors['pw'] = 'Password should be at least 8 characters'
        if postData['cpw'] != postData['pw']:
            errors['cpw'] = 'Password confirmation does not match password'          
        return errors
    def delete_all(self):
        User.objects.all().delete()

class JobManager(models.Manager):
    def basic_validator(self,postData):
        errors={}
        errors['title']=''
        errors['description'] =''
        errors['location']=''
        if len(postData['title'])<3:
            errors['title'] = 'Job title must be at least 3 characters'
        if len(postData['description'])<3:
            errors['description'] = 'Job description must be at least 3 characters'
        if len(postData['location'])<3:
            errors['location'] = 'Job location must be at least 3 characters'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name='posted_jobs')
    owned_by = models.ForeignKey(User, related_name='jobs_owned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

class Categories(models.Model):
    title = models.CharField(max_length=255)
    attached_to = models.ManyToManyField(Job, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)