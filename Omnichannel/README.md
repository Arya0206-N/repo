# Omnichannel Customer Support System

A comprehensive backend system for intelligent routing and resolution of customer support inquiries across multiple communication channels.


## Overview

The Omnichannel Customer Support System is a skill and queue-based routing platform that intelligently handles customer support inquiries from multiple channels (email, Slack, Twitter, WhatsApp). It uses AI-powered classification to categorize issues, assess their criticality, and route them to the most suitable support staff. The system leverages RAG (Retrieval-Augmented Generation) with vector embeddings to provide automated solutions for low-criticality issues and assist agents with relevant documentation.

## Features

- **Multi-channel Integration**: Starting with email, with planned support for Slack, Twitter, and WhatsApp
- **AI-powered Classification**: Uses Groq LLM to categorize issues and determine criticality
- **Intelligent Routing**: Skills-based matching between issues and support staff
- **Round-robin Load Balancing**: Prevents agent overload with fair distribution
- **RAG Document Retrieval**: Uses vector embeddings and reranking for accurate solutions
- **Knowledge Base Management**: Import documentation via URL crawling or file upload
- **Data Collection Pipeline**: Stores query → assignment → solution for analytics and training
- **Comprehensive Analytics**: Track performance metrics and identify improvement areas

## Tech Stack

### Core Technologies
- **FastAPI**: Web framework for building APIs
- **LangChain**: Framework for LLM applications
- **CrewAI**: Agent-based workflow automation
- **Groq**: LLM provider for classification and generation
- **MySQL**: Primary relational database
- **Redis**: Caching and session management
- **RabbitMQ**: Message queue for task distribution
- **Qdrant/Pinecone/Chroma**: Vector database for document embeddings

### DevOps & Infrastructure
- **Docker**: Containerization
- **AWS Services**: Cloud infrastructure
- **Grafana**: Monitoring and dashboards

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  CHANNEL LAYER  │────▶│  CLASSIFICATION │────▶│  QUEUE & ROUTING│
│ (Email/Slack/   │     │  LLM            │     │                 │
│ Twitter/WhatsApp)│     │                 │     │                 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  DATA STORAGE   │◀────│  RAG SYSTEM     │◀────│  SUPPORT AGENTS │
│  & ANALYTICS    │     │  (Vector DB)    │     │                 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Directory Structure

