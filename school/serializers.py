# from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, HyperlinkedRelatedField
from .models import Schools, Students


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = Schools
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'schools_pk': 'schools__pk'
    }

    class Meta:
        model = Students
        fields = '__all__'
