from rest_framework import serializers
from .models import Client,Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']

class ClientSerializer(serializers.ModelSerializer):
    # projects = ProjectSerializer(many=True,read_only = True)
    class Meta:
        model = Client
        fields = ["id", "client_name", "created_at", "created_by"]
        read_only_fields = ['created_by']

    def validate_client_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Client name cannot be empty")
        return value.strip()

