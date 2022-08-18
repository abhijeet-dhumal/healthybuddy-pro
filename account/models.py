from time import time, timezone
from django.db import models
from django.contrib.auth.models import PermissionsMixin, User, UserManager
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import BaseUserManager, AbstractUser


CATEGORY = (
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient')
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("Email* ",unique=True)
    name=models.CharField("UserName* ",max_length=200,default='User')
    user_type = models.CharField("UserType* ",
        max_length=520, blank=True, choices=CATEGORY, default='Patient')
    phone = models.CharField("Contact no. ",max_length=200, null=True)
    image = models.ImageField("Profile Image ",upload_to='app/images/users/%Y%m%d',null=True, blank=True)
    age=models.IntegerField("Age ",default=1)
    specialization = models.CharField("Area of Expertise(For doctor user only) ", max_length=100, blank=True)
    address_line1 = models.CharField("Address_Line1 ", max_length=100, blank=True)
    city = models.CharField("City ", max_length=50, blank=True)
    state = models.CharField("State ", max_length=50, blank=True)
    country = models.CharField("Country ", max_length=50, blank=True)
    pincode = models.CharField("Pincode ", max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
from django.db import models
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from .models import User

BLOG_CATEGORY=(
    ('Mental health','Mental health'),
    ('Heart disease','Heart disease'),
    ('Covid-19','Covid-19'),
    ('Immunization','Immunization'),
)
CHOICES=(
    ('Save as a draft','Save as a draft'),
    ('Post content as a blog','Post content as a blog'),
)  
from django.utils import timezone
class Blog(TimeStampedModel):
    category = models.CharField(max_length=50, choices=BLOG_CATEGORY, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    text = models.CharField(max_length=1024, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='app/images/blog/%Y%m%d')
    publish_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    draft=models.BooleanField(default=False)

    def __str__(self):
        if self.title==None:
            return "ERROR-BLOG TITLE NAME IS NULL"
        return self.title


    class Meta:
        ordering = ('-publish_on',)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField(max_length=500)
    is_read =models.BooleanField(default=False)
    datetime= models.DateTimeField(blank=True,auto_now_add=True)
    value=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return "Notification: " + str(self.text)

class AppointmentSlot(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)

    def __str__(self):
        return "Doctor User: " + str(self.user) + " | Date: " + str(self.date)+ " | Time slot: " + str(self.start_time)+" to "+str(self.end_time)

from django.core.mail import EmailMessage

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE,default=None)
    is_accepted = models.BooleanField(default=None,null=True,blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        if self.is_accepted:
            accepted='Accepted'
        else:
            accepted='Rejected'
        return str(self.user) + " | " + str(self.slot) + " | " + str(accepted)

    def save(self,*args,**kwargs):
        if self.is_accepted!=None:
            if self.is_accepted==True and self.is_paid==False:
                notifications_objs= Notification(user=self.user,text=f' "{self.user.first_name} {self.user.last_name}" has accepted/booked for the appointment slot scheduled with : \n"{self.slot}" ,\n Proceed with Payment.')
                email = EmailMessage('HealthyBuddy Notification', f' "{self.user.first_name} {self.user.last_name}" has accepted/booked for the appointment slot scheduled with : \n"{self.slot}" ,\n Proceed with Payment.', to=[f'{self.user.email}'])
                email.send()
            elif self.is_accepted==True and self.is_paid==True:
                notifications_objs= Notification(user=self.user,text=f'Payment successfull for this service.Appointment is booked for the slot : \n"{self.slot}".')
                email = EmailMessage('HealthyBuddy Notification', f'Payment successfull for this service.Appointment is booked for the slot : \n"{self.slot}".', to=[f'{self.user.email}'])
                email.send()

            notifications_objs.save()
        
        super(Appointment,self).save(*args,**kwargs)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars=models.IntegerField(default=0)
    comment =models.CharField(max_length=50)
    feedback =models.CharField(max_length=100,null=True, blank=True)
    posted_on= models.DateTimeField(blank=True,auto_now_add=True)

    def __str__(self):
        return "Review: " + str(self.user)

class Contact(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    message =models.CharField(max_length=100)
    feedback =models.CharField(max_length=100,null=True, blank=True)
    posted_on= models.DateTimeField(blank=True,auto_now_add=True)

    def __str__(self):
        return "Contact: " + str(self.name)
