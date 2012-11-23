def get_param(request, param_name, default=None):
    """Returns a value of a request parameter.
    """
    args = request.args
    if args and param_name in args:
        val = args[param_name]
        if isinstance(val, list):
            return val[0]
        else: return val
    return default