"""API documentation utilities using OpenAPI/Swagger"""
from flask import Blueprint, jsonify, current_app
from flask_swagger_ui import get_swaggerui_blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
import json
import os
import re
from typing import Dict, Any, List, Optional, Callable, Tuple

# OpenAPI/Swagger blueprint setup
def create_swagger_blueprint():
    """Create a blueprint for Swagger UI"""
    swagger_url = '/api/docs'
    api_url = '/openapi.json'
    
    swagger_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': "Fitness/Food App API"
        }
    )
    
    return swagger_blueprint

# OpenAPI JSON specification
class APIDocumentation:
    """API documentation generator for OpenAPI/Swagger"""
    
    def __init__(self, title="Fitness/Food App API", version="1.0.0"):
        """Initialize the API documentation generator
        
        Args:
            title: API title
            version: API version
        """
        self.spec = APISpec(
            title=title,
            version=version,
            openapi_version="3.0.2",
            info=dict(description="API for fitness and food tracking application"),
            plugins=[MarshmallowPlugin()],
        )
        
        # Add security schemes
        self.spec.components.security_scheme(
            "BearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        )
        
        # Register tags
        self.spec.tag({"name": "auth", "description": "Authentication endpoints"})
        self.spec.tag({"name": "recipes", "description": "Recipe management endpoints"})
        self.spec.tag({"name": "nutrition", "description": "Nutrition tracking endpoints"})
        self.spec.tag({"name": "social", "description": "Social features endpoints"})
        
        # Tracked endpoints
        self.endpoints = []
        
    def add_route(self, path: str, methods: List[str], summary: str, tags: List[str], 
                 description: Optional[str] = None, 
                 parameters: Optional[List[Dict[str, Any]]] = None,
                 request_body: Optional[Dict[str, Any]] = None,
                 responses: Optional[Dict[str, Dict[str, Any]]] = None,
                 security: Optional[List[Dict[str, List]]] = None):
        """Add a route to the API documentation
        
        Args:
            path: URL path of the endpoint
            methods: HTTP methods supported by the endpoint
            summary: Short summary of the endpoint
            tags: List of tags to categorize the endpoint
            description: Detailed description of the endpoint
            parameters: List of parameters for the endpoint
            request_body: Request body schema
            responses: Response schemas for different status codes
            security: Security requirements for the endpoint
        """
        # Default responses if not provided
        if not responses:
            responses = {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object"
                            }
                        }
                    }
                },
                "400": {
                    "description": "Bad request",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "error": {"type": "string"},
                                    "message": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "401": {
                    "description": "Unauthorized",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "error": {"type": "string"},
                                    "message": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
            
        # Default security for authenticated endpoints
        if security is None and any(tag != 'auth' for tag in tags):
            security = [{"BearerAuth": []}]
            
        # Store endpoint details
        for method in methods:
            method = method.lower()
            operation = {
                "summary": summary,
                "tags": tags,
                "responses": responses
            }
            
            if description:
                operation["description"] = description
                
            if parameters:
                operation["parameters"] = parameters
                
            if request_body:
                operation["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": request_body
                        }
                    }
                }
                
            if security:
                operation["security"] = security
                
            # Add to tracked endpoints
            self.endpoints.append((path, method, operation))
            
    def add_schema(self, name: str, schema: Dict[str, Any]):
        """Add a schema to the API documentation
        
        Args:
            name: Schema name
            schema: Schema definition
        """
        self.spec.components.schema(name, schema)
        
    def finalize_spec(self) -> Dict[str, Any]:
        """Generate the final OpenAPI specification
        
        Returns:
            OpenAPI specification as a dictionary
        """
        # Add all tracked endpoints to the spec
        for path, method, operation in self.endpoints:
            self.spec.path(path=path, operations={method: operation})
            
        return self.spec.to_dict()
        
    def save_spec(self, filename: str):
        """Save the OpenAPI specification to a file
        
        Args:
            filename: Path to save the specification
        """
        spec_dict = self.finalize_spec()
        
        with open(filename, 'w') as f:
            json.dump(spec_dict, f, indent=2)
            
        return spec_dict

# Function to extract path parameters from routes
def extract_path_params(path: str) -> List[Dict[str, Any]]:
    """Extract path parameters from a route path
    
    Args:
        path: Route path (e.g., '/users/<user_id>')
        
    Returns:
        List of parameter definitions
    """
    params = []
    pattern = r'<(?:(?P<converter>[a-zA-Z_]+):)?(?P<parameter>\w+)>'
    
    for match in re.finditer(pattern, path):
        converter = match.group('converter') or 'string'
        parameter = match.group('parameter')
        
        param_type = 'string'
        if converter == 'int':
            param_type = 'integer'
        elif converter == 'float':
            param_type = 'number'
        elif converter == 'path':
            param_type = 'string'
            
        params.append({
            'name': parameter,
            'in': 'path',
            'required': True,
            'schema': {
                'type': param_type
            }
        })
        
    return params

# Function to extract query parameters from Flask view functions
def extract_query_params(view_func: Callable) -> List[Dict[str, Any]]:
    """Extract query parameters from a Flask view function documentation
    
    Args:
        view_func: Flask view function
        
    Returns:
        List of parameter definitions
    """
    params = []
    
    # Check if the function has a docstring
    if not view_func.__doc__:
        return params
        
    # Parse docstring for query parameters
    docstring = view_func.__doc__
    param_matches = re.findall(r'Args:\s+([^:]+):([^:]+)(?=\w+:|$)', docstring)
    
    for param_name, param_desc in param_matches:
        param_name = param_name.strip()
        param_desc = param_desc.strip()
        
        # Check if it's a query parameter
        if 'query parameter' in param_desc.lower() or 'request.args' in param_desc.lower():
            # Extract type information if available
            param_type = 'string'  # Default type
            type_match = re.search(r'type: ([a-zA-Z]+)', param_desc.lower())
            if type_match:
                type_str = type_match.group(1)
                if type_str in ('int', 'integer'):
                    param_type = 'integer'
                elif type_str in ('float', 'number'):
                    param_type = 'number'
                elif type_str == 'bool':
                    param_type = 'boolean'
                    
            # Extract required information if available
            required = False
            if 'required' in param_desc.lower():
                required = True
                
            params.append({
                'name': param_name,
                'in': 'query',
                'required': required,
                'schema': {
                    'type': param_type
                },
                'description': param_desc
            })
            
    return params

# Function to register API documentation route
def register_api_docs(app, filename="openapi.json"):
    """Register API documentation routes with the Flask app
    
    Args:
        app: Flask application
        filename: Filename to save the OpenAPI specification
    """
    @app.route(f"/{filename}")
    def serve_openapi_spec():
        """Serve the OpenAPI specification"""
        # Load the spec from file if it exists
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    spec = json.load(f)
                    return jsonify(spec)
                except json.JSONDecodeError:
                    pass
                    
        # Return a placeholder spec if file doesn't exist
        return jsonify({
            "openapi": "3.0.2",
            "info": {
                "title": "Fitness/Food App API",
                "version": "1.0.0",
                "description": "API documentation not fully generated yet."
            },
            "paths": {}
        })
    
    # Register Swagger UI blueprint
    swagger_blueprint = create_swagger_blueprint()
    app.register_blueprint(swagger_blueprint, url_prefix='/api/docs')

# Common response schemas for reuse
STANDARD_ERROR_RESPONSES = {
    "400": {
        "description": "Bad request",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "message": {"type": "string"}
                    }
                }
            }
        }
    },
    "401": {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "message": {"type": "string"}
                    }
                }
            }
        }
    },
    "403": {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "message": {"type": "string"}
                    }
                }
            }
        }
    },
    "404": {
        "description": "Not found",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "message": {"type": "string"}
                    }
                }
            }
        }
    },
    "500": {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "message": {"type": "string"}
                    }
                }
            }
        }
    }
}

# Common schemas for reuse
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "profile_image_url": {"type": "string", "nullable": True},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    }
}

PAGINATION_SCHEMA = {
    "type": "object",
    "properties": {
        "total": {"type": "integer"},
        "limit": {"type": "integer"},
        "offset": {"type": "integer"}
    }
}