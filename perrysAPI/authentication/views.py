from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.status import HTTP_200_OK 
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, CreateUserSerializer


class UserViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  ListModelMixin, 
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [p() for p in permission_classes]

    def get_serializer_class(self):
        return CreateUserSerializer if self.action == 'create' else UserSerializer

    @action(detail=True, methods=['get'], url_path='contacts')
    def contacts(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        contacts = set([u.id for c in user.conversations.all() for u in c.users.all()])
        queryset = self.queryset.filter(id__in=contacts)
        serializer = UserSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
