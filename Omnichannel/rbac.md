# Role-Based Access Control (RBAC) Documentation

## Setup Guide
1. Define permissions in `app/models/permission.py`
2. Create roles with associated permissions in `app/models/role.py`
3. Assign roles to users through User model relationships

## Core Permissions
| Permission Name       | Description                          |
|------------------------|--------------------------------------|
| ticket:create         | Create new support tickets           |
| ticket:read           | View ticket details                  |
| ticket:update         | Modify existing tickets              |
| ticket:delete         | Archive/remove tickets               |
| channel:manage        | Configure communication channels     |
| analytics:view        | Access reporting dashboards          |

## API Endpoints

### Role Management

**Create Role**
```http
POST /api/v1/roles
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "support_lead",
  "description": "Team lead role",
  "permissions": ["ticket:escalate", "analytics:view"]
}
```
Required Permission: `admin.system.config`

**Update Role**
```http
PUT /api/v1/roles/{role_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "description": "Updated role description",
  "permissions": ["ticket:create", "ticket:read"]
}
```

**List Permissions**
```http
GET /api/v1/permissions
Authorization: Bearer <token>
```

### Access Control

**Check Resource Access**
```http
GET /api/v1/access-check?resource_type=skill&resource_id=123
Authorization: Bearer <token>
```

Response:
```json
{
  "has_access": true,
  "granted_by": "ownership"
}
```

### Ownership Verification
Access to resources is granted if either:
1. User has required permission via role
2. User owns the resource (creator/assigned owner)

Dual-layer authorization ensures:
- Permissions are checked first through role assignments
- Fallback to resource ownership verification
- Combined checks happen in `app/middleware/rbac.py`

```python
# Example ownership check implementation
if not (user.has_permission(permission) or resource.is_owner(user)):
    raise HTTPException(status_code=403)
```

Error Responses:
```json
{
  "detail": "Missing permission: ticket.delete or resource ownership"
}
```

### Check User Permissions
```http
GET /api/v1/users/me/permissions
Authorization: Bearer <token>
```

Response:
```json
{
  "permissions": [
    "ticket:read",
    "ticket:create"
  ]
}
```

## Middleware Enforcement
Permissions and ownership are checked in `app/middleware/rbac.py`:
```python
async def check_access(request: Request, permission: str, resource: Optional[BaseModel] = None):
    user = request.state.user
    
    # Role-based permission check
    if user.has_permission(permission):
        return
    
    # Ownership fallback check
    if resource and resource.is_owned_by(user):
        return
    
    raise HTTPException(
        status_code=403,
        detail={
            "error": "ACCESS_DENIED",
            "required_permission": permission,
            "resource_type": resource.__class__.__name__ if resource else None
        }
    )
```

## Error Codes
- 403 Forbidden: Missing required permission or resource ownership
- 404 Not Found: Role/Permission not found

Error response format:
```json
{
  "error": "ACCESS_DENIED",
  "message": "Missing required permission or resource ownership",
  "required_permission": "ticket:delete",
  "resource_type": "ticket"
}
```

## Version History
| Version | Date       | Changes               |
|---------|------------|-----------------------|
| 1.0     | 2024-02-01 | Initial RBAC rollout  |