from django.test import TestCase
from accounts.forms import SchoolUserCreationForm, TeacherForm, ParentForm, StudentForm, CourseForm


class FormTests(TestCase):
    def test_school_user_creation_form(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_type': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+1234567890',
            'street_address1': '123 Test Street',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Test City',
            'county': 'Test County',
            'postcode': '12345',
            'country': 'US',
        }
        form = SchoolUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_teacher_form(self):
        # Create a Teacher object or use mock data for testing the form
        teacher_data = {
            'honorific_title': 'Mr',
            'students': [1, 2, 3],
            'courses': [1, 2, 3],
            'qualifications': 'Test qualifications',
            'experience': 'Test experience',
        }
        form = TeacherForm(data=teacher_data)
        self.assertTrue(form.is_valid())

    def test_parent_form(self):
        # Create a Parent object or use mock data for testing the form
        parent_data = {
            'honorific_title': 'Mrs',
            'children': [1, 2, 3],
            'occupation': 'Test occupation',
        }
        form = ParentForm(data=parent_data)
        self.assertTrue(form.is_valid())

    def test_student_form(self):
        # Create a Student object or use mock data for testing the form
        student_data = {
            'date_of_birth': '2000-01-01',
            'hobby': 'drawing',
            'grade_level': 5,
            'student_id': '123456789',
        }
        form = StudentForm(data=student_data)
        self.assertTrue(form.is_valid())

    def test_course_form(self):
        # Create a Course object or use mock data for testing the form
        course_data = {
            'name': 'Test Course',
            'code': 'TEST123',
            'description': 'Test description',
            'teacher': 1,
            'students': [1, 2, 3],
        }
        form = CourseForm(data=course_data)
        self.assertTrue(form.is_valid())
