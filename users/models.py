import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .mixins import CustomPermissionMixin


class ServicePriceTypes(models.TextChoices):
    PER_HOUR = "PH", _("Per hour")
    PER_LESSON = "PL", _("Per lesson")


class ServiceTypes(models.TextChoices):
    SEEKING = "S", _("Seeking")
    PROVIDING = "P", _("Providing")


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(UUIDModel, AbstractBaseUser, CustomPermissionMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)
    name = models.CharField(max_length=50)
    profile_picture = models.URLField()
    id_card_photo = models.URLField(null=True)
    is_verified = models.BooleanField(default=False)
    balance = models.PositiveSmallIntegerField(default=0)
    cv_link = models.URLField(null=True)
    about_me_text = models.TextField(blank=True)
    about_me_video_link = models.URLField(null=True)
    service_price = models.FloatField()
    service_price_type = models.CharField(
        max_length=2, choices=ServicePriceTypes, default=ServicePriceTypes.PER_LESSON
    )
    longitude = models.CharField(max_length=25, blank=True)
    latitude = models.CharField(max_length=25, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_staff(self):
        """ Return True if the user is an admin. """
        return self.is_admin

    # Custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class UserVerifications(UUIDModel):
    class Statuses(models.TextChoices):
        PENDING = (
            "PD",
            _("Pending"),
        )
        APPROVED = (
            "AP",
            _("Approved"),
        )
        DECLINED = (
            "DC",
            _("Declined"),
        )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Statuses)
    admin_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_verifications"


class ActivityCategory(UUIDModel):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "activity_categories"


class ActivityCategoryRelation(models.Model):
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=ServiceTypes)

    class Meta:
        abstract = True


class ActivityCategoryUser(ActivityCategoryRelation):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "activity_categories_users"
        unique_together = ("user", "type", "category")
