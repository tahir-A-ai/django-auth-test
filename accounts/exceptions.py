from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'status': 'error',
            'errors': {}
        }

        if hasattr(response, 'data'):
            for field, value in response.data.items():
                if isinstance(value, list):
                    custom_response['errors'][field] = value[0]
                else:
                    custom_response['errors'][field] = value
        
        response.data = custom_response
    
    return response