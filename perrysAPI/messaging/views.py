from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import MessageSerializer, CreateMessageSerializer, LikeSerializer, CreateLikeSerializer, ConversationSerializer, CreateConversationSerializer
from .models import Message, Like, Conversation
from django.db.models import Q


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return CreateMessageSerializer if self.action == 'create' else MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ConversationViewSet(CreateModelMixin, 
                          RetrieveModelMixin, 
                          ListModelMixin, 
                          DestroyModelMixin,
                          GenericViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return CreateConversationSerializer if self.action == 'create' else ConversationSerializer

    def perform_create(self, serializer):
        serializer.save(users=serializer.validated_data['users'] + [self.request.user])

    def create(self, request):
        data = dict(request.POST)
        if len(data['users']) > 1:
            rspns = Response(data={'users': ['This list may not be greater than 1.']}, status=HTTP_400_BAD_REQUEST)
        elif int(data['users'][0]) in set([u.id for c in request.user.conversations.all() for u in c.users.all() if u.id != request.user.id]):
            rspns = Response(data={'users': ['Cannot have more than 1 conversation with the same user.']}, status=HTTP_400_BAD_REQUEST)
        else:
            rspns = super().create(request)
        return rspns


class LikeViewset(CreateModelMixin, 
                  RetrieveModelMixin, 
                  ListModelMixin, 
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return CreateLikeSerializer if self.action == 'create' else LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
