from django.shortcuts import render
from rest_framework import viewsets,status,generics
from api.models import Client,Project
from .serializers import ClientSerializer,ProjectSerializer,ProjectCreateSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
    def destroy(self, request, *args, **kwargs):
        client = self.get_object()
        client_name = client.client_name  
        response = super().destroy(request, *args, **kwargs)
        print(f"Client '{client_name}' with id {client.id} was deleted.")
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # False for PUT, True for PATCH
        instance = self.get_object()
        
        # Store old name for logging
        old_name = instance.client_name
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            # Save the updated instance
            updated_instance = serializer.save()
            
            # Log the name change if it was updated
            if old_name != updated_instance.client_name:
                print(f"Client name updated from '{old_name}' to '{updated_instance.client_name}' for id {instance.id}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        # added manually
        @action(detail=True, methods=['post'], url_path='projects')
        def assign_project(self, request, pk=None):
            client = self.get_object()  # Get the client by ID
            project_name = request.data.get('project_name')
            users = request.data.get('users')

            # Create a new project
            project = Project.objects.create(
                project_name=project_name,
                client=client,
                users=users,
                created_by=request.user.username  # Assuming the user is authenticated
            )

            # Serialize the project data
            serializer = ProjectSerializer(project)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # Assuming you have a separate viewset for projects, else adjust accordingly
    @action(detail=True, methods=['get'], url_path='')
    def retrieve_project(self, request, pk=None):
        try:
            project = self.get_object()  # Get the project by ID
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    class ProjectViewSet(viewsets.ModelViewSet):
        serializer_ = ProjectSerializer

        def perform_create(self, serializer):
            client_id = self.kwargs['client_id']  # Assuming you pass client_id as part of the URL
            client = Client.objects.get(id=client_id)
            serializer.save(client=client)

        def create(self, request, *args, **kwargs):
            return super().create(request, *args, **kwargs)

# class ProjectListCreateView(generics.ListCreateAPIView):
#     # queryset = Project.objects.all()
    
#     # def get_serializer_class(self):
#     #     if self.request.method == 'POST':
#     #         return ProjectCreateSerializer
#     #     return ProjectSerializer
    
#     # def create(self, request, *args, **kwargs):
#     #     serializer = self.get_serializer(data=request.data)
#     #     if serializer.is_valid():
#     #         project = serializer.save()
#     #         response_serializer = ProjectSerializer(project)
#     #         return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         # Set created_by if not provided
#         if 'created_by' not in data:
#             data['created_by'] = 'Ganesh'  # Or get from request.user if using authentication
            
#         serializer = self.get_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        projects = self.get_queryset()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # Get client (for example, using first client - modify as needed)
        try:
            client = Client.objects.first()
            if not client:
                return Response(
                    {"error": "No client exists. Please create a client first."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Client.DoesNotExist:
            return Response(
                {"error": "No client exists. Please create a client first."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare data for project creation
        project_data = {
            'project_name': request.data.get('project_name'),
            'created_by': request.data.get('created_by', 'Ganesh'),
            'client_id': client,
            'user': request.data.get('users', [])  # Default to empty list if no users provided
        }

        try:
            # Create project
            project = Project.objects.create(**project_data)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )