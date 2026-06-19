
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

class WasteBin(models.Model):
    bin_code = models.CharField(
        max_length=100,
        unique=True
    )

    location = models.TextField()

    waste_type = models.CharField(
        max_length=100
    )

    capacity = models.FloatField()

    current_level = models.FloatField(
        default=0
    )

    status = models.CharField(
        max_length=50,
        default="empty"
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    installation_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.bin_code


# ---------------- PICKUP REQUEST ---------------- #

class PickupRequest(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    waste_type = models.CharField(
        max_length=100
    )

    quantity = models.CharField(
        max_length=100
    )

    pickup_address = models.TextField()

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=50,
        default="pending"
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
        return f"{self.user.name} - {self.waste_type}"


# ---------------- COLLECTION TASK ---------------- #

class CollectionTask(models.Model):
    pickup_request = models.ForeignKey(
        PickupRequest,
        on_delete=models.CASCADE
    )

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE
    )

    assigned_date = models.DateTimeField(
        auto_now_add=True
    )

    scheduled_date = models.DateField(
        null=True,
        blank=True
    )

    scheduled_time = models.TimeField(
        null=True,
        blank=True
    )

    collection_status = models.CharField(
        max_length=50,
        default="assigned"
    )

    collected_quantity = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    notes = models.TextField(
        null=True,
        blank=True
    )

    completed_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.pickup_request.id} - {self.staff.name}"


# ---------------- WASTE COLLECTION RECORD ---------------- #

class WasteCollectionRecord(models.Model):
    task = models.ForeignKey(
        CollectionTask,
        on_delete=models.CASCADE
    )

    recycling_center = models.ForeignKey(
        RecyclingCenterProfile,
        on_delete=models.SET_NULL,
        null=True
    )

    collected_at = models.DateTimeField(
        auto_now_add=True
    )

    total_quantity = models.CharField(
        max_length=100
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Collection #{self.id}"


# ---------------- BIN REPORT ---------------- #

class BinReport(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    bin = models.ForeignKey(
        WasteBin,
        on_delete=models.CASCADE
    )

    issue_type = models.CharField(
        max_length=100
    )

    description = models.TextField()

    status = models.CharField(
        max_length=30,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.bin.bin_code} - {self.issue_type}"


# ---------------- RECYCLING RECORD ---------------- #

class RecyclingRecord(models.Model):
    center = models.ForeignKey(
        RecyclingCenterProfile,
        on_delete=models.CASCADE
    )

    waste_collection = models.ForeignKey(
        WasteCollectionRecord,
        on_delete=models.CASCADE
    )

    waste_type = models.CharField(
        max_length=100
    )

    quantity = models.CharField(
        max_length=100
    )

    processing_status = models.CharField(
        max_length=50,
        default="pending"
    )

    processed_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.waste_type} - {self.center.center_name}"


# ---------------- FEEDBACK ---------------- #


class Feedback(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.name} - {self.rating}"


# ---------------- COMPLAINT ---------------- #

class Complaint(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    recycling_center = models.ForeignKey(
        RecyclingCenterProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    reply = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subject


# ---------------- NOTIFICATION ---------------- #

class Notification(models.Model):
    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    target_role = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.title