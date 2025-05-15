import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useRecipes } from '../../contexts/RecipeContext';
import { Recipe } from '../../types/recipe';

/**
 * Recipe detail component for displaying a specific recipe
 */
const RecipeDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { 
    currentRecipe, 
    loading, 
    error, 
    fetchRecipe, 
    deleteRecipe,
    shareRecipe,
    unshareRecipe,
    clearRecipeState
  } = useRecipes();

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [sharingLoading, setSharingLoading] = useState(false);

  // Load recipe on component mount
  useEffect(() => {
    if (id) {
      fetchRecipe(id);
    }

    // Clear recipe state when unmounting
    return () => {
      clearRecipeState();
    };
  }, [id, fetchRecipe, clearRecipeState]);

  // Format the recipe time (prep + cook time)
  const formatTime = (recipe: Recipe): string => {
    const totalMinutes = (recipe.prepTime || 0) + (recipe.cookTime || 0);
    if (totalMinutes === 0) return 'N/A';

    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;

    if (hours === 0) return `${minutes} minutes`;
    if (minutes === 0) return `${hours} hour${hours > 1 ? 's' : ''}`;
    return `${hours} hour${hours > 1 ? 's' : ''} ${minutes} minute${minutes > 1 ? 's' : ''}`;
  };

  // Handle deleting a recipe
  const handleDelete = async () => {
    if (!id) return;
    
    try {
      await deleteRecipe(id);
      navigate('/recipes');
    } catch (err) {
      console.error('Error deleting recipe:', err);
    }
  };

  // Handle editing a recipe
  const handleEdit = () => {
    if (!id) return;
    navigate(`/recipes/edit/${id}`);
  };

  // Handle sharing/unsharing a recipe
  const handleToggleShare = async () => {
    if (!id || !currentRecipe) return;
    
    setSharingLoading(true);
    try {
      if (currentRecipe.isPublic) {
        await unshareRecipe(id);
      } else {
        await shareRecipe(id);
      }
    } catch (err) {
      console.error('Error toggling recipe share status:', err);
    } finally {
      setSharingLoading(false);
    }
  };

  // Default placeholder image if no recipe image
  const placeholderImage = 'https://via.placeholder.com/600x400?text=No+Image';

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 flex justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading recipe...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error! </strong>
          <span className="block sm:inline">{error}</span>
        </div>
        <div className="mt-4">
          <button 
            onClick={() => navigate('/recipes')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
          >
            Back to Recipes
          </button>
        </div>
      </div>
    );
  }

  if (!currentRecipe) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <p className="text-gray-600">Recipe not found</p>
          <button 
            onClick={() => navigate('/recipes')}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
          >
            Back to Recipes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Recipe header */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <h1 className="text-3xl font-bold text-gray-800">{currentRecipe.title}</h1>
          
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleEdit}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Edit
            </button>
            
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Delete
            </button>
            
            <button
              onClick={handleToggleShare}
              disabled={sharingLoading}
              className={`${
                currentRecipe.isPublic
                  ? 'bg-amber-600 hover:bg-amber-700'
                  : 'bg-green-600 hover:bg-green-700'
              } text-white px-4 py-2 rounded-md flex items-center`}
            >
              {sharingLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              ) : (
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
              )}
              {currentRecipe.isPublic ? 'Make Private' : 'Share Recipe'}
            </button>
          </div>
        </div>
        
        {currentRecipe.description && (
          <p className="text-gray-600 mb-4">{currentRecipe.description}</p>
        )}
        
        {/* Tags */}
        {currentRecipe.tags && currentRecipe.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {currentRecipe.tags.map((tag, index) => (
              <span 
                key={index}
                className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
        
        {/* Recipe meta information */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 bg-gray-100 p-4 rounded-lg">
          <div className="flex flex-col">
            <span className="text-gray-500 text-sm">Prep + Cook Time</span>
            <span className="font-semibold">{formatTime(currentRecipe)}</span>
          </div>
          
          {currentRecipe.servings && (
            <div className="flex flex-col">
              <span className="text-gray-500 text-sm">Servings</span>
              <span className="font-semibold">{currentRecipe.servings}</span>
            </div>
          )}
          
          {currentRecipe.difficulty && (
            <div className="flex flex-col">
              <span className="text-gray-500 text-sm">Difficulty</span>
              <span className="font-semibold capitalize">{currentRecipe.difficulty}</span>
            </div>
          )}
          
          {currentRecipe.cuisine && (
            <div className="flex flex-col">
              <span className="text-gray-500 text-sm">Cuisine</span>
              <span className="font-semibold capitalize">{currentRecipe.cuisine}</span>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Recipe image and nutrition */}
        <div className="md:col-span-1">
          <div className="mb-6">
            <img 
              src={currentRecipe.imageUrl || placeholderImage} 
              alt={currentRecipe.title}
              className="w-full h-auto rounded-lg shadow-md"
            />
          </div>
          
          {/* Nutrition information if available */}
          {currentRecipe.nutrition && (
            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
              <h3 className="text-xl font-semibold mb-4">Nutrition Information</h3>
              <div className="space-y-2">
                {currentRecipe.nutrition.calories !== undefined && (
                  <div className="flex justify-between border-b pb-1">
                    <span>Calories</span>
                    <span className="font-semibold">{currentRecipe.nutrition.calories}</span>
                  </div>
                )}
                {currentRecipe.nutrition.protein !== undefined && (
                  <div className="flex justify-between border-b pb-1">
                    <span>Protein</span>
                    <span className="font-semibold">{currentRecipe.nutrition.protein}g</span>
                  </div>
                )}
                {currentRecipe.nutrition.carbs !== undefined && (
                  <div className="flex justify-between border-b pb-1">
                    <span>Carbohydrates</span>
                    <span className="font-semibold">{currentRecipe.nutrition.carbs}g</span>
                  </div>
                )}
                {currentRecipe.nutrition.fat !== undefined && (
                  <div className="flex justify-between border-b pb-1">
                    <span>Fat</span>
                    <span className="font-semibold">{currentRecipe.nutrition.fat}g</span>
                  </div>
                )}
                {currentRecipe.nutrition.fiber !== undefined && (
                  <div className="flex justify-between border-b pb-1">
                    <span>Fiber</span>
                    <span className="font-semibold">{currentRecipe.nutrition.fiber}g</span>
                  </div>
                )}
                {currentRecipe.nutrition.sugar !== undefined && (
                  <div className="flex justify-between">
                    <span>Sugar</span>
                    <span className="font-semibold">{currentRecipe.nutrition.sugar}g</span>
                  </div>
                )}
              </div>
            </div>
          )}
          
          {/* Source information if imported */}
          {currentRecipe.source !== 'user' && (
            <div className="bg-white rounded-lg shadow-md p-4">
              <h3 className="text-xl font-semibold mb-2">Source</h3>
              <p className="text-gray-600 capitalize">{currentRecipe.source}</p>
              {currentRecipe.sourceUrl && (
                <a 
                  href={currentRecipe.sourceUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline block mt-1 break-all"
                >
                  {new URL(currentRecipe.sourceUrl).hostname}
                </a>
              )}
            </div>
          )}
        </div>
        
        {/* Recipe ingredients and instructions */}
        <div className="md:col-span-2 space-y-8">
          {/* Ingredients */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Ingredients</h2>
            <ul className="space-y-2">
              {currentRecipe.ingredients.map((ingredient, index) => (
                <li key={index} className="flex items-start">
                  <span className="inline-flex items-center justify-center h-6 w-6 bg-blue-100 text-blue-800 rounded-full mr-3 flex-shrink-0 mt-0.5">
                    ✓
                  </span>
                  <span>{ingredient}</span>
                </li>
              ))}
            </ul>
          </div>
          
          {/* Instructions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Instructions</h2>
            <ol className="space-y-4">
              {currentRecipe.instructions.map((instruction, index) => (
                <li key={index} className="flex">
                  <span className="inline-flex items-center justify-center h-6 w-6 bg-gray-200 text-gray-800 rounded-full mr-3 flex-shrink-0 mt-0.5">
                    {index + 1}
                  </span>
                  <span>{instruction}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </div>

      {/* Delete confirmation modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-xl font-semibold mb-4">Delete Recipe</h3>
            <p className="mb-6">Are you sure you want to delete "{currentRecipe.title}"? This action cannot be undone.</p>
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecipeDetail;