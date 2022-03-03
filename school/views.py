from .models import Schools, Students
from .serializers import SchoolSerializer, StudentSerializer
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [filters.SearchFilter]
    # Bonus, add search
    search_fields = ['name']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        if self.kwargs.get('schools_pk'):
            return Students.objects.filter(school=self.kwargs.get('schools_pk'))
        else:
            return Students.objects.all()

    def create(self, request, schools_pk=None,  *args, **kwargs):
        if not schools_pk:
            return super(StudentViewSet, self).create(request, *args, **kwargs)
        school = get_object_or_404(Schools.objects.filter(pk=schools_pk))
        _mutable = None
        if hasattr(request.data, '_mutable'):
            _mutable = request.data._mutable
            request.data._mutable = True
        request.data['school'] = school.pk
        if hasattr(request.data, '_mutable'):
            request.data._mutable = _mutable
        return super(StudentViewSet, self).create(request, *args, **kwargs)

    def update(self, request, schools_pk=None,  *args, **kwargs):
        if not schools_pk:
            return super(StudentViewSet, self).update(request, *args, **kwargs)
        school = get_object_or_404(Schools.objects.filter(pk=schools_pk))
        _mutable = None
        if hasattr(request.data, '_mutable'):
            _mutable = request.data._mutable
            request.data._mutable = True
        request.data['school'] = school.pk
        if hasattr(request.data, '_mutable'):
            request.data._mutable = _mutable
        return super(StudentViewSet, self).update(request, *args, **kwargs)
