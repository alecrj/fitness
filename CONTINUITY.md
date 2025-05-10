# Fitness & Food App - Comprehensive Project Documentation

This document serves as the authoritative reference for the Fitness & Food App project structure, architecture, implementation status, and development roadmap.

## 1. Project Overview

- **Name**: Fitness & Food App
- **Purpose**: A comprehensive platform for nutrition tracking, recipe management, and social fitness community
- **Tech Stack**:
  - **Backend**: Flask (Python), Firebase (Firestore, Authentication, Storage)
  - **APIs**: USDA Food Data Central API, recipe scrapers
  - **Frontend**: React with TailwindCSS
- **Current Development Phase**: Backend completed, Frontend in progress
- **Current Git Branch**: main

## 2. Project Architecture

### System Architecture Overview

The application follows a modular architecture with a Flask backend and React frontend, both integrated with Firebase:

```
                    ┌───────────────────────────────────────────┐
                    │                                           │
                    │              User's Browser               │
                    │                                           │
                    └───────────────────────┬───────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────┐
                    │                                           │
                    │            React Frontend                 │
                    │                                           │
                    └───────────────────────┬───────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────┐
                    │               REST API                    │
                    └───────────────────────┬───────────────────┘
                                            │
                                            ▼
                    ┌─────────────────┐     │
                    │   Flask App     │     │
                    └────────┬────────┘     │
        ┌───────────────────┼───────────────┴─────┐
        │                   │                     │
┌───────┴───────┐   ┌───────┴───────┐    ┌────────┴───────┐
│ Auth Module   │   │ Recipe Module │    │Nutrition Module│
└───────┬───────┘   └───────┬───────┘    └────────┬───────┘
        │                   │                     │
┌───────┴───────┐           │            ┌────────┴───────┐
│ Social Module │           │            │  Utils Module  │
└───────┬───────┘           │            └────────┬───────┘
        │                   │                     │
        └───────────────────┼─────────────────────┘
                            ▼
                   ┌────────┴────────┐
                   │  Firebase API   │
                   └────────┬────────┘
        ┌─────────────────────────────────────────┐
        │                   │                     │
┌───────┴────────┐ ┌────────┴────────┐   ┌────────┴────────┐
│ Authentication │ │   Firestore     │   │     Storage     │
└────────────────┘ └─────────────────┘   └─────────────────┘
```

### Backend Directory Structure

```
fitness-food-app/
├── app.py                  # Application entry point
├── config.py               # Configuration management
├── auth/                   # Authentication features
│   ├── __init__.py         # Blueprint registration
│   └── routes.py           # API endpoints for auth
├── recipes/                # Recipe management features
│   ├── __init__.py         # Blueprint registration
│   ├── models.py           # Recipe data models
│   ├── routes.py           # API endpoints for recipes
│   └── services.py         # Recipe business logic
├── nutrition/              # Nutrition tracking features
│   ├── __init__.py         # Blueprint registration
│   ├── models.py           # Nutrition data models
│   ├── routes.py           # API endpoints for nutrition
│   └── services.py         # Nutrition business logic
├── social/                 # Community and sharing features
│   ├── __init__.py         # Blueprint registration
│   ├── models.py           # Social data models
│   ├── routes.py           # API endpoints for social
│   └── services.py         # Social business logic
├── utils/                  # Shared utilities
│   ├── __init__.py
│   ├── api_clients.py      # External API integration
│   ├── api_docs.py         # API documentation (Swagger/OpenAPI)
│   ├── background_tasks.py # Async task processing
│   ├── cache.py            # Response caching
│   ├── error_handlers.py   # Error handling middleware
│   ├── firebase_admin.py   # Firebase integration
│   ├── health_check.py     # System health monitoring
│   ├── logging.py          # Logging configuration
│   ├── migrations.py       # Database migration framework
│   ├── monitoring.py       # Performance metrics
│   ├── rate_limit.py       # API rate limiting
│   └── validators.py       # Input validation
├── migrations/             # Database migrations
│   └── migrate_001_add_metadata_to_users.py
├── tests/                  # Test suite
│   ├── unit/               # Unit tests for individual modules
│   │   ├── test_auth.py
│   │   ├── test_nutrition.py
│   │   ├── test_recipes.py
│   │   ├── test_social.py
│   │   └── test_validators.py
│   ├── integration/        # Integration tests
│   │   └── test_integration.py
│   ├── conftest.py         # Test configuration
│   └── test_api_clients.py # API client tests
├── .env                    # Environment variables (development)
├── .env.example            # Example environment configuration
├── Dockerfile              # Docker container configuration
├── gunicorn_config.py      # Production WSGI server configuration
├── Procfile                # Deployment configuration
├── openapi.json            # API documentation (Swagger/OpenAPI)
├── requirements.txt        # Project dependencies
├── manage.py               # CLI utility for managing the application
├── run_tests.py            # Test runner utility
└── .github/                # CI/CD workflows
    └── workflows/
        └── test.yml        # GitHub Actions test configuration
```

