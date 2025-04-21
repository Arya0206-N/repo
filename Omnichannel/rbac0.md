### Roles
1. **Admin**
   - **Description**: Full system control, including configuration, user management, and monitoring.
   - **Typical Users**: IT staff, system architects.
2. **Supervisor**
   - **Description**: Oversees agents, manages queues, and reviews performance analytics.
   - **Typical Users**: Support team leads, managers.
3. **Agent**
   - **Description**: Handles customer tickets and uses knowledge base tools.
   - **Typical Users**: Frontline support staff.
4. **System**
   - **Description**: Internal services (e.g., classification engine, RAG pipeline) for automated operations.
   - **Typical Users**: Backend processes, not human users.
5. **Customer** 
   - **Description**: End-users interacting with self-service features (e.g., viewing tickets, accessing knowledge base).
   - **Typical Users**: Firm’s customers seeking support.
6. **Analyst** 
   - **Description**: Focuses on data analysis, reporting, and system performance insights.
   - **Typical Users**: Data analysts, business intelligence staff.

### Permissions 

#### Ticket Management
- `tickets.create`: POST /api/v1/tickets
- `tickets.read`: GET /api/v1/tickets, GET /api/v1/tickets/{ticket_id}
- `tickets.assign`: POST /api/v1/tickets/{ticket_id}/assign
- `tickets.resolve`: POST /api/v1/tickets/{ticket_id}/resolve

#### Agent Management
- `agents.read`: GET /api/v1/agents, GET /api/v1/agents/{agent_id}
- `agents.update`: PUT /api/v1/agents/{agent_id}
- `agents.skills.manage`: POST /api/v1/agents/{agent_id}/skills
- `agents.queue.read`: GET /api/v1/agents/{agent_id}/queue
- `agents.status.update`: PUT /api/v1/agents/{agent_id}/status

#### Category Management
- `categories.read`: GET /api/v1/categories
- `categories.manage`: POST, PUT, DELETE /api/v1/categories/*

#### Knowledge Base
- `kb.read`: GET /api/v1/documents, GET /api/v1/documents/{document_id}
- `kb.manage`: POST, PUT, DELETE /api/v1/documents/*
- `kb.crawl`: POST /api/v1/documents/crawl
- `kb.upload`: POST /api/v1/documents/upload

#### RAG Endpoints
- `rag.query`: POST /api/v1/rag/query
- `rag.suggestions.read`: GET /api/v1/rag/suggestions/{ticket_id}

#### Analytics
- `analytics.read`: GET /api/v1/analytics/* (tickets, agents, performance, categories)

#### Admin Operations
- `admin.system.read`: GET /api/v1/admin/system/status
- `admin.system.config`: POST /api/v1/admin/system/config
- `admin.logs.read`: GET /api/v1/admin/logs
- `admin.reindex`: POST /api/v1/admin/reindex

#### New Customer-Specific Permissions
- `tickets.customer.read`: View own tickets only (subset of `tickets.read`)
- `tickets.customer.create`: Submit new tickets (subset of `tickets.create`)

### Role-Permission Matrix
Permission matrix with all six roles:

| **Permission**            | **Admin** | **Supervisor** | **Agent** | **System** | **Customer** | **Analyst** |
|---------------------------|-----------|----------------|-----------|------------|--------------|-------------|
| `tickets.create`          | ✓         | ✓              | ✓         | ✓          | ✗            | ✗           |
| `tickets.read`            | ✓         | ✓              | ✓ (own)   | ✓          | ✗            | ✓           |
| `tickets.assign`          | ✓         | ✓              | ✗         | ✓          | ✗            | ✗           |
| `tickets.resolve`         | ✓         | ✓              | ✓ (own)   | ✓          | ✗            | ✗           |
| `tickets.customer.read`   | ✓         | ✓              | ✓ (own)   | ✓          | ✓ (own)      | ✓           |
| `tickets.customer.create` | ✓         | ✓              | ✓         | ✓          | ✓            | ✗           |
| `agents.read`             | ✓         | ✓              | ✗         | ✓          | ✗            | ✓           |
| `agents.update`           | ✓         | ✓              | ✗         | ✗          | ✗            | ✗           |
| `agents.skills.manage`    | ✓         | ✓              | ✗         | ✗          | ✗            | ✗           |
| `agents.queue.read`       | ✓         | ✓              | ✓ (own)   | ✓          | ✗            | ✓           |
| `agents.status.update`    | ✓         | ✓              | ✓ (own)   | ✗          | ✗            | ✗           |
| `categories.read`         | ✓         | ✓              | ✓         | ✓          | ✓            | ✓           |
| `categories.manage`       | ✓         | ✓              | ✗         | ✗          | ✗            | ✗           |
| `kb.read`                 | ✓         | ✓              | ✓         | ✓          | ✓            | ✓           |
| `kb.manage`               | ✓         | ✗              | ✗         | ✗          | ✗            | ✗           |
| `kb.crawl`                | ✓         | ✗              | ✗         | ✓          | ✗            | ✗           |
| `kb.upload`               | ✓         | ✗              | ✗         | ✗          | ✗            | ✗           |
| `rag.query`               | ✓         | ✓              | ✓         | ✓          | ✓            | ✓           |
| `rag.suggestions.read`    | ✓         | ✓              | ✓         | ✓          | ✗            | ✓           |
| `analytics.read`          | ✓         | ✓              | ✗         | ✗          | ✗            | ✓           |
| `admin.system.read`       | ✓         | ✗              | ✗         | ✗          | ✗            | ✗           |
| `admin.system.config`     | ✓         | ✗              | ✗         | ✗          | ✗            | ✗           |
| `admin.logs.read`         | ✓         | ✗              | ✗         | ✗          | ✗            | ✗           |
| `admin.reindex`           | ✓         | ✗              | ✗         | ✗          | ✗            | ✗           |

#### Notes:
- **✓ (own)**: Restricted to the user’s own data (e.g., Agents can only resolve their assigned tickets, Customers can only see their own tickets).
- **Customer Role**: Limited to self-service actions (creating tickets, reading their own tickets, accessing the knowledge base). Assumes a future customer portal, which isn’t fully detailed in your current doc but aligns with an Intercom-like omnichannel system.
- **Analyst Role**: Focused on read-only access to tickets, agents, queues, and analytics for reporting and insights, without operational control.
- **System Role**: Retains operational permissions (e.g., ticket assignment, RAG queries) for automation, secured via API keys.

### Implementation Adjustments
1. **Database Schema**:
   - Update the `users.role` ENUM to include all roles:
     ```sql
     ALTER TABLE users MODIFY COLUMN role ENUM('admin', 'supervisor', 'agent', 'system', 'customer', 'analyst') NOT NULL;
     ```
   - For Customers, use the `customers` table (`customer_id`, `email`, etc.) and link to `tickets` via `customer_id`. Authentication might use a lighter method (e.g., OAuth or temporary tokens) for external access.

2. **Authentication**:
   - **JWT for Human Roles**: Admin, Supervisor, Agent, Analyst, and Customer use JWTs with role and scope claims.
   - **API Keys for System**: Separate key-based auth for internal services.
   - **Customer Auth**: Consider a customer portal with email-based login or integration with an existing identity provider.

3. **Authorization Middleware**:
   - Use a middleware to check the role and scope claims in the JWT.

4. **Data Filtering**:
   - For **Agent** and **Customer**, enforce ownership checks (e.g., `WHERE assigned_agent_id = :user_id` or `WHERE customer_id = :user_id`) in SQL queries.
   - Use database views or stored procedures to simplify access control.