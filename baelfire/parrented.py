def parrented(method):
    def wrapper(self, *args, **kwargs):
        if self.parent:
            method_name = method.__name__
            parent_method = getattr(self.parent, method_name)
            if hasattr(parent_method, '__call__'):
                return parent_method(self, *args, **kwargs)
            else:
                return parent_method
        else:
            return method(self, *args, **kwargs)
    return wrapper
