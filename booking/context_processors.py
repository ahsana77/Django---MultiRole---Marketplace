from services.models import Category
def cat_context(request):
    all_cats = Category.objects.all()
    return {
        'nav_categories' : all_cats[:4],
        'more_categories' : all_cats[4:],
        'categories' : all_cats,

    }