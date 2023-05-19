from django.contrib import admin
from . import models
# Register the User model with the admin site
admin.site.register(models.User)
admin.site.register(models.Teacher)
admin.site.register(models.Parent)
admin.site.register(models.Student)
admin.site.register(models.Admin)
admin.site.register(models.Course)