import django_filters.rest_framework
from rest_framework import viewsets
from .models import User, Admin
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

