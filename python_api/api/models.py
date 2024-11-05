from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100, default='default_user')

    def __str__(self) -> str:
        return self.client_name

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    user = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    client_id = models.ForeignKey(Client,related_name='projects',on_delete=models.CASCADE)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name
