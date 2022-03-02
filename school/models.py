from django.db import models
from django.core.validators import RegexValidator
from uuid import uuid4
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class SchoolFullExcpetion(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'

    def __init__(self, num, status_code=None):
        self.detail = f'The school is already full. , Max students = {num}'
        if status_code is not None:
            self.status_code = status_code


# Check at least 1 alphabet, spaces are allowed, numbers are not allowed, using this for names and surnames
alphabets = RegexValidator(r'^[a-zA-Z]+[a-zA-Z\s]*$', 'Only alphabets characters are allowed.')


class Schools(models.Model):
    name = models.CharField(max_length=20, unique=True)
    max_students = models.IntegerField()

    def __str__(self):
        return self.name


class Students(models.Model):
    first_name = models.CharField(max_length=20, validators=[alphabets])
    last_name = models.CharField(max_length=20, validators=[alphabets])
    nationality = models.CharField(max_length=20, blank=True)  # Trivial bonus about adding fields
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    school = models.ForeignKey(Schools, db_column='school_id', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Capitalize first names and last names
        self.first_name = self.first_name.capitalize().strip()
        self.last_name = self.last_name.capitalize().strip()
        # Validate school's capacity here, we don't do that when creating the object,
        # because we want to make it work for PUT/ PATCH
        school = Schools.objects.filter(name=self.school)[0]
        max_students_allowed = school.max_students
        students_set = school.students_set
        # If the student id exists in the school --> it is updating, should allow
        # if not --> the school is full, should raise an exception
        if not students_set.filter(id=self.id).exists():
            current_students = len(students_set.all())
            if current_students >= max_students_allowed:
                raise SchoolFullExcpetion(school.max_students)
        # Also, enforcing unique "student_id"
        if self.student_id:
            super(Students, self).save(*args, **kwargs)
            return
        unique = False
        while not unique:
            try:
                self.student_id = uuid4().hex[: 20]
                super(Students, self).save(*args, **kwargs)
            except IntegrityError:
                self.student_id = uuid4().hex[: 20]
            else:
                unique = True
