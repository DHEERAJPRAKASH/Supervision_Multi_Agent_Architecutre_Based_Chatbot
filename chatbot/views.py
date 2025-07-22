from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
import json
from datetime import datetime

from .models import ChatSession, ChatMessage, WorkflowExecution
from .agents import MultiAgentSystem
from django.urls import reverse


class HomeView(TemplateView):
    """Home page view"""
    template_name = 'chatbot/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AI Multi-Agent Chatbot'
        context['description'] = 'Experience the power of collaborative AI agents'
        return context


@method_decorator(csrf_exempt, name='dispatch')
class SendMessageAPIView(LoginRequiredMixin, View):
    """API endpoint to send messages and get AI responses"""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            message_content = data.get('message', '').strip()

            if not message_content:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)

            # Get or create current session
            session, created = ChatSession.objects.get_or_create(
                user=request.user,
                is_active=True,
                defaults={'title': f"Chat Session {datetime.now().strftime('%m/%d/%Y %H:%M')}"}
            )

            # Save user message
            user_message = ChatMessage.objects.create(
                session=session,
                message_type='human',
                content=message_content,
                agent_type='user'
            )

            # Initialize multi-agent system
            multi_agent = MultiAgentSystem()

            try:
                # Execute workflow
                response = multi_agent.execute_workflow(message_content)

                # Save all agent messages
                agent_messages = []
                for msg in response.get('messages', []):
                    if hasattr(msg, 'content'):
                        # Determine agent type from message content
                        agent_type = 'supervisor'
                        if '🔍 Researcher:' in msg.content:
                            agent_type = 'researcher'
                        elif '📊 Analyst:' in msg.content:
                            agent_type = 'analyst'
                        elif '✍️ Writer:' in msg.content:
                            agent_type = 'writer'

                        ai_message = ChatMessage.objects.create(
                            session=session,
                            message_type='ai',
                            content=msg.content,
                            agent_type=agent_type,
                            research_data=response.get('research_data', ''),
                            analysis_data=response.get('analysis', ''),
                            final_report=response.get('final_report', '')
                        )
                        agent_messages.append({
                            'id': ai_message.id,
                            'content': ai_message.content,
                            'agent_type': ai_message.agent_type,
                            'timestamp': ai_message.timestamp.isoformat()
                        })

                # Save workflow execution
                WorkflowExecution.objects.create(
                    session=session,
                    task=message_content,
                    research_data=response.get('research_data', ''),
                    analysis=response.get('analysis', ''),
                    final_report=response.get('final_report', ''),
                    is_complete=response.get('task_complete', False),
                    completed_at=datetime.now() if response.get('task_complete', False) else None
                )

                # Update session title if it's the first message
                if session.messages.count() == len(agent_messages) + 1:  # +1 for user message
                    session.title = message_content[:50] + ('...' if len(message_content) > 50 else '')
                    session.save()

                return JsonResponse({
                    'success': True,
                    'user_message': {
                        'id': user_message.id,
                        'content': user_message.content,
                        'timestamp': user_message.timestamp.isoformat()
                    },
                    'agent_messages': agent_messages,
                    'final_report': response.get('final_report', ''),
                    'task_complete': response.get('task_complete', False)
                })

            except Exception as e:
                # Save error message
                error_message = ChatMessage.objects.create(
                    session=session,
                    message_type='system',
                    content=f"Error processing request: {str(e)}",
                    agent_type='supervisor'
                )

                return JsonResponse({
                    'success': False,
                    'error': str(e),
                    'error_message': {
                        'id': error_message.id,
                        'content': error_message.content,
                        'timestamp': error_message.timestamp.isoformat()
                    }
                })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class GetMessagesAPIView(LoginRequiredMixin, View):
    """API endpoint to get messages for current session"""

    def get(self, request, *args, **kwargs):
        try:
            session_id = request.GET.get('session_id')

            if session_id:
                session = get_object_or_404(
                    ChatSession,
                    id=session_id,
                    user=request.user
                )
            else:
                # Get current active session
                session = ChatSession.objects.filter(
                    user=request.user,
                    is_active=True
                ).first()

                if not session:
                    return JsonResponse({'messages': []})

            messages = []
            for msg in session.messages.all():
                messages.append({
                    'id': msg.id,
                    'content': msg.content,
                    'message_type': msg.message_type,
                    'agent_type': msg.agent_type,
                    'timestamp': msg.timestamp.isoformat(),
                    'research_data': msg.research_data,
                    'analysis_data': msg.analysis_data,
                    'final_report': msg.final_report
                })

            return JsonResponse({
                'success': True,
                'messages': messages,
                'session_id': session.id,
                'session_title': session.title
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ChatView(LoginRequiredMixin, TemplateView):
    """Main chat interface view"""
    template_name = 'chatbot/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if we should create a new session
        create_new = self.request.GET.get('new', False)

        if create_new:
            # Set all current sessions to inactive
            ChatSession.objects.filter(
                user=self.request.user,
                is_active=True
            ).update(is_active=False)

            # Create new session
            session = ChatSession.objects.create(
                user=self.request.user,
                title=f"New Chat {datetime.now().strftime('%m/%d/%Y %H:%M')}",
                is_active=True
            )
        else:
            # Get or create current session (existing logic)
            session, created = ChatSession.objects.get_or_create(
                user=self.request.user,
                is_active=True,
                defaults={'title': f"Chat Session {datetime.now().strftime('%m/%d/%Y %H:%M')}"}
            )

        # Get recent sessions for sidebar
        recent_sessions = ChatSession.objects.filter(user=self.request.user)[:10]

        context.update({
            'title': 'AI Chat',
            'current_session': session,
            'recent_sessions': recent_sessions,
        })
        return context


class AboutView(TemplateView):
    """About page with workflow diagram"""
    template_name = 'chatbot/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        diagram_path = f"graphs/workflow_diagram.png"

        context.update({
            'title': 'About Multi-Agent System',
            'workflow_diagram': diagram_path,
            'description': 'Learn how our AI agents collaborate to solve complex tasks',
            'features': [
                {
                    'name': 'Supervisor Agent',
                    'icon': '🎯',
                    'description': 'Orchestrates the entire workflow and decides which agent works next'
                },
                {
                    'name': 'Researcher Agent',
                    'icon': '🔍',
                    'description': 'Gathers comprehensive information and background data'
                },
                {
                    'name': 'Analyst Agent',
                    'icon': '📊',
                    'description': 'Analyzes data, identifies patterns, and provides insights'
                },
                {
                    'name': 'Writer Agent',
                    'icon': '✍️',
                    'description': 'Creates professional reports and final documentation'
                }
            ]
        })
        return context


class ChatSessionListView(LoginRequiredMixin, ListView):
    """List all chat sessions for the user"""
    model = ChatSession
    template_name = 'chatbot/chat_sessions.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chat History'
        return context


class ChatSessionDetailView(LoginRequiredMixin, DetailView):
    """View specific chat session"""
    model = ChatSession
    template_name = 'chatbot/chat_session_detail.html'
    context_object_name = 'session'
    pk_url_kwarg = 'session_id'

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).prefetch_related('messages')

    def dispatch(self, request, *args, **kwargs):
        # Set this session as active and others as inactive when viewing
        session_id = kwargs.get('session_id')
        if session_id:
            ChatSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
            ChatSession.objects.filter(id=session_id, user=request.user).update(is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = self.object.messages.all().order_by('timestamp')

        # Calculate statistics
        unique_agents = messages.values('agent_type').distinct().count()
        workflow_count = self.object.workflowexecution_set.count() if hasattr(self.object, 'workflowexecution_set') else 0

        context.update({
            'title': f'Chat Session - {self.object.title}',
            'messages': messages,
            'unique_agents': unique_agents,
            'workflow_count': workflow_count,
        })
        return context

class NewChatView(LoginRequiredMixin, View):
    """Create a new chat session"""

    def post(self, request, *args, **kwargs):
        try:
            # Set all current sessions to inactive
            ChatSession.objects.filter(
                user=request.user,
                is_active=True
            ).update(is_active=False)

            # Create new session
            new_session = ChatSession.objects.create(
                user=request.user,
                title=f"New Chat {datetime.now().strftime('%m/%d/%Y %H:%M')}",
                is_active=True
            )

            return JsonResponse({
                'success': True,
                'session_id': new_session.id,
                'redirect_url': reverse('chatbot:chat')
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        # Handle GET request by redirecting to POST
        return self.post(request, *args, **kwargs)