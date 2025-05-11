# Fitness & Food App - Comprehensive Project Documentation

This document serves as the authoritative reference for the Fitness & Food App project structure, architecture, implementation status, and development roadmap.

## 1. Project Overview

- **Name**: Fitness & Food App
- **Purpose**: A comprehensive platform for nutrition tracking, recipe management, and social fitness community
- **Tech Stack**:
  - **Backend**: Flask (Python), Firebase (Firestore, Authentication, Storage)
  - **APIs**: USDA Food Data Central API, recipe scrapers
  - **Frontend**: React with TypeScript and TailwindCSS
- **Current Development Phase**: Backend completed, Frontend modules in development
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
                    │        React/TypeScript Frontend          │
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

The React frontend follows a component-based architecture with TypeScript:

```
frontend/
├── public/                # Static files
└── src/
    ├── api/              # API client and service functions
    │   ├── authService.ts   # Authentication API
    │   ├── client.ts        # API client with auth interceptors
    │   ├── nutritionService.ts # Nutrition API
    │   ├── profileService.ts # Profile API
    │   ├── recipeService.ts # Recipe API
    │   └── socialService.ts # Social API
    ├── assets/           # Static assets
    │   ├── images/       # Image files
    │   └── styles/       # CSS files
    ├── components/       # Reusable UI components
    │   ├── auth/         # Authentication components
    │   │   ├── forms/    # Auth-related forms
    │   │   │   ├── LoginForm.tsx
    │   │   │   ├── RegisterForm.tsx
    │   │   │   ├── PasswordResetForm.tsx
    │   │   │   └── ProfileForm.tsx
    │   │   └── ProtectedRoute.tsx
    │   ├── common/       # General UI components
    │   ├── layouts/      # Page layouts
    │   │   ├── AuthLayout.tsx
    │   │   ├── MainLayout.tsx
    │   │   └── DashboardLayout.tsx
    │   ├── navigation/   # Navigation components
    │   ├── nutrition/    # Nutrition-specific components
    │   │   ├── BarcodeScanner.tsx
    │   │   ├── FoodItemCard.tsx
    │   │   ├── FoodItemForm.tsx
    │   │   ├── MealCard.tsx
    │   │   ├── MealForm.tsx
    │   │   ├── NutritionStats.tsx
    │   │   ├── NutritionSummary.tsx
    │   │   └── USDAFoodSearch.tsx
    │   ├── recipes/      # Recipe-specific components
    │   │   ├── RecipeCard.tsx
    │   │   ├── RecipeDetail.tsx
    │   │   ├── RecipeForm.tsx
    │   │   ├── RecipeImport.tsx
    │   │   └── RecipeList.tsx
    │   ├── social/       # Social-specific components
    │   └── ui/           # UI elements (buttons, inputs, etc.)
    │       ├── Alert.tsx
    │       ├── Avatar.tsx
    │       ├── Button.tsx
    │       ├── Card.tsx
    │       ├── Input.tsx
    │       └── Spinner.tsx
    ├── config/           # Configuration
    │   └── firebase.ts   # Firebase initialization
    ├── contexts/         # React context providers
    │   ├── AuthContext.tsx # Authentication state
    │   ├── NutritionContext.tsx # Nutrition state management
    │   └── RecipeContext.tsx # Recipe state management
    ├── hooks/            # Custom React hooks
    │   ├── usePagination.ts
    │   └── useRecipeFilter.ts
    ├── pages/            # Page components
    │   ├── auth/         # Authentication pages
    │   │   ├── Login.tsx
    │   │   ├── Register.tsx
    │   │   ├── ForgotPassword.tsx
    │   │   ├── ResetPassword.tsx
    │   │   └── Profile.tsx
    │   ├── nutrition/    # Nutrition pages
    │   │   ├── AddEditFoodItem.tsx
    │   │   ├── AddEditMeal.tsx
    │   │   ├── Dashboard.tsx
    │   │   ├── FoodItemDetail.tsx
    │   │   ├── FoodItems.tsx
    │   │   ├── MealDetail.tsx
    │   │   ├── Meals.tsx
    │   │   └── USDASearch.tsx
    │   ├── recipes/      # Recipe pages
    │   └── social/       # Social pages
    ├── routes/           # Route configurations
    │   ├── NutritionRoutes.tsx
    │   └── RecipeRoutes.tsx
    ├── types/            # TypeScript type definitions
    │   ├── auth.ts       # Auth-related types
    │   ├── nutrition.ts  # Nutrition-related types
    │   ├── recipe.ts     # Recipe-related types
    │   ├── social.ts     # Social-related types
    │   └── user.ts       # User profile types
    ├── utils/            # Utility functions
    │   ├── validation/   # Form validation
    │   │   ├── authValidation.ts
    │   │   └── recipeValidation.ts
    │   ├── toast.ts      # Toast notifications
    │   └── errorHandler.ts # Error handling
    ├── App.tsx           # Main application component
    ├── index.tsx         # Application entry point
    └── react-app-env.d.ts # React app type definitions
```

## 3. Core Project Components

### Authentication Module (COMPLETE)

**Backend Key Files**:
- `auth/__init__.py`: Blueprint registration
- `auth/routes.py`: API endpoints for auth actions
- `utils/firebase_admin.py`: Firebase authentication integration

**Frontend Key Files**:
- `src/contexts/AuthContext.tsx`: Authentication state management
- `src/components/auth/forms/LoginForm.tsx`: Login form component
- `src/components/auth/forms/RegisterForm.tsx`: Registration form component
- `src/components/auth/forms/PasswordResetForm.tsx`: Password reset form
- `src/components/auth/forms/ProfileForm.tsx`: Profile update form
- `src/components/auth/ProtectedRoute.tsx`: Route protection component
- `src/pages/auth/Login.tsx`: Login page
- `src/pages/auth/Register.tsx`: Registration page
- `src/pages/auth/ForgotPassword.tsx`: Forgot password page
- `src/pages/auth/ResetPassword.tsx`: Reset password page
- `src/pages/auth/Profile.tsx`: User profile page

**Features**:
- User registration and authentication via Firebase
- User profile management
- Profile image upload and storage
- JWT token validation via auth middleware
- Protected routes for authenticated users
- Password reset functionality
- Email verification

### Recipe Module (COMPLETE)

**Backend Key Files**:
- `recipes/__init__.py`: Blueprint registration
- `recipes/routes.py`: API endpoints for recipe management
- `recipes/models.py`: Recipe data structures

**Frontend Key Files**:
- `src/types/recipe.ts`: Recipe type definitions
- `src/api/recipeService.ts`: Recipe API service
- `src/contexts/RecipeContext.tsx`: Recipe state management
- `src/components/recipes/RecipeCard.tsx`: Recipe card component
- `src/components/recipes/RecipeList.tsx`: Recipe listing component
- `src/components/recipes/RecipeDetail.tsx`: Recipe detail component
- `src/components/recipes/RecipeForm.tsx`: Recipe creation/editing component
- `src/components/recipes/RecipeImport.tsx`: Recipe import component
- `src/routes/RecipeRoutes.tsx`: Recipe routing configuration

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

**Backend Key Files**:
- `nutrition/__init__.py`: Blueprint registration
- `nutrition/models.py`: Data models for nutrition tracking
- `nutrition/routes.py`: API endpoints for nutrition tracking

**Frontend Key Files**:
- `src/types/nutrition.ts`: Nutrition type definitions
- `src/api/nutritionService.ts`: Nutrition API service
- `src/contexts/NutritionContext.tsx`: Nutrition state management
- `src/components/nutrition/FoodItemCard.tsx`: Food item card component
- `src/components/nutrition/FoodItemForm.tsx`: Food item form component
- `src/components/nutrition/USDAFoodSearch.tsx`: USDA food search component
- `src/components/nutrition/MealCard.tsx`: Meal card component
- `src/components/nutrition/MealForm.tsx`: Meal form component
- `src/components/nutrition/NutritionStats.tsx`: Nutrition statistics component
- `src/components/nutrition/NutritionSummary.tsx`: Nutrition summary component
- `src/components/nutrition/BarcodeScanner.tsx`: Barcode scanner component
- `src/pages/nutrition/Dashboard.tsx`: Nutrition dashboard page
- `src/pages/nutrition/FoodItems.tsx`: Food items listing page
- `src/pages/nutrition/FoodItemDetail.tsx`: Food item detail page
- `src/pages/nutrition/AddEditFoodItem.tsx`: Add/edit food item page
- `src/pages/nutrition/USDASearch.tsx`: USDA food search page
- `src/pages/nutrition/Meals.tsx`: Meals listing page
- `src/pages/nutrition/MealDetail.tsx`: Meal detail page
- `src/pages/nutrition/AddEditMeal.tsx`: Add/edit meal page
- `src/routes/NutritionRoutes.tsx`: Nutrition routing configuration

**Features**:
- Food item database (custom and USDA items)
- USDA API integration for food data
- Meal logging with portioning
- Nutrition calculations and tracking
- Daily and weekly nutrition statistics
- Barcode scanning for food lookup
- Food favorites management
- Detailed nutritional breakdown for foods

### Social Module (BACKEND COMPLETE, FRONTEND PLANNED)

**Backend Key Files**:
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

**Backend Key Files**:
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

**Frontend Key Files**:
- `src/api/client.ts`: API client with authentication
- `src/utils/toast.ts`: Toast notification service
- `src/utils/validation/`: Form validation
- `src/hooks/usePagination.ts`: Pagination hook
- `src/hooks/useRecipeFilter.ts`: Recipe filtering hook
- `src/components/ui/Spinner.tsx`: Loading spinner component

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

### Testing Framework (BACKEND COMPLETE, FRONTEND PLANNED)

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
- ✅ Authentication module (backend)
- ✅ Recipe module with import functionality (backend)
- ✅ Nutrition module with USDA integration (backend)
- ✅ Social module with all features (backend)
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
- ✅ Frontend authentication module
- ✅ Frontend Recipe module
- ✅ Frontend Nutrition module

### In Progress:
- ✅ Frontend Nutrition module implementation
  - ✅ Nutrition type definitions
  - ✅ Nutrition API service
  - ✅ Nutrition context provider
  - ✅ Basic Nutrition components (FoodItemCard, FoodItemForm, etc.)
  - ✅ Food-related pages (FoodItems, FoodItemDetail, AddEditFoodItem, USDASearch)
  - ✅ Dashboard page
  - ✅ Meal-related pages (Meals, MealDetail, AddEditMeal)
  - ⏳ Testing and refining the implementation

### Upcoming:
- ⏳ Frontend Social module
- ⏳ Production deployment configuration

### Frontend Status:
- ✅ Frontend project structure setup with TypeScript
- ✅ Firebase integration for frontend
- ✅ API client with token handling
- ✅ Authentication context for state management
- ✅ Login component and page
- ✅ Registration component and page
- ✅ Password reset components and pages
- ✅ Profile management component and page
- ✅ Protected route component
- ✅ Main layout with navigation
- ✅ Recipe components (listing, detail, create/edit, import)
- ✅ Recipe context for state management
- ✅ Recipe routing configuration
- ✅ Nutrition components implementation
  - ✅ Food item management
  - ✅ Food item form
  - ✅ USDA food search
  - ✅ Nutrition statistics visualization
  - ✅ Meal logging form
- ✅ Nutrition pages implementation
  - ✅ Dashboard
  - ✅ Food Items
  - ✅ Food Item Detail
  - ✅ Add/Edit Food Item
  - ✅ USDA Search
  - ✅ Meals
  - ✅ Meal Detail
  - ✅ Add/Edit Meal
- ⏳ Social components (feed, post creation, interactions)
- ⏳ Mobile responsive design improvements
- ⏳ Frontend testing implementation

## 9. Development Process

### Workflows and Standards
- **Git Workflow**: Feature branches for development, main for stable releases
- **Testing Process**: Unit tests for all new features, integration tests for cross-module functionality
- **API Design**: RESTful principles with consistent endpoint patterns
- **Error Handling**: Standardized error formats across all endpoints
- **Input Validation**: Comprehensive validation for all input data
- **Frontend Development**: Component-based architecture with React and TypeScript
- **State Management**: Context API for global state, local state for component-specific data
- **Form Handling**: Consistent validation patterns and error handling
- **Styling**: TailwindCSS for consistent design system
- **Code Quality**: TypeScript for type safety, ESLint for code quality

### Best Practices
- Modular design with Flask blueprints (backend)
- Clear separation of concerns (routes, models, services)
- Consistent error handling and response formats
- Comprehensive documentation
- Test-driven development (TDD) approach
- Component reusability and standardized UI patterns
- Context providers for global state management
- Custom hooks for shared functionality
- Type safety with TypeScript interfaces

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

### Backend Dependencies
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
- **TypeScript**: Type-safe JavaScript
- **React Router**: Navigation and routing
- **TailwindCSS**: Utility-first CSS framework
- **Firebase**: Authentication and storage
- **Axios**: HTTP client for API requests

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

### Immediate Focus (Current Tasks):
1. Test and refine the Nutrition module functionality
   - Test CRUD operations for food items
   - Test meal logging and tracking
   - Test USDA search and import
   - Verify nutrition statistics calculations
   - Improve user experience and fix any bugs

2. Begin planning the Social module implementation
   - Define Social module types
   - Implement Social API service
   - Create Social context provider
   - Design core Social components

### Short-term Goals (1-2 Weeks):
1. Complete testing of the Nutrition module
   - Fix any issues or bugs discovered during testing
   - Implement user experience improvements
   - Add missing features or enhancements

2. Begin implementing the Social module
   - Create Social module pages and components
   - Integrate with backend Social API
   - Implement posting, following, and commenting functionalities

### Medium-term Goals (2-4 Weeks):
1. Complete the Social module implementation
   - Implement feed generation
   - Add post creation with images
   - Enable meal and recipe sharing
   - Add commenting and liking functionality

2. Enhance user experience across all modules
   - Improve mobile responsiveness
   - Add micro-interactions and visual feedback
   - Implement more intuitive navigation
   - Add progressive loading for better performance

### Long-term Goals (1-2 Months):
1. Progressive Web App capabilities
2. Offline support
3. Push notifications
4. Enhanced personalization
5. Advanced analytics dashboard
6. Performance optimizations
7. Enhanced data visualization

## 14. Known Issues & Limitations

- Recipe import doesn't handle all possible website formats
- No export functionality for data
- Limited offline capabilities
- Frontend Firebase configuration needs to be populated with real values
- Nutrition module needs comprehensive testing
- Meal form needs improvement for better food item selection
- The UX for adding multiple food items to a meal could be more intuitive
- Some components need additional error handling
- No barcode scanning functionality implementation yet (placeholder only)
- Social module not yet implemented
- Need to improve mobile responsiveness across components

## 15. Frontend Development Status

### Authentication Module
- ✅ User registration
- ✅ User login
- ✅ Password reset functionality
- ✅ Profile management
- ✅ Protected route handling

### Recipe Module
- ✅ Recipe listing
- ✅ Recipe detail view
- ✅ Recipe creation/editing
- ✅ Recipe import from URLs
- ✅ Recipe search and filtering

### Nutrition Module
- ✅ Food item management (create, view, edit, delete)
- ✅ USDA food search and import
- ✅ Meal logging (create, view, edit, delete)
- ✅ Nutrition dashboard with statistics
- ✅ Food item favoriting
- ✅ Barcode scanning placeholder (UI only)

### Social Module (Planned)
- ⏳ User feed
- ⏳ Post creation
- ⏳ Post interaction (comments, likes)
- ⏳ Following/follower management
- ⏳ Meal and recipe sharing
- ⏳ Profile viewing

### UI/UX Status
- ✅ Basic responsive layouts
- ✅ Form handling and validation
- ✅ Error messaging
- ✅ Loading indicators
- ⏳ Polish for mobile devices
- ⏳ Advanced animations and transitions
- ⏳ Performance optimizations

---

This document represents the current state of the Fitness & Food App project as of May 11, 2025. It will be updated regularly as development progresses.