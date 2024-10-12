from django.db import models

from users.models import ActivityCategoryRelation, ServiceTypes, User, UUIDModel


class Advertisement(UUIDModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_price = models.FloatField(default=0)
    number_of_views = models.PositiveIntegerField(default=0)
    service_type = models.CharField(max_length=2, choices=ServiceTypes)
    user_id = models.ForeignKey(User, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "advertisements"


class ActivityCategoryAdvertisement(ActivityCategoryRelation):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)

    class Meta:
        db_table = "activity_categories_advertisements"
        unique_together = ("advertisement", "type", "category")
