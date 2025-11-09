from blogs.models import Categorias


def get_categories(request):
    categories = Categorias.objects.all()
    return dict(categories=categories)