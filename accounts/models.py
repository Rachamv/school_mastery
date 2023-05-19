from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class SchoolUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='accounts_users',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_users',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(
        _('Email Address'), unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    user_type = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=3
    )
    first_name = models.CharField(
        _('first name'), max_length=150, null=False, blank=False
    )
    last_name = models.CharField(
        _('last name'), max_length=150, null=False, blank=False
    )
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
        return f"{self.honorific_title} {self.user.last_name}"

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
        return f"{self.first_name} {self.last_name}"

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
        return f"{self.user.first_name} {self.user.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField('Student', blank=True)

    def __str__(self):
        return self.name
