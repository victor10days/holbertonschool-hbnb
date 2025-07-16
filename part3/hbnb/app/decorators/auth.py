"""
Authentication and authorization decorators for API endpoints
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import AuthService

auth_service = AuthService()

def require_ownership(resource_type):
    """
    Decorator to ensure user can only access/modify their own resources
    
    Args:
        resource_type (str): Type of resource ('user', 'place', 'review')
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            try:
                # Check if token is blacklisted
                from app.api.v1.auth import jwt_blacklist
                jti = get_jwt()['jti']
                if jti in jwt_blacklist:
                    return jsonify({'error': 'Token has been revoked'}), 401
                
                current_user_id = get_jwt_identity()
                current_user = auth_service.get_current_user()
                
                if not current_user:
                    return jsonify({'error': 'User not found'}), 404
                
                # If user is admin, allow access to any resource
                if current_user.is_admin:
                    return f(*args, **kwargs)
                
                # For user resources, check if user is accessing their own profile
                if resource_type == 'user':
                    resource_id = kwargs.get('id') or kwargs.get('user_id')
                    if resource_id and resource_id != current_user_id:
                        return jsonify({'error': 'Access denied. You can only access your own profile'}), 403
                
                # For places, check ownership
                elif resource_type == 'place':
                    place_id = kwargs.get('id') or kwargs.get('place_id')
                    if place_id:
                        # Get place and verify ownership
                        place = auth_service.facade.get_place(place_id)
                        if not place:
                            return jsonify({'error': 'Place not found'}), 404
                        if hasattr(place, 'user_id') and place.user_id != current_user_id:
                            return jsonify({'error': 'Access denied. You can only modify your own places'}), 403
                
                # For reviews, check ownership
                elif resource_type == 'review':
                    review_id = kwargs.get('id') or kwargs.get('review_id')
                    if review_id:
                        # Get review and verify ownership
                        review = auth_service.facade.get_review(review_id)
                        if not review:
                            return jsonify({'error': 'Review not found'}), 404
                        if hasattr(review, 'user_id') and review.user_id != current_user_id:
                            return jsonify({'error': 'Access denied. You can only modify your own reviews'}), 403
                
                return f(*args, **kwargs)
                
            except Exception as e:
                return jsonify({'error': 'Authentication failed'}), 401
        
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorator to ensure only admin users can access the endpoint
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            # Check if token is blacklisted
            from app.api.v1.auth import jwt_blacklist
            jti = get_jwt()['jti']
            if jti in jwt_blacklist:
                return jsonify({'error': 'Token has been revoked'}), 401
            
            current_user = auth_service.get_current_user()
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            if not current_user.is_admin:
                return jsonify({'error': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function

def authenticated_only(f):
    """
    Decorator to ensure user is authenticated (but no ownership check)
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            # Check if token is blacklisted
            from app.api.v1.auth import jwt_blacklist
            jti = get_jwt()['jti']
            if jti in jwt_blacklist:
                return jsonify({'error': 'Token has been revoked'}), 401
            
            current_user = auth_service.get_current_user()
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function