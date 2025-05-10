# Fitness & Food App - Continuity Document

This document serves as the primary reference for project status, planning, and development continuity.

## 1. Project Overview
- **Name**: Fitness & Food App
- **Purpose**: A comprehensive application for nutrition tracking, recipe management, and social fitness community
- **Tech Stack**: 
  - **Backend**: Flask, Firebase (Firestore, Authentication, Storage)
  - **Frontend**: React, TypeScript
  - **APIs**: USDA Food Data Central API, recipe scrapers
- **Current Phase**: Implementation

## 2. Project Architecture

### Backend Structure
```
fitness-food-app/
├── app.py                  # Application entry point
├── config.py               # Configuration management
├── auth/                   # Authentication features
├── recipes/                # Recipe management features
├── nutrition/              # Nutrition tracking features
├── social/                 # Community and sharing features
├── utils/                  # Shared utilities
├── tests/                  # Test suite
└── requirements.txt        # Project dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── api/                # API client code
│   ├── components/         # React components
│   ├── contexts/           # React contexts
│   ├── config/             # Configuration
│   └── App.tsx             # Main app component
└── public/                 # Static assets
```

## 3. Module Status

### Backend Core
- **Status**: Complete
- **Key Files**: 
  - `app.py`: Main application setup with blueprints and middleware
  - `config.py`: Application configuration with environment variables
  - `manage.py`: CLI utility for management tasks
  - `run_tests.py`: Test runner
- **Next Steps**: Maintain and extend as needed

### Authentication Module
- **Status**: Complete
- **Key Files**: 
  - `auth/routes.py`: API endpoints for auth
  - `auth/__init__.py`: Blueprint registration
  - `utils/firebase_admin.py`: Firebase auth integration
- **Features**:
  - User registration and authentication via Firebase
  - Profile management
  - Auth middleware for protected routes

### Recipe Module
- **Status**: Complete
- **Key Files**: 
  - `recipes/routes.py`: API endpoints for recipes
  - `recipes/__init__.py`: Blueprint registration
- **Features**:
  - Recipe creation and management
  - Recipe import from URLs
  - Recipe search and filtering
  - Recipe sharing
  - Nutrition calculation for recipes

### Nutrition Module
- **Status**: Complete
- **Key Files**: 
  - `nutrition/models.py`: Data models for nutrition tracking
  - `nutrition/routes.py`: API endpoints for nutrition tracking
  - `nutrition/__init__.py`: Blueprint registration
- **Features**:
  - Food item database
  - USDA API integration
  - Meal logging
  - Nutrition tracking and statistics
  - Barcode scanning support

### Social Module
- **Status**: Complete
- **Key Files**: 
  - `social/models.py`: Data models for social features
  - `social/routes.py`: API endpoints for social features
  - `social/__init__.py`: Blueprint registration
- **Features**:
  - Social posts creation
  - User following system
  - Feed generation
  - Comments and likes
  - Activity tracking

### Utilities
- **Status**: Complete
- **Key Files**:
  - `utils/api_clients.py`: External API clients (USDA, barcode)
  - `utils/validators.py`: Input validation utilities
  - `utils/error_handlers.py`: Error handling
  - `utils/logging.py`: Logging configuration
  - `utils/background_tasks.py`: Background task processing
  - `utils/rate_limit.py`: Rate limiting
  - `utils/api_docs.py`: API documentation with Swagger
  - `utils/health_check.py`: Service health monitoring
  - `utils/monitoring.py`: Performance metrics

### Frontend
- **Status**: In Progress
- **Key Files**:
  - `frontend/src/api/authService.ts`: Authentication service
  - `frontend/src/api/client.ts`: API client
  - `frontend/src/contexts/AuthContext.tsx`: Auth context for React
  - `frontend/src/components/auth/Login.tsx`: Auth components
- **Features**:
  - Authentication UI
  - Basic application structure

## 4. API Documentation

The API is documented with OpenAPI/Swagger and available at `/api/docs`.

### API Routes

#### Auth Endpoints
- `POST /api/auth/profile`: Create user profile
- `GET /api/auth/profile`: Get user profile

#### Recipe Endpoints
- `POST /api/recipes/import`: Import recipe from URL
- `GET /api/recipes`: Get user's recipes
- `POST /api/recipes`: Create recipe
- `GET /api/recipes/{id}`: Get specific recipe
- `PUT /api/recipes/{id}`: Update recipe
- `DELETE /api/recipes/{id}`: Delete recipe
- `GET /api/recipes/search`: Search recipes

#### Nutrition Endpoints
- `POST /api/nutrition/foods`: Create food item
- `GET /api/nutrition/foods`: Get food items
- `GET /api/nutrition/foods/search`: Search food database
- `POST /api/nutrition/meals`: Create meal log
- `GET /api/nutrition/meals`: Get meal logs
- `GET /api/nutrition/stats/daily`: Get daily nutrition stats

#### Social Endpoints
- `POST /api/social/posts`: Create social post
- `GET /api/social/posts`: Get social feed
- `POST /api/social/posts/{id}/like`: Like a post
- `POST /api/social/posts/{id}/comments`: Comment on a post
- `POST /api/social/users/{id}/follow`: Follow a user

## 5. Testing Strategy

- Unit tests for each module using `unittest`
- Integration tests for cross-module functionality
- Test fixtures and mocks for external dependencies
- Comprehensive test plan in `TEST_PLAN.md`

## 6. Deployment Options

- Docker containerization support
- Gunicorn for production WSGI server
- CI/CD pipeline setup in progress

## 7. Current Sprint Focus
- Complete frontend components for recipe management
- Implement frontend nutrition tracking
- Create comprehensive frontend tests
- Improve API documentation
- Set up CI/CD pipeline

## 8. Next Actions

1. **Frontend Development**:
   - Complete recipe components
   - Implement nutrition tracking UI
   - Develop social feature components

2. **Integration Testing**:
   - Create end-to-end tests
   - Test full user workflows

3. **DevOps**:
   - Finalize CI/CD pipeline
   - Create production deployment scripts
   - Implement monitoring and logging in production

4. **Documentation**:
   - Complete API documentation
   - Create user documentation
   - Document deployment process

## 9. Development Notes

- Firebase is used for authentication, database, and storage
- The application follows a modular design with Flask blueprints
- The frontend uses React with TypeScript
- The project uses a RESTful API design