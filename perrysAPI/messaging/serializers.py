from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Message, Like, Conversation
from authentication.serializers import UserSerializer


class MessageSerializer(ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['id', 'url', 'conversation', 'sender', 'text', 'timestamp', 'liked_by']
        read_only_fields = ['conversation', 'sender', 'timestamp', 'liked_by']


class ConversationChoiceField(PrimaryKeyRelatedField):

    def get_queryset(self):
        """Ensures users can only send messages to conversations they're in."""
        return Conversation.objects.filter(id__in=[c.id for c in self.context['request'].user.conversations.all()])


class CreateMessageSerializer(ModelSerializer):
    conversation = ConversationChoiceField()

    class Meta:
        model = Message
        fields = ['id', 'url', 'conversation', 'sender', 'text', 'timestamp']
        read_only_fields = ['sender', 'timestamp']


class ConversationSerializer(ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'url', 'users', 'messages']
        read_only_fields = ['users']


class CreateConversationSerializer(ModelSerializer):

    class Meta:
        model = Conversation
        fields = ['id', 'url', 'users']


class LikeSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    message = MessageSerializer(many=False, read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'message', 'timestamp']
        read_only_fields = ['user', 'timestamp']


class MessageChoiceField(PrimaryKeyRelatedField):

    def get_queryset(self):
        """Ensures users can't like their own messages or messages they've previously liked."""
        user = self.context['request'].user
        msg_ids = [m.id for c in user.conversations.all() for m in c.messages.all() if m.sender != user and m.id not in [l.message.id for l in user.likes.all()]]
        return Message.objects.filter(id__in=msg_ids)


class CreateLikeSerializer(ModelSerializer):
    message = MessageChoiceField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'message', 'timestamp']
        read_only_fields = ['user', 'timestamp']
