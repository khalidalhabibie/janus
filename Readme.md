# Janus - Email Scheduler API

## Overview

**Janus** is an email scheduling application that allows you to schedule emails to be sent at specified times. The application uses Flask for the backend and provides a web interface and API for managing scheduled emails.


## Tech Stack

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database Migration**: [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- **API Documentation**: [Flasgger](https://github.com/flasgger/flasgger)
- **Time Management**: [pytz](https://pytz.sourceforge.net/)
- **Task Scheduling**: [APScheduler](https://apscheduler.readthedocs.io/en/latest/)
- **Email Sending**: [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
- **Email Service**: [Mailtrap](https://mailtrap.io//)
- **Testing**: [pytest](https://docs.pytest.org/en/latest/)


## Project Architecture

Here’s an explanation of the application architecture used in the Janus project:

Architecture Overview
Janus follows a modular, layered architecture pattern that separates concerns and enhances maintainability. Here’s a breakdown of the architecture:

```
janus/
│
├── app/
│   ├── __init__.py       # Initialize the Flask app and register blueprints
│   ├── models.py         # Define database models
│   ├── routes.py         # Define API routes and request handling
│   ├── scheduler.py      # Define the scheduler for sending emails
│   ├── tasks.py          # Define tasks for scheduling emails
│   ├── utils/
│   │   ├── __init__.py   # Initialize the utils package
│   │   ├── email_utils.py      # Email utility functions
│   │   ├── time_utils.py       # Time utility functions
│   ├── static/
│   │   └── styles/       # Static styles for the web app
|   ├── swagger/
│   |    └── swagger.yaml      # Swagger/OpenAPI specification for the API
│   └── templates/
│       ├── add_email.html # HTML template for adding email events
│       └── index.html    # HTML template for the main page
│
│
├── Dockerfile            # Dockerfile for building the application image
├── docker-compose.yaml   # Docker Compose configuration for the app and the database
├── Makefile              # Makefile for managing tasks
├── requirements.txt     # Python dependencies
└── run.py                # Entry point for the Flask application
```

## Installation

To get started with the Email Scheduler API, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/email-scheduler-api.git
cd email-scheduler-api
```

### 2. Create and Activate the Virtual Environment

```bash
make venv
```

### 3. Install Dependencies

```bash
make install
```

### 4. Set Up Environment Variables

Copy the `.env.example` file to `.env` and update it with your own values.

```bash
cp .env.example .env
```

### 5. Initialize the Database

Start the database container:

```bash
make docker-run-only-db
```

Initialize Flask-Migrate:

```bash
make db-init
```

### 6. Apply Migrations

```bash
make db-upgrade
```

### 7. Run the Application

```bash
make run
```

The application will be available at `http://localhost:5000`.

## API Endpoints

### POST /api/events

**Description**: Create a new email event.

**Request Body**:
```json
{
    "email_subject": "Subject of the email",
    "email_content": "Content of the email",
    "expected_sent_at": "2024-07-15T10:00:00",  # ISO 8601 format
    "recipients": "recipient1@example.com,recipient2@example.com"
}
```

**Response**:
- **Success**:
  ```json
  {
      "status": "success",
      "message": "Email scheduled successfully"
  }
  ```
- **Error**:
  ```json
  {
      "error": "Error message"
  }
  ```

**Example**:

```bash
curl -X POST http://localhost:5000/api/events \
-H "Content-Type: application/json" \
-d '{
    "email_subject": "Hello World",
    "email_content": "This is a test email.",
    "expected_sent_at": "2024-07-15T10:00:00",
    "recipients": "test@example.com"
}'
```

### API Documentation

Visit `http://localhost:5000/api/docs` for the Swagger UI documentation.

## Web Interface

### Adding an Email Event

Visit `http://localhost:5000/add` to access the web interface for adding email events. Fill out the form to schedule a new email.

## Troubleshooting

If you encounter issues related to timezone or datetime formats, ensure that you are using the correct ISO 8601 format for `expected_sent_at`. Timezone management can be complex, so please make sure your `TZ` environment variable is set correctly.

## Contribution

Feel free to open issues or submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## `.env.example`

Here's a template for the `.env` file. Copy this to `.env` and update with your environment-specific values.

```env

# database configuration
DATABASE_URL=postgresql://user:password@localhost:5432/email_scheduler
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=email_scheduler

# mailtrap configuration
MAIL_SERVER=smtp.mailtrap.io
MAIL_PORT=587
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=your_email@example.com

```

## Makefile Usage

### **Available Commands**

- `make venv` - Create a virtual environment and install dependencies.
- `make install` - Install Python dependencies.
- `make docker-run-only-db` - Start only the database container.
- `make db-init` - Initialize Flask-Migrate.
- `make db-migrate` - Create a new migration.
- `make db-upgrade` - Apply migrations.
- `make db-reset` - Reset the database and reapply migrations.
- `make run` - Run the Flask application.

### **Example Command**

To create the virtual environment, install dependencies, and run the app:

```bash
make venv
make install
make docker-run-only-db
make db-init
make db-upgrade
make run
```

## Future Plans

### 1. Frontend Migration
- **React**: Move the frontend to React to build a modern, interactive user interface.
- **Tailwind CSS**: Use Tailwind CSS for a responsive and customizable design.

### 2. Separate Cron Job Service
- **Separate Cron Job Service**: Decouple the cron jobs from the main application to improve maintainability and scalability. This service will handle scheduled tasks independently from the Flask application.

### 3. Message Queue Integration
- **Message Queue**: Integrate a message queue (such as RabbitMQ or Redis Queue) for managing the email sending process. This will offload tasks from the main application to a dedicated worker service, enhancing scalability and reliability.

### 4. Enhanced Error Handling and Monitoring
- **Error Handling**: Improve error handling mechanisms and implement better logging for both the application and scheduled tasks.
- **Monitoring**: Set up monitoring and alerting for the application and worker services to ensure smooth operation and quick response to issues.

### 5. User Authentication and Authorization
- **User Management**: Add user authentication and authorization features to manage access and permissions within the application.

### 6. API Rate Limiting and Security
- **Rate Limiting**: Implement rate limiting to prevent abuse of API endpoints.
- **Security Enhancements**: Apply additional security measures to protect against common vulnerabilities.

### 7. Advanced Email Features
- **Email Templates**: Support for customizable email templates to make it easier to create and manage different types of email content.
- **Email Analytics**: Add features for tracking email open rates, click-through rates, and other analytics to measure the effectiveness of email campaigns.

### 8. Internationalization and Localization
- **Multi-Language Support**: Add support for multiple languages to make the application accessible to a global audience.

### 9. API Enhancements
- **Additional Endpoints**: Add new API endpoints for advanced email management features and integrations with other services.

### 10. Documentation Improvements
- **Enhanced Documentation**: Expand the documentation to cover new features, usage examples, and developer guides for contributing to the project.

## Contact

For any questions or feedback, please reach out to [your-email@example.com](mailto:your-email@example.com).

