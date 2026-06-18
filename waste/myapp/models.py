
from django.db import models
from django.contrib.auth.models import AbstractUser


# ---------------- LOGIN ---------------- #

class Login(AbstractUser):
    userType = models.CharField(
        max_length=50
    )  

    viewPass = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


# ---------------- CITIZEN (USER) ---------------- #

class UserProfile(models.Model):
    loginid = models.ForeignKey(
        Login,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    address = models.TextField()

    profile_pic = models.ImageField(
        upload_to="user_profiles",
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# ---------------- WASTE COLLECTION STAFF ---------------- #

class StaffProfile(models.Model):
    loginid = models.ForeignKey(
        Login,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    address = models.TextField()

    status = models.CharField(
        max_length=30,
        default="pending"
    )  

    profile_pic = models.ImageField(
        upload_to="staff_profiles",
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# ---------------- RECYCLING CENTER ---------------- #

class RecyclingCenterProfile(models.Model):
    loginid = models.ForeignKey(
        Login,
        on_delete=models.CASCADE
    )

    center_name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    status = models.CharField(
        max_length=30,
        default="pending"
    ) 

    logo = models.ImageField(
        upload_to="recycling_centers",
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.center_name


# ---------------- SMART WASTE BIN ---------------- #