### Frontend Architecture

The React frontend follows a component-based architecture:

```
frontend/
├── public/                # Static files
└── src/
    ├── api/              # API client and service functions
    │   ├── auth/         # Authentication API
    │   ├── recipes/      # Recipe API
    │   ├── nutrition/    # Nutrition API
    │   └── social/       # Social API
    ├── assets/           # Static assets
    │   ├── images/       # Image files
    │   └── styles/       # CSS files
    ├── components/       # Reusable UI components
    │   ├── common/       # General UI components
    │   ├── layouts/      # Page layouts
    │   ├── navigation/   # Navigation components
    │   ├── recipes/      # Recipe-specific components
    │   ├── nutrition/    # Nutrition-specific components
    │   └── social/       # Social-specific components
    ├── contexts/         # React context providers
    │   ├── AuthContext   # Authentication state
    │   └── AppContext    # Application state
    ├── hooks/            # Custom React hooks
    ├── pages/            # Page components
    │   ├── auth/         # Authentication pages
    │   ├── recipes/      # Recipe pages
    │   ├── nutrition/    # Nutrition pages
    │   └── social/       # Social pages
    └── utils/            # Utility functions
```

## 3. Core Project Components

### Authentication Module (COMPLETE)

**Key Files**:
- `auth/__init__.py`: Blueprint registration
- `auth/routes.py`: API endpoints for auth actions
- `utils/firebase_admin.py`: Firebase authentication integration

**Features**:
- User registration and authentication via Firebase
- User profile management
- Profile image upload and storage
- JWT token validation via auth middleware
- Protected routes for authenticated users

### Recipe Module (COMPLETE)

**Key Files**:
- `recipes/__init__.py`: Blueprint registration
- `recipes/routes.py`: API endpoints for recipe management
- `recipes/models.py`: Recipe data structures

**Features**:
- Recipe creation, retrieval, update, deletion
- Recipe import from external websites via URL
- Support for Instagram recipe imports
- Recipe search and filtering
- Recipe sharing (public/private)
- Recipe image upload and management
- Recipe tagging and categorization
- Nutritional analysis for recipes
- List of supported recipe import sites

### Nutrition Module (COMPLETE)

**Key Files**:
- `nutrition/__init__.py`: Blueprint registration
- `nutrition/models.py`: Data models for nutrition tracking
- `nutrition/routes.py`: API endpoints for nutrition tracking

**Features**:
- Food item database (custom and USDA items)
- USDA API integration for food data
- Meal logging with portioning
- Nutrition calculations and tracking
- Daily and weekly nutrition statistics
- Barcode scanning for food lookup
- Food favorites management
- Detailed nutritional breakdown for foods

### Social Module (COMPLETE)

**Key Files**:
- `social/__init__.py`: Blueprint registration
- `social/models.py`: Social features data models
- `social/routes.py`: API endpoints for social features

**Features**:
- Social post creation with images
- User following system
- Feed generation (all posts, profile, following)
- Comments on posts
- Post likes and like tracking
- User followers and following lists
- Social sharing of meals and recipes
- Trending tags analysis
- Activity tracking

### Utilities & Infrastructure (COMPLETE)

**Key Files**:
- `utils/api_clients.py`: External API integration (USDA, barcode)
- `utils/background_tasks.py`: Asynchronous task processing
- `utils/error_handlers.py`: Error handling
- `utils/firebase_admin.py`: Firebase integration
- `utils/rate_limit.py`: API rate limiting
- `utils/validators.py`: Input validation
- `utils/api_docs.py`: API documentation
- `utils/health_check.py`: System health monitoring
- `utils/monitoring.py`: Performance metrics
- `utils/cache.py`: Response caching
- `utils/logging.py`: Logging configuration
- `utils/migrations.py`: Database migration system

**Features**:
- API documentation with OpenAPI/Swagger
- Background task processing for long-running operations
- Rate limiting with Redis (with in-memory fallback)
- Health check endpoints for monitoring
- Performance monitoring metrics
- Request/response logging
- Database migrations
- Error handling middleware
- Input validation with various validation functions
- External API clients for USDA and barcode lookup
- Request caching for improved performance

### Testing Framework (COMPLETE)

**Key Files**:
- `tests/conftest.py`: Test configuration and fixtures
- `tests/unit/`: Unit tests for all modules
- `tests/integration/`: Integration tests for cross-module functionality
- `run_tests.py`: Test runner utility

**Features**:
- Comprehensive test suite for all modules
- Unit tests for individual components
- Integration tests for cross-module functionality
- Mock Firebase services for testing
- Test fixtures for common objects
- GitHub Actions CI integration

### DevOps & Infrastructure (COMPLETE)

**Key Files**:
- `.github/workflows/test.yml`: GitHub Actions workflow configuration
- `Dockerfile`: Docker container definition
- `gunicorn_config.py`: Production WSGI server configuration
- `Procfile`: Deployment configuration
- `manage.py`: CLI utility for app management

**Features**:
- Automated testing on push and pull requests
- Docker containerization
- Production deployment with Gunicorn
- Environment variable configuration
- CLI utilities for common tasks:
  - Running database migrations
  - Creating backups
  - Running tests
  - Managing the application

## 4. Firebase Data Model

### Collections:

- **users**: User profiles and preferences
  ```
  {
    id: string (Firebase UID),
    name: string,
    profile_image_url: string (optional),
    created_at: timestamp,
    updated_at: timestamp,
    following_count: number,
    follower_count: number,
    metadata: {
      onboarding_completed: boolean,
      version: number
    }
  }
  ```

- **food_items**: Nutrition database items
  ```
  {
    id: string,
    userId: string,
    name: string,
    brand: string (optional),
    barcode: string (optional),
    fdcId: string (optional, USDA reference),
    serving_size: number,
    serving_unit: string,
    calories: number,
    protein: number,
    carbs: number,
    fat: number,
    nutrition: {
      calories: number,
      protein: number,
      carbs: number,
      fat: number,
      fiber: number (optional),
      sugar: number (optional),
      sodium: number (optional),
      cholesterol: number (optional)
    },
    is_custom: boolean,
    is_favorite: boolean,
    created_at: timestamp,
    updated_at: timestamp
  }
  ```

- **meals**: User logged meals
  ```
  {
    id: string,
    userId: string,
    name: string,
    meal_type: string (breakfast, lunch, dinner, snack),
    meal_time: timestamp,
    food_items: [
      {
        food_item_id: string,
        food_item_name: string,
        servings: number,
        nutrition: {
          calories: number,
          protein: number,
          carbs: number,
          fat: number,
          fiber: number (optional),
          sugar: number (optional),
          sodium: number (optional),
          cholesterol: number (optional)
        }
      }
    ],
    nutrition_totals: {
      calories: number,
      protein: number,
      carbs: number,
      fat: number,
      fiber: number (optional),
      sugar: number (optional),
      sodium: number (optional),
      cholesterol: number (optional)
    },
    notes: string (optional),
    tags: [string] (optional),
    created_at: timestamp,
    updated_at: timestamp
  }
  ```

- **recipes**: User saved and imported recipes
  ```
  {
    id: string,
    userId: string,
    title: string,
    description: string (optional),
    ingredients: [string],
    instructions: [string],
    prepTime: number (optional),
    cookTime: number (optional),
    servings: number (optional),
    difficulty: string (optional),
    cuisine: string (optional),
    imageUrl: string (optional),
    imageStoragePath: string (optional),
    tags: [string] (optional),
    createdAt: timestamp,
    updatedAt: timestamp,
    isPublic: boolean,
    source: string (user, web, instagram),
    sourceUrl: string (optional),
    nutrition: {
      calories: number (optional),
      protein: number (optional),
      carbs: number (optional),
      fat: number (optional),
      fiber: number (optional),
      sugar: number (optional)
    },
    needsReview: boolean (optional)
  }
  ```

- **posts**: Social posts
  ```
  {
    id: string,
    userId: string,
    userName: string,
    userProfileImage: string (optional),
    content: string,
    imageUrl: string (optional),
    recipeId: string (optional),
    mealId: string (optional),
    tags: [string] (optional),
    likes: number,
    comments: number,
    createdAt: timestamp,
    updatedAt: timestamp
  }
  ```

- **comments**: Post comments
  ```
  {
    id: string,
    userId: string,
    userName: string,
    userProfileImage: string (optional),
    postId: string,
    content: string,
    createdAt: timestamp,
    updatedAt: timestamp
  }
  ```

- **likes**: Post likes
  ```
  {
    id: string (userId_postId),
    userId: string,
    postId: string,
    createdAt: timestamp
  }
  ```

- **follows**: User follow relationships
  ```
  {
    id: string (followerId_followingId),
    followerId: string,
    followingId: string,
    createdAt: timestamp
  }
  ```

- **tasks**: Background task status
  ```
  {
    id: string,
    name: string,
    status: string (queued, running, completed, failed),
    progress: number,
    created_at: timestamp,
    started_at: timestamp (optional),
    completed_at: timestamp (optional),
    result: any (optional),
    error: string (optional)
  }
  ```

- **_migrations**: Database migration tracking
  ```
  {
    version: string,
    name: string,
    started_at: timestamp,
    completed_at: timestamp (optional),
    status: string (in_progress, completed, failed),
    duration_seconds: number (optional),
    error: string (optional)
  }
  ```

## 5. API Documentation

### Auth Endpoints

- `POST /api/auth/profile`: Create or update user profile
  - Request body: `name`, optional `profile_image_base64`
  - Response: User profile object
  - Authentication: Required

- `GET /api/auth/profile`: Get user profile
  - Response: User profile object
  - Authentication: Required

### Recipe Endpoints

- `POST /api/recipes/import`: Import recipe from URL
  - Request body: `url`
  - Response: Imported recipe object
  - Authentication: Required

- `GET /api/recipes`: Get user's recipes
  - Query parameters: `limit`, `offset`
  - Response: List of recipes with pagination
  - Authentication: Required

- `POST /api/recipes`: Create recipe
  - Request body: `title`, `ingredients`, `instructions`, optional fields
  - Response: Created recipe object
  - Authentication: Required

- `GET /api/recipes/{id}`: Get specific recipe
  - Response: Recipe object
  - Authentication: Required

- `PUT /api/recipes/{id}`: Update recipe
  - Request body: Fields to update
  - Response: Updated recipe object
  - Authentication: Required

- `DELETE /api/recipes/{id}`: Delete recipe
  - Response: Success message
  - Authentication: Required

- `GET /api/recipes/search`: Search recipes
  - Query parameters: `q`, `tags`, `cuisine`, `difficulty`, `includePublic`
  - Response: List of recipes with pagination
  - Authentication: Required

- `POST /api/recipes/share/{id}`: Share recipe publicly
  - Response: Share status
  - Authentication: Required

- `POST /api/recipes/unshare/{id}`: Make recipe private
  - Response: Share status
  - Authentication: Required

- `POST /api/recipes/nutritional-analysis`: Analyze recipe nutrition
  - Request body: `ingredients`, optional `servings`
  - Response: Nutritional analysis
  - Authentication: Required

- `GET /api/recipes/supported-sites`: Get supported recipe import sites
  - Response: List of supported sites
  - Authentication: Not required

### Nutrition Endpoints

- `POST /api/nutrition/foods`: Create food item
  - Request body: `name`, `nutrition`, optional fields
  - Response: Created food item
  - Authentication: Required

- `GET /api/nutrition/foods`: Get food items
  - Query parameters: `limit`, `offset`, `is_favorite`, `is_custom`, `q`
  - Response: List of food items with pagination
  - Authentication: Required

