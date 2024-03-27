from django.db import models

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

from uuid import uuid4


phone_regex = RegexValidator(
    regex=r"^(\+\d{1,3})?,?\s?\d{8,13}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)


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
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex],
        blank=True,
        null=True,
        unique=True,
        help_text="format: +25470000000 start with your country code",
    )
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    is_artist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

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

    def delete(self, *args, **kwargs):
        """Delete local files on delete"""
        if self.image:
            self.image.delete()
        return super(UserMedia, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return "{}".format(self.media_id)
