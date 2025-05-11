import { useState, useCallback, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { RecipeSearchParams, RecipeDifficulty } from '../types/recipe';

interface UseRecipeFilterOptions {
  persistInUrl?: boolean;
  initialFilters?: Partial<RecipeSearchParams>;
}

/**
 * Custom hook for handling recipe filtering and search
 */
const useRecipeFilter = ({
  persistInUrl = false,
  initialFilters = {}
}: UseRecipeFilterOptions = {}) => {
  // Use URL search params if persistInUrl is true
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Initialize filter state from URL or initial filters
  const [filters, setInternalFilters] = useState<RecipeSearchParams>(() => {
    if (persistInUrl) {
      return {
        q: searchParams.get('q') || initialFilters.q || '',
        tags: searchParams.getAll('tag') || initialFilters.tags || [],
        cuisine: searchParams.get('cuisine') || initialFilters.cuisine || undefined,
        difficulty: (searchParams.get('difficulty') as RecipeDifficulty) || initialFilters.difficulty,
        includePublic: searchParams.get('includePublic') === 'true' || initialFilters.includePublic || false,
        // Pagination handled by usePagination hook
      };
    }
    return {
      q: initialFilters.q || '',
      tags: initialFilters.tags || [],
      cuisine: initialFilters.cuisine,
      difficulty: initialFilters.difficulty,
      includePublic: initialFilters.includePublic || false,
      // Pagination handled by usePagination hook
    };
  });

  // Update URL when filters change if persistInUrl is true
  useEffect(() => {
    if (!persistInUrl) return;
    
    const newParams = new URLSearchParams(searchParams);
    
    // Handle search query
    if (filters.q) {
      newParams.set('q', filters.q);
    } else {
      newParams.delete('q');
    }
    
    // Handle tags (multiple possible)
    newParams.delete('tag');
    filters.tags?.forEach(tag => {
      newParams.append('tag', tag);
    });
    
    // Handle cuisine
    if (filters.cuisine) {
      newParams.set('cuisine', filters.cuisine);
    } else {
      newParams.delete('cuisine');
    }
    
    // Handle difficulty
    if (filters.difficulty) {
      newParams.set('difficulty', filters.difficulty);
    } else {
      newParams.delete('difficulty');
    }
    
    // Handle includePublic
    if (filters.includePublic) {
      newParams.set('includePublic', 'true');
    } else {
      newParams.delete('includePublic');
    }
    
    setSearchParams(newParams, { replace: true });
  }, [filters, persistInUrl, searchParams, setSearchParams]);

  // Set search query
  const setSearchQuery = useCallback((query: string) => {
    setInternalFilters(prev => ({ ...prev, q: query }));
  }, []);

  // Add a tag
  const addTag = useCallback((tag: string) => {
    setInternalFilters(prev => {
      const currentTags = prev.tags || [];
      // Don't add duplicate tags
      if (currentTags.includes(tag)) return prev;
      return { ...prev, tags: [...currentTags, tag] };
    });
  }, []);

  // Remove a tag
  const removeTag = useCallback((tag: string) => {
    setInternalFilters(prev => {
      const currentTags = prev.tags || [];
      return { ...prev, tags: currentTags.filter(t => t !== tag) };
    });
  }, []);

  // Set cuisine
  const setCuisine = useCallback((cuisine: string | undefined) => {
    setInternalFilters(prev => ({ ...prev, cuisine }));
  }, []);

  // Set difficulty
  const setDifficulty = useCallback((difficulty: RecipeDifficulty | undefined) => {
    setInternalFilters(prev => ({ ...prev, difficulty }));
  }, []);

  // Toggle include public recipes
  const toggleIncludePublic = useCallback(() => {
    setInternalFilters(prev => ({ ...prev, includePublic: !prev.includePublic }));
  }, []);

  // Set include public recipes
  const setIncludePublic = useCallback((include: boolean) => {
    setInternalFilters(prev => ({ ...prev, includePublic: include }));
  }, []);

  // Reset all filters
  const resetFilters = useCallback(() => {
    setInternalFilters({
      q: '',
      tags: [],
      cuisine: undefined,
      difficulty: undefined,
      includePublic: false,
    });
  }, []);

  // Get filter count (how many active filters)
  const getActiveFilterCount = useCallback(() => {
    let count = 0;
    if (filters.q) count++;
    if (filters.tags && filters.tags.length > 0) count++;
    if (filters.cuisine) count++;
    if (filters.difficulty) count++;
    if (filters.includePublic) count++;
    return count;
  }, [filters]);

  return {
    filters,
    setFilters: setInternalFilters,
    setSearchQuery,
    addTag,
    removeTag,
    setCuisine,
    setDifficulty,
    toggleIncludePublic,
    setIncludePublic,
    resetFilters,
    getActiveFilterCount,
  };
};

export default useRecipeFilter;