- `GET /api/nutrition/foods/{id}`: Get specific food item
  - Response: Food item object
  - Authentication: Required

- `PUT /api/nutrition/foods/{id}`: Update food item
  - Request body: Fields to update
  - Response: Updated food item
  - Authentication: Required

- `DELETE /api/nutrition/foods/{id}`: Delete food item
  - Response: Success message
  - Authentication: Required

- `POST /api/nutrition/foods/{id}/favorite`: Toggle food favorite status
  - Response: Updated favorite status
  - Authentication: Required

- `GET /api/nutrition/foods/search`: Search USDA food database
  - Query parameters: `q`
  - Response: List of foods from USDA
  - Authentication: Required

- `GET /api/nutrition/foods/details/{fdc_id}`: Get detailed USDA food info
  - Response: Detailed food information
  - Authentication: Required

- `POST /api/nutrition/foods/import`: Import food from USDA database
  - Request body: `fdcId`, optional customizations
  - Response: Imported food item
  - Authentication: Required

- `POST /api/nutrition/meals`: Create meal log
  - Request body: `name`, `meal_type`, `food_items`, optional fields
  - Response: Created meal
  - Authentication: Required

- `GET /api/nutrition/meals`: Get meal logs
  - Query parameters: `limit`, `offset`, `date`, `meal_type`
  - Response: List of meals with pagination
  - Authentication: Required

- `GET /api/nutrition/meals/{id}`: Get specific meal
  - Response: Meal object
  - Authentication: Required

- `PUT /api/nutrition/meals/{id}`: Update meal
  - Request body: Fields to update
  - Response: Updated meal
  - Authentication: Required

- `DELETE /api/nutrition/meals/{id}`: Delete meal
  - Response: Success message
  - Authentication: Required

- `GET /api/nutrition/stats/daily`: Get daily nutrition stats
  - Query parameters: `date`
  - Response: Daily nutrition statistics
  - Authentication: Required

- `GET /api/nutrition/stats/weekly`: Get weekly nutrition stats
  - Query parameters: `start_date`, `end_date`
  - Response: Weekly nutrition statistics
  - Authentication: Required

- `GET /api/nutrition/barcode/lookup`: Look up food by barcode
  - Query parameters: `code`
  - Response: Food information
  - Authentication: Required

### Social Endpoints

- `POST /api/social/posts`: Create social post
  - Request body: `content`, optional `imageBase64`, `tags`, `recipeId`, `mealId`
  - Response: Created post
  - Authentication: Required

- `GET /api/social/posts`: Get social feed
  - Query parameters: `limit`, `offset`, `userId`, `tag`, `feed` (all, profile, following)
  - Response: List of posts with pagination
  - Authentication: Required

- `GET /api/social/posts/{id}`: Get specific post
  - Response: Post object
  - Authentication: Required

- `PUT /api/social/posts/{id}`: Update post
  - Request body: Fields to update
  - Response: Updated post
  - Authentication: Required

- `DELETE /api/social/posts/{id}`: Delete post
  - Response: Success message
  - Authentication: Required

- `POST /api/social/posts/{id}/like`: Like/unlike a post
  - Response: Like status
  - Authentication: Required

- `POST /api/social/posts/{id}/comments`: Comment on a post
  - Request body: `content`
  - Response: Created comment
  - Authentication: Required

- `GET /api/social/posts/{id}/comments`: Get post comments
  - Query parameters: `limit`, `offset`, `sort_by`, `sort_dir`
  - Response: List of comments with pagination
  - Authentication: Required

- `DELETE /api/social/comments/{id}`: Delete comment
  - Response: Success message
  - Authentication: Required

- `POST /api/social/users/{id}/follow`: Follow/unfollow user
  - Response: Follow status
  - Authentication: Required

- `GET /api/social/users/{id}/followers`: Get user followers
  - Query parameters: `limit`, `offset`
  - Response: List of followers with pagination
  - Authentication: Required

- `GET /api/social/users/{id}/following`: Get user following
  - Query parameters: `limit`, `offset`
  - Response: List of following with pagination
  - Authentication: Required

- `GET /api/social/users/me/likes`: Get liked posts
  - Query parameters: `limit`, `offset`
  - Response: List of liked posts with pagination
  - Authentication: Required

