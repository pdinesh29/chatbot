import uuid
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    """
    Represents a chat room.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='rooms')  # Users in the room

    def __str__(self):
        return self.name

class Message(models.Model):
    """
    Represents a message in a chat room.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} in {self.room.name} at {self.timestamp}"

    class Meta:
        ordering = ('timestamp',)  # Order messages by timestamp