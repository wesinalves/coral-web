def breadcrumbs(request):
    """
    Context processor to add breadcrumbs to all templates
    """
    return {'breadcrumbs': []}