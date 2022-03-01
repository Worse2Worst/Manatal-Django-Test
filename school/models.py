from django.db import models


class School(models.Model):
    name = models.CharField(max_length=20)
    max_students = models.IntegerField()


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=20, primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
