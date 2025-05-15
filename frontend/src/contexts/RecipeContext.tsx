import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { 
  Recipe, 
  RecipeListResponse, 
  RecipeSearchParams, 
  RecipeFormData,
  RecipeImportRequest 
} from '../types/recipe';
import { recipeService } from '../api/recipeService';

interface RecipeContextType {
  // State
  recipes: Recipe[];
  totalRecipes: number;
  currentPage: number;
  totalPages: number;
  loading: boolean;
  error: string | null;
  currentRecipe: Recipe | null;
  
  // Actions
  fetchRecipes: (limit?: number, offset?: number) => Promise<void>;
  fetchRecipe: (id: string) => Promise<void>;
  createRecipe: (recipeData: RecipeFormData) => Promise<Recipe>;
  updateRecipe: (id: string, recipeData: Partial<RecipeFormData>) => Promise<Recipe>;
  deleteRecipe: (id: string) => Promise<void>;
  searchRecipes: (params: RecipeSearchParams) => Promise<void>;
  importRecipe: (importData: RecipeImportRequest) => Promise<Recipe>;
  shareRecipe: (id: string) => Promise<void>;
  unshareRecipe: (id: string) => Promise<void>;
  clearRecipeState: () => void;
}

const RecipeContext = createContext<RecipeContextType | undefined>(undefined);

export const useRecipes = (): RecipeContextType => {
  const context = useContext(RecipeContext);
  if (!context) {
    throw new Error('useRecipes must be used within a RecipeProvider');
  }
  return context;
};

interface RecipeProviderProps {
  children: ReactNode;
}

export const RecipeProvider: React.FC<RecipeProviderProps> = ({ children }) => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [totalRecipes, setTotalRecipes] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [currentRecipe, setCurrentRecipe] = useState<Recipe | null>(null);

  // Fetch all recipes with pagination
  const fetchRecipes = useCallback(async (limit = 10, offset = 0) => {
    setLoading(true);
    setError(null);
    try {
      const data = await recipeService.getRecipes(limit, offset);
      setRecipes(data.recipes);
      setTotalRecipes(data.total);
      setCurrentPage(Math.floor(offset / limit) + 1);
      setTotalPages(data.totalPages);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch recipes');
      console.error('Error fetching recipes:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch a single recipe by ID
  const fetchRecipe = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await recipeService.getRecipe(id);
      setCurrentRecipe(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch recipe');
      console.error('Error fetching recipe:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Create a new recipe
  const createRecipe = useCallback(async (recipeData: RecipeFormData) => {
    setLoading(true);
    setError(null);
    try {
      const newRecipe = await recipeService.createRecipe(recipeData);
      
      // Update the recipes list if we have it loaded
      if (recipes.length > 0) {
        setRecipes(prevRecipes => [newRecipe, ...prevRecipes]);
        setTotalRecipes(prev => prev + 1);
      }
      
      return newRecipe;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to create recipe';
      setError(errorMessage);
      console.error('Error creating recipe:', err);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [recipes]);

  // Update an existing recipe
  const updateRecipe = useCallback(async (id: string, recipeData: Partial<RecipeFormData>) => {
    setLoading(true);
    setError(null);
    try {
      const updatedRecipe = await recipeService.updateRecipe(id, recipeData);
      
      // Update current recipe if it's the one we're viewing
      if (currentRecipe && currentRecipe.id === id) {
        setCurrentRecipe(updatedRecipe);
      }
      
      // Update the recipe in the list if it's there
      setRecipes(prevRecipes => 
        prevRecipes.map(recipe => 
          recipe.id === id ? updatedRecipe : recipe
        )
      );
      
      return updatedRecipe;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to update recipe';
      setError(errorMessage);
      console.error('Error updating recipe:', err);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [currentRecipe]);

  // Delete a recipe
  const deleteRecipe = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await recipeService.deleteRecipe(id);
      
      // Remove from recipes list if present
      setRecipes(prevRecipes => prevRecipes.filter(recipe => recipe.id !== id));
      setTotalRecipes(prev => prev - 1);
      
      // Clear current recipe if it's the one we're deleting
      if (currentRecipe && currentRecipe.id === id) {
        setCurrentRecipe(null);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to delete recipe');
      console.error('Error deleting recipe:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [currentRecipe]);

  // Search recipes
  const searchRecipes = useCallback(async (params: RecipeSearchParams) => {
    setLoading(true);
    setError(null);
    try {
      const data = await recipeService.searchRecipes(params);
      setRecipes(data.recipes);
      setTotalRecipes(data.total);
      setCurrentPage(data.page);
      setTotalPages(data.totalPages);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to search recipes');
      console.error('Error searching recipes:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Import a recipe
  const importRecipe = useCallback(async (importData: RecipeImportRequest) => {
    setLoading(true);
    setError(null);
    try {
      const { recipe } = await recipeService.importRecipe(importData);
      
      // Add to recipes list if we have it loaded
      if (recipes.length > 0) {
        setRecipes(prevRecipes => [recipe, ...prevRecipes]);
        setTotalRecipes(prev => prev + 1);
      }
      
      return recipe;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to import recipe';
      setError(errorMessage);
      console.error('Error importing recipe:', err);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [recipes]);

  // Share a recipe
  const shareRecipe = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await recipeService.shareRecipe(id);
      
      // Update the recipe in state
      if (currentRecipe && currentRecipe.id === id) {
        setCurrentRecipe({
          ...currentRecipe,
          isPublic: true
        });
      }
      
      setRecipes(prevRecipes => 
        prevRecipes.map(recipe => 
          recipe.id === id ? { ...recipe, isPublic: true } : recipe
        )
      );
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to share recipe');
      console.error('Error sharing recipe:', err);
    } finally {
      setLoading(false);
    }
  }, [currentRecipe]);

  // Unshare a recipe
  const unshareRecipe = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await recipeService.unshareRecipe(id);
      
      // Update the recipe in state
      if (currentRecipe && currentRecipe.id === id) {
        setCurrentRecipe({
          ...currentRecipe,
          isPublic: false
        });
      }
      
      setRecipes(prevRecipes => 
        prevRecipes.map(recipe => 
          recipe.id === id ? { ...recipe, isPublic: false } : recipe
        )
      );
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to unshare recipe');
      console.error('Error unsharing recipe:', err);
    } finally {
      setLoading(false);
    }
  }, [currentRecipe]);

  // Clear recipe state
  const clearRecipeState = useCallback(() => {
    setCurrentRecipe(null);
    setError(null);
  }, []);

  const value = {
    // State
    recipes,
    totalRecipes,
    currentPage,
    totalPages,
    loading,
    error,
    currentRecipe,
    
    // Actions
    fetchRecipes,
    fetchRecipe,
    createRecipe,
    updateRecipe,
    deleteRecipe,
    searchRecipes,
    importRecipe,
    shareRecipe,
    unshareRecipe,
    clearRecipeState
  };

  return (
    <RecipeContext.Provider value={value}>
      {children}
    </RecipeContext.Provider>
  );
};