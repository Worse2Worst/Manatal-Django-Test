from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from uuid import uuid4
from django.db import IntegrityError


# Check at least 1 alphabet, spaces are allowed, numbers are not allowed, using this for names and surnames
alphabets = RegexValidator(r'^[a-zA-Z]+[a-zA-Z\s]*$', 'Only alphabets characters are allowed.')


def restrict_amount(value):
    # "value" is the name of the school, not an id
    school = Schools.objects.filter(name=value)[0]
    max_students_allowed = school.max_students
    current_students = len(school.students_set.all())
    if current_students >= max_students_allowed:
        raise ValidationError(f'The school {value} is already full. , Max students = {school.max_students}')


class Schools(models.Model):
    name = models.CharField(max_length=20, unique=True)
    max_students = models.IntegerField()

    def __str__(self):
        return self.name


class Students(models.Model):
    first_name = models.CharField(max_length=20, validators=[alphabets])
    last_name = models.CharField(max_length=20, validators=[alphabets])
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    school = models.ForeignKey(Schools, db_column='school_id', on_delete=models.CASCADE, validators=(restrict_amount, ))

    def save(self, *args, **kwargs):
        # Capitalize first names and last names
        self.first_name = self.first_name.capitalize().strip()
        self.last_name = self.last_name.capitalize().strip()
        # Enforcing unique "student_id"
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
