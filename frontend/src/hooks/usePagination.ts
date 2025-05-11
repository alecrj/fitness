import { useState, useCallback, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';

interface UsePaginationOptions {
  initialLimit?: number;
  initialPage?: number;
  persistInUrl?: boolean;
}

/**
 * Custom hook for handling pagination logic
 */
const usePagination = ({
  initialLimit = 10,
  initialPage = 1,
  persistInUrl = false
}: UsePaginationOptions = {}) => {
  // Use URL search params if persistInUrl is true
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Initialize from URL if available, otherwise use defaults
  const [page, setInternalPage] = useState(() => {
    if (persistInUrl && searchParams.has('page')) {
      const pageParam = Number(searchParams.get('page'));
      return isNaN(pageParam) ? initialPage : pageParam;
    }
    return initialPage;
  });
  
  const [limit, setInternalLimit] = useState(() => {
    if (persistInUrl && searchParams.has('limit')) {
      const limitParam = Number(searchParams.get('limit'));
      return isNaN(limitParam) ? initialLimit : limitParam;
    }
    return initialLimit;
  });

  // Calculate offset
  const offset = (page - 1) * limit;

  // Update URL when page or limit changes if persistInUrl is true
  useEffect(() => {
    if (!persistInUrl) return;
    
    const newParams = new URLSearchParams(searchParams);
    newParams.set('page', page.toString());
    newParams.set('limit', limit.toString());
    setSearchParams(newParams, { replace: true });
  }, [page, limit, persistInUrl, searchParams, setSearchParams]);

  // Set page with validation
  const setPage = useCallback((newPage: number) => {
    if (newPage < 1) {
      setInternalPage(1);
    } else {
      setInternalPage(newPage);
    }
  }, []);

  // Set limit with validation and reset page
  const setLimit = useCallback((newLimit: number) => {
    if (newLimit < 1) {
      setInternalLimit(1);
    } else {
      setInternalLimit(newLimit);
      setInternalPage(1); // Reset to first page when changing limit
    }
  }, []);

  // Go to next page
  const nextPage = useCallback(() => {
    setInternalPage(prev => prev + 1);
  }, []);

  // Go to previous page
  const prevPage = useCallback(() => {
    setInternalPage(prev => (prev > 1 ? prev - 1 : 1));
  }, []);

  // Go to first page
  const firstPage = useCallback(() => {
    setInternalPage(1);
  }, []);

  // Go to last page (requires totalPages)
  const lastPage = useCallback((totalPages: number) => {
    setInternalPage(totalPages > 0 ? totalPages : 1);
  }, []);

  // Reset pagination to initial values
  const resetPagination = useCallback(() => {
    setInternalPage(initialPage);
    setInternalLimit(initialLimit);
  }, [initialPage, initialLimit]);

  return {
    page,
    limit,
    offset,
    setPage,
    setLimit,
    nextPage,
    prevPage,
    firstPage,
    lastPage,
    resetPagination
  };
};

export default usePagination;