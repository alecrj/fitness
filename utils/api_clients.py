import requests
from typing import Dict, List, Any, Optional

class USDAClient:
    """Client for interacting with the USDA FoodData Central API"""
    
    def __init__(self, api_key: str, base_url: str):
        """Initialize the USDA API client
        
        Args:
            api_key (str): USDA API key
            base_url (str): Base URL for USDA API
        """
        self.api_key = api_key
        self.base_url = base_url
        
    def search_foods(self, query: str, page_size: int = 25, page_number: int = 1) -> Dict[str, Any]:
        """Search for foods in the USDA database
        
        Args:
            query (str): Search query
            page_size (int, optional): Number of results per page. Defaults to 25.
            page_number (int, optional): Page number. Defaults to 1.
            
        Returns:
            Dict[str, Any]: Search results
        """
        url = f"{self.base_url}/foods/search"
        params = {
            'api_key': self.api_key,
            'query': query,
            'pageSize': page_size,
            'pageNumber': page_number
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()
    
    def get_food_details(self, fdc_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific food
        
        Args:
            fdc_id (str): FDC ID of the food
            
        Returns:
            Dict[str, Any]: Food details
        """
        url = f"{self.base_url}/food/{fdc_id}"
        params = {
            'api_key': self.api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def format_nutrient_data(self, nutrients: List[Dict[str, Any]]) -> Dict[str, float]:
        """Format nutrient data from USDA API to a simplified format
        
        Args:
            nutrients (List[Dict[str, Any]]): List of nutrients from USDA API
            
        Returns:
            Dict[str, float]: Simplified nutrient data
        """
        nutrient_data = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0,
            'sodium': 0,
            'cholesterol': 0
        }
        
        nutrient_mapping = {
            'Energy': 'calories',
            'Protein': 'protein',
            'Carbohydrate, by difference': 'carbs',
            'Total lipid (fat)': 'fat',
            'Fiber, total dietary': 'fiber',
            'Sugars, total including NLEA': 'sugar',
            'Sodium, Na': 'sodium',
            'Cholesterol': 'cholesterol'
        }
        
        for nutrient in nutrients:
            nutrient_name = nutrient.get('nutrient', {}).get('name', '')
            
            if nutrient_name in nutrient_mapping and 'amount' in nutrient:
                key = nutrient_mapping[nutrient_name]
                nutrient_data[key] = round(nutrient.get('amount', 0), 2)
                
        return nutrient_data