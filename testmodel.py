from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Teacher, Parent, Student, Admin, Course

class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_teacher_model(self):
        teacher = Teacher.objects.create(user=self.user, qualifications='Some qualifications', experience='Some experience')
        self.assertEqual(str(teacher), 'Mr Doe')
    
    def test_parent_model(self):
        parent = Parent.objects.create(user=self.user, occupation='Engineer')
        self.assertEqual(str(parent), 'John Doe')
    
    def test_student_model(self):
        student = Student.objects.create(date_of_birth='2000-01-01', grade_level=10, student_id='12345')
        self.assertEqual(str(student), 'John Doe')
    
    def test_admin_model(self):
        admin = Admin.objects.create(user=self.user, admin_id='A001')
        self.assertEqual(str(admin), 'John Doe')
    
    def test_course_model(self):
        course = Course.objects.create(name='Mathematics', code='MATH101')
        self.assertEqual(str(course), 'Mathematics')

