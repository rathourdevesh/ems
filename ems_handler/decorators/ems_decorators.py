"""This file contains all the common decorators required by ems handler."""
from django.http import HttpRequest, HttpResponse
from functools import wraps
from typing import Callable



def http_allowed_method(method='GET') -> Callable:
    """Validates if request.method is in the allowed method or not.
    
    kwargs: method ['GET','POST'] default is GET.
    returns: wrapped object."""
    def http_method_dec(view_function: Callable) -> Callable:
        @wraps(view_function)
        def function_wrapper(request: HttpRequest, **kwargs) -> HttpResponse:
            if not request.method == method:
                return HttpResponse(status=405)
            return view_function(request, **kwargs)
        return function_wrapper
    return http_method_dec
