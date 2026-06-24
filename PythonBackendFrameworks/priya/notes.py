# ==========================================
# HANDSON 01: ARCHITECTURAL NOTES
# ==========================================

"""
1. REQUEST-RESPONSE CYCLE:
   - Client sends an HTTP request (e.g., clicks a link or hits an API endpoint).
   - The web server (WSGI/ASGI) passes the request to the Django framework.
   - Django's URL Router matches the path to a specific View function.
   - The View processes logic, interacts with the Database via Models if needed.
   - The View renders a Template or serializes data, returning an HTTP Response.
   - The client receives the response (HTML, JSON, etc.) and renders it.

2. MVC vs MVT ARCHITECTURE:
   - MVC (Model-View-Controller):
     * Model: Manages data and database logic.
     * View: Handles UI display/layout.
     * Controller: Intermediary that handles business logic and routes.
   - MVT (Model-View-Template) - Django's Pattern:
     * Model: Manages database tables (same as MVC).
     * View: Handles business logic and processing (equivalent to Controller).
     * Template: Handles the UI/presentation layer (equivalent to View).

3. WSGI vs ASGI:
   - WSGI (Web Server Gateway Interface): Synchronous standard. Handles requests 
     one-by-one. Great for traditional synchronous web apps (e.g., default Flask/Django).
   - ASGI (Asynchronous Server Gateway Interface): Asynchronous successor. 
     Handles multiple concurrent connections concurrently using async/await. 
     Ideal for WebSockets and streaming APIs (e.g., FastAPI, modern Django).

4. MIDDLEWARE IN DJANGO:
   - A framework of hooks that intercepts requests and responses globally.
   - Runs code *before* a request reaches the view, or *before* a response is returned.
   - Common use cases: Authentication checks, Security headers, Session handling, and CORS configurations.
"""

# REQUEST RESPONSE CYCLE

# Browser sends:
# GET /api/courses/

# 1. URL Router receives request
# 2. Router finds matching URL pattern
# 3. Calls corresponding View
# 4. View interacts with Model
# 5. Model fetches data from Database
# 6. Data returns to View
# 7. View creates Response
# 8. Response sent back to Browser


# MIDDLEWARE

# Middleware sits between request and response.

# Request
# Browser
#    ↓
# Middleware
#    ↓
# URL
#    ↓
# View
#    ↓
# Response
#    ↑
# Middleware
#    ↑
# Browser


# Built-in Middleware Examples

# AuthenticationMiddleware
# Identifies logged-in users

# SecurityMiddleware
# Adds security headers and HTTPS support


# WSGI vs ASGI

# WSGI
# Synchronous
# Handles one request at a time

# ASGI
# Asynchronous
# Handles many requests concurrently

# Django uses WSGI by default.

# Use ASGI when:
# WebSockets
# Real-time chat
# Notifications
# Async applications


# MVC vs MVT

# MVC

# Model -> Database
# View -> UI
# Controller -> Business Logic

# Django MVT

# Model -> Database
# View -> Controller Logic
# Template -> UI

# MVC Controller = Django View
# MVC View = Django Template
