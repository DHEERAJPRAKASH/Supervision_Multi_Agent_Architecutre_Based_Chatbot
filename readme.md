# Django Multi-Agent AI Chatbot

A sophisticated Django-based chatbot application that uses multiple AI agents to collaboratively solve complex problems. The system features a Supervisor agent that coordinates Researcher, Analyst, and Writer agents to provide comprehensive, well-researched responses.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v5.2+-green.svg)
![LangChain](https://img.shields.io/badge/langchain-latest-orange.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-v5.1+-purple.svg)

## 🚀 Features

### Multi-Agent System
- **🎯 Supervisor Agent**: Orchestrates the workflow and decides which agent should work next
- **🔍 Researcher Agent**: Gathers comprehensive information and background data
- **📊 Analyst Agent**: Analyzes data, identifies patterns, and provides insights
- **✍️ Writer Agent**: Creates professional reports and final documentation

### Web Application Features
- **🔐 User Authentication**: Complete registration and login system
- **💬 Real-time Chat Interface**: Interactive chat with live agent responses
- **📱 Responsive Design**: Works seamlessly on desktop and mobile
- **📄 Session Management**: Save and view chat history
- **📊 Workflow Visualization**: Auto-generated diagrams showing agent interactions
- **🎨 Modern UI**: Clean, professional interface with Bootstrap 5

### Technical Features
- **🔗 RESTful APIs**: Clean API endpoints for chat functionality
- **🗄️ Database Integration**: SQLite for development, easily configurable for production
- **🔒 CSRF Protection**: Secure forms and API calls
- **📝 Rich Text Support**: Markdown-like formatting in messages
- **🎯 Session Tracking**: Comprehensive chat session management

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**
- **Django 5.2+**
- **LangChain** - AI agent framework
- **LangGraph** - Multi-agent workflow management
- **Groq API** - High-performance LLM inference

### Frontend
- **HTML5 & CSS3**
- **JavaScript (ES6+)**
- **Bootstrap 5.1+**
- **Font Awesome** - Icons

### Database
- **SQLite** (development)
- **PostgreSQL/MySQL** (production ready)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (get it from [Groq Console](https://console.groq.com/))
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multiagent-chatbot.git
cd multiagent-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
````

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GROQ_API_KEY=your-groq-api-key-here
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 🎯 Usage Guide

### Getting Started

1. **Register/Login**: Create an account or log in to access the chatbot
2. **Start Chatting**: Navigate to the chat interface
3. **Ask Questions**: Submit any question or task to the multi-agent system
4. **Watch Agents Work**: See how different agents collaborate:
    - Supervisor coordinates the workflow
    - Researcher gathers information
    - Analyst provides insights
    - Writer creates final reports

### Example Queries

```
Tell me about renewable energy trends in 2024
Analyze the impact of AI on healthcare
Create a business plan for a tech startup
Research and analyze cryptocurrency market trends
```

### Managing Sessions

- **New Chat**: Click the "+" button to start a fresh conversation
- **Session History**: View all your previous chat sessions
- **Continue Chat**: Resume any previous conversation
- **Session Details**: View detailed conversation history with timestamps

## 📁 Project Structure

```
multiagent_chatbot/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── multiagent_chatbot/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       └── registration/
├── chatbot/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── agents.py          # Multi-agent system
│   └── templates/
│       ├── base.html
│       ├── chatbot/
│       └── includes/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── media/
    └── graphs/
```

## 🔌 API Endpoints

### Authentication
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /accounts/logout/` - User logout

### Chat API
- `POST /chatbot/api/send-message/` - Send message to agents
- `GET /chatbot/api/get-messages/` - Retrieve session messages
- `POST /chatbot/chat/new/` - Create new chat session

### Pages
- `/` - Home page
- `/chatbot/` - Main chat interface
- `/chatbot/about/` - About page with workflow diagram
- `/chatbot/sessions/` - Chat history
- `/chatbot/session/<id>/` - Session detail view

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** - For the amazing AI agent framework
- **Groq** - For high-performance LLM inference
- **Django** - For the robust web framework
- **Bootstrap** - For the responsive UI components

---

**Built with ❤️ using Django and Multi-Agent AI**