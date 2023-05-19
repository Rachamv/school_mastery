from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from .models import SchoolUser, Teacher, Parent, Student, Course


class SchoolUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email', 'password1', 'password2', 'user_type', 'first_name', 'last_name', 'phone_number',
                  'street_address1', 'street_address2', 'town_or_city', 'county', 'postcode', 'country']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['honorific_title', 'students', 'courses', 'qualifications', 'experience']


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['honorific_title', 'children', 'occupation']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'hobby', 'grade_level', 'student_id']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'teacher', 'students']
