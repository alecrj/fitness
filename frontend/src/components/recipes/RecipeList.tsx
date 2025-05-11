import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRecipes } from '../../contexts/RecipeContext';
import { RecipeSearchParams } from '../../types/recipe';
import RecipeCard from './RecipeCard';

/**
 * Recipe list component for displaying and filtering recipes
 */
const RecipeList: React.FC = () => {
  const navigate = useNavigate();
  const { 
    recipes, 
    totalRecipes, 
    currentPage, 
    totalPages,
    loading, 
    error, 
    fetchRecipes,
    searchRecipes
  } = useRecipes();

  // Search params state
  const [searchParams, setSearchParams] = useState<RecipeSearchParams>({
    q: '',
    limit: 12,
    offset: 0
  });

  // Load recipes on initial render
  useEffect(() => {
    fetchRecipes(searchParams.limit, searchParams.offset);
  }, [fetchRecipes, searchParams.limit, searchParams.offset]);

  // Handle pagination
  const handlePageChange = (page: number) => {
    const newOffset = (page - 1) * (searchParams.limit || 12);
    setSearchParams(prev => ({ ...prev, offset: newOffset }));
  };

  // Handle search
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    searchRecipes({ ...searchParams, offset: 0 });
  };

  // Handle search input change
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchParams(prev => ({ ...prev, q: e.target.value }));
  };

  // Navigate to recipe creation page
  const handleCreateRecipe = () => {
    navigate('/recipes/create');
  };

  // Navigate to recipe import page
  const handleImportRecipe = () => {
    navigate('/recipes/import');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-4 md:mb-0">My Recipes</h1>
        
        <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={handleCreateRecipe}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center justify-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Create Recipe
          </button>
          
          <button
            onClick={handleImportRecipe}
            className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md flex items-center justify-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Import Recipe
          </button>
        </div>
      </div>

      {/* Search and filters */}
      <div className="mb-8">
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
          <div className="flex-grow">
            <input
              type="text"
              placeholder="Search recipes..."
              value={searchParams.q || ''}
              onChange={handleSearchChange}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
          >
            Search
          </button>
          {searchParams.q && (
            <button
              type="button"
              onClick={() => {
                setSearchParams(prev => ({ ...prev, q: '', offset: 0 }));
                fetchRecipes(searchParams.limit, 0);
              }}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md"
            >
              Clear
            </button>
          )}
        </form>
      </div>

      {/* Loading and error states */}
      {loading && <div className="text-center py-8">Loading recipes...</div>}
      {error && <div className="text-center text-red-600 py-8">{error}</div>}
      {!loading && !error && recipes.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">You don't have any recipes yet.</p>
          <div className="flex flex-col sm:flex-row justify-center gap-3">
            <button
              onClick={handleCreateRecipe}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
            >
              Create Your First Recipe
            </button>
            <button
              onClick={handleImportRecipe}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
            >
              Import a Recipe
            </button>
          </div>
        </div>
      )}

      {/* Recipe grid */}
      {!loading && !error && recipes.length > 0 && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {recipes.map((recipe) => (
              <RecipeCard
                key={recipe.id}
                recipe={recipe}
                onClick={() => navigate(`/recipes/${recipe.id}`)}
              />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center mt-8">
              <nav className="flex items-center">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage <= 1}
                  className={`mx-1 px-3 py-1 rounded-md ${
                    currentPage <= 1
                      ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                  }`}
                >
                  Previous
                </button>
                
                {[...Array(totalPages)].map((_, index) => (
                  <button
                    key={index}
                    onClick={() => handlePageChange(index + 1)}
                    className={`mx-1 px-3 py-1 rounded-md ${
                      currentPage === index + 1
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                    }`}
                  >
                    {index + 1}
                  </button>
                ))}
                
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage >= totalPages}
                  className={`mx-1 px-3 py-1 rounded-md ${
                    currentPage >= totalPages
                      ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                  }`}
                >
                  Next
                </button>
              </nav>
            </div>
          )}
          
          <div className="text-center text-gray-500 mt-4">
            Showing {Math.min((searchParams.offset || 0) + 1, totalRecipes)} to{' '}
            {Math.min((searchParams.offset || 0) + recipes.length, totalRecipes)} of {totalRecipes} recipes
          </div>
        </>
      )}
    </div>
  );
};

export default RecipeList;