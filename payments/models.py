from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User, UUIDModel


class Transaction(UUIDModel):
    class PaymentTypes(models.TextChoices):
        GOOGLE_PAY = "GP", _("Google Pay")
        CREDIT_CARD = "CC", _("Credit card")

    class Statuses(models.TextChoices):
        PENDING = "PE", _("Pending")
        SUCCESS = "SS", _("Success")
        CANCELED = "CD", _("Canceled")

    user = models.ForeignKey(User, models.SET_NULL, null=True)
    credits_amount = models.PositiveSmallIntegerField()
    payment_type = models.CharField(max_length=2, choices=PaymentTypes)
    status = models.CharField(max_length=2, choices=Statuses)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
