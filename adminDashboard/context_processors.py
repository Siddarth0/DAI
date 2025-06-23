from .utils import get_all_models

def available_models(request):
    return {'models': get_all_models()}