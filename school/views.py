from .models import Schools, Students
from .serializers import SchoolSerializer, StudentSerializer
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [filters.SearchFilter]
    # Bonus, add search
    search_fields = ['name']

    def retrieve(self, request, pk=None):
        queryset = Schools.objects.filter()
        client = get_object_or_404(queryset, pk=pk)
        serializer = SchoolSerializer(client, context={'request': request})
        return Response(serializer.data)


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
