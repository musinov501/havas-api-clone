from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from apps.recipes.views.recipe_list_create import RecipeListCreateAPIView, RecipeDetailAPIView

app_name = 'recipes'

urlpatterns = [
   path('', RecipeListCreateAPIView.as_view(), name='recipe-list'),
   path('<int:pk>/', RecipeDetailAPIView.as_view(), name='recipe-detail')
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)