from django.shortcuts import render
from rest_framework import viewsets,status
from api.models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# # Create your views here.

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
        
        



