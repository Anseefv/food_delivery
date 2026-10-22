from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    email=models.EmailField(unique=True)
    ROLE_OPTIONS=[
        ('admin','admin'),
        ('resturent_partner','resturent_partner'),
        ('delivery_boy','delivery_boy'),
        ('customer','customer')
    ]
    role=models.CharField(max_length=30,choices=ROLE_OPTIONS,default='customer')

    def __str__(self):
        return self.username


class DeliveryBoyProfile(models.Model):

    phone=models.PositiveBigIntegerField(unique=True)
    address=models.TextField()
    photo=models.ImageField(upload_to='profile_photo')
    age=models.PositiveIntegerField()
    document=models.FileField(upload_to='delivery_boy_files')
    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='boyprofile')

    def __str__(self):
        return self.owner.username


class Resturent_PartnerProfile(models.Model):

    phone=models.PositiveBigIntegerField(unique=True)
    address=models.TextField()
    photo=models.ImageField(upload_to='Partner_photo')
    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='partnerprofile')

    def __str__(self):
        return self.owner.username



# resturent  and branches


class Resturent(models.Model):

    name=models.CharField(max_length=100,unique=True)
    added_at=models.DateTimeField(auto_now_add=True)
    owner=models.OneToOneField(Resturent_PartnerProfile,on_delete=models.CASCADE,related_name='resturent')
    
    def __str__(self):
        return self.name

class ResturentBranches(models.Model):

    place=models.CharField(max_length=100)
    address=models.TextField()
    open_time=models.TimeField()
    closing_time=models.TimeField()
    main_resturent=models.ForeignKey(Resturent,on_delete=models.CASCADE,related_name='branches')

    def __str__(self):
        return f"{self.main_resturent.name} - {self.place}"
