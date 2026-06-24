# Microservices Decomposition

| Service Name         | Responsibility                           | Endpoints Owned                                                   | Database Owned   |
| -------------------- | ---------------------------------------- | ----------------------------------------------------------------- | ---------------- |
| Student Service      | Student management and enrollment        | GET/POST/PUT/DELETE /api/students, POST /api/students/<id>/enroll | students.db      |
| Course Service       | Course management                        | GET/POST/PUT/DELETE /api/courses                                  | courses.db       |
| Auth Service         | User registration, login, JWT validation | /api/auth/register, /api/auth/login                               | auth.db          |
| Notification Service | Email notifications and alerts           | /api/notifications/send                                           | notifications.db |

## Why this decomposition?

1. Student operations scale independently.
2. Course catalog changes independently.
3. Authentication is reusable across applications.
4. Notifications can be processed separately.

## Synchronous vs Asynchronous Communication

### Synchronous (HTTP)

Advantages:

* Simple to implement.
* Immediate response.
* Easy debugging.

Disadvantages:

* Tight coupling.
* Service downtime affects dependent services.
* Higher latency.

### Asynchronous (RabbitMQ/Kafka)

Advantages:

* Loose coupling.
* Better scalability.
* Fault tolerant.

Disadvantages:

* Eventual consistency.
* More infrastructure.
* More complex debugging.

### When to use RabbitMQ/Kafka?

Use when:

* Sending emails.
* Processing payments.
* Logging.
* Analytics pipelines.
* High-volume event processing.

Use HTTP when:

* Immediate response is required.
* Data validation is needed before continuing.
