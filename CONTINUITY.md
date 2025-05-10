# Fitness & Food App - Continuity Document

This document serves as the comprehensive reference for project status, architecture, and development continuity. It reflects the current state of the project as of May 10, 2025.

## 1. Project Overview
- **Name**: Fitness & Food App
- **Purpose**: A comprehensive application for nutrition tracking, recipe management, and social fitness community
- **Tech Stack**: 
  - **Backend**: Flask, Firebase (Firestore, Authentication, Storage)
  - **Frontend**: React (in progress)
  - **APIs**: USDA Food Data Central API, recipe scrapers
- **Current Phase**: Backend implementation completed, Frontend in progress

## 2. Project Architecture

### Backend Structure
```
fitness-food-app/
├── app.py                  # Application entry point and configuration
├── config.py               # Environment and application settings
├── auth/                   # Authentication features
│   ├── __init__.py         # Blueprint registration
│   ├── routes.py           # API endpoints for auth
│   └── services.py         # Auth business logic
├── recipes/                # Recipe management features
│   ├── __init__.py         # Blueprint registration
│   ├── routes.py           # API endpoints for recipes
│   ├── models.py           # Recipe data models
│   └── services.py         # Recipe business logic
├── nutrition/              # Nutrition tracking features
│   ├── __init__.py         # Blueprint registration
│   ├── routes.py           # API endpoints for nutrition
│   ├── models.py           # Nutrition data models
│   └── services.py         # Nutrition business logic
├── social/                 # Community and sharing features
│   ├── __init__.py         # Blueprint registration
│   ├── routes.py           # API endpoints for social
│   ├── models.py           # Social data models
│   └── services.py         # Social business logic
├── utils/                  # Shared utilities
│   ├── __init__.py
│   ├── api_clients.py      # External API integration
│   ├── api_docs.py         # API documentation (Swagger/OpenAPI)
│   ├── background_tasks.py # Async task processing
│   ├── cache.py            # Response caching
│   ├── error_handlers.py   # Error handling middlewares
│   ├── firebase_admin.py   # Firebase integration
│   ├── health_check.py     # System health monitoring
│   ├── logging.py          # Logging configuration
│   ├── migrations.py       # Database migration framework
│   ├── monitoring.py       # Performance metrics
│   ├── rate_limit.py       # API rate limiting
│   └── validators.py       # Input validation
├── migrations/             # Database migrations
│   └── migrate_001_add_metadata_to_users.py
├── .env                    # Environment variables (development)
├── .env.example            # Example environment variables
├── .dockerignore           # Docker build exclusions
├── requirements.txt        # Project dependencies
└── .github/                # CI/CD workflows
    └── workflows/
        └── test.yml        # GitHub Actions test configuration
```

### Firebase Data Model

#### Collections:
- **users**: User profiles and settings
- **food_items**: Nutrition database items (user custom and imported)
- **meals**: User logged meals with nutritional data
- **recipes**: User saved and imported recipes
- **posts**: Social posts shared by users
- **comments**: Comments on social posts
- **likes**: Post like relationships
- **follows**: User following relationships
- **tasks**: Background task status tracking
- **_migrations**: Database migration tracking

## 3. Module Status

### Authentication Module (COMPLETE)
- **Status**: Complete
- **Key Files**: 
  - `auth/routes.py`: API endpoints for auth
  - `auth/__init__.py`: Blueprint registration
  - `utils/firebase_admin.py`: Firebase auth integration
- **Features**:
  - User registration and authentication via Firebase
  - Profile management with image upload
  - Auth middleware for protected routes
  - JWT token validation

### Recipe Module (COMPLETE)
- **Status**: Complete
- **Key Files**: 
  - `recipes/routes.py`: API endpoints for recipes
  - `recipes/__init__.py`: Blueprint registration
- **Features**:
  - Recipe creation and management
  - Recipe import from URLs (including Instagram)
  - Recipe search and filtering
  - Recipe sharing between users
  - Nutrition calculation for recipes
  - Recipe tags and categories
  - Image upload and management

### Nutrition Module (COMPLETE)
- **Status**: Complete
- **Key Files**: 
  - `nutrition/models.py`: Data models for nutrition tracking
  - `nutrition/routes.py`: API endpoints for nutrition tracking
  - `nutrition/__init__.py`: Blueprint registration
- **Features**:
  - Food item database with custom and USDA items
  - USDA API integration for food lookup
  - Meal logging with nutritional tracking
  - Daily and weekly nutrition statistics
  - Barcode scanning support
  - Nutrition calculation and tracking
  - Food favorites and categorization

