from functools import wraps
from fastapi import HTTPException

def validate_user_access(allowed_roles: list[str]):
    def validate_user_access_wrapper(func):
        
        @wraps(func)
        async def has_role_wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=403, 
                    detail={"title": "Error", "message": "Access Denied"}
                )
            
            return await func(*args, **kwargs)
        
        return has_role_wrapper
    
    return validate_user_access_wrapper
