import requests
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import urljoin
import json

logger = logging.getLogger(__name__)

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
        
    def search_foods(self, query: str, page_size: int = 25, page_number: int = 1, 
                    additional_filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search for foods in the USDA database
        
        Args:
            query (str): Search query
            page_size (int, optional): Number of results per page. Defaults to 25.
            page_number (int, optional): Page number. Defaults to 1.
            additional_filters (Dict[str, Any], optional): Additional search parameters
            
        Returns:
            Dict[str, Any]: Search results
        """
        url = urljoin(self.base_url, "/foods/search")
        params = {
            'api_key': self.api_key,
            'query': query,
            'pageSize': page_size,
            'pageNumber': page_number
        }
        
        # Add any additional filters
        if additional_filters:
            params.update(additional_filters)
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"USDA API search error: {str(e)}")
            return {"error": str(e), "foods": []}
    
    def get_food_details(self, fdc_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific food
        
        Args:
            fdc_id (str): FDC ID of the food
            
        Returns:
            Dict[str, Any]: Food details
        """
        url = urljoin(self.base_url, f"/food/{fdc_id}")
        params = {
            'api_key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"USDA API food details error: {str(e)}")
            return {"error": str(e)}
    
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
            nutrient_name = None
            amount = None
            
            # Handle different API response formats
            if 'nutrient' in nutrient and 'name' in nutrient['nutrient']:
                nutrient_name = nutrient['nutrient']['name']
                amount = nutrient.get('amount')
            elif 'nutrientName' in nutrient:
                nutrient_name = nutrient['nutrientName']
                amount = nutrient.get('value')
                
            if nutrient_name in nutrient_mapping and amount is not None:
                key = nutrient_mapping[nutrient_name]
                nutrient_data[key] = round(float(amount), 2)
                
        return nutrient_data
    
    def format_food_item(self, food_data: Dict[str, Any], is_detailed: bool = False) -> Dict[str, Any]:
        """Format food data from USDA API to a format compatible with our application
        
        Args:
            food_data (Dict[str, Any]): Food data from USDA API
            is_detailed (bool, optional): Whether the data is from a detailed food lookup
            
        Returns:
            Dict[str, Any]: Formatted food item data
        """
        if is_detailed:
            # Format data from detailed food endpoint
            nutrients = food_data.get('foodNutrients', [])
            nutrition = self.format_nutrient_data(nutrients)
            
            return {
                'name': food_data.get('description', ''),
                'brand': food_data.get('brandName', ''),
                'fdcId': food_data.get('fdcId'),
                'serving_size': food_data.get('servingSize', 100),
                'serving_unit': food_data.get('servingSizeUnit', 'g'),
                'ingredients': food_data.get('ingredients', ''),
                'category': food_data.get('foodCategory', {}).get('description', ''),
                'nutrition': nutrition,
                'is_custom': False,
                'source': 'usda'
            }
        else:
            # Format data from search endpoint
            nutrients = food_data.get('foodNutrients', [])
            nutrition = {}
            
            for nutrient in nutrients:
                if nutrient.get('nutrientName') == 'Energy' and nutrient.get('unitName', '').lower() == 'kcal':
                    nutrition['calories'] = nutrient.get('value', 0)
                elif nutrient.get('nutrientName') == 'Protein':
                    nutrition['protein'] = nutrient.get('value', 0)
                elif nutrient.get('nutrientName') == 'Total lipid (fat)':
                    nutrition['fat'] = nutrient.get('value', 0)
                elif nutrient.get('nutrientName') == 'Carbohydrate, by difference':
                    nutrition['carbs'] = nutrient.get('value', 0)
            
            return {
                'name': food_data.get('description', ''),
                'brand': food_data.get('brandOwner', food_data.get('brandName', '')),
                'fdcId': food_data.get('fdcId'),
                'serving_size': food_data.get('servingSize', 100),
                'serving_unit': food_data.get('servingSizeUnit', 'g'),
                'nutrition': nutrition,
                'is_custom': False,
                'source': 'usda'
            }


class BarcodeClient:
    """Client for barcode lookup services"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the barcode client
        
        Args:
            api_key (str, optional): API key for commercial barcode services
        """
        self.api_key = api_key
        # Primary API endpoint - OpenFoodFacts (free and open source)
        self.open_food_facts_url = "https://world.openfoodfacts.org/api/v0/product/"
        # Backup API endpoint - can be replaced with a commercial service
        self.backup_api_url = None
    
    def lookup_barcode(self, barcode: str) -> Dict[str, Any]:
        """Look up product information by barcode
        
        Args:
            barcode (str): Product barcode (UPC, EAN, etc.)
            
        Returns:
            Dict[str, Any]: Product information
        """
        # Try Open Food Facts first
        try:
            url = f"{self.open_food_facts_url}{barcode}.json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 1:  # Success
                return self._format_open_food_facts(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenFoodFacts API error: {str(e)}")
            
        # If we have a backup API configured, try that
        if self.backup_api_url and self.api_key:
            try:
                return self._lookup_backup_api(barcode)
            except requests.exceptions.RequestException as e:
                logger.error(f"Backup barcode API error: {str(e)}")
                
        # Return empty result if all lookups failed
        return {"found": False, "message": "Barcode not found in database"}
    
    def _format_open_food_facts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Open Food Facts data to our application format
        
        Args:
            data (Dict[str, Any]): OpenFoodFacts API response
            
        Returns:
            Dict[str, Any]: Formatted food item data
        """
        product = data.get('product', {})
        
        # Extract nutrition data
        nutrients = product.get('nutriments', {})
        
        nutrition = {
            'calories': nutrients.get('energy-kcal_100g', 0),
            'protein': nutrients.get('proteins_100g', 0),
            'carbs': nutrients.get('carbohydrates_100g', 0),
            'fat': nutrients.get('fat_100g', 0),
            'fiber': nutrients.get('fiber_100g', 0),
            'sugar': nutrients.get('sugars_100g', 0),
            'sodium': nutrients.get('sodium_100g', 0),
            'cholesterol': nutrients.get('cholesterol_100g', 0)
        }
        
        return {
            'found': True,
            'barcode': data.get('code'),
            'name': product.get('product_name', ''),
            'brand': product.get('brands', ''),
            'image_url': product.get('image_url'),
            'serving_size': 100,  # OpenFoodFacts uses per 100g/ml
            'serving_unit': 'g',
            'ingredients': product.get('ingredients_text', ''),
            'nutrition': nutrition,
            'is_custom': False,
            'source': 'open_food_facts'
        }
    
    def _lookup_backup_api(self, barcode: str) -> Dict[str, Any]:
        """Look up product using backup API (placeholder for commercial API)
        
        Args:
            barcode (str): Product barcode
            
        Returns:
            Dict[str, Any]: Product information
        """
        # This is a placeholder for a commercial API integration
        # Implement according to the specific API being used
        params = {
            'api_key': self.api_key,
            'barcode': barcode
        }
        
        response = requests.get(self.backup_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Format response according to the specific API
        # This is just a placeholder structure
        return {
            'found': True,
            'barcode': barcode,
            'name': data.get('name', ''),
            'brand': data.get('brand', ''),
            'nutrition': {
                'calories': data.get('calories', 0),
                'protein': data.get('protein', 0),
                'carbs': data.get('carbs', 0),
                'fat': data.get('fat', 0)
            },
            'source': 'backup_api'
        }


class NutritionLabelRecognizer:
    """Client for nutrition label recognition services (OCR)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the nutrition label recognizer
        
        Args:
            api_key (str, optional): API key for OCR service
        """
        self.api_key = api_key
        # Placeholder for OCR service URL
        # In production, use a service like Google Cloud Vision, AWS Rekognition, etc.
        self.ocr_service_url = None
    
    def recognize_label(self, image_data: bytes) -> Dict[str, Any]:
        """Recognize nutrition information from an image
        
        Args:
            image_data (bytes): Image data of nutrition label
            
        Returns:
            Dict[str, Any]: Extracted nutrition information
        """
        if not self.ocr_service_url or not self.api_key:
            return {
                "success": False,
                "message": "OCR service not configured"
            }
            
        try:
            headers = {
                "Content-Type": "application/octet-stream",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                self.ocr_service_url,
                headers=headers,
                data=image_data
            )
            response.raise_for_status()
            ocr_result = response.json()
            
            # Process the OCR result to extract nutrition information
            # This would be heavily dependent on the specific OCR service being used
            # and would require custom parsing logic
            
            # Placeholder for extracted data
            extracted_data = self._parse_ocr_result(ocr_result)
            
            return {
                "success": True,
                "nutrition": extracted_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OCR API error: {str(e)}")
            return {
                "success": False,
                "message": f"Error communicating with OCR service: {str(e)}"
            }
    
    def _parse_ocr_result(self, ocr_result: Dict[str, Any]) -> Dict[str, float]:
        """Parse OCR result to extract nutrition information
        
        Args:
            ocr_result (Dict[str, Any]): Raw OCR result
            
        Returns:
            Dict[str, float]: Extracted nutrition values
        """
        # This is a placeholder implementation
        # In a real implementation, this would contain complex parsing logic
        # to extract nutrition information from the OCR text
        
        # Example: looking for patterns like "Calories 200" or "Total Fat 10g"
        nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0,
            'sodium': 0,
            'cholesterol': 0
        }
        
        # Extract text from OCR result
        # The exact format would depend on the OCR service being used
        text = ""
        if 'text' in ocr_result:
            text = ocr_result['text']
        elif 'fullTextAnnotation' in ocr_result:
            text = ocr_result['fullTextAnnotation'].get('text', '')
        
        # Simple pattern matching example
        # In a real implementation, this would be much more sophisticated
        lines = text.split('\n')
        for line in lines:
            line = line.lower()
            
            # Check for calories
            if 'calories' in line:
                try:
                    # Extract digits
                    calories = ''.join(c for c in line if c.isdigit())
                    if calories:
                        nutrition['calories'] = float(calories)
                except ValueError:
                    pass
                    
            # Check for protein
            if 'protein' in line:
                try:
                    # Extract digits
                    protein = ''.join(c for c in line if c.isdigit() or c == '.')
                    if protein:
                        nutrition['protein'] = float(protein)
                except ValueError:
                    pass
                    
            # Similar patterns for other nutrients
            # ...
        
        return nutrition