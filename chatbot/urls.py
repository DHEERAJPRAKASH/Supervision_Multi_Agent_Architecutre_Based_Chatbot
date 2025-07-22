from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('chat/new/', views.NewChatView.as_view(), name='new_chat'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('api/send-message/', views.SendMessageAPIView.as_view(), name='send_message'),
    path('api/get-messages/', views.GetMessagesAPIView.as_view(), name='get_messages'),
    path('session/<int:session_id>/', views.ChatSessionDetailView.as_view(), name='chat_session'),
    path('sessions/', views.ChatSessionListView.as_view(), name='chat_sessions'),
]