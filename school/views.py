from .models import Schools, Students
from .serializers import SchoolSerializer, StudentSerializer
from rest_framework import viewsets


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        if self.kwargs.get('schools_pk'):
            return Students.objects.filter(school=self.kwargs.get('schools_pk'))
        else:
            return Students.objects.all()