### Social Module (COMPLETE)
- **Status**: Complete
- **Key Files**: 
  - `social/models.py`: Data models for social features
  - `social/routes.py`: API endpoints for social features
  - `social/__init__.py`: Blueprint registration
- **Features**:
  - Social post creation with images
  - User following system
  - Feed generation (all, profile, following)
  - Comments and likes
  - Social sharing of meals and recipes
  - Trending tags

### Utilities & Infrastructure (COMPLETE)
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
  - `migrations/migrate_001_add_metadata_to_users.py`: Initial migration
- **Features**:
  - API documentation with OpenAPI/Swagger
  - Background task processing
  - Rate limiting with Redis or in-memory fallback
  - Health check endpoints
  - Performance monitoring
  - Structured logging
  - Database migrations
  - Error handling middleware
  - Input validation
  - Request caching

### Frontend (IN PROGRESS)
- **Status**: In Progress
- **Key Files**:
  - `frontend/src/api/authService.ts`: Authentication service
  - `frontend/src/api/client.ts`: API client
  - `frontend/src/contexts/AuthContext.tsx`: Auth context for React
  - `frontend/src/components/auth/Login.tsx`: Auth components
- **Features**:
  - Authentication UI
  - Basic application structure
  - React hooks for data fetching

## 4. API Documentation

The API is documented with OpenAPI/Swagger and available at `/api/docs`.

### Auth Endpoints
- `POST /api/auth/profile`: Create user profile
- `GET /api/auth/profile`: Get user profile

### Recipe Endpoints
- `POST /api/recipes/import`: Import recipe from URL
- `GET /api/recipes`: Get user's recipes
- `POST /api/recipes`: Create recipe
- `GET /api/recipes/{id}`: Get specific recipe
- `PUT /api/recipes/{id}`: Update recipe
- `DELETE /api/recipes/{id}`: Delete recipe
- `GET /api/recipes/search`: Search recipes
- `POST /api/recipes/share/{id}`: Share recipe publicly
- `POST /api/recipes/unshare/{id}`: Make recipe private
- `POST /api/recipes/nutritional-analysis`: Analyze recipe nutrition
- `GET /api/recipes/supported-sites`: Get supported recipe import sites

### Nutrition Endpoints
- `POST /api/nutrition/foods`: Create food item
- `GET /api/nutrition/foods`: Get food items
- `GET /api/nutrition/foods/{id}`: Get specific food item
- `PUT /api/nutrition/foods/{id}`: Update food item
- `DELETE /api/nutrition/foods/{id}`: Delete food item
- `POST /api/nutrition/foods/{id}/favorite`: Toggle food favorite status
- `GET /api/nutrition/foods/search`: Search USDA food database
- `GET /api/nutrition/foods/details/{fdc_id}`: Get detailed USDA food info
- `POST /api/nutrition/foods/import`: Import food from USDA database
- `POST /api/nutrition/meals`: Create meal log
- `GET /api/nutrition/meals`: Get meal logs
- `GET /api/nutrition/meals/{id}`: Get specific meal
- `PUT /api/nutrition/meals/{id}`: Update meal
- `DELETE /api/nutrition/meals/{id}`: Delete meal
- `GET /api/nutrition/stats/daily`: Get daily nutrition stats
- `GET /api/nutrition/stats/weekly`: Get weekly nutrition stats
- `GET /api/nutrition/barcode/lookup`: Look up food by barcode

### Social Endpoints
- `POST /api/social/posts`: Create social post
- `GET /api/social/posts`: Get social feed
- `GET /api/social/posts/{id}`: Get specific post
- `PUT /api/social/posts/{id}`: Update post
- `DELETE /api/social/posts/{id}`: Delete post
- `POST /api/social/posts/{id}/like`: Like/unlike a post
- `POST /api/social/posts/{id}/comments`: Comment on a post
- `GET /api/social/posts/{id}/comments`: Get post comments
- `DELETE /api/social/comments/{id}`: Delete comment
- `POST /api/social/users/{id}/follow`: Follow/unfollow user
- `GET /api/social/users/{id}/followers`: Get user followers
- `GET /api/social/users/{id}/following`: Get user following
- `GET /api/social/users/me/likes`: Get liked posts
- `GET /api/social/users/{id}/follow-status`: Check follow status
- `GET /api/social/trending/tags`: Get trending tags

### System Endpoints
- `GET /health`: Health check endpoint
- `GET /metrics`: Performance metrics endpoint
- `GET /api/tasks/{id}`: Check background task status

## 5. Data Models

