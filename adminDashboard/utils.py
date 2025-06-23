from django.apps import apps

def get_all_models(app_labels=['dashboard']):
    all_models = {}
    for label in app_labels:
        app_models = apps.get_app_config(label).get_models()
        all_models.update({model.__name__.lower(): model for model in app_models})
    return all_models