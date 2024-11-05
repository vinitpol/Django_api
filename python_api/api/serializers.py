from rest_framework import serializers
from .models import Client,Project,User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name','created_at', 'created_by']

    def to_representation(self, instance):
        # Format the created_at timestamp to match desired output
        
        representation = super().to_representation(instance)
        if instance.created_at:
            representation['created_at'] = instance.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return representation
    
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        for user_data in users_data:
            user, created = User.objects.get_or_create(id=user_data['id'], defaults={'user_name': user_data['name']})
            project.users.add(user)
        return project

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
    
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'created_by']

    def validate_project_name(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Project name cannot be empty")
        return value