### User Profile
```json
{
  "id": "string (Firebase UID)",
  "name": "string",
  "profile_image_url": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "following_count": "integer",
  "follower_count": "integer",
  "metadata": {
    "onboarding_completed": "boolean",
    "version": "integer"
  }
}
```

### Food Item
```json
{
  "id": "string",
  "userId": "string",
  "name": "string",
  "brand": "string",
  "barcode": "string (optional)",
  "fdcId": "string (optional, USDA reference)",
  "serving_size": "number",
  "serving_unit": "string",
  "calories": "number",
  "protein": "number",
  "carbs": "number",
  "fat": "number",
  "nutrition": {
    "calories": "number",
    "protein": "number",
    "carbs": "number",
    "fat": "number",
    "fiber": "number",
    "sugar": "number",
    "sodium": "number",
    "cholesterol": "number"
  },
  "is_custom": "boolean",
  "is_favorite": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Meal Log
```json
{
  "id": "string",
  "userId": "string",
  "name": "string",
  "meal_type": "string (breakfast, lunch, dinner, snack)",
  "meal_time": "timestamp",
  "food_items": [
    {
      "food_item_id": "string",
      "food_item_name": "string",
      "servings": "number",
      "nutrition": {
        "calories": "number",
        "protein": "number",
        "carbs": "number",
        "fat": "number",
        "fiber": "number",
        "sugar": "number",
        "sodium": "number",
        "cholesterol": "number"
      }
    }
  ],
  "nutrition_totals": {
    "calories": "number",
    "protein": "number",
    "carbs": "number",
    "fat": "number",
    "fiber": "number",
    "sugar": "number",
    "sodium": "number",
    "cholesterol": "number"
  },
  "notes": "string",
  "tags": ["string"],
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Recipe
```json
{
  "id": "string",
  "userId": "string",
  "title": "string",
  "description": "string",
  "ingredients": ["string"],
  "instructions": ["string"],
  "prepTime": "number (minutes)",
  "cookTime": "number (minutes)",
  "servings": "number",
  "difficulty": "string",
  "cuisine": "string",
  "imageUrl": "string",
  "imageStoragePath": "string",
  "tags": ["string"],
  "createdAt": "timestamp",
  "updatedAt": "timestamp",
  "isPublic": "boolean",
  "source": "string (user, web, instagram)",
  "sourceUrl": "string",
  "nutrition": {
    "calories": "number",
    "protein": "number",
    "carbs": "number",
    "fat": "number",
    "fiber": "number",
    "sugar": "number"
  }
}
```

### Social Post
```json
{
  "id": "string",
  "userId": "string",
  "userName": "string",
  "userProfileImage": "string",
  "content": "string",
  "imageUrl": "string",
  "recipeId": "string (optional)",
  "mealId": "string (optional)",
  "tags": ["string"],
  "likes": "number",
  "comments": "number",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

### Comment
```json
{
  "id": "string",
  "userId": "string",
  "userName": "string",
  "userProfileImage": "string",
  "postId": "string",
  "content": "string",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

### Like
```json
{
  "id": "string (userId_postId)",
  "userId": "string",
  "postId": "string",
  "createdAt": "timestamp"
}
```

### Follow
```json
{
  "id": "string (followerId_followingId)",
  "followerId": "string",
  "followingId": "string",
  "createdAt": "timestamp"
}
```

## 6. Testing Strategy

- Unit tests for each module using `unittest`
- Integration tests for cross-module functionality
- Test fixtures and mocks for external dependencies
- GitHub Actions CI for automated testing

## 7. Deployment Options

- Docker containerization support
- Gunicorn for production WSGI server
- Environment variable configuration
- Health check endpoints for monitoring

## 8. Current Sprint Focus
- Complete frontend components for recipe management
- Implement frontend nutrition tracking
- Create comprehensive frontend tests
- Improve API documentation
- Set up CI/CD pipeline

## 9. Next Actions

1. **Frontend Implementation**:
   - Complete recipe components
   - Implement nutrition tracking UI
   - Develop social feature components
   - Create mobile-responsive design

2. **Integration Testing**:
   - Create end-to-end tests with Cypress
   - Test full user workflows
   - Optimize performance

3. **DevOps**:
   - Finalize CI/CD pipeline
   - Create production deployment scripts
   - Implement monitoring and logging in production

4. **Documentation**:
   - Complete API documentation
   - Create user documentation
   - Document deployment process

## 10. Development Notes

- The application follows a modular design with Flask blueprints
- Firebase is used for authentication, database, and storage
- The API follows RESTful design principles
- Input validation is implemented for all endpoints
- Error handling is standardized across the application
- The frontend will use React with TypeScript
- The app supports multiple environments through configuration