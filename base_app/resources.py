from import_export import resources
from .models import Movie


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie