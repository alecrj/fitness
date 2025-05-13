className={`ml-3 text-sm font-medium text-gray-700 ${disabled || option.disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {option.label}
            </label>
          </div>
        ))}
      </div>
      
      {error && touched ? (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      ) : helper ? (
        <p className="mt-1 text-sm text-gray-500">{helper}</p>
      ) : null}
    </div>
  );
};

export default RadioGroup;
EOL

# Create a common form component that uses Formik
cat > frontend/src/components/common/Form.js << 'EOL'
import React from 'react';
import { Formik, Form as FormikForm } from 'formik';
import * as Yup from 'yup';

const Form = ({
  initialValues,
  validationSchema,
  onSubmit,
  children,
  className = '',
  ...props
}) => {
  return (
    <Formik
      initialValues={initialValues}
      validationSchema={Yup.object(validationSchema)}
      onSubmit={onSubmit}
      enableReinitialize
      {...props}
    >
      {(formik) => (
        <FormikForm className={className}>
          {typeof children === 'function' ? children(formik) : children}
        </FormikForm>
      )}
    </Formik>
  );
};

export default Form;
EOL

# Create a confirmation modal component
cat > frontend/src/components/common/ConfirmationModal.js << 'EOL'
import React, { Fragment, useRef } from 'react';
import { Dialog, Transition } from '@headlessui/react';

const ConfirmationModal = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  confirmButtonClass = 'bg-red-600 hover:bg-red-700',
  isLoading = false,
}) => {
  const cancelButtonRef = useRef(null);

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog
        as="div"
        className="fixed z-10 inset-0 overflow-y-auto"
        initialFocus={cancelButtonRef}
        onClose={onClose}
      >
        <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Dialog.Overlay className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
          </Transition.Child>

          {/* This element is to trick the browser into centering the modal contents. */}
          <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">
            &#8203;
          </span>
          
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enterTo="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 translate-y-0 sm:scale-100"
            leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                    <svg className="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                    <Dialog.Title as="h3" className="text-lg leading-6 font-medium text-gray-900">
                      {title}
                    </Dialog.Title>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">{message}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  className={`w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm ${confirmButtonClass}`}
                  onClick={onConfirm}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </>
                  ) : (
                    confirmLabel
                  )}
                </button>
                <button
                  type="button"
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                  onClick={onClose}
                  ref={cancelButtonRef}
                  disabled={isLoading}
                >
                  {cancelLabel}
                </button>
              </div>
            </div>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition.Root>
  );
};

export default ConfirmationModal;
EOL

# Create a README file for the components directory
mkdir -p frontend/src/components
cat > frontend/src/components/README.md << 'EOL'
# Components Directory

This directory contains all the reusable UI components for the Fitness & Food App.

## Directory Structure

- `common/` - General purpose UI components that can be used across the app
  - `Button.js` - Custom button component with various styles
  - `Card.js` - Card container with header, body, and footer
  - `Checkbox.js` - Custom checkbox input
  - `ConfirmationModal.js` - Modal for confirming actions
  - `Form.js` - Form wrapper using Formik
  - `Grid.js` - Responsive grid layout
  - `Input.js` - Text input with validation
  - `LoadingIndicator.js` - Loading spinner
  - `Logo.js` - App logo component
  - `Notification.js` - Toast notification
  - `NotificationsContainer.js` - Container for multiple notifications
  - `Pagination.js` - Pagination controls
  - `ProtectedRoute.js` - Route that requires authentication
  - `RadioGroup.js` - Radio button group
  - `Select.js` - Dropdown select input
  - `TextArea.js` - Multiline text input

- `layouts/` - Page layout components
  - `MainLayout.js` - Layout for authenticated pages
  - `AuthLayout.js` - Layout for authentication pages

- `navigation/` - Navigation components
  - `Navbar.js` - Top navigation bar
  - `Footer.js` - Page footer

- `nutrition/` - Nutrition-related components
  - `MealCard.js` - Card for displaying meal information

- `recipes/` - Recipe-related components
  - `RecipeCard.js` - Card for displaying recipe information

- `social/` - Social-related components
  - `PostCard.js` - Card for displaying social posts

## Usage Guidelines

### Form Components

Form components are designed to work with Formik for form management:

```jsx
import { Form, Input, Select, Button } from '../components/common';
import * as Yup from 'yup';

const MyForm = () => {
  const initialValues = {
    name: '',
    email: '',
    type: ''
  };
  
  const validationSchema = {
    name: Yup.string().required('Name is required'),
    email: Yup.string().email('Invalid email').required('Email is required'),
    type: Yup.string().required('Type is required')
  };
  
  const handleSubmit = (values, { setSubmitting }) => {
    // Handle form submission
    console.log(values);
    setSubmitting(false);
  };
  
  return (
    <Form
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {({ values, errors, touched, handleChange, handleBlur, isSubmitting }) => (
        <>
          <Input
            id="name"
            label="Name"
            value={values.name}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.name}
            touched={touched.name}
            required
          />
          
          <Input
            id="email"
            label="Email"
            type="email"
            value={values.email}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.email}
            touched={touched.email}
            required
          />
          
          <Select
            id="type"
            label="Type"
            value={values.type}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.type}
            touched={touched.type}
            options={[
              { value: 'type1', label: 'Type 1' },
              { value: 'type2', label: 'Type 2' }
            ]}
            required
          />
          
          <Button type="submit" disabled={isSubmitting} loading={isSubmitting}>
            Submit
          </Button>
        </>
      )}
    </Form>
  );
};
```

### Card Component

The Card component can be used to display content in a consistent style:

```jsx
import { Card } from '../components/common';

const MyCard = () => {
  return (
    <Card>
      <Card.Header>
        <Card.Title>Card Title</Card.Title>
        <Card.Subtitle>Card Subtitle</Card.Subtitle>
      </Card.Header>
      
      <Card.Body>
        <p>Card content goes here...</p>
      </Card.Body>
      
      <Card.Footer>
        <Button>Action</Button>
      </Card.Footer>
    </Card>
  );
};
```

### Layout Components

Layout components provide consistent page structure:

```jsx
import { MainLayout } from '../components/layouts';

const MyPage = () => {
  return (
    <MainLayout>
      <h1>Page Content</h1>
      <p>This content will be wrapped in the main layout with navigation.</p>
    </MainLayout>
  );
};
```
EOL

# Now create a package.json in the project root
cat > package.json << 'EOL'
{
  "name": "fitness-food-app",
  "version": "1.0.0",
  "description": "A comprehensive platform for nutrition tracking, recipe management, and social fitness community",
  "main": "app.py",
  "scripts": {
    "start": "python app.py",
    "install:backend": "pip install -r requirements.txt",
    "install:frontend": "cd frontend && npm install",
    "install:all": "npm run install:backend && npm run install:frontend",
    "start:frontend": "cd frontend && npm start",
    "build:frontend": "cd frontend && npm run build",
    "test:backend": "python run_tests.py",
    "test:frontend": "cd frontend && npm test",
    "deploy": "echo \"Deployment script would go here\" && exit 0"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/your-username/fitness-food-app.git"
  },
  "keywords": [
    "fitness",
    "nutrition",
    "recipes",
    "flask",
    "react",
    "firebase"
  ],
  "author": "",
  "license": "MIT",
  "bugs": {
    "url": "https://github.com/your-username/fitness-food-app/issues"
  },
  "homepage": "https://github.com/your-username/fitness-food-app#readme"
}
EOL

# Create a simple script to install frontend dependencies
cat > install_frontend.sh << 'EOL'
#!/bin/bash

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create empty .env.local file for development
touch .env.local

echo "Frontend dependencies installed successfully!"
echo "Please update the .env.local file in the frontend directory with your Firebase configuration."
EOL

chmod +x install_frontend.sh

echo "Frontend setup script completed successfully!"
echo "To set up the frontend, run the following commands:"
echo "1. ./frontend_setup.sh - This will create the frontend directory structure"
echo "2. ./install_frontend.sh - This will install the dependencies"
echo "3. cd frontend && npm start - This will start the development server"
EOL

# Make the script executable
chmod +x frontend_setup.sh

echo "Frontend setup script created successfully!"
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        );
      case 'snack':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        );
    }
  };

  const getMealTypeColor = (type) => {
    switch (type) {
      case 'breakfast':
        return 'bg-yellow-100 text-yellow-800';
      case 'lunch':
        return 'bg-green-100 text-green-800';
      case 'dinner':
        return 'bg-blue-100 text-blue-800';
      case 'snack':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <Card
      hover
      className="h-full flex flex-col"
      onClick={handleClick}
    >
      <div className="p-4 flex-grow flex flex-col">
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
          <span className={`flex items-center px-2 py-1 rounded text-xs font-medium ${getMealTypeColor(meal_type)}`}>
            {getMealTypeIcon(meal_type)}
            <span className="ml-1 capitalize">{meal_type}</span>
          </span>
        </div>
        
        <div className="text-sm text-gray-500 mb-4">
          {formatDate(meal_time)} at {formatTime(meal_time)}
        </div>
        
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Food Items:</h4>
          <ul className="text-sm text-gray-600">
            {food_items.slice(0, 3).map((item, index) => (
              <li key={index} className="mb-1 flex justify-between">
                <span>{item.food_item_name}</span>
                <span className="text-gray-500">{item.servings > 1 ? `${item.servings} servings` : '1 serving'}</span>
              </li>
            ))}
            {food_items.length > 3 && (
              <li className="text-primary-600">+ {food_items.length - 3} more items</li>
            )}
          </ul>
        </div>
        
        {tags && tags.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-1">
            {tags.map((tag, index) => (
              <span
                key={index}
                className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
        
        <div className="mt-auto">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Nutrition Summary:</h4>
          <div className="flex justify-between text-sm">
            <div className="text-center">
              <div className="font-medium text-gray-900">{formatCalories(nutrition_totals.calories || 0)}</div>
              <div className="text-xs text-gray-500">Calories</div>
            </div>
            <div className="text-center">
              <div className="font-medium text-gray-900">{formatNutrient(nutrition_totals.protein || 0)}</div>
              <div className="text-xs text-gray-500">Protein</div>
            </div>
            <div className="text-center">
              <div className="font-medium text-gray-900">{formatNutrient(nutrition_totals.carbs || 0)}</div>
              <div className="text-xs text-gray-500">Carbs</div>
            </div>
            <div className="text-center">
              <div className="font-medium text-gray-900">{formatNutrient(nutrition_totals.fat || 0)}</div>
              <div className="text-xs text-gray-500">Fat</div>
            </div>
          </div>
        </div>
      </div>

      <div className="px-4 py-3 bg-gray-50 rounded-b-lg">
        <Link
          to={`/nutrition/meals/${id}`}
          className="text-primary-600 hover:text-primary-800 text-sm font-medium"
          onClick={(e) => e.stopPropagation()}
        >
          View Details →
        </Link>
      </div>
    </Card>
  );
};

export default MealCard;
EOL

# Create a component for displaying social posts
mkdir -p frontend/src/components/social
cat > frontend/src/components/social/PostCard.js << 'EOL'
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Card from '../common/Card';
import { getRelativeTimeString } from '../../utils/dateUtils';
import { togglePostLike } from '../../api/social';

const PostCard = ({ post, onLikeToggle, onCommentClick }) => {
  const { currentUser } = useAuth();
  const [isLiking, setIsLiking] = useState(false);
  const [likeCount, setLikeCount] = useState(post.likes || 0);
  const [isLiked, setIsLiked] = useState(post.isLiked || false);
  
  const {
    id,
    userId,
    userName,
    userProfileImage,
    content,
    imageUrl,
    tags = [],
    recipeId,
    mealId,
    comments = 0,
    createdAt,
  } = post;

  const handleLikeToggle = async (e) => {
    e.stopPropagation();
    
    if (isLiking) return;
    
    setIsLiking(true);
    try {
      await togglePostLike(id);
      
      // Update local state
      setIsLiked(!isLiked);
      setLikeCount(prevCount => isLiked ? prevCount - 1 : prevCount + 1);
      
      // Notify parent component
      if (onLikeToggle) {
        onLikeToggle(id, !isLiked);
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    } finally {
      setIsLiking(false);
    }
  };

  const handleCommentClick = (e) => {
    e.stopPropagation();
    if (onCommentClick) {
      onCommentClick(post);
    }
  };

  return (
    <Card className="mb-4">
      <div className="flex items-center mb-4">
        <Link 
          to={`/social/users/${userId}`}
          className="flex items-center"
          onClick={(e) => e.stopPropagation()}
        >
          {userProfileImage ? (
            <img
              src={userProfileImage}
              alt={userName}
              className="w-10 h-10 rounded-full mr-3"
            />
          ) : (
            <div className="w-10 h-10 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold mr-3">
              {userName ? userName.charAt(0).toUpperCase() : '?'}
            </div>
          )}
          <div>
            <h3 className="text-sm font-medium text-gray-900">{userName}</h3>
            <p className="text-xs text-gray-500">{getRelativeTimeString(createdAt)}</p>
          </div>
        </Link>
      </div>

      <div className="mb-4">
        <p className="text-gray-700 whitespace-pre-line">{content}</p>
      </div>

      {imageUrl && (
        <div className="mb-4">
          <img
            src={imageUrl}
            alt="Post content"
            className="w-full h-auto rounded-lg"
          />
        </div>
      )}

      {tags && tags.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-1">
          {tags.map((tag, index) => (
            <Link 
              key={index}
              to={`/social/tags/${tag}`}
              className="inline-block bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded"
              onClick={(e) => e.stopPropagation()}
            >
              #{tag}
            </Link>
          ))}
        </div>
      )}

      {(recipeId || mealId) && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          {recipeId && (
            <Link 
              to={`/recipes/${recipeId}`}
              className="flex items-center text-sm text-primary-600 hover:text-primary-800"
              onClick={(e) => e.stopPropagation()}
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              View Recipe
            </Link>
          )}
          {mealId && (
            <Link 
              to={`/nutrition/meals/${mealId}`}
              className="flex items-center text-sm text-primary-600 hover:text-primary-800"
              onClick={(e) => e.stopPropagation()}
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              View Meal
            </Link>
          )}
        </div>
      )}

      <div className="flex border-t border-gray-200 pt-3">
        <button
          className={`flex items-center mr-4 text-sm font-medium ${
            isLiked ? 'text-primary-600' : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={handleLikeToggle}
          disabled={isLiking}
        >
          <svg 
            className="w-5 h-5 mr-1" 
            fill={isLiked ? 'currentColor' : 'none'} 
            stroke="currentColor" 
            viewBox="0 0 24 24" 
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          {likeCount > 0 && <span>{likeCount}</span>}
          <span className="sr-only">Like</span>
        </button>
        
        <button
          className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-700"
          onClick={handleCommentClick}
        >
          <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          {comments > 0 && <span>{comments}</span>}
          <span className="sr-only">Comment</span>
        </button>
      </div>
    </Card>
  );
};

export default PostCard;
EOL

# Create a pagination component
cat > frontend/src/components/common/Pagination.js << 'EOL'
import React from 'react';

const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  showInfo = true,
  showFirstLast = true,
  disabled = false,
}) => {
  // If there's only one page, don't show pagination
  if (totalPages <= 1) {
    return null;
  }

  // Create array of page numbers to display
  const getPageNumbers = () => {
    const pageNumbers = [];
    let startPage, endPage;

    if (totalPages <= 5) {
      // Less than 5 pages, show all
      startPage = 1;
      endPage = totalPages;
    } else {
      // More than 5 pages, calculate start and end
      if (currentPage <= 3) {
        startPage = 1;
        endPage = 5;
      } else if (currentPage + 2 >= totalPages) {
        startPage = totalPages - 4;
        endPage = totalPages;
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(i);
    }

    return pageNumbers;
  };

  const handlePageChange = (page) => {
    if (page === currentPage || page < 1 || page > totalPages || disabled) {
      return;
    }
    onPageChange(page);
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="flex flex-col items-center space-y-2 mt-4">
      {showInfo && (
        <div className="text-sm text-gray-500">
          Page {currentPage} of {totalPages}
        </div>
      )}
      
      <div className="flex space-x-1">
        {showFirstLast && (
          <button
            onClick={() => handlePageChange(1)}
            disabled={currentPage === 1 || disabled}
            className={`px-3 py-1 rounded text-sm font-medium ${
              currentPage === 1 || disabled
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            }`}
            aria-label="First Page"
          >
            <span className="sr-only">First Page</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
        )}
        
        <button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1 || disabled}
          className={`px-3 py-1 rounded text-sm font-medium ${
            currentPage === 1 || disabled
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
          }`}
          aria-label="Previous Page"
        >
          <span className="sr-only">Previous Page</span>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        {pageNumbers.map(number => (
          <button
            key={number}
            onClick={() => handlePageChange(number)}
            disabled={disabled}
            className={`px-3 py-1 rounded text-sm font-medium ${
              currentPage === number
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            }`}
            aria-label={`Page ${number}`}
            aria-current={currentPage === number ? 'page' : undefined}
          >
            {number}
          </button>
        ))}
        
        <button
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages || disabled}
          className={`px-3 py-1 rounded text-sm font-medium ${
            currentPage === totalPages || disabled
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
          }`}
          aria-label="Next Page"
        >
          <span className="sr-only">Next Page</span>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
        
        {showFirstLast && (
          <button
            onClick={() => handlePageChange(totalPages)}
            disabled={currentPage === totalPages || disabled}
            className={`px-3 py-1 rounded text-sm font-medium ${
              currentPage === totalPages || disabled
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            }`}
            aria-label="Last Page"
          >
            <span className="sr-only">Last Page</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default Pagination;
EOL

# Create a custom input component
cat > frontend/src/components/common/Input.js << 'EOL'
import React from 'react';

const Input = ({
  id,
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  error,
  touched,
  helper,
  disabled = false,
  required = false,
  className = '',
  labelClassName = '',
  inputClassName = '',
  ...props
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label htmlFor={id} className={`block text-sm font-medium text-gray-700 mb-1 ${labelClassName}`}>
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <input
        id={id}
        name={id}
        type={type}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        disabled={disabled}
        placeholder={placeholder}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
          ${error && touched ? 'border-red-500' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-white'}
          ${inputClassName}
        `}
        {...props}
      />
      
      {error && touched ? (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      ) : helper ? (
        <p className="mt-1 text-sm text-gray-500">{helper}</p>
      ) : null}
    </div>
  );
};

export default Input;
EOL

# Create a select input component
cat > frontend/src/components/common/Select.js << 'EOL'
import React from 'react';

const Select = ({
  id,
  label,
  options = [],
  value,
  onChange,
  onBlur,
  error,
  touched,
  helper,
  disabled = false,
  required = false,
  placeholder,
  className = '',
  labelClassName = '',
  selectClassName = '',
  ...props
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label htmlFor={id} className={`block text-sm font-medium text-gray-700 mb-1 ${labelClassName}`}>
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <select
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        disabled={disabled}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
          ${error && touched ? 'border-red-500' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-white'}
          ${selectClassName}
        `}
        {...props}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        
        {options.map((option) => (
          <option 
            key={option.value} 
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>
      
      {error && touched ? (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      ) : helper ? (
        <p className="mt-1 text-sm text-gray-500">{helper}</p>
      ) : null}
    </div>
  );
};

export default Select;
EOL

# Create a textarea component
cat > frontend/src/components/common/TextArea.js << 'EOL'
import React from 'react';

const TextArea = ({
  id,
  label,
  placeholder,
  value,
  onChange,
  onBlur,
  error,
  touched,
  helper,
  disabled = false,
  required = false,
  rows = 4,
  className = '',
  labelClassName = '',
  textareaClassName = '',
  ...props
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label htmlFor={id} className={`block text-sm font-medium text-gray-700 mb-1 ${labelClassName}`}>
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <textarea
        id={id}
        name={id}
        rows={rows}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        disabled={disabled}
        placeholder={placeholder}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
          ${error && touched ? 'border-red-500' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-white'}
          ${textareaClassName}
        `}
        {...props}
      />
      
      {error && touched ? (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      ) : helper ? (
        <p className="mt-1 text-sm text-gray-500">{helper}</p>
      ) : null}
    </div>
  );
};

export default TextArea;
EOL

# Create a checkbox component
cat > frontend/src/components/common/Checkbox.js << 'EOL'
import React from 'react';

const Checkbox = ({
  id,
  label,
  checked,
  onChange,
  error,
  touched,
  helper,
  disabled = false,
  required = false,
  className = '',
  labelClassName = '',
  checkboxClassName = '',
  ...props
}) => {
  return (
    <div className={`flex items-start mb-4 ${className}`}>
      <div className="flex items-center h-5">
        <input
          id={id}
          name={id}
          type="checkbox"
          checked={checked}
          onChange={onChange}
          disabled={disabled}
          className={`
            h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
            ${checkboxClassName}
          `}
          {...props}
        />
      </div>
      
      <div className="ml-3 text-sm">
        {label && (
          <label htmlFor={id} className={`font-medium text-gray-700 ${labelClassName} ${disabled ? 'opacity-50' : ''}`}>
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        
        {error && touched ? (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        ) : helper ? (
          <p className="mt-1 text-sm text-gray-500">{helper}</p>
        ) : null}
      </div>
    </div>
  );
};

export default Checkbox;
EOL

# Create a radio group component
cat > frontend/src/components/common/RadioGroup.js << 'EOL'
import React from 'react';

const RadioGroup = ({
  id,
  label,
  options = [],
  value,
  onChange,
  error,
  touched,
  helper,
  disabled = false,
  required = false,
  inline = false,
  className = '',
  labelClassName = '',
  radioClassName = '',
  ...props
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label className={`block text-sm font-medium text-gray-700 mb-2 ${labelClassName}`}>
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <div className={`space-y-2 ${inline ? 'sm:space-y-0 sm:space-x-6 sm:flex sm:items-center' : ''}`}>
        {options.map((option) => (
          <div key={option.value} className="flex items-center">
            <input
              id={`${id}-${option.value}`}
              name={id}
              type="radio"
              value={option.value}
              checked={value === option.value}
              onChange={onChange}
              disabled={disabled || option.disabled}
              className={`
                h-4 w-4 text-primary-600 border-gray-300 focus:ring-primary-500
                ${disabled || option.disabled ? 'opacity-50 cursor-not-allowed' : ''}
                ${radioClassName}
              `}
              {...props}
            />
            <label
              htmlFor={`${id}-${option.value}`}
              className={`ml-3 text-sm font-medium text-gray-700 ${disabled || option.disabled ? 'opacity-          <App />
        </AppProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
EOL

# Create a common notification component
mkdir -p frontend/src/components/common
cat > frontend/src/components/common/Notification.js << 'EOL'
import React, { useEffect, useState } from 'react';

const Notification = ({ id, type, message, onClose, autoClose = true, duration = 5000 }) => {
  const [isVisible, setIsVisible] = useState(true);
  
  useEffect(() => {
    if (autoClose) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        setTimeout(() => {
          onClose(id);
        }, 300); // Allow time for exit animation
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [autoClose, duration, id, onClose]);
  
  const getTypeStyles = () => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-500 text-green-800';
      case 'error':
        return 'bg-red-50 border-red-500 text-red-800';
      case 'warning':
        return 'bg-yellow-50 border-yellow-500 text-yellow-800';
      case 'info':
      default:
        return 'bg-blue-50 border-blue-500 text-blue-800';
    }
  };
  
  const getIcon = () => {
    switch (type) {
      case 'success':
        return (
          <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        );
      case 'warning':
        return (
          <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      case 'info':
      default:
        return (
          <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        );
    }
  };
  
  return (
    <div
      className={`transform transition-all duration-300 ease-in-out ${
        isVisible ? 'translate-y-0 opacity-100' : '-translate-y-2 opacity-0'
      }`}
    >
      <div className={`border-l-4 p-4 mb-2 rounded shadow-md ${getTypeStyles()}`}>
        <div className="flex items-start">
          <div className="flex-shrink-0 mr-3">
            {getIcon()}
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">{message}</p>
          </div>
          <div className="ml-4 flex-shrink-0">
            <button
              type="button"
              className="inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
              onClick={() => {
                setIsVisible(false);
                setTimeout(() => {
                  onClose(id);
                }, 300);
              }}
            >
              <span className="sr-only">Close</span>
              <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Notification;
EOL

# Create a notifications container component
cat > frontend/src/components/common/NotificationsContainer.js << 'EOL'
import React from 'react';
import { useApp } from '../../contexts/AppContext';
import Notification from './Notification';

const NotificationsContainer = () => {
  const { notifications, removeNotification } = useApp();
  
  if (notifications.length === 0) {
    return null;
  }
  
  return (
    <div className="fixed top-5 right-5 z-50 w-80 space-y-2">
      {notifications.map(notification => (
        <Notification
          key={notification.id}
          id={notification.id}
          type={notification.type}
          message={notification.message}
          onClose={removeNotification}
        />
      ))}
    </div>
  );
};

export default NotificationsContainer;
EOL

# Update App.js to include the NotificationsContainer
cat > frontend/src/App.js << 'EOL'
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';

// Layout components
import MainLayout from './components/layouts/MainLayout';
import AuthLayout from './components/layouts/AuthLayout';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import ProfilePage from './pages/auth/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

// Protected route wrapper
import ProtectedRoute from './components/common/ProtectedRoute';

// Common components
import NotificationsContainer from './components/common/NotificationsContainer';

function App() {
  const { loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <>
      <NotificationsContainer />
      
      <Routes>
        {/* Auth routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/profile" element={<ProfilePage />} />
            {/* Add more protected routes here */}
          </Route>
        </Route>

        {/* 404 route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
}

export default App;
EOL

# Create a basic loading indicator component
cat > frontend/src/components/common/LoadingIndicator.js << 'EOL'
import React from 'react';

const LoadingIndicator = ({ size = 'medium', fullScreen = false, message = 'Loading...' }) => {
  let sizeClass;
  switch (size) {
    case 'small':
      sizeClass = 'h-4 w-4 border-2';
      break;
    case 'large':
      sizeClass = 'h-16 w-16 border-4';
      break;
    case 'medium':
    default:
      sizeClass = 'h-8 w-8 border-2';
      break;
  }
  
  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-75 flex items-center justify-center z-50">
        <div className="text-center">
          <div className={`animate-spin rounded-full ${sizeClass} border-b-2 border-primary-600 mx-auto`}></div>
          {message && <p className="mt-2 text-gray-600">{message}</p>}
        </div>
      </div>
    );
  }
  
  return (
    <div className="flex flex-col items-center justify-center">
      <div className={`animate-spin rounded-full ${sizeClass} border-b-2 border-primary-600`}></div>
      {message && <p className="mt-2 text-gray-600 text-sm">{message}</p>}
    </div>
  );
};

export default LoadingIndicator;
EOL

# Create a basic button component
cat > frontend/src/components/common/Button.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';

const Button = ({
  children,
  type = 'button',
  variant = 'primary',
  size = 'medium',
  className = '',
  disabled = false,
  loading = false,
  to = null,
  onClick,
  ...props
}) => {
  // Base styles
  const baseStyles = 'inline-flex items-center justify-center rounded-md font-medium transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  // Variant styles
  const variantStyles = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500',
    outline: 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-primary-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
    link: 'bg-transparent text-primary-600 hover:text-primary-700 hover:underline focus:ring-primary-500',
  };
  
  // Size styles
  const sizeStyles = {
    small: 'px-2.5 py-1.5 text-xs',
    medium: 'px-4 py-2 text-sm',
    large: 'px-6 py-3 text-base',
  };
  
  // Disabled styles
  const disabledStyles = 'opacity-50 cursor-not-allowed';
  
  // Combine all styles
  const buttonStyles = `
    ${baseStyles} 
    ${variantStyles[variant] || variantStyles.primary} 
    ${sizeStyles[size] || sizeStyles.medium}
    ${disabled ? disabledStyles : ''}
    ${className}
  `;
  
  // If it's a link
  if (to) {
    return (
      <Link
        to={to}
        className={buttonStyles}
        {...props}
      >
        {children}
      </Link>
    );
  }
  
  // Regular button
  return (
    <button
      type={type}
      className={buttonStyles}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      )}
      {children}
    </button>
  );
};

export default Button;
EOL

# Create a responsive grid component
cat > frontend/src/components/common/Grid.js << 'EOL'
import React from 'react';

const Grid = ({
  children,
  columns = { default: 1, sm: 2, md: 3, lg: 4 },
  gap = { x: 4, y: 4 },
  className = '',
  ...props
}) => {
  // Process column settings
  const columnsClass = Object.entries(columns)
    .map(([breakpoint, count]) => {
      if (breakpoint === 'default') {
        return `grid-cols-${count}`;
      }
      return `${breakpoint}:grid-cols-${count}`;
    })
    .join(' ');
  
  // Process gap settings
  const gapClass = `gap-x-${gap.x} gap-y-${gap.y}`;
  
  return (
    <div
      className={`grid ${columnsClass} ${gapClass} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Grid;
EOL

# Create a card component
cat > frontend/src/components/common/Card.js << 'EOL'
import React from 'react';

const Card = ({
  children,
  className = '',
  hover = false,
  onClick,
  padding = 'normal',
  ...props
}) => {
  const paddingClass = {
    none: 'p-0',
    small: 'p-2',
    normal: 'p-4',
    large: 'p-6',
  }[padding];
  
  const hoverClass = hover
    ? 'transition-shadow duration-200 hover:shadow-lg cursor-pointer'
    : '';
  
  return (
    <div
      className={`bg-white rounded-lg shadow-md ${paddingClass} ${hoverClass} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </div>
  );
};

// Card subcomponents
Card.Header = ({ children, className = '', ...props }) => {
  return (
    <div className={`mb-4 ${className}`} {...props}>
      {children}
    </div>
  );
};

Card.Body = ({ children, className = '', ...props }) => {
  return (
    <div className={className} {...props}>
      {children}
    </div>
  );
};

Card.Footer = ({ children, className = '', ...props }) => {
  return (
    <div className={`mt-4 pt-4 border-t border-gray-200 ${className}`} {...props}>
      {children}
    </div>
  );
};

Card.Title = ({ children, className = '', ...props }) => {
  return (
    <h3 className={`text-lg font-semibold text-gray-900 ${className}`} {...props}>
      {children}
    </h3>
  );
};

Card.Subtitle = ({ children, className = '', ...props }) => {
  return (
    <h4 className={`text-sm font-medium text-gray-500 ${className}`} {...props}>
      {children}
    </h4>
  );
};

export default Card;
EOL

# Create an empty README file placeholder
cat > README.md << 'EOL'
# Fitness & Food App

A comprehensive platform for nutrition tracking, recipe management, and social fitness community.

## Getting Started

1. Clone the repository
2. Set up backend environment
3. Set up frontend environment

## Directory Structure

```
fitness-food-app/
├── app.py                  # Backend application entry point
├── config.py               # Backend configuration
├── frontend/               # Frontend React application
│   ├── public/             # Static assets
│   └── src/                # React source code
│       ├── api/            # API client and service functions
│       ├── assets/         # Static assets
│       ├── components/     # Reusable UI components
│       ├── contexts/       # React context providers
│       ├── hooks/          # Custom React hooks
│       ├── pages/          # Page components
│       └── utils/          # Utility functions
└── ... (other backend directories)
```

## Backend Setup

1. Create a virtual environment
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Firebase credentials
5. Run the backend server
   ```bash
   python app.py
   ```

## Frontend Setup

1. Navigate to the frontend directory
   ```bash
   cd frontend
   ```
2. Install dependencies
   ```bash
   npm install
   ```
3. Set up environment variables in `.env.local`
4. Start the development server
   ```bash
   npm start
   ```

## Features

- 🔐 Authentication with Firebase
- 🍽️ Recipe management and import
- 📊 Nutrition tracking with USDA database integration
- 👥 Social community features
- 📱 Responsive design for all devices

## Documentation

For more detailed documentation, see CONTINUITY.md.
EOL

# Make the script executable
chmod +x frontend_setup.sh

echo "Frontend setup script created successfully!"
EOL

# Create a README specifically for the frontend directory
cat > frontend/README.md << 'EOL'
# Fitness & Food App Frontend

This is the frontend application for the Fitness & Food App, built with React.

## Features

- User authentication and profile management
- Recipe management, import, and sharing
- Nutrition tracking and meal logging
- Social community features
- Responsive design

## Setup Instructions

1. Install dependencies
   ```bash
   npm install
   ```

2. Set up environment variables
   - Copy `.env.development.local` to `.env.local`
   - Fill in your Firebase configuration

3. Start the development server
   ```bash
   npm start
   ```

4. Build for production
   ```bash
   npm run build
   ```

## Directory Structure

```
src/
├── api/            # API client and service functions
├── assets/         # Static assets (images, styles)
├── components/     # Reusable UI components
│   ├── common/     # General purpose components
│   ├── layouts/    # Layout components
│   └── navigation/ # Navigation components
├── contexts/       # React context providers
├── hooks/          # Custom React hooks
├── pages/          # Page components
│   └── auth/       # Authentication pages
└── utils/          # Utility functions
```

## Technologies

- React
- React Router for navigation
- Firebase Authentication
- Axios for API requests
- Formik & Yup for form handling
- TailwindCSS for styling

## Development Workflow

1. Run the backend server (from the project root)
   ```bash
   python app.py
   ```

2. In a separate terminal, run the frontend dev server
   ```bash
   cd frontend
   npm start
   ```

3. The application will be available at http://localhost:3000
EOL

# Create .gitignore file
cat > frontend/.gitignore << 'EOL'
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
EOL

# Create a component for displaying recipe cards
mkdir -p frontend/src/components/recipes
cat > frontend/src/components/recipes/RecipeCard.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../common/Card';
import { formatDate } from '../../utils/dateUtils';

const RecipeCard = ({ recipe, onClick }) => {
  const {
    id,
    title,
    description,
    imageUrl,
    prepTime,
    cookTime,
    difficulty,
    tags = [],
    createdAt,
    isPublic,
  } = recipe;

  const handleClick = () => {
    if (onClick) {
      onClick(recipe);
    }
  };

  return (
    <Card
      hover
      className="h-full flex flex-col"
      onClick={handleClick}
    >
      <div className="relative">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-48 object-cover rounded-t-lg"
          />
        ) : (
          <div className="w-full h-48 bg-gray-200 rounded-t-lg flex items-center justify-center">
            <svg
              className="w-12 h-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>
        )}
        
        {isPublic && (
          <div className="absolute top-2 right-2 bg-primary-500 text-white text-xs font-bold px-2 py-1 rounded">
            Public
          </div>
        )}
      </div>

      <div className="p-4 flex-grow flex flex-col">
        <h3 className="text-lg font-semibold mb-1 text-gray-900">{title}</h3>
        
        {description && (
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">{description}</p>
        )}
        
        <div className="flex items-center text-xs text-gray-500 mb-3">
          {prepTime && (
            <div className="flex items-center mr-3">
              <svg
                className="w-3 h-3 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>Prep: {prepTime} min</span>
            </div>
          )}
          
          {cookTime && (
            <div className="flex items-center">
              <svg
                className="w-3 h-3 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>Cook: {cookTime} min</span>
            </div>
          )}
        </div>
        
        {difficulty && (
          <div className="mb-3">
            <span className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
              {difficulty}
            </span>
          </div>
        )}
        
        {tags && tags.length > 0 && (
          <div className="mb-3 flex flex-wrap gap-1">
            {tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="inline-block bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded"
              >
                {tag}
              </span>
            ))}
            {tags.length > 3 && (
              <span className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                +{tags.length - 3} more
              </span>
            )}
          </div>
        )}
        
        <div className="mt-auto pt-2 text-xs text-gray-500">
          Added {formatDate(createdAt)}
        </div>
      </div>

      <div className="px-4 py-3 bg-gray-50 rounded-b-lg">
        <Link
          to={`/recipes/${id}`}
          className="text-primary-600 hover:text-primary-800 text-sm font-medium"
          onClick={(e) => e.stopPropagation()}
        >
          View Recipe →
        </Link>
      </div>
    </Card>
  );
};

export default RecipeCard;
EOL

# Create a component for displaying meal cards
mkdir -p frontend/src/components/nutrition
cat > frontend/src/components/nutrition/MealCard.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../common/Card';
import { formatDate, formatTime } from '../../utils/dateUtils';
import { formatCalories, formatNutrient } from '../../utils/numberUtils';

const MealCard = ({ meal, onClick }) => {
  const {
    id,
    name,
    meal_type,
    meal_time,
    food_items = [],
    nutrition_totals = {},
    tags = [],
  } = meal;

  const handleClick = () => {
    if (onClick) {
      onClick(meal);
    }
  };

  const getMealTypeIcon = (type) => {
    switch (type) {
      case 'breakfast':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        );
      case 'lunch':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        );
      case 'dinner':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018    return response.data;
  } catch (error) {
    console.error(`Error deleting comment ${id}:`, error);
    throw error;
  }
};

/**
 * Follow or unfollow a user
 * @param {string} userId - User ID to follow/unfollow
 * @returns {Promise} - Follow status response
 */
export const toggleFollowUser = async (userId) => {
  try {
    const response = await api.post(`/api/social/users/${userId}/follow`);
    return response.data;
  } catch (error) {
    console.error(`Error toggling follow for user ${userId}:`, error);
    throw error;
  }
};

/**
 * Get followers for a user
 * @param {string} userId - User ID
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of followers to return
 * @param {number} params.offset - Pagination offset
 * @returns {Promise} - Followers list response
 */
export const getUserFollowers = async (userId, params = { limit: 20, offset: 0 }) => {
  try {
    const response = await api.get(`/api/social/users/${userId}/followers`, { params });
    return response.data;
  } catch (error) {
    console.error(`Error fetching followers for user ${userId}:`, error);
    throw error;
  }
};

/**
 * Get users that a user is following
 * @param {string} userId - User ID
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of following to return
 * @param {number} params.offset - Pagination offset
 * @returns {Promise} - Following list response
 */
export const getUserFollowing = async (userId, params = { limit: 20, offset: 0 }) => {
  try {
    const response = await api.get(`/api/social/users/${userId}/following`, { params });
    return response.data;
  } catch (error) {
    console.error(`Error fetching following for user ${userId}:`, error);
    throw error;
  }
};

/**
 * Get current user's liked posts
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of posts to return
 * @param {number} params.offset - Pagination offset
 * @returns {Promise} - Liked posts response
 */
export const getLikedPosts = async (params = { limit: 10, offset: 0 }) => {
  try {
    const response = await api.get('/api/social/users/me/likes', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching liked posts:', error);
    throw error;
  }
};

/**
 * Check follow status between current user and another user
 * @param {string} userId - User ID to check
 * @returns {Promise} - Follow status response
 */
export const checkFollowStatus = async (userId) => {
  try {
    const response = await api.get(`/api/social/users/${userId}/follow-status`);
    return response.data;
  } catch (error) {
    console.error(`Error checking follow status for user ${userId}:`, error);
    throw error;
  }
};

/**
 * Get trending tags
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of tags to return
 * @returns {Promise} - Trending tags response
 */
export const getTrendingTags = async (params = { limit: 10 }) => {
  try {
    const response = await api.get('/api/social/trending/tags', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching trending tags:', error);
    throw error;
  }
};

export default {
  createPost,
  getPosts,
  getPostById,
  updatePost,
  deletePost,
  togglePostLike,
  createComment,
  getPostComments,
  deleteComment,
  toggleFollowUser,
  getUserFollowers,
  getUserFollowing,
  getLikedPosts,
  checkFollowStatus,
  getTrendingTags
};
EOL

# Create a custom hook for fetching data
mkdir -p frontend/src/hooks
cat > frontend/src/hooks/useFetch.js << 'EOL'
import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for handling data fetching with loading, error, and pagination state
 * @param {Function} fetchFunction - API function to fetch data
 * @param {Object} [initialParams={}] - Initial parameters for the fetch function
 * @param {boolean} [fetchOnMount=true] - Whether to fetch data on component mount
 * @returns {Object} - Fetch state and handlers
 */
const useFetch = (fetchFunction, initialParams = {}, fetchOnMount = true) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [params, setParams] = useState(initialParams);
  
  // For pagination
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(initialParams.limit || 10);
  
  /**
   * Execute the fetch operation with updated params
   */
  const fetchData = useCallback(async (overrideParams = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const fetchParams = overrideParams || params;
      const result = await fetchFunction(fetchParams);
      
      // Handle common pagination response formats
      if (result.items && Array.isArray(result.items)) {
        setData(result.items);
        setHasMore(result.items.length === pageSize && result.hasMore !== false);
      } else if (Array.isArray(result)) {
        setData(result);
        setHasMore(result.length === pageSize);
      } else {
        setData(result);
      }
    } catch (err) {
      setError(err.message || 'An error occurred while fetching data');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, params, pageSize]);
  
  // Fetch on mount if enabled
  useEffect(() => {
    if (fetchOnMount) {
      fetchData();
    }
  }, [fetchOnMount, fetchData]);
  
  /**
   * Update fetch parameters and execute fetch
   * @param {Object} newParams - New parameters to use
   */
  const updateParams = useCallback((newParams) => {
    const updatedParams = { ...params, ...newParams };
    setParams(updatedParams);
    fetchData(updatedParams);
  }, [params, fetchData]);
  
  /**
   * Go to next page of data
   */
  const nextPage = useCallback(() => {
    if (!loading && hasMore) {
      const nextPageIndex = page + 1;
      const nextPageParams = {
        ...params,
        offset: nextPageIndex * pageSize,
        limit: pageSize
      };
      setPage(nextPageIndex);
      updateParams(nextPageParams);
    }
  }, [loading, hasMore, page, pageSize, params, updateParams]);
  
  /**
   * Go to previous page of data
   */
  const prevPage = useCallback(() => {
    if (!loading && page > 0) {
      const prevPageIndex = page - 1;
      const prevPageParams = {
        ...params,
        offset: prevPageIndex * pageSize,
        limit: pageSize
      };
      setPage(prevPageIndex);
      updateParams(prevPageParams);
    }
  }, [loading, page, pageSize, params, updateParams]);
  
  /**
   * Refresh the current data
   */
  const refresh = useCallback(() => {
    fetchData();
  }, [fetchData]);
  
  return {
    data,
    loading,
    error,
    params,
    hasMore,
    page,
    pageSize,
    updateParams,
    nextPage,
    prevPage,
    refresh,
    setPageSize
  };
};

export default useFetch;
EOL

# Create a global context for app settings/notifications
cat > frontend/src/contexts/AppContext.js << 'EOL'
import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export function useApp() {
  return useContext(AppContext);
}

export function AppProvider({ children }) {
  // Notifications system
  const [notifications, setNotifications] = useState([]);
  
  // Theme preference
  const [darkMode, setDarkMode] = useState(false);
  
  // App-wide settings
  const [settings, setSettings] = useState({
    calorieGoal: 2000,
    proteinGoal: 150,
    carbsGoal: 200,
    fatGoal: 65,
    measurementSystem: 'metric', // or 'imperial'
    defaultMealTypes: ['breakfast', 'lunch', 'dinner', 'snack'],
  });
  
  // Add a notification
  const addNotification = (message, type = 'info', autoClose = true) => {
    const id = Date.now();
    const newNotification = {
      id,
      message,
      type, // 'info', 'success', 'warning', 'error'
      timestamp: new Date(),
    };
    
    setNotifications(prev => [newNotification, ...prev]);
    
    if (autoClose) {
      setTimeout(() => {
        removeNotification(id);
      }, 5000); // Auto-close after 5 seconds
    }
    
    return id;
  };
  
  // Remove a notification by ID
  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };
  
  // Toggle dark mode
  const toggleDarkMode = () => {
    const newValue = !darkMode;
    setDarkMode(newValue);
    localStorage.setItem('darkMode', JSON.stringify(newValue));
    
    // Apply theme class to body
    if (newValue) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  };
  
  // Update settings
  const updateSettings = (newSettings) => {
    const updatedSettings = { ...settings, ...newSettings };
    setSettings(updatedSettings);
    localStorage.setItem('appSettings', JSON.stringify(updatedSettings));
  };
  
  // Load saved preferences from localStorage on mount
  useEffect(() => {
    // Load dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode !== null) {
      const parsedDarkMode = JSON.parse(savedDarkMode);
      setDarkMode(parsedDarkMode);
      
      if (parsedDarkMode) {
        document.body.classList.add('dark');
      }
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      // Use system preference as default if available
      setDarkMode(true);
      document.body.classList.add('dark');
    }
    
    // Load app settings
    const savedSettings = localStorage.getItem('appSettings');
    if (savedSettings) {
      try {
        setSettings(JSON.parse(savedSettings));
      } catch (error) {
        console.error('Failed to parse saved settings:', error);
      }
    }
  }, []);
  
  const value = {
    // Notifications
    notifications,
    addNotification,
    removeNotification,
    
    // Theme
    darkMode,
    toggleDarkMode,
    
    // Settings
    settings,
    updateSettings,
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}
EOL

# Create a utility file for date formatting
mkdir -p frontend/src/utils
cat > frontend/src/utils/dateUtils.js << 'EOL'
/**
 * Format a date to YYYY-MM-DD string
 * @param {Date} date - Date to format
 * @returns {string} - Formatted date string
 */
export const formatDateYYYYMMDD = (date) => {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

/**
 * Format a date to a readable string
 * @param {Date|string} date - Date to format
 * @param {Object} options - Intl.DateTimeFormat options
 * @returns {string} - Formatted date string
 */
export const formatDate = (date, options = {}) => {
  const d = new Date(date);
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  };
  
  return new Intl.DateTimeFormat('en-US', { ...defaultOptions, ...options }).format(d);
};

/**
 * Format a time string
 * @param {Date|string} date - Date to format
 * @returns {string} - Formatted time string
 */
export const formatTime = (date) => {
  const d = new Date(date);
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(d);
};

/**
 * Format a datetime string
 * @param {Date|string} date - Date to format
 * @returns {string} - Formatted datetime string
 */
export const formatDateTime = (date) => {
  const d = new Date(date);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(d);
};

/**
 * Return the relative time string (e.g., "2 hours ago")
 * @param {Date|string} date - Date to format
 * @returns {string} - Relative time string
 */
export const getRelativeTimeString = (date) => {
  const d = new Date(date);
  const now = new Date();
  const diffMs = now - d;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  const diffMonth = Math.floor(diffDay / 30);
  const diffYear = Math.floor(diffDay / 365);
  
  if (diffSec < 60) {
    return 'just now';
  } else if (diffMin < 60) {
    return `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`;
  } else if (diffHour < 24) {
    return `${diffHour} hour${diffHour !== 1 ? 's' : ''} ago`;
  } else if (diffDay < 30) {
    return `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`;
  } else if (diffMonth < 12) {
    return `${diffMonth} month${diffMonth !== 1 ? 's' : ''} ago`;
  } else {
    return `${diffYear} year${diffYear !== 1 ? 's' : ''} ago`;
  }
};

/**
 * Get start and end dates for a week containing the given date
 * @param {Date} date - Date within the desired week
 * @returns {Object} - { startDate, endDate }
 */
export const getWeekDateRange = (date = new Date()) => {
  const d = new Date(date);
  const day = d.getDay(); // 0 = Sunday, 6 = Saturday
  
  // Calculate start date (Sunday)
  const startDate = new Date(d);
  startDate.setDate(d.getDate() - day);
  
  // Calculate end date (Saturday)
  const endDate = new Date(startDate);
  endDate.setDate(startDate.getDate() + 6);
  
  return {
    startDate,
    endDate,
  };
};

/**
 * Get start and end dates for the current month
 * @param {Date} date - Date within the desired month
 * @returns {Object} - { startDate, endDate }
 */
export const getMonthDateRange = (date = new Date()) => {
  const d = new Date(date);
  
  // First day of the month
  const startDate = new Date(d.getFullYear(), d.getMonth(), 1);
  
  // Last day of the month
  const endDate = new Date(d.getFullYear(), d.getMonth() + 1, 0);
  
  return {
    startDate,
    endDate,
  };
};

/**
 * Check if two dates are on the same day
 * @param {Date} date1 - First date
 * @param {Date} date2 - Second date
 * @returns {boolean} - True if dates are on the same day
 */
export const isSameDay = (date1, date2) => {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  
  return (
    d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate()
  );
};

/**
 * Add days to a date
 * @param {Date} date - Base date
 * @param {number} days - Number of days to add
 * @returns {Date} - New date
 */
export const addDays = (date, days) => {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
};

/**
 * Subtract days from a date
 * @param {Date} date - Base date
 * @param {number} days - Number of days to subtract
 * @returns {Date} - New date
 */
export const subtractDays = (date, days) => {
  const d = new Date(date);
  d.setDate(d.getDate() - days);
  return d;
};
EOL

# Create some utility functions for formatting numbers
cat > frontend/src/utils/numberUtils.js << 'EOL'
/**
 * Format a number with commas as thousands separators
 * @param {number} num - Number to format
 * @returns {string} - Formatted number string
 */
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

/**
 * Round a number to the specified number of decimal places
 * @param {number} num - Number to round
 * @param {number} decimals - Number of decimal places
 * @returns {number} - Rounded number
 */
export const roundToDecimal = (num, decimals = 1) => {
  return Math.round(num * 10 ** decimals) / 10 ** decimals;
};

/**
 * Format a calorie value
 * @param {number} calories - Calorie value
 * @returns {string} - Formatted calorie string
 */
export const formatCalories = (calories) => {
  return `${Math.round(calories)} cal`;
};

/**
 * Format a macro nutrient value (e.g., protein, carbs, fat)
 * @param {number} value - Nutrient value
 * @param {string} unit - Unit of measurement (default: g)
 * @returns {string} - Formatted nutrient string
 */
export const formatNutrient = (value, unit = 'g') => {
  return `${roundToDecimal(value, 1)}${unit}`;
};

/**
 * Calculate the percentage of a value against a total
 * @param {number} value - Value to calculate percentage for
 * @param {number} total - Total value
 * @returns {number} - Percentage value
 */
export const calculatePercentage = (value, total) => {
  if (total === 0) return 0;
  return (value / total) * 100;
};

/**
 * Format a percentage value
 * @param {number} value - Percentage value
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted percentage string
 */
export const formatPercentage = (value, decimals = 0) => {
  return `${roundToDecimal(value, decimals)}%`;
};

/**
 * Format a weight value with appropriate units
 * @param {number} weight - Weight value
 * @param {string} unit - Unit of measurement (g, kg, oz, lb)
 * @returns {string} - Formatted weight string
 */
export const formatWeight = (weight, unit = 'g') => {
  if (unit === 'g' && weight >= 1000) {
    return `${roundToDecimal(weight / 1000, 2)} kg`;
  } else if (unit === 'oz' && weight >= 16) {
    return `${roundToDecimal(weight / 16, 2)} lb`;
  } else {
    return `${roundToDecimal(weight, 1)} ${unit}`;
  }
};

/**
 * Convert between weight units
 * @param {number} value - Weight value
 * @param {string} fromUnit - Original unit
 * @param {string} toUnit - Target unit
 * @returns {number} - Converted weight
 */
export const convertWeight = (value, fromUnit, toUnit) => {
  // Convert to grams first
  let grams;
  switch (fromUnit) {
    case 'g':
      grams = value;
      break;
    case 'kg':
      grams = value * 1000;
      break;
    case 'oz':
      grams = value * 28.3495;
      break;
    case 'lb':
      grams = value * 453.592;
      break;
    default:
      throw new Error(`Unknown unit: ${fromUnit}`);
  }
  
  // Convert from grams to target unit
  switch (toUnit) {
    case 'g':
      return grams;
    case 'kg':
      return grams / 1000;
    case 'oz':
      return grams / 28.3495;
    case 'lb':
      return grams / 453.592;
    default:
      throw new Error(`Unknown unit: ${toUnit}`);
  }
};
EOL

# Add a utility file for form validation
cat > frontend/src/utils/validationUtils.js << 'EOL'
/**
 * Check if a string is a valid email address
 * @param {string} email - Email address to validate
 * @returns {boolean} - True if email is valid
 */
export const isValidEmail = (email) => {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

/**
 * Check if a string is not empty
 * @param {string} value - String to check
 * @returns {boolean} - True if string is not empty
 */
export const isNotEmpty = (value) => {
  return value !== null && value !== undefined && value.trim() !== '';
};

/**
 * Check if a value is a valid number
 * @param {any} value - Value to check
 * @returns {boolean} - True if value is a valid number
 */
export const isValidNumber = (value) => {
  return !isNaN(parseFloat(value)) && isFinite(value);
};

/**
 * Check if a value is a positive number
 * @param {any} value - Value to check
 * @returns {boolean} - True if value is a positive number
 */
export const isPositiveNumber = (value) => {
  return isValidNumber(value) && parseFloat(value) > 0;
};

/**
 * Check if a value is a non-negative number
 * @param {any} value - Value to check
 * @returns {boolean} - True if value is a non-negative number
 */
export const isNonNegativeNumber = (value) => {
  return isValidNumber(value) && parseFloat(value) >= 0;
};

/**
 * Check if a value is within a range
 * @param {number} value - Value to check
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {boolean} - True if value is within range
 */
export const isInRange = (value, min, max) => {
  return isValidNumber(value) && parseFloat(value) >= min && parseFloat(value) <= max;
};

/**
 * Check if a value is a valid URL
 * @param {string} url - URL to validate
 * @returns {boolean} - True if URL is valid
 */
export const isValidUrl = (url) => {
  try {
    new URL(url);
    return true;
  } catch (e) {
    return false;
  }
};

/**
 * Check if a password meets minimum requirements
 * @param {string} password - Password to validate
 * @param {Object} options - Validation options
 * @param {number} options.minLength - Minimum length
 * @param {boolean} options.requireLetters - Require at least one letter
 * @param {boolean} options.requireNumbers - Require at least one number
 * @param {boolean} options.requireSpecialChars - Require at least one special character
 * @returns {boolean} - True if password meets requirements
 */
export const isValidPassword = (password, options = {}) => {
  const defaults = {
    minLength: 6,
    requireLetters: true,
    requireNumbers: true,
    requireSpecialChars: false
  };
  
  const config = { ...defaults, ...options };
  
  if (typeof password !== 'string') return false;
  if (password.length < config.minLength) return false;
  
  if (config.requireLetters && !/[a-zA-Z]/.test(password)) return false;
  if (config.requireNumbers && !/[0-9]/.test(password)) return false;
  if (config.requireSpecialChars && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) return false;
  
  return true;
};

/**
 * Generate validation error messages
 * @param {Object} values - Form values
 * @param {Object} rules - Validation rules
 * @returns {Object} - Error messages keyed by field name
 */
export const validateForm = (values, rules) => {
  const errors = {};
  
  Object.keys(rules).forEach(field => {
    const fieldRules = rules[field];
    const value = values[field];
    
    // Check required
    if (fieldRules.required && !isNotEmpty(value)) {
      errors[field] = fieldRules.requiredMessage || 'This field is required';
      return;
    }
    
    // Skip other validations if empty and not required
    if (!isNotEmpty(value) && !fieldRules.required) {
      return;
    }
    
    // Check email
    if (fieldRules.email && !isValidEmail(value)) {
      errors[field] = fieldRules.emailMessage || 'Please enter a valid email address';
      return;
    }
    
    // Check number
    if (fieldRules.isNumber && !isValidNumber(value)) {
      errors[field] = fieldRules.numberMessage || 'Please enter a valid number';
      return;
    }
    
    // Check positive number
    if (fieldRules.isPositive && !isPositiveNumber(value)) {
      errors[field] = fieldRules.positiveMessage || 'Please enter a positive number';
      return;
    }
    
    // Check min length
    if (fieldRules.minLength && value.length < fieldRules.minLength) {
      errors[field] = fieldRules.minLengthMessage || `Must be at least ${fieldRules.minLength} characters`;
      return;
    }
    
    // Check max length
    if (fieldRules.maxLength && value.length > fieldRules.maxLength) {
      errors[field] = fieldRules.maxLengthMessage || `Must be no more than ${fieldRules.maxLength} characters`;
      return;
    }
    
    // Check custom validation
    if (fieldRules.validate && typeof fieldRules.validate === 'function') {
      const customError = fieldRules.validate(value, values);
      if (customError) {
        errors[field] = customError;
        return;
      }
    }
  });
  
  return errors;
};
EOL

# Create API module for auth
mkdir -p frontend/src/api/auth
cat > frontend/src/api/auth/index.js << 'EOL'
import api from '../client';

/**
 * Auth API service functions for interacting with the backend
 */

/**
 * Get user profile
 * @returns {Promise} - User profile response
 */
export const getUserProfile = async () => {
  try {
    const response = await api.get('/api/auth/profile');
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

/**
 * Create or update user profile
 * @param {Object} profileData - Profile data to update
 * @param {string} profileData.name - User's name
 * @param {string} [profileData.profile_image_base64] - Base64 encoded profile image
 * @returns {Promise} - Updated profile response
 */
export const updateUserProfile = async (profileData) => {
  try {
    const response = await api.post('/api/auth/profile', profileData);
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

export default {
  getUserProfile,
  updateUserProfile
};
EOL

# Update the index.js to include the AppProvider
cat > frontend/src/index.js << 'EOL'
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './assets/styles/index.css';
import App from './App';
import { AuthProvider } from './contexts/AuthContext';
import { AppProvider } from './contexts/AppContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <AppProvider>
          <App />
        </AppProvider>
      </AuthProvider>#!/bin/bash

# Script to set up the React frontend for the Fitness & Food App
# This script creates the necessary folder structure and base files

# Create frontend directory if it doesn't exist
mkdir -p frontend/src/components
mkdir -p frontend/src/pages
mkdir -p frontend/src/api
mkdir -p frontend/src/contexts
mkdir -p frontend/src/hooks
mkdir -p frontend/src/utils
mkdir -p frontend/src/assets/images
mkdir -p frontend/src/assets/styles
mkdir -p frontend/public

# Create package.json file
cat > frontend/package.json << 'EOL'
{
  "name": "fitness-food-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.6.2",
    "firebase": "^10.7.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4",
    "formik": "^2.4.5",
    "yup": "^1.3.2",
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:5000"
}
EOL

# Create tailwind.config.js
cat > frontend/tailwind.config.js << 'EOL'
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        secondary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
EOL

# Create postcss.config.js
cat > frontend/postcss.config.js << 'EOL'
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOL

# Create main index.js file
cat > frontend/src/index.js << 'EOL'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './assets/styles/index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
EOL

# Create App.js
cat > frontend/src/App.js << 'EOL'
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';

// Layout components
import MainLayout from './components/layouts/MainLayout';
import AuthLayout from './components/layouts/AuthLayout';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import ProfilePage from './pages/auth/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

// Protected route wrapper
import ProtectedRoute from './components/common/ProtectedRoute';

function App() {
  const { loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <Routes>
      {/* Auth routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Protected routes */}
      <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<ProfilePage />} />
          {/* Add more protected routes here */}
        </Route>
      </Route>

      {/* 404 route */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default App;
EOL

# Create index.css for Tailwind
cat > frontend/src/assets/styles/index.css << 'EOL'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-all duration-200;
  }
  
  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800;
  }
  
  .btn-secondary {
    @apply bg-secondary-600 text-white hover:bg-secondary-700 active:bg-secondary-800;
  }
  
  .btn-outline {
    @apply border border-gray-300 hover:bg-gray-100 active:bg-gray-200;
  }
  
  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
EOL

# Create AuthContext
cat > frontend/src/contexts/AuthContext.js << 'EOL'
import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  updateProfile,
  sendPasswordResetEmail
} from 'firebase/auth';
import { initializeApp } from 'firebase/app';
import api from '../api/client';

// Firebase configuration
// This should be replaced with your actual Firebase config
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Sign up with email and password
  async function signup(email, password, name) {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(userCredential.user, { displayName: name });
      return userCredential.user;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }

  // Login with email and password
  async function login(email, password) {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      return userCredential.user;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }

  // Logout
  async function logout() {
    try {
      await signOut(auth);
      setUserProfile(null);
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }

  // Reset password
  async function resetPassword(email) {
    try {
      await sendPasswordResetEmail(auth, email);
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }

  // Fetch user profile from backend
  async function fetchUserProfile() {
    if (!currentUser) return;
    
    try {
      const token = await currentUser.getIdToken();
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const response = await api.get('/api/auth/profile');
      setUserProfile(response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching user profile:", error);
      setError(error.message);
    }
  }

  // Update user profile
  async function updateUserProfile(profileData) {
    if (!currentUser) return;
    
    try {
      const token = await currentUser.getIdToken();
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const response = await api.post('/api/auth/profile', profileData);
      setUserProfile(response.data);
      return response.data;
    } catch (error) {
      console.error("Error updating user profile:", error);
      setError(error.message);
      throw error;
    }
  }

  // Listen for auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      setCurrentUser(user);
      if (user) {
        await fetchUserProfile();
      }
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    userProfile,
    loading,
    error,
    signup,
    login,
    logout,
    resetPassword,
    fetchUserProfile,
    updateUserProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
EOL

# Create API client
cat > frontend/src/api/client.js << 'EOL'
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
api.interceptors.request.use(
  async (config) => {
    // Get the current token from local storage or another source
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If the error is due to an expired token and we haven't already tried to refresh
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Here you would normally refresh the token
        // For Firebase, you would get a new token from the current user
        // This is placeholder code - implement actual token refresh here
        const auth = window.firebaseAuth;
        if (auth.currentUser) {
          const newToken = await auth.currentUser.getIdToken(true);
          localStorage.setItem('authToken', newToken);
          api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
EOL

# Create ProtectedRoute component
cat > frontend/src/components/common/ProtectedRoute.js << 'EOL'
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute = () => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return currentUser ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
EOL

# Create layout components
mkdir -p frontend/src/components/layouts

# MainLayout component
cat > frontend/src/components/layouts/MainLayout.js << 'EOL'
import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../navigation/Navbar';
import Footer from '../navigation/Footer';

const MainLayout = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;
EOL

# AuthLayout component
cat > frontend/src/components/layouts/AuthLayout.js << 'EOL'
import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Logo from '../common/Logo';

const AuthLayout = () => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (currentUser) {
    return <Navigate to="/" />;
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <div className="w-full max-w-md m-auto">
        <div className="flex justify-center mb-8">
          <Logo />
        </div>
        <div className="bg-white p-8 rounded-lg shadow-md">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
EOL

# Create navigation components
mkdir -p frontend/src/components/navigation

# Navbar component
cat > frontend/src/components/navigation/Navbar.js << 'EOL'
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Logo from '../common/Logo';

const Navbar = () => {
  const { currentUser, userProfile, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Failed to log out', error);
    }
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <Logo />
            </Link>
            
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              <Link to="/" className="inline-flex items-center px-1 pt-1 border-b-2 border-primary-500 text-sm font-medium text-gray-900">
                Home
              </Link>
              <Link to="/recipes" className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                Recipes
              </Link>
              <Link to="/nutrition" className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                Nutrition
              </Link>
              <Link to="/social" className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                Community
              </Link>
            </div>
          </div>
          
          <div className="hidden md:ml-6 md:flex md:items-center">
            <div className="ml-3 relative">
              <div>
                <button 
                  type="button" 
                  className="bg-white rounded-full flex items-center text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  onClick={() => setIsMenuOpen(!isMenuOpen)}
                >
                  <span className="sr-only">Open user menu</span>
                  {userProfile && userProfile.profile_image_url ? (
                    <img
                      className="h-8 w-8 rounded-full"
                      src={userProfile.profile_image_url}
                      alt={userProfile.name || currentUser.displayName}
                    />
                  ) : (
                    <div className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center text-white">
                      {currentUser && currentUser.displayName ? currentUser.displayName.charAt(0).toUpperCase() : 'U'}
                    </div>
                  )}
                </button>
              </div>
              
              {isMenuOpen && (
                <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
                  <Link to="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    Your Profile
                  </Link>
                  <Link to="/settings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    Settings
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Sign out
                  </button>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex items-center md:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              <span className="sr-only">Open main menu</span>
              <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="pt-2 pb-3 space-y-1">
            <Link to="/" className="block pl-3 pr-4 py-2 border-l-4 border-primary-500 text-base font-medium text-primary-700 bg-primary-50">
              Home
            </Link>
            <Link to="/recipes" className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800">
              Recipes
            </Link>
            <Link to="/nutrition" className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800">
              Nutrition
            </Link>
            <Link to="/social" className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800">
              Community
            </Link>
          </div>
          
          <div className="pt-4 pb-3 border-t border-gray-200">
            <div className="flex items-center px-4">
              {userProfile && userProfile.profile_image_url ? (
                <img
                  className="h-10 w-10 rounded-full"
                  src={userProfile.profile_image_url}
                  alt={userProfile.name || currentUser.displayName}
                />
              ) : (
                <div className="h-10 w-10 rounded-full bg-primary-500 flex items-center justify-center text-white">
                  {currentUser && currentUser.displayName ? currentUser.displayName.charAt(0).toUpperCase() : 'U'}
                </div>
              )}
              <div className="ml-3">
                <div className="text-base font-medium text-gray-800">
                  {userProfile?.name?.charAt(0).toUpperCase() || currentUser?.displayName?.charAt(0).toUpperCase() || 'U'}
                    </div>
                  )}
                  <label
                    htmlFor="profile_image"
                    className="absolute bottom-0 right-0 bg-gray-800 bg-opacity-75 rounded-full p-1 cursor-pointer hover:bg-opacity-100"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </label>
                  <input
                    id="profile_image"
                    name="profile_image"
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(e) => handleImageChange(e, setFieldValue)}
                  />
                </div>
                <p className="text-sm text-gray-500">Click the camera icon to change your profile picture</p>
              </div>

              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Name
                </label>
                <Field
                  id="name"
                  name="name"
                  type="text"
                  className="mt-1 input"
                />
                <ErrorMessage name="name" component="p" className="mt-1 text-sm text-red-600" />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <div className="mt-1 input bg-gray-50">{currentUser?.email}</div>
                <p className="mt-1 text-sm text-gray-500">Email cannot be changed</p>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={isSubmitting || isLoading}
                  className="flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                >
                  {isLoading ? (
                    <span className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Updating...
                    </span>
                  ) : (
                    'Update Profile'
                  )}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>

      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Account Information</h2>
        
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-gray-500">Account Created</p>
            <p className="text-base">{currentUser?.metadata?.creationTime ? new Date(currentUser.metadata.creationTime).toLocaleDateString() : 'N/A'}</p>
          </div>
          
          <div>
            <p className="text-sm font-medium text-gray-500">Last Sign In</p>
            <p className="text-base">{currentUser?.metadata?.lastSignInTime ? new Date(currentUser.metadata.lastSignInTime).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
EOL

# Create public files
cat > frontend/public/index.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#22c55e" />
    <meta
      name="description"
      content="Fitness & Food App - Track nutrition, discover recipes, connect with health-minded individuals"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <title>Fitness & Food App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOL

cat > frontend/public/manifest.json << 'EOL'
{
  "short_name": "Fitness & Food",
  "name": "Fitness & Food App",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#22c55e",
  "background_color": "#ffffff"
}
EOL

cat > frontend/public/robots.txt << 'EOL'
# https://www.robotstxt.org/robotstxt.html
User-agent: *
Disallow:
EOL

# Create .env file for local development
cat > frontend/.env.development.local << 'EOL'
REACT_APP_API_URL=http://localhost:5000
REACT_APP_FIREBASE_API_KEY=
REACT_APP_FIREBASE_AUTH_DOMAIN=
REACT_APP_FIREBASE_PROJECT_ID=
REACT_APP_FIREBASE_STORAGE_BUCKET=
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=
REACT_APP_FIREBASE_APP_ID=
EOL

# Create environment-specific files
cat > frontend/.env.production << 'EOL'
REACT_APP_API_URL=https://api.fitness-food-app.com
EOL

# Create README file
cat > frontend/README.md << 'EOL'
# Fitness & Food App Frontend

This is the frontend application for the Fitness & Food App, built with React.

## Setup Instructions

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure environment variables:
   - Copy `.env.development.local` to `.env.local`
   - Fill in your Firebase configuration details

3. Start the development server:
   ```bash
   npm start
   ```

4. Build for production:
   ```bash
   npm run build
   ```

## Project Structure

- `src/api`: API client and service functions
- `src/assets`: Static assets like images and stylesheets
- `src/components`: Reusable UI components
- `src/contexts`: React context providers
- `src/hooks`: Custom React hooks
- `src/pages`: Page components for each route
- `src/utils`: Utility functions and helpers

## Features

- Authentication (login, register, profile management)
- Recipe management
- Nutrition tracking
- Social/community features
- Mobile-responsive design

## Technology Stack

- React
- React Router
- Firebase Authentication
- Axios for API requests
- Formik & Yup for form handling
- TailwindCSS for styling
EOL

# Make the script executable
chmod +x frontend_setup.sh

echo "Frontend setup script created successfully!"
EOL

# Create API module for recipes

mkdir -p frontend/src/api/recipes
cat > frontend/src/api/recipes/index.js << 'EOL'
import api from '../client';

/**
 * Recipe API service functions for interacting with the backend
 */

/**
 * Get user's recipes with pagination
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of recipes to return
 * @param {number} params.offset - Pagination offset
 * @returns {Promise} - Recipe list response
 */
export const getUserRecipes = async (params = { limit: 10, offset: 0 }) => {
  try {
    const response = await api.get('/api/recipes', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching recipes:', error);
    throw error;
  }
};

/**
 * Get a specific recipe by ID
 * @param {string} id - Recipe ID
 * @returns {Promise} - Recipe data response
 */
export const getRecipeById = async (id) => {
  try {
    const response = await api.get(`/api/recipes/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching recipe ${id}:`, error);
    throw error;
  }
};

/**
 * Create a new recipe
 * @param {Object} recipeData - Recipe data
 * @returns {Promise} - Created recipe response
 */
export const createRecipe = async (recipeData) => {
  try {
    const response = await api.post('/api/recipes', recipeData);
    return response.data;
  } catch (error) {
    console.error('Error creating recipe:', error);
    throw error;
  }
};

/**
 * Update an existing recipe
 * @param {string} id - Recipe ID
 * @param {Object} recipeData - Updated recipe data
 * @returns {Promise} - Updated recipe response
 */
export const updateRecipe = async (id, recipeData) => {
  try {
    const response = await api.put(`/api/recipes/${id}`, recipeData);
    return response.data;
  } catch (error) {
    console.error(`Error updating recipe ${id}:`, error);
    throw error;
  }
};

/**
 * Delete a recipe
 * @param {string} id - Recipe ID
 * @returns {Promise} - Delete response
 */
export const deleteRecipe = async (id) => {
  try {
    const response = await api.delete(`/api/recipes/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting recipe ${id}:`, error);
    throw error;
  }
};

/**
 * Import a recipe from a URL
 * @param {string} url - Recipe URL to import
 * @returns {Promise} - Imported recipe response
 */
export const importRecipe = async (url) => {
  try {
    const response = await api.post('/api/recipes/import', { url });
    return response.data;
  } catch (error) {
    console.error('Error importing recipe:', error);
    throw error;
  }
};

/**
 * Search for recipes
 * @param {Object} params - Search parameters
 * @param {string} params.q - Search query
 * @param {Array} params.tags - Recipe tags
 * @param {string} params.cuisine - Recipe cuisine
 * @param {string} params.difficulty - Recipe difficulty
 * @param {boolean} params.includePublic - Include public recipes
 * @returns {Promise} - Search results response
 */
export const searchRecipes = async (params = {}) => {
  try {
    const response = await api.get('/api/recipes/search', { params });
    return response.data;
  } catch (error) {
    console.error('Error searching recipes:', error);
    throw error;
  }
};

/**
 * Share a recipe publicly
 * @param {string} id - Recipe ID
 * @returns {Promise} - Share status response
 */
export const shareRecipe = async (id) => {
  try {
    const response = await api.post(`/api/recipes/share/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error sharing recipe ${id}:`, error);
    throw error;
  }
};

/**
 * Make a recipe private
 * @param {string} id - Recipe ID
 * @returns {Promise} - Unshare status response
 */
export const unshareRecipe = async (id) => {
  try {
    const response = await api.post(`/api/recipes/unshare/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error making recipe ${id} private:`, error);
    throw error;
  }
};

/**
 * Get supported recipe import sites
 * @returns {Promise} - Supported sites response
 */
export const getSupportedImportSites = async () => {
  try {
    const response = await api.get('/api/recipes/supported-sites');
    return response.data;
  } catch (error) {
    console.error('Error fetching supported import sites:', error);
    throw error;
  }
};

/**
 * Analyze recipe nutritional content
 * @param {Object} data - Recipe data for analysis
 * @param {Array} data.ingredients - Recipe ingredients
 * @param {number} data.servings - Recipe servings
 * @returns {Promise} - Nutritional analysis response
 */
export const analyzeRecipeNutrition = async (data) => {
  try {
    const response = await api.post('/api/recipes/nutritional-analysis', data);
    return response.data;
  } catch (error) {
    console.error('Error analyzing recipe nutrition:', error);
    throw error;
  }
};

export default {
  getUserRecipes,
  getRecipeById,
  createRecipe,
  updateRecipe,
  deleteRecipe,
  importRecipe,
  searchRecipes,
  shareRecipe,
  unshareRecipe,
  getSupportedImportSites,
  analyzeRecipeNutrition
};
EOL

# Create API module for nutrition

mkdir -p frontend/src/api/nutrition
cat > frontend/src/api/nutrition/index.js << 'EOL'
import api from '../client';

/**
 * Nutrition API service functions for interacting with the backend
 */

/**
 * Get user's food items with pagination and filtering
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of food items to return
 * @param {number} params.offset - Pagination offset
 * @param {boolean} params.is_favorite - Filter for favorite foods
 * @param {boolean} params.is_custom - Filter for custom foods
 * @param {string} params.q - Search query
 * @returns {Promise} - Food items list response
 */
export const getFoodItems = async (params = { limit: 20, offset: 0 }) => {
  try {
    const response = await api.get('/api/nutrition/foods', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching food items:', error);
    throw error;
  }
};

/**
 * Get a specific food item by ID
 * @param {string} id - Food item ID
 * @returns {Promise} - Food item data response
 */
export const getFoodItemById = async (id) => {
  try {
    const response = await api.get(`/api/nutrition/foods/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching food item ${id}:`, error);
    throw error;
  }
};

/**
 * Create a new food item
 * @param {Object} foodItemData - Food item data
 * @returns {Promise} - Created food item response
 */
export const createFoodItem = async (foodItemData) => {
  try {
    const response = await api.post('/api/nutrition/foods', foodItemData);
    return response.data;
  } catch (error) {
    console.error('Error creating food item:', error);
    throw error;
  }
};

/**
 * Update an existing food item
 * @param {string} id - Food item ID
 * @param {Object} foodItemData - Updated food item data
 * @returns {Promise} - Updated food item response
 */
export const updateFoodItem = async (id, foodItemData) => {
  try {
    const response = await api.put(`/api/nutrition/foods/${id}`, foodItemData);
    return response.data;
  } catch (error) {
    console.error(`Error updating food item ${id}:`, error);
    throw error;
  }
};

/**
 * Delete a food item
 * @param {string} id - Food item ID
 * @returns {Promise} - Delete response
 */
export const deleteFoodItem = async (id) => {
  try {
    const response = await api.delete(`/api/nutrition/foods/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting food item ${id}:`, error);
    throw error;
  }
};

/**
 * Toggle favorite status for a food item
 * @param {string} id - Food item ID
 * @returns {Promise} - Updated favorite status response
 */
export const toggleFoodFavorite = async (id) => {
  try {
    const response = await api.post(`/api/nutrition/foods/${id}/favorite`);
    return response.data;
  } catch (error) {
    console.error(`Error toggling favorite for food item ${id}:`, error);
    throw error;
  }
};

/**
 * Search USDA food database
 * @param {string} query - Search query
 * @returns {Promise} - Search results response
 */
export const searchUSDAFoods = async (query) => {
  try {
    const response = await api.get('/api/nutrition/foods/search', { params: { q: query } });
    return response.data;
  } catch (error) {
    console.error('Error searching USDA database:', error);
    throw error;
  }
};

/**
 * Get detailed information about a USDA food
 * @param {string} fdcId - USDA FDC ID
 * @returns {Promise} - Detailed food info response
 */
export const getUSDAFoodDetails = async (fdcId) => {
  try {
    const response = await api.get(`/api/nutrition/foods/details/${fdcId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching USDA food details for ${fdcId}:`, error);
    throw error;
  }
};

/**
 * Import a food from USDA database
 * @param {Object} data - Import data
 * @param {string} data.fdcId - USDA FDC ID
 * @returns {Promise} - Imported food item response
 */
export const importUSDAFood = async (data) => {
  try {
    const response = await api.post('/api/nutrition/foods/import', data);
    return response.data;
  } catch (error) {
    console.error('Error importing USDA food:', error);
    throw error;
  }
};

/**
 * Create a new meal log
 * @param {Object} mealData - Meal data
 * @returns {Promise} - Created meal response
 */
export const createMeal = async (mealData) => {
  try {
    const response = await api.post('/api/nutrition/meals', mealData);
    return response.data;
  } catch (error) {
    console.error('Error creating meal:', error);
    throw error;
  }
};

/**
 * Get user's meal logs with pagination and filtering
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of meals to return
 * @param {number} params.offset - Pagination offset
 * @param {string} params.date - Filter by date (YYYY-MM-DD)
 * @param {string} params.meal_type - Filter by meal type
 * @returns {Promise} - Meals list response
 */
export const getMeals = async (params = { limit: 10, offset: 0 }) => {
  try {
    const response = await api.get('/api/nutrition/meals', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching meals:', error);
    throw error;
  }
};

/**
 * Get a specific meal by ID
 * @param {string} id - Meal ID
 * @returns {Promise} - Meal data response
 */
export const getMealById = async (id) => {
  try {
    const response = await api.get(`/api/nutrition/meals/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching meal ${id}:`, error);
    throw error;
  }
};

/**
 * Update an existing meal
 * @param {string} id - Meal ID
 * @param {Object} mealData - Updated meal data
 * @returns {Promise} - Updated meal response
 */
export const updateMeal = async (id, mealData) => {
  try {
    const response = await api.put(`/api/nutrition/meals/${id}`, mealData);
    return response.data;
  } catch (error) {
    console.error(`Error updating meal ${id}:`, error);
    throw error;
  }
};

/**
 * Delete a meal
 * @param {string} id - Meal ID
 * @returns {Promise} - Delete response
 */
export const deleteMeal = async (id) => {
  try {
    const response = await api.delete(`/api/nutrition/meals/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting meal ${id}:`, error);
    throw error;
  }
};

/**
 * Get daily nutrition statistics
 * @param {string} date - Date string (YYYY-MM-DD)
 * @returns {Promise} - Daily stats response
 */
export const getDailyStats = async (date = new Date().toISOString().split('T')[0]) => {
  try {
    const response = await api.get('/api/nutrition/stats/daily', { params: { date } });
    return response.data;
  } catch (error) {
    console.error('Error fetching daily nutrition stats:', error);
    throw error;
  }
};

/**
 * Get weekly nutrition statistics
 * @param {string} startDate - Start date string (YYYY-MM-DD)
 * @param {string} endDate - End date string (YYYY-MM-DD)
 * @returns {Promise} - Weekly stats response
 */
export const getWeeklyStats = async (startDate, endDate) => {
  try {
    const response = await api.get('/api/nutrition/stats/weekly', { params: { start_date: startDate, end_date: endDate } });
    return response.data;
  } catch (error) {
    console.error('Error fetching weekly nutrition stats:', error);
    throw error;
  }
};

/**
 * Look up food by barcode
 * @param {string} code - Barcode
 * @returns {Promise} - Barcode lookup response
 */
export const lookupBarcode = async (code) => {
  try {
    const response = await api.get('/api/nutrition/barcode/lookup', { params: { code } });
    return response.data;
  } catch (error) {
    console.error('Error looking up barcode:', error);
    throw error;
  }
};

export default {
  getFoodItems,
  getFoodItemById,
  createFoodItem,
  updateFoodItem,
  deleteFoodItem,
  toggleFoodFavorite,
  searchUSDAFoods,
  getUSDAFoodDetails,
  importUSDAFood,
  createMeal,
  getMeals,
  getMealById,
  updateMeal,
  deleteMeal,
  getDailyStats,
  getWeeklyStats,
  lookupBarcode
};
EOL

# Create API module for social features

mkdir -p frontend/src/api/social
cat > frontend/src/api/social/index.js << 'EOL'
import api from '../client';

/**
 * Social API service functions for interacting with the backend
 */

/**
 * Create a new social post
 * @param {Object} postData - Post data
 * @param {string} postData.content - Post content
 * @param {string} [postData.imageBase64] - Base64 encoded image
 * @param {Array} [postData.tags] - Post tags
 * @param {string} [postData.recipeId] - Related recipe ID
 * @param {string} [postData.mealId] - Related meal ID
 * @returns {Promise} - Created post response
 */
export const createPost = async (postData) => {
  try {
    const response = await api.post('/api/social/posts', postData);
    return response.data;
  } catch (error) {
    console.error('Error creating post:', error);
    throw error;
  }
};

/**
 * Get social feed with pagination and filtering
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of posts to return
 * @param {number} params.offset - Pagination offset
 * @param {string} [params.userId] - Filter by user ID
 * @param {string} [params.tag] - Filter by tag
 * @param {string} [params.feed] - Feed type (all, profile, following)
 * @returns {Promise} - Post feed response
 */
export const getPosts = async (params = { limit: 10, offset: 0, feed: 'all' }) => {
  try {
    const response = await api.get('/api/social/posts', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error;
  }
};

/**
 * Get a specific post by ID
 * @param {string} id - Post ID
 * @returns {Promise} - Post data response
 */
export const getPostById = async (id) => {
  try {
    const response = await api.get(`/api/social/posts/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching post ${id}:`, error);
    throw error;
  }
};

/**
 * Update an existing post
 * @param {string} id - Post ID
 * @param {Object} postData - Updated post data
 * @returns {Promise} - Updated post response
 */
export const updatePost = async (id, postData) => {
  try {
    const response = await api.put(`/api/social/posts/${id}`, postData);
    return response.data;
  } catch (error) {
    console.error(`Error updating post ${id}:`, error);
    throw error;
  }
};

/**
 * Delete a post
 * @param {string} id - Post ID
 * @returns {Promise} - Delete response
 */
export const deletePost = async (id) => {
  try {
    const response = await api.delete(`/api/social/posts/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting post ${id}:`, error);
    throw error;
  }
};

/**
 * Like or unlike a post
 * @param {string} id - Post ID
 * @returns {Promise} - Like status response
 */
export const togglePostLike = async (id) => {
  try {
    const response = await api.post(`/api/social/posts/${id}/like`);
    return response.data;
  } catch (error) {
    console.error(`Error toggling like for post ${id}:`, error);
    throw error;
  }
};

/**
 * Comment on a post
 * @param {string} postId - Post ID
 * @param {Object} commentData - Comment data
 * @param {string} commentData.content - Comment content
 * @returns {Promise} - Created comment response
 */
export const createComment = async (postId, commentData) => {
  try {
    const response = await api.post(`/api/social/posts/${postId}/comments`, commentData);
    return response.data;
  } catch (error) {
    console.error(`Error creating comment on post ${postId}:`, error);
    throw error;
  }
};

/**
 * Get comments for a post
 * @param {string} postId - Post ID
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of comments to return
 * @param {number} params.offset - Pagination offset
 * @param {string} params.sort_by - Sort field
 * @param {string} params.sort_dir - Sort direction
 * @returns {Promise} - Comments list response
 */
export const getPostComments = async (postId, params = { limit: 10, offset: 0, sort_by: 'createdAt', sort_dir: 'asc' }) => {
  try {
    const response = await api.get(`/api/social/posts/${postId}/comments`, { params });
    return response.data;
  } catch (error) {
    console.error(`Error fetching comments for post ${postId}:`, error);
    throw error;
  }
};

/**
 * Delete a comment
 * @param {string} id - Comment ID
 * @returns {Promise} - Delete response
 */
export const deleteComment = async (id) => {
  try {
    const response = await api.delete(`/api/social/comments/${id}`);
    return response.name || currentUser?.displayName}
                </div>
                <div className="text-sm font-medium text-gray-500">
                  {currentUser?.email}
                </div>
              </div>
            </div>
            <div className="mt-3 space-y-1">
              <Link to="/profile" className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                Your Profile
              </Link>
              <Link to="/settings" className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                Settings
              </Link>
              <button
                onClick={handleLogout}
                className="w-full text-left block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
EOL

# Footer component
cat > frontend/src/components/navigation/Footer.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../common/Logo';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="container mx-auto px-4 py-8">
        <div className="md:flex md:justify-between">
          <div className="mb-6 md:mb-0">
            <Link to="/" className="flex items-center">
              <Logo />
            </Link>
            <p className="mt-2 text-sm text-gray-600 max-w-xs">
              Your comprehensive platform for nutrition tracking, recipe management, and social fitness community.
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-8 sm:gap-6 sm:grid-cols-3">
            <div>
              <h3 className="mb-6 text-sm font-semibold text-gray-900 uppercase">Features</h3>
              <ul className="text-gray-600">
                <li className="mb-4">
                  <Link to="/recipes" className="hover:underline">Recipes</Link>
                </li>
                <li className="mb-4">
                  <Link to="/nutrition" className="hover:underline">Nutrition</Link>
                </li>
                <li>
                  <Link to="/social" className="hover:underline">Community</Link>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="mb-6 text-sm font-semibold text-gray-900 uppercase">Legal</h3>
              <ul className="text-gray-600">
                <li className="mb-4">
                  <Link to="/privacy-policy" className="hover:underline">Privacy Policy</Link>
                </li>
                <li>
                  <Link to="/terms-of-service" className="hover:underline">Terms of Service</Link>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="mb-6 text-sm font-semibold text-gray-900 uppercase">Company</h3>
              <ul className="text-gray-600">
                <li className="mb-4">
                  <Link to="/about" className="hover:underline">About</Link>
                </li>
                <li>
                  <Link to="/contact" className="hover:underline">Contact</Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <hr className="my-6 border-gray-200 sm:mx-auto" />
        
        <div className="sm:flex sm:items-center sm:justify-between">
          <span className="text-sm text-gray-500 sm:text-center">
            © {currentYear} Fitness & Food App. All Rights Reserved.
          </span>
          <div className="flex mt-4 space-x-6 sm:justify-center sm:mt-0">
            <a href="#" className="text-gray-500 hover:text-gray-900">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd"></path>
              </svg>
            </a>
            <a href="#" className="text-gray-500 hover:text-gray-900">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.14.046 1.94.262 2.627.552.719.3 1.33.638 1.938 1.247.61.609.948 1.22 1.247 1.938.29.688.506 1.488.552 2.627.047 1.024.06 1.379.06 3.808 0 2.43-.013 2.784-.06 3.808-.046 1.14-.262 1.94-.552 2.627-.3.719-.638 1.33-1.247 1.938-.61.61-1.22.948-1.938 1.247-.688.29-1.488.506-2.627.552-1.024.047-1.379.06-3.808.06-2.43 0-2.784-.013-3.808-.06-1.14-.046-1.94-.262-2.627-.552a5.359 5.359 0 01-1.938-1.247 5.359 5.359 0 01-1.247-1.938c-.29-.688-.506-1.488-.552-2.627-.047-1.024-.06-1.379-.06-3.808 0-2.43.013-2.784.06-3.808.046-1.14.262-1.94.552-2.627.3-.719.638-1.33 1.247-1.938.61-.61 1.22-.948 1.938-1.247.688-.29 1.488-.506 2.627-.552 1.024-.047 1.379-.06 3.808-.06M12 0C9.556 0 9.25.01 8.214.06c-1.203.05-2.023.245-2.743.525a6.916 6.916 0 00-2.55 1.64 6.916 6.916 0 00-1.64 2.55c-.28.72-.475 1.54-.525 2.744C.01 9.25 0 9.555 0 12s.01 2.75.06 3.786c.05 1.203.245 2.023.525 2.743.282.72.7 1.4 1.64 2.55a6.915 6.915 0 002.55 1.64c.72.28 1.54.475 2.743.525C9.25 23.99 9.556 24 12 24s2.75-.01 3.786-.06c1.203-.05 2.023-.245 2.743-.525a6.915 6.915 0 002.55-1.64c.94-1.15 1.358-1.83 1.64-2.55.28-.72.475-1.54.525-2.743C23.99 14.75 24 14.445 24 12s-.01-2.75-.06-3.786c-.05-1.203-.245-2.023-.525-2.743a6.916 6.916 0 00-1.64-2.55 6.916 6.916 0 00-2.55-1.64C18.023.305 17.203.11 16 .06 14.75.01 14.444 0 12 0zm0 5.838a6.162 6.162 0 100 12.323 6.162 6.162 0 000-12.323zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z" clipRule="evenodd"></path>
              </svg>
            </a>
            <a href="#" className="text-gray-500 hover:text-gray-900">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
EOL

# Create Logo component
mkdir -p frontend/src/components/common
cat > frontend/src/components/common/Logo.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';

const Logo = () => {
  return (
    <Link to="/" className="flex items-center">
      <span className="text-xl font-bold text-primary-600">Fitness</span>
      <span className="text-xl font-bold text-gray-700">&</span>
      <span className="text-xl font-bold text-secondary-600">Food</span>
    </Link>
  );
};

export default Logo;
EOL

# Create basic pages
mkdir -p frontend/src/pages
mkdir -p frontend/src/pages/auth

# Home Page
cat > frontend/src/pages/HomePage.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
  const { userProfile } = useAuth();
  const userName = userProfile?.name || 'there';

  return (
    <div className="space-y-8">
      <section className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome, {userName}!
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Track your nutrition, discover new recipes, and connect with a community of health-minded individuals.
        </p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card hover:shadow-lg transition-shadow">
          <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Recipes</h3>
          <p className="text-gray-600 mb-4">
            Discover, save, and share delicious and healthy recipes. Import recipes from your favorite websites.
          </p>
          <Link to="/recipes" className="text-primary-600 font-medium hover:text-primary-700">
            Explore Recipes →
          </Link>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="h-12 w-12 bg-secondary-100 rounded-lg flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-secondary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Nutrition</h3>
          <p className="text-gray-600 mb-4">
            Track your daily meals, calories, and macronutrients. Monitor your nutrition goals and progress.
          </p>
          <Link to="/nutrition" className="text-secondary-600 font-medium hover:text-secondary-700">
            Track Nutrition →
          </Link>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Community</h3>
          <p className="text-gray-600 mb-4">
            Connect with others, share your fitness journey, and get inspired by the community.
          </p>
          <Link to="/social" className="text-purple-600 font-medium hover:text-purple-700">
            Join Community →
          </Link>
        </div>
      </section>

      <section className="bg-gray-50 p-8 rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-4">Quick Stats</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <p className="text-gray-500 text-sm">Today's Calories</p>
            <p className="text-2xl font-bold">--</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <p className="text-gray-500 text-sm">Saved Recipes</p>
            <p className="text-2xl font-bold">--</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <p className="text-gray-500 text-sm">Meal Streak</p>
            <p className="text-2xl font-bold">--</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <p className="text-gray-500 text-sm">Community Posts</p>
            <p className="text-2xl font-bold">--</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
EOL

# Not Found Page
cat > frontend/src/pages/NotFoundPage.js << 'EOL'
import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <div>
          <h1 className="text-9xl font-extrabold text-primary-600">404</h1>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">Page not found</h2>
          <p className="mt-2 text-sm text-gray-600">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </div>
        <div className="mt-8">
          <Link
            to="/"
            className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-primary-600 hover:bg-primary-700"
          >
            Go back home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
EOL

# Login Page
cat > frontend/src/pages/auth/LoginPage.js << 'EOL'
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const LoginSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (values, { setSubmitting }) => {
    setError('');
    setIsLoading(true);
    
    try {
      await login(values.email, values.password);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Failed to log in. Please try again.');
    } finally {
      setIsLoading(false);
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">Log in to your account</h2>
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6" role="alert">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      
      <Formik
        initialValues={{ email: '', password: '' }}
        validationSchema={LoginSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors }) => (
          <Form className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email Address
              </label>
              <Field
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                className={`mt-1 input ${
                  touched.email && errors.email ? 'border-red-500' : ''
                }`}
              />
              <ErrorMessage name="email" component="p" className="mt-1 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <Field
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                className={`mt-1 input ${
                  touched.password && errors.password ? 'border-red-500' : ''
                }`}
              />
              <ErrorMessage name="password" component="p" className="mt-1 text-sm text-red-600" />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember_me"
                  name="remember_me"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="remember_me" className="ml-2 block text-sm text-gray-700">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <Link to="/forgot-password" className="font-medium text-primary-600 hover:text-primary-500">
                  Forgot your password?
                </Link>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={isSubmitting || isLoading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {isLoading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Logging in...
                  </span>
                ) : (
                  'Log in'
                )}
              </button>
            </div>
          </Form>
        )}
      </Formik>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Don't have an account?{' '}
          <Link to="/register" className="font-medium text-primary-600 hover:text-primary-500">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
EOL

# Register Page
cat > frontend/src/pages/auth/RegisterPage.js << 'EOL'
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const RegisterSchema = Yup.object().shape({
  name: Yup.string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), null], 'Passwords must match')
    .required('Confirm password is required'),
});

const RegisterPage = () => {
  const { signup, updateUserProfile } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (values, { setSubmitting }) => {
    setError('');
    setIsLoading(true);
    
    try {
      // Create user with Firebase Auth
      const user = await signup(values.email, values.password, values.name);
      
      // Create or update profile in backend
      await updateUserProfile({ name: values.name });
      
      // Redirect to home page
      navigate('/');
    } catch (err) {
      setError(err.message || 'Failed to create account. Please try again.');
    } finally {
      setIsLoading(false);
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">Create your account</h2>
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6" role="alert">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      
      <Formik
        initialValues={{ name: '', email: '', password: '', confirmPassword: '' }}
        validationSchema={RegisterSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors }) => (
          <Form className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Name
              </label>
              <Field
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                className={`mt-1 input ${
                  touched.name && errors.name ? 'border-red-500' : ''
                }`}
              />
              <ErrorMessage name="name" component="p" className="mt-1 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email Address
              </label>
              <Field
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                className={`mt-1 input ${
                  touched.email && errors.email ? 'border-red-500' : ''
                }`}
              />
              <ErrorMessage name="email" component="p" className="mt-1 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <Field
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                className={`mt-1 input ${
                  touched.password && errors.password ? 'border-red-500' : ''
                }`}
              />
              <ErrorMessage name="password" component="p" className="mt-1 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirm Password
              </label>
              <Field
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autoComplete="new-password"
                className={`mt-1 input ${
                  touched.confirmPassword && errors.confirmPassword ? 'border-red-500' : ''
                }`}
              />
              <ErrorMessage name="confirmPassword" component="p" className="mt-1 text-sm text-red-600" />
            </div>

            <div>
              <button
                type="submit"
                disabled={isSubmitting || isLoading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {isLoading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating Account...
                  </span>
                ) : (
                  'Sign Up'
                )}
              </button>
            </div>
          </Form>
        )}
      </Formik>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
EOL

# Profile Page
cat > frontend/src/pages/auth/ProfilePage.js << 'EOL'
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const ProfileSchema = Yup.object().shape({
  name: Yup.string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters'),
});

const ProfilePage = () => {
  const { currentUser, userProfile, updateUserProfile } = useAuth();
  const [successMessage, setSuccessMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  
  // Reset messages when component mounts
  useEffect(() => {
    setSuccessMessage('');
    setError('');
  }, []);

  const handleSubmit = async (values, { setSubmitting }) => {
    setSuccessMessage('');
    setError('');
    setIsLoading(true);
    
    try {
      const profileData = {
        name: values.name,
      };
      
      // If there's a new image, add it to the profile data
      if (values.profile_image_base64) {
        profileData.profile_image_base64 = values.profile_image_base64;
      }
      
      // Update profile in backend
      await updateUserProfile(profileData);
      
      setSuccessMessage('Profile updated successfully!');
    } catch (err) {
      setError(err.message || 'Failed to update profile. Please try again.');
    } finally {
      setIsLoading(false);
      setSubmitting(false);
    }
  };

  const handleImageChange = (event, setFieldValue) => {
    const file = event.currentTarget.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
        setFieldValue('profile_image_base64', reader.result.split(',')[1]);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Your Profile</h1>
      
      {successMessage && (
        <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-6" role="alert">
          <p className="text-green-700">{successMessage}</p>
        </div>
      )}
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6" role="alert">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      
      <div className="bg-white shadow-md rounded-lg p-6 mb-8">
        <Formik
          initialValues={{
            name: userProfile?.name || currentUser?.displayName || '',
            profile_image_base64: '',
          }}
          enableReinitialize
          validationSchema={ProfileSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, setFieldValue }) => (
            <Form className="space-y-6">
              <div className="flex flex-col items-center space-y-4 mb-6">
                <div className="relative">
                  {imagePreview || userProfile?.profile_image_url ? (
                    <img
                      src={imagePreview || userProfile?.profile_image_url}
                      alt="Profile"
                      className="h-24 w-24 rounded-full object-cover"
                    />
                  ) : (
                    <div className="h-24 w-24 rounded-full bg-primary-500 flex items-center justify-center text-white text-3xl font-bold">
                      {userProfile?.