- `GET /api/social/users/{id}/follow-status`: Check follow status
  - Response: Follow status
  - Authentication: Required

- `GET /api/social/trending/tags`: Get trending tags
  - Query parameters: `limit`
  - Response: List of trending tags
  - Authentication: Required

### System Endpoints

- `GET /health`: Health check endpoint
  - Query parameters: `detailed` (boolean)
  - Response: System health status
  - Authentication: Not required

- `GET /metrics`: Performance metrics endpoint
  - Response: System performance metrics
  - Authentication: Optional API key

- `GET /api/tasks/{id}`: Check background task status
  - Response: Task status
  - Authentication: Not required

## 6. Environment Configuration

The application is configured using environment variables, with defaults in `config.py`:

```python
class Config:
    # Flask settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'development-key')
    ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Firebase settings
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', './firebase-credentials.json')
    FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET')
    
    # External API settings
    USDA_API_KEY = os.environ.get('USDA_API_KEY')
    USDA_API_BASE_URL = 'https://api.nal.usda.gov/fdc/v1'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Feature flags
    ENABLE_SOCIAL_FEATURES = os.environ.get('ENABLE_SOCIAL_FEATURES', 'True').lower() == 'true'
    ENABLE_RECIPE_IMPORT = os.environ.get('ENABLE_RECIPE_IMPORT', 'True').lower() == 'true'
```

## 7. Testing Framework

The testing framework uses pytest with the following components:

- **Test Configuration**: `tests/conftest.py` contains fixtures and setup for all tests
- **Unit Tests**: Tests for individual module functionality
  - Auth: `tests/unit/test_auth.py`
  - Nutrition: `tests/unit/test_nutrition.py`
  - Recipes: `tests/unit/test_recipes.py`
  - Social: `tests/unit/test_social.py`
  - Validators: `tests/unit/test_validators.py`
- **Integration Tests**: Tests for cross-module functionality
  - `tests/integration/test_integration.py`
- **API Client Tests**: Tests for external API clients
  - `tests/test_api_clients.py`

Key testing aspects:
- Mock Firebase services for isolated testing
- Parametrized test cases for multiple scenarios
- Test fixtures for reusable test data
- Authentication simulation for protected routes testing
- Custom test runner (`run_tests.py`) for organizing test execution

## 8. Development Status

### Completed Components:
- ✅ Core Flask application setup with blueprint architecture
- ✅ Firebase integration (Authentication, Firestore, Storage)
- ✅ Authentication module
- ✅ Recipe module with import functionality
- ✅ Nutrition module with USDA integration
- ✅ Social module with all features
- ✅ Utility components (validators, API clients, etc.)
- ✅ Comprehensive test suite (unit & integration)
- ✅ GitHub Actions CI pipeline
- ✅ API documentation with Swagger/OpenAPI
- ✅ Background task processing
- ✅ Performance monitoring and metrics
- ✅ Health check endpoints
- ✅ Error handling middleware
- ✅ Rate limiting
- ✅ Logging system
- ✅ Database migrations framework
- ✅ Docker & Gunicorn deployment configuration
- ✅ CLI utility for management tasks

### In Progress:
- 🔄 Frontend development with React
- 🔄 Production deployment configuration

### Completed Frontend Components:
- ✅ Frontend project structure setup
- ✅ React application with TailwindCSS configuration
- ✅ Basic authentication flow (login screen)
- ✅ AuthContext for Firebase integration
- ✅ AppContext for application state management
- ✅ API client with token handling
- ✅ Common UI components (Layout, Navbar, Notifications)
- ✅ Authentication page layouts

### Upcoming Frontend Work:
- ⏳ Complete authentication module functionality
- ⏳ Frontend for recipe module 
- ⏳ Frontend for nutrition module
- ⏳ Frontend for social module
- ⏳ Mobile-responsive design
- ⏳ Frontend testing
- ⏳ User onboarding flow optimization
- ⏳ Analytics and reporting dashboards

## 9. Development Process

