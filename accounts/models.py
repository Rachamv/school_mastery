from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(null=False, unique=True, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()
    user_type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    first_name = models.CharField(_('first name'), max_length=150, null=False, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, null=False, blank=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    street_address1 = models.CharField(max_length=100, null=True, blank=True)
    street_address2 = models.CharField(max_length=100, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label="Country", null=False, blank=False)


class Teacher(models.Model):
    MR, MRS, MS, DR, BLANK = 'Mr', 'Mrs', 'Ms', 'Dr', ''
    HONORIFIC_TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MS, 'Ms'),
        (DR, 'Dr'),
        (BLANK, ''),
    )

    user = models.OneToOneField(
        get_user_model(),
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='teacher',
        null=False
    )
    honorific_title = models.CharField(max_length=3, choices=HONORIFIC_TITLE, default=MR)
    students = models.ManyToManyField('Student', related_name='teachers', blank=True)
    courses = models.ManyToManyField('Course', related_name='teachers')
    qualifications = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.honorific_title} {self.user.last_name}"

    class Meta:
        verbose_name_plural = "teachers"

class Parent(models.Model):
    MR, MRS, MS, DR, BLANK = 'Mr', 'Mrs', 'Ms', 'Dr', ''
    HONORIFIC_TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MS, 'Ms'),
        (DR, 'Dr'),
        (BLANK, ''),
    )

    user = models.OneToOneField(
        get_user_model(),
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='parent',
        null=False
    )
    honorific_title = models.CharField(max_length=3, choices=HONORIFIC_TITLE, default=MR)
    children = models.ManyToManyField('Student')
    occupation = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
     
    class Meta:
        verbose_name_plural = "parents"

class Student(models.Model):
    BAKING, CHESS, DRAWING, MUSIC, SPORTS = 'baking', 'chess', 'drawing', 'music', 'sports'
    HOBBY_CHOICES = (
        (BAKING, 'Baking'),
        (CHESS, 'Chess'),
        (DRAWING, 'Drawing'),
        (MUSIC, 'Music'),
        (SPORTS, 'Sports'),
    )

    GRADE_LEVEL = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
    )
    date_of_birth = models.DateField(blank=False)
    hobby = models.CharField(choices=HOBBY_CHOICES, max_length=10, blank=True, default=BAKING)
    grade_level = models.IntegerField(choices=GRADE_LEVEL, default=1)
    student_id = models.CharField(blank=False, null=False, max_length=255)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name_plural = "students"

class Admin(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='admin',
        null=False
    )
    admin_id = models.CharField(blank=False, null=False, max_length=255)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField('Student', blank=True)

    def __str__(self):
        return self.name


