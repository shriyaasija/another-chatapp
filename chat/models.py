from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

def deserialise_user(user):
    """Deserialise user instance to JSON"""
    return {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}

class TrackableDateModel(models.Model):
    """Abstract model to track the creation/updated date for a model"""
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

def _generate_unique_uri():
    """Generates a unique uri for the chat session"""
    return str(uuid4()).replace('-', '')[:15]

class ChatSession(TrackableDateModel):
    """Chat session"""

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    uri = models.URLField(default=_generate_unique_uri)

class ChatSessionMessage(TrackableDateModel):
    """Stores messages for a session"""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.PROTECT)
    message = models.TextField(max_length=2000)

    def to_json(self):
        """deserialise message to JSON"""
        return {'user': deserialise_user(self.user), 'message': self.message}
    
class ChatSessionMember(TrackableDateModel):
    """Store all users in a chat session"""
    chat_session = models.ForeignKey(ChatSession, related_name='members', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
