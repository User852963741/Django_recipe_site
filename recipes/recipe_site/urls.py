from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('myrecipes/', views.MyRecipeListView.as_view(), name='my_recipe_list'),
    path('create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipes/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
]