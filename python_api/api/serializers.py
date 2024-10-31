from rest_framework import serializers
from .models import Client,Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']

    # def get_projects(self, obj):
    #     # Fetch projects from MySQL project table for this client
    #     projects = Project.objects.filter(client=obj.id)
    #     return ProjectSerializer(projects, many=True).data

class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True,read_only = True)
    class Meta:
        model = Client
        fields = ["id", "client_name",'projects', "created_at", "created_by"]

