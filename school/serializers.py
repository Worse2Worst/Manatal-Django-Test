from rest_framework.serializers import ModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .models import Schools, Students


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = Schools
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