```
omnichannel-support/
├── app/
│   ├── api/                  # API endpoints
│   │   ├── v1/
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── tickets.py    # Ticket management
│   │   │   ├── agents.py     # Agent management
│   │   │   ├── categories.py # Category management
│   │   │   ├── documents.py  # Knowledge base management
│   │   │   ├── rag.py        # RAG query endpoints
│   │   │   └── analytics.py  # Analytics endpoints
│   ├── core/                 # Core application code
│   │   ├── config.py         # Configuration
│   │   ├── security.py       # Authentication & security
│   │   ├── logging.py        # Logging configuration
│   │   └── errors.py         # Error handling
│   ├── db/                   # Database
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── session.py        # Database session
│   │   └── migrations/       # Alembic migrations
│   ├── services/             # Business logic
│   │   ├── email_service.py    # Email processing
│   │   ├── slack_service.py    # Slack integration
│   │   ├── twitter_service.py  # Twitter integration
│   │   ├── whatsapp_service.py # WhatsApp integration
│   │   ├── classification.py # Issue classification
│   │   ├── routing.py        # Ticket routing
│   │   ├── document.py       # Document processing
│   │   ├── vector_store.py   # Vector DB integration
│   │   ├── rag.py            # RAG implementation
│   │   └── analytics.py      # Analytics service
│   ├── schemas/              # Pydantic models
│   │   ├── ticket.py         # Ticket schemas
│   │   ├── agent.py          # Agent schemas
│   │   ├── category.py       # Category schemas
│   │   └── document.py       # Document schemas
│   ├── queues/               # Message queue
│   │   ├── producer.py       # Message producers
│   │   ├── consumer.py       # Message consumers
│   │   └── tasks.py          # Background tasks
│   └── main.py               # Application entry point
├── scripts/                  # Utility scripts
│   ├── seed_data.py          # Seed initial data
│   ├── crawl_docs.py         # Document crawling
│   └── generate_embeddings.py # Generate embeddings
├── tests/                    # Tests
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── conftest.py           # Test configuration
├── docs/                     # Documentation
│   ├── architecture.md       # System architecture
│   ├── api.md                # API documentation
│   ├── deployment.md         # Deployment guide
│   └── development.md        # Development guide
├── .env.example              # Example environment variables
├── docker-compose.yml        # Docker compose configuration
├── Dockerfile                # Application Dockerfile
├── requirements.txt          # Python dependencies
├── alembic.ini               # Alembic configuration
├── pytest.ini                # Pytest configuration
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- MySQL
- RabbitMQ
- Redis
- AWS account (for production deployment)
- Groq API key
- Vector DB account (Qdrant/Pinecone/Chroma)

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/omnichannel-support.git
cd omnichannel-support
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running Locally with Docker

1. Start the services:
```bash
docker-compose up -d
```

2. Run database migrations:
```bash
alembic upgrade head
```

3. Seed initial data:
```bash
python scripts/seed_data.py
```

4. Start the application:
```bash
uvicorn app.main:app --reload
```

5. Access the API documentation at http://localhost:8000/docs


## API Documentation

The API documentation is available via Swagger UI at `/docs` and ReDoc at `/redoc` when the application is running.

Key API endpoints:

- **Authentication**: `/api/v1/auth/*`
- **Tickets**: `/api/v1/tickets/*`
- **Agents**: `/api/v1/agents/*`
- **Categories**: `/api/v1/categories/*`
- **Documents**: `/api/v1/documents/*`
- **RAG**: `/api/v1/rag/*`
- **Analytics**: `/api/v1/analytics/*`

## Database Schema

The system uses MySQL as the primary database with the following core tables:

- `users`: User accounts (admins, agents, supervisors)
- `agents`: Support agent profiles and availability
- `skills`: Available skills for routing
- `agent_skills`: Many-to-many relationship between agents and skills
- `categories`: Issue categories
- `channels`: Communication channels
- `tickets`: Support tickets
- `customers`: Customer information
- `messages`: Individual messages in tickets
- `documents`: Knowledge base documents
- `document_chunks`: Chunked documents for vector search
- `solutions`: Ticket resolutions

## Message Queue Structure

RabbitMQ is used for task distribution with the following queues:

- `email.incoming`: New email messages
- `classification.queue`: Tickets awaiting classification
- `agent.{skill_id}`: Skill-specific queues
- `direct.resolution`: Low criticality tickets for auto-resolution
- `notification.{type}`: Notification queues

## RAG Implementation

The RAG system uses the following pipeline:

1. **Document Processing**:
   - Document crawling using Crawl4AI
   - Text extraction and chunking
   - Embedding generation
   - Storage in vector database

2. **Query Processing**:
   - Query analysis
   - Vector similarity search
   - Reranking for relevance
   - Response generation

## Security

The system implements:

- JWT-based authentication
- Role-based access control (RBAC)
- API keys for service-to-service communication
- HTTPS for all communication
- Data encryption at rest and in transit
- Input validation and sanitization
- Rate limiting

## Deployment

### Development Environment

```bash
docker-compose up -d
uvicorn app.main:app --reload
```

### Production Environment (AWS)

1. Build Docker image:
```bash
docker build -t omnichannel-support:latest .
```

2. Push to ECR or similar container registry

3. Deploy using ECS, EKS, or EC2 with appropriate load balancing and scaling

Detailed deployment instructions are available in the [deployment guide](docs/deployment.md).

## Monitoring

The system uses Grafana dashboards to monitor:

- System health and performance
- Queue depths and processing rates
- Classification accuracy
- Resolution times
- Agent performance

## Future Roadmap

- Integration with Slack, Twitter, WhatsApp
- In-house NLP model to replace Groq
- Analytics and reporting
- Automation for common workflows

