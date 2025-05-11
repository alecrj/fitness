import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRecipes } from '../../contexts/RecipeContext';
import { recipeService } from '../../api/recipeService';
import { RecipeSupportedSite } from '../../types/recipe';

/**
 * Recipe import component for importing recipes from external websites
 */
const RecipeImport: React.FC = () => {
  const navigate = useNavigate();
  const { importRecipe } = useRecipes();

  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [supportedSites, setSupportedSites] = useState<RecipeSupportedSite[]>([]);
  const [loadingSites, setLoadingSites] = useState(false);

  // Fetch supported sites on component mount
  useEffect(() => {
    const fetchSupportedSites = async () => {
      setLoadingSites(true);
      try {
        const sites = await recipeService.getSupportedSites();
        setSupportedSites(sites);
      } catch (err) {
        console.error('Failed to fetch supported sites:', err);
      } finally {
        setLoadingSites(false);
      }
    };

    fetchSupportedSites();
  }, []);

  // Handle URL input change
  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    setError(null);
  };

  // Check if URL is from a supported site
  const isSupportedUrl = (testUrl: string): boolean => {
    if (!testUrl) return false;
    
    try {
      const hostname = new URL(testUrl).hostname;
      return supportedSites.some(site => 
        hostname === site.domain || hostname.endsWith(`.${site.domain}`)
      );
    } catch {
      return false;
    }
  };

  // Get site info for a URL
  const getSiteInfo = (testUrl: string): RecipeSupportedSite | undefined => {
    if (!testUrl) return undefined;
    
    try {
      const hostname = new URL(testUrl).hostname;
      return supportedSites.find(site => 
        hostname === site.domain || hostname.endsWith(`.${site.domain}`)
      );
    } catch {
      return undefined;
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate URL
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }
    
    // Validate URL format
    try {
      new URL(url);
    } catch {
      setError('Please enter a valid URL');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const recipe = await importRecipe({ url });
      navigate(`/recipes/${recipe.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to import recipe. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Import Recipe</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2" htmlFor="url">
                Recipe URL
              </label>
              <input
                type="text"
                id="url"
                value={url}
                onChange={handleUrlChange}
                className={`w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  error ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="https://example.com/recipe"
              />
              {error && (
                <p className="text-red-500 text-sm mt-1">{error}</p>
              )}
              
              {url && !error && (
                <div className="mt-2">
                  {isSupportedUrl(url) ? (
                    <p className="text-green-600 text-sm flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      This website is supported for automatic imports
                    </p>
                  ) : (
                    <p className="text-amber-600 text-sm flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      This website may not be fully supported
                    </p>
                  )}
                </div>
              )}
            </div>

            <div className="flex justify-between">
              <button
                type="button"
                onClick={() => navigate('/recipes')}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className={`bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md ${
                  loading ? 'opacity-70 cursor-not-allowed' : ''
                }`}
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    <span>Importing...</span>
                  </div>
                ) : (
                  'Import Recipe'
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Supported sites section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Supported Websites</h2>
          
          {loadingSites ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : supportedSites.length === 0 ? (
            <p className="text-gray-600">No supported websites information available.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {supportedSites.map((site, index) => (
                <div key={index} className="border border-gray-200 rounded-md p-3 flex items-center">
                  {site.icon ? (
                    <img src={site.icon} alt={site.name} className="w-6 h-6 mr-3" />
                  ) : (
                    <div className="w-6 h-6 bg-gray-200 rounded-full mr-3 flex items-center justify-center text-xs">
                      {site.name.charAt(0).toUpperCase()}
                    </div>
                  )}
                  <div>
                    <div className="font-semibold">{site.name}</div>
                    <div className="text-gray-500 text-sm">{site.domain}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          <div className="mt-6 text-gray-600 text-sm">
            <p>
              If a website is not officially supported, the app will still attempt to import the recipe,
              but results may vary. For best results, use supported websites.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeImport;