from functools import wraps

def log_user_action(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        print(f"[LOG] User={user} | View={self.__class__.__name__}")
        return func(self, request, *args, **kwargs)
    return wrapper