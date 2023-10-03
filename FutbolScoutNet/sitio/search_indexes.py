from haystack import indexes
from sitio.models import *

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    fecha = indexes.DateTimeField(model_attr='fecha')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Queremos que se indexen todas los post con verificado = False"""
        return self.get_model().objects.filter(verificado=False)
