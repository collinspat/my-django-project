from django.contrib.auth.models import AbstractUser, UserManager  # Importing necessary classes from Django's auth system
from django.db import models  # Importing Django's model module for ORM functionality
from django.contrib.auth.hashers import make_password  # Importing Django's password hashing function
from django.db.models.signals import post_save  # Importing Django's signal for actions post model save
from django.dispatch import receiver  # Importing Django's receiver for handling signals

class CustomUserManager(UserManager):
    # Custom user manager that overrides the default UserManager to handle user creation with email instead of username
    def _create_user(self, email, password, **extra_fields):
        # Protected method to create and save a user with the given email and password
        email = self.normalize_email(email)  # Normalizes the email address by lowercasing the domain part of it
        user = CustomUser(email=email, **extra_fields)  # Creates a new CustomUser instance
        user.password = make_password(password)  # Hashes the user's password
        user.save(using=self._db)  # Saves the CustomUser instance using the current database
        return user  # Returns the created CustomUser instance

    def create_user(self, email, password=None, **extra_fields):
        # Public method to create a regular user with the given email and password
        extra_fields.setdefault("is_staff", False)  # Sets 'is_staff' to False by default
        extra_fields.setdefault("is_superuser", False)  # Sets 'is_superuser' to False by default
        return self._create_user(email, password, **extra_fields)  # Calls the protected method to create the user

    def create_superuser(self, email, password=None, **extra_fields):
        # Public method to create a superuser with the given email and password
        extra_fields.setdefault("is_staff", True)  # Sets 'is_staff' to True by default for superusers
        extra_fields.setdefault("is_superuser", True)  # Sets 'is_superuser' to True by default for superusers
        extra_fields.setdefault("user_type", 1)  # Sets the user type to Admin by default for superusers
        extra_fields.setdefault("last_name", "System")  # Sets a default last name
        extra_fields.setdefault("first_name", "Administrator")  # Sets a default first name

        assert extra_fields["is_staff"]  # Asserts that 'is_staff' is True
        assert extra_fields["is_superuser"]  # Asserts that 'is_superuser' is True
        return self._create_user(email, password, **extra_fields)  # Calls the protected method to create the superuser


class CustomUser(AbstractUser):
    # Custom user model that extends Django's AbstractUser
    USER_TYPE = ((1, "Admin"), (2, "Voter"))  # Defines user types as a tuple of tuples
    username = None  # Removes the username field, using email as the primary identifier instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=2, choices=USER_TYPE, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + " " + self.first_name
