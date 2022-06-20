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
    path('userrecipes/<int:pk>/', views.UserRecipeDetailView.as_view(), name='user_recipe'),
    path('userrecipes/', views.UserRecipeListView.as_view(), name='user_recipes'),
    path('createuserrecipe/', views.UserRecipeCreateView.as_view(), name='user_recipe_create'),
    path('userrecipes/<int:pk>/edit/', views.UserRecipeUpdateView.as_view(), name='user_recipe_update'),
    path('userrecipes/<int:pk>/delete/', views.UserRecipeDeleteView.as_view(), name='user_recipe_delete'),

]