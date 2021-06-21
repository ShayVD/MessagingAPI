from django.db.models import Model, ManyToManyField, ForeignKey, CharField, DateTimeField, CASCADE, SET_NULL
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Conversation(Model):
    users = ManyToManyField(User, related_name='conversations')
    timestamp = DateTimeField(_("Date"), auto_now_add=True)

    def __str__(self):
        s = "Conversation between users;"
        for u in self.users.all():
            s += " '{}',".format(u.username)
        return s


class Message(Model):
    conversation = ForeignKey(Conversation, on_delete=CASCADE, null=False, related_name="messages")
    sender = ForeignKey(User, on_delete=SET_NULL, null=True, editable=False, related_name='sent')
    text = CharField(max_length=255, null=False)
    timestamp = DateTimeField(_("Date"), auto_now_add=True)

    def __str__(self):
        return "'{}' sent '{}'".format(self.sender, self.text)


class Like(Model):
    user = ForeignKey(User, on_delete=CASCADE, null=False, editable=False, related_name='likes')
    message = ForeignKey(Message, on_delete=CASCADE, null=False, related_name='liked_by')
    timestamp = DateTimeField(_("Date"), auto_now_add=True)

    def __str__(self):
        return "'{}' liked message '{}':'{}'".format(self.user.username, self.message.id, self.message.text)
