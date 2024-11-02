# serializers.py
from rest_framework import serializers
from .models import Prisoner, ActivityType, RequestTemplate, ApprovalProcess, DepartmentRole
from django.contrib.auth.models import User

# Prisoner Serializer
class PrisonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prisoner
        fields = '__all__'

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'


class RequestTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestTemplate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'date_of_request', 'created_by']


class ApprovalProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalProcess
        fields = '__all__'
        read_only_fields = ['approved_at']


class DepartmentRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRole
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
