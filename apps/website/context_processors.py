from ..produto.models import Category


def menu(request):
    categories = Category.objects.all()
    return {'categories': categories}


