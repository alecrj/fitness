# Fitness & Food App

A comprehensive Flask and Firebase-based application for nutrition tracking, recipe management, and social fitness community.

## Features

- **User Authentication**: Secure user registration and authentication via Firebase
- **Recipe Management**: Import, create, and share recipes
- **Nutrition Tracking**: Track daily nutrition intake with USDA database integration
- **Social Features**: Share progress, follow friends, and engage with the community

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: Firebase Firestore
- **Storage**: Firebase Storage
- **Authentication**: Firebase Authentication
- **API Integration**: USDA Food Data Central API
- **Recipe Scraping**: recipe-scrapers library

## Project Structure

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

## Setup Instructions

### Prerequisites

- Python 3.8+
- Firebase account with Firestore and Storage enabled
- USDA API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fitness-food-app.git
   cd fitness-food-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your Firebase credentials and USDA API key.

5. Run the application:
   ```
   python app.py
   ```

## API Documentation

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

### Nutrition Endpoints

- `POST /api/nutrition/foods`: Create food item
- `GET /api/nutrition/foods`: Get food items
- `GET /api/nutrition/foods/search`: Search food database
- `POST /api/nutrition/meals`: Create meal log
- `GET /api/nutrition/meals`: Get meal logs
- `GET /api/nutrition/stats/daily`: Get daily nutrition stats

### Social Endpoints

- `POST /api/social/posts`: Create social post
- `GET /api/social/posts`: Get social feed
- `POST /api/social/posts/{id}/like`: Like a post
- `POST /api/social/posts/{id}/comments`: Comment on a post
- `POST /api/social/users/{id}/follow`: Follow a user

## Deployment

### Using Gunicorn (Recommended for Production)

1. Install Gunicorn:
   ```
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```
   gunicorn --bind 0.0.0.0:5000 --workers 4 "app:create_app()"
   ```

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t fitness-food-app .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 fitness-food-app
   ```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- USDA Food Data Central for nutrition data
- recipe-scrapers library for recipe import functionality