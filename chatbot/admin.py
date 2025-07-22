from django.contrib import admin
from .models import ChatSession, ChatMessage, WorkflowExecution

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at', 'is_active', 'message_count']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'title']
    readonly_fields = ['created_at', 'updated_at']

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'agent_type', 'timestamp', 'content_preview']
    list_filter = ['message_type', 'agent_type', 'timestamp']
    search_fields = ['content', 'session__user__username']
    readonly_fields = ['timestamp']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(WorkflowExecution)
class WorkflowExecutionAdmin(admin.ModelAdmin):
    list_display = ['session', 'task_preview', 'is_complete', 'created_at', 'completed_at']
    list_filter = ['is_complete', 'created_at', 'completed_at']
    search_fields = ['task', 'session__user__username']
    readonly_fields = ['created_at', 'completed_at']

    def task_preview(self, obj):
        return obj.task[:50] + '...' if len(obj.task) > 50 else obj.task
    task_preview.short_description = 'Task Preview'