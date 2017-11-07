from .models import Page


# Makes menu_items variable available to all templates
def menu_processor(request):
    page_items = Page.objects.filter(show_in_menu='True').order_by('sorting_value')
    return {'page_items': page_items}
