from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title or 'Chat Session'} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Chat Session {self.created_at.strftime('%m/%d/%Y %H:%M')}"
        super().save(*args, **kwargs)

class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('human', 'Human'),
        ('ai', 'AI'),
        ('system', 'System'),
    ]

    AGENT_TYPES = [
        ('supervisor', 'Supervisor'),
        ('researcher', 'Researcher'),
        ('analyst', 'Analyst'),
        ('writer', 'Writer'),
        ('user', 'User'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES, default='user')
    research_data = models.TextField(blank=True)
    analysis_data = models.TextField(blank=True)
    final_report = models.TextField(blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type} - {self.agent_type} ({self.timestamp.strftime('%H:%M')})"

class WorkflowExecution(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    task = models.TextField()
    research_data = models.TextField(blank=True)
    analysis = models.TextField(blank=True)
    final_report = models.TextField(blank=True)
    workflow_graph_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Workflow: {self.task[:50]}... ({'Complete' if self.is_complete else 'In Progress'})"