from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User, UUIDModel


class ChatConversation(UUIDModel):
    first_user_id = models.UUIDField()
    second_user_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_conversations"


class ChatMessage(UUIDModel):
    class MessageTypes(models.TextChoices):
        TEXT = "T", _("Text")
        FILE = "F", _("File")

    conversation = models.ForeignKey(ChatConversation, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    message_type = models.CharField(max_length=1, choices=MessageTypes)
    text = models.TextField(blank=True)
    file_url = models.URLField(null=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_messages"