### Workflows and Standards
- **Git Workflow**: Feature branches for development, main for stable releases
- **Testing Process**: Unit tests for all new features, integration tests for cross-module functionality
- **API Design**: RESTful principles with consistent endpoint patterns
- **Error Handling**: Standardized error formats across all endpoints
- **Input Validation**: Comprehensive validation for all input data
- **Frontend Development**: Component-based architecture with React and TailwindCSS

### Best Practices
- Modular design with Flask blueprints (backend)
- Clear separation of concerns (routes, models, services)
- Consistent error handling and response formats
- Comprehensive documentation
- Test-driven development (TDD) approach
- Component reusability and standardized UI patterns
- Context providers for global state management
- Custom hooks for shared functionality

## 10. Deployment Options

### Development Deployment:
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
export FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
export USDA_API_KEY=your-usda-api-key

# Run the application
python app.py
```

### Production Deployment:
```bash
# Run with Gunicorn
gunicorn --config gunicorn_config.py app:create_app()
```

### Docker Deployment:
```bash
# Build the Docker image
docker build -t fitness-food-app .

# Run the Docker container
docker run -p 5000:5000 fitness-food-app
```

## 11. External Dependencies

- **Firebase Admin SDK**: Firebase integration for authentication, database, and storage
- **Flask**: Web framework for the API
- **Flask-CORS**: Cross-origin resource sharing support
- **recipe-scrapers**: Recipe import from supported websites
- **BeautifulSoup4**: HTML parsing for recipe imports from unsupported sites
- **Requests**: HTTP client for API integrations
- **PyJWT**: JWT token handling for authentication
- **apispec**: OpenAPI/Swagger documentation generation
- **flask-swagger-ui**: Interactive API documentation UI
- **gunicorn**: Production WSGI HTTP server
- **python-dotenv**: Environment variable loading
- **psutil**: System resource monitoring
- **redis**: Redis client for rate limiting (optional)

### Frontend Dependencies
- **React**: Frontend UI library
- **React Router**: Navigation and routing
- **TailwindCSS**: Utility-first CSS framework
- **Formik & Yup**: Form handling and validation
- **Axios**: HTTP client for API requests
- **Firebase**: Authentication and storage

## 12. Management Commands

The application includes a CLI utility (`manage.py`) for common maintenance tasks:

```bash
# Run tests
python manage.py test

# Run database migrations
python manage.py migrate

# Create a new migration
python manage.py create-migration 002 add_user_preferences

# Backup database
python manage.py backup

# Restore database from backup
python manage.py restore backup_file.json

# Clean up old data
python manage.py cleanup --days 30 --tasks

# Run development server
python manage.py runserver
```

## 13. Next Steps and Roadmap

### Immediate Focus (Next 2 Weeks):
1. Complete React frontend for authentication module
2. Implement frontend recipe management pages
3. Set up user onboarding workflow

### Short-term Goals (1-2 Months):
1. Complete frontend for nutrition tracking
2. Implement frontend social features
3. Optimize mobile experience
4. Set up monitoring and analytics

### Long-term Goals (2+ Months):
1. Progressive Web App capabilities
2. Offline support
3. Push notifications
4. Enhanced personalization
5. Advanced analytics dashboard

## 14. Known Issues & Limitations

- Barcode lookup API integration is incomplete (placeholder implementation)
- Limited nutrition database without complete micronutrients
- Recipe import doesn't handle all possible website formats
- No export functionality for data
- Limited offline capabilities
- Frontend Firebase configuration needs to be populated with real values

## 15. Frontend Development Status

The frontend development is in progress with the following components already in place:

- **Project Structure**: Complete directory structure for a React application
- **UI Framework**: TailwindCSS for styling with custom component classes
- **Authentication**: Basic login screen, context provider for Firebase Auth
- **State Management**: Context providers for application state
- **API Integration**: API client with token handling and request/response interceptors
- **UI Components**: Core reusable components for consistent UI patterns
- **Responsive Design**: Mobile-first approach with responsive design patterns

### Next Frontend Steps

1. Complete the authentication flows (registration, profile management)
2. Implement recipe listing and management pages
3. Implement nutrition tracking and meal logging pages
4. Implement social feed and interaction pages
5. Add comprehensive testing for frontend components
6. Optimize for production deployment

---

This document represents the current state of the Fitness & Food App project as of May 10, 2025. It will be updated regularly as development progresses.