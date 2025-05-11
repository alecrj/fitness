import React from 'react';
import { Link } from 'react-router-dom';
import { Recipe } from '../../types/recipe';

interface RecipeCardProps {
  recipe: Recipe;
  onClick?: () => void;
}

/**
 * Recipe card component for displaying recipes in a grid or list
 */
const RecipeCard: React.FC<RecipeCardProps> = ({ recipe, onClick }) => {
  // Format time in minutes to a readable format
  const formatTime = (minutes?: number): string => {
    if (!minutes) return 'N/A';
    
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours === 0) return `${mins} min`;
    if (mins === 0) return `${hours} hr`;
    return `${hours} hr ${mins} min`;
  };

  // Format date to a readable format
  const formatDate = (dateString: string | number | Date): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  // Default placeholder image if no recipe image
  const placeholderImage = 'https://via.placeholder.com/300x200?text=No+Image';

  return (
    <div 
      className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-200 hover:shadow-lg hover:-translate-y-1 hover:cursor-pointer"
      onClick={onClick}
    >
      <Link to={`/recipes/${recipe.id}`} className="block">
        <div className="relative pb-[60%]">
          <img 
            src={recipe.imageUrl || placeholderImage} 
            alt={recipe.title}
            className="absolute inset-0 w-full h-full object-cover"
          />
          {recipe.isPublic && (
            <span className="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
              Public
            </span>
          )}
        </div>
        
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-1 line-clamp-1">{recipe.title}</h3>
          
          {recipe.description && (
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">{recipe.description}</p>
          )}
          
          <div className="flex flex-wrap gap-2 mb-3">
            {recipe.tags && recipe.tags.slice(0, 3).map((tag, index) => (
              <span 
                key={index}
                className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
              >
                {tag}
              </span>
            ))}
            {recipe.tags && recipe.tags.length > 3 && (
              <span className="text-gray-500 text-xs">+{recipe.tags.length - 3} more</span>
            )}
          </div>
          
          <div className="flex justify-between text-xs text-gray-500">
            <div className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {recipe.prepTime || recipe.cookTime ? (
                <span>
                  {formatTime((recipe.prepTime || 0) + (recipe.cookTime || 0))}
                </span>
              ) : (
                <span>Time N/A</span>
              )}
            </div>
            
            <div className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{formatDate(recipe.createdAt)}</span>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default RecipeCard;