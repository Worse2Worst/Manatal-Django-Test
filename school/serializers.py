from rest_framework.serializers import ModelSerializer
from .models import Schools, Students


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = Schools
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
