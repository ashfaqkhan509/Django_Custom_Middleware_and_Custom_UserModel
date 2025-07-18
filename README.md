# Django Custom Middleware & Custom User Model Project

This project demonstrates the implementation of **custom Django middleware**
for logging, rate limiting, and role-based access control, along with a
**custom user model** that uses email instead of username for authentication.

##  Features

### Logging Middleware
- Logs each request's IP address and method.
- Stores logs using Python’s `logging` module in a local file.
- Ensures logs are appended and not overwritten.

### Rate Limiting Middleware
- Restricts clients to **5 requests per minute** by default.
- Automatically unblocks after **1 minute**.
- Returns **403 Forbidden** if the limit is exceeded.

### Role-Based Rate Limiting Middleware
- Limits vary by authenticated user role:
  - **Gold**: 10 req/min
  - **Silver**: 5 req/min
  - **Bronze**: 2 req/min
- **Unauthenticated users**: 1 req/min
- Exceeding the limit returns **429 Too Many Requests**.

### Custom User Model
- Replaces username with **email** as the primary login credential.
- Supports creating superusers with email.
- Admin interface customized:
  - Groups fields by authentication, permissions, and metadata.

### Authentication Views
- **Register**: Create a new user account.
- **Login**: Authenticate using email and password.
- **Logout**: End session.

### Testing
- Test cases for:
  - Logging middleware
  - Rate limiting logic
  - Role-based control
- Testable via `python manage.py test` and includes test coverage support.



## Getting Started

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/ashfaqkhan509/Django_Custom_Middleware_and_Custom_UserModel.git
cd custom_middleware_project

# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (email-based login)
python manage.py createsuperuser

# Start development server
python manage.py runserver
