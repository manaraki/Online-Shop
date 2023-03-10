from products.models import Category


def category(request):
    return {'categories': Category.objects.filter(is_sub=False)}
