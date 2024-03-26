from django.db import models

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from uuid import uuid4


class CustomUserManager(BaseUserManager):
    """Custom manager class
    Args:
        BaseUserManager (_type_): _description_
    """

    def create_user(self, email: str, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """User model
    Args:
        AbstractBaseUser (_type_): abstract base class
    """

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    username = models.CharField(max_length=255, null=False, blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_artist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label) -> bool:
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class UserMedia(models.Model):

    media_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    user_media = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_media",
        blank=True,
    )
    image = models.ImageField(upload_to="users_media")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User's Media"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # change file names on save
        image_name = "user_image_{}.{}".format(
            str(uuid4()), self.image.name.split(".")[-1]
        )
        self.image.name = image_name

        super(UserMedia, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return "{}".format(self.media_id)
