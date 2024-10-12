from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault(
            "profile_picture", "https://dummyimage.com/500/000/fff&text=Admin"
        )
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("balance", 0)
        extra_fields.setdefault("service_price", 1488)

        if extra_fields.get("is_admin") is not True:
            raise ValueError(_("Superuser must have is_admin=True."))

        return self.create_user(email, password, **extra_fields)
