from django.shortcuts import render
from django.views import generic
from . models import Recipe, UserRecipe, RecipeIngredient, Ingredient
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse_lazy
from . forms import RecipeForm, UserRecipeForm, RecipeIngredientForm, IngredientForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import random 

def index(request):
    return render(request, 'base.html')


class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipe_site/recipe.html'
    

class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10
    template_name = 'recipe_site/recipe_list.html' 


class MyRecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10
    template_name = 'recipe_site/my_recipe_list.html'
    context_object_name = 'my_recipe_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=get_user(self.request))
        return queryset


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    template_name = 'recipe_site/recipe_create.html'
    success_url = reverse_lazy('my_recipe_list')
    form_class = RecipeForm

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Created successfully'))
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Recipe
    template_name = 'recipe_site/recipe_update.html'
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.id = self.get_object().id
        form.instance.owner = self.request.user
        messages.success(self.request, _('Updated successfully'))
        return super().form_valid(form)

    def test_func(self):
        post_instance = self.get_object()
        return post_instance.owner == self.request.user


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Recipe
    template_name = 'recipe_site/recipe_delete.html'

    def test_func(self):
        recipe_instance = self.get_object()
        return recipe_instance.owner == self.request.user

    def get_success_url(self):
        messages.success(self.request, _('Deleted successfully'))
        return reverse_lazy('my_recipe_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete'] = True
        return context

class UserRecipeDetailView(generic.DetailView):
    model = UserRecipe
    template_name = 'recipe_site/user_recipe.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user1'] = self.request.user
        return context


class UserRecipeListView(generic.ListView):
    model = UserRecipe
    paginate_by = 10
    template_name = 'recipe_site/user_recipe_list.html'
    context_object_name = 'user_recipes'


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=get_user(self.request))
        return queryset


class UserRecipeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    template_name = 'recipe_site/user_recipe_create.html'
    success_url = reverse_lazy('user_recipes')
    form_class = UserRecipeForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['recipe'] = self.request.GET.get('recipe_id')
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Created successfully'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object)
        return context

class UserRecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = UserRecipe
    template_name = 'recipe_site/user_recipe_update.html'
    form_class = UserRecipeForm

    def form_valid(self, form):
        form.instance.id = self.get_object().id
        form.instance.user = self.request.user
        messages.success(self.request, _('Updated successfully'))
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user


class UserRecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = UserRecipe
    template_name = 'recipe_site/user_recipe_delete.html'

    def test_func(self):
        user_recipe_instance = self.get_object()
        return user_recipe_instance.user == self.request.user

    def get_success_url(self):
        messages.success(self.request, _('Deleted successfully'))
        return reverse_lazy('user_recipes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete'] = True
        return context


class LuckyListView(generic.ListView):
    model = Recipe
    template_name = 'recipe_site/user_recipes.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        list = []
        for recipe in queryset:
            list.append(recipe.id)
        lucky = random.choice(list)
        queryset = queryset.filter(id=lucky)
        return queryset


class FavouriteListView(generic.ListView):
    model = UserRecipe
    template_name = 'recipe_site/user_favourites.html'
    context_object_name = 'favourite_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=get_user(self.request), favourite=True)
        return queryset


class RecipeIngredientDetailView(generic.DetailView):
    model = RecipeIngredient
    template_name = 'recipe_site/recipe_ingredient.html'


class RecipeIngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = RecipeIngredient
    template_name = 'recipe_site/recipe_ingredient_create.html'
    form_class = RecipeIngredientForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['recipe'] = self.request.GET.get('recipe_id')
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Added successfully'))
        return super().form_valid(form)

    def get_success_url(self):
          recipe_id=self.object.recipe.id
          return reverse_lazy('recipe', kwargs={'pk': recipe_id})
    

class RecipeIngredientUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = RecipeIngredient
    template_name = 'recipe_site/recipe_ingredient_update.html'
    form_class = RecipeIngredientForm

    def form_valid(self, form):
        form.instance.id = self.get_object().id
        form.instance.user = self.request.user
        messages.success(self.request, _('Updated successfully'))
        return super().form_valid(form)

    def test_func(self):
        recipe_ingredient_instance = self.get_object()
        return recipe_ingredient_instance.recipe.owner == self.request.user

    def get_success_url(self):
        recipe_id=self.object.recipe.id
        return reverse_lazy('recipe', kwargs={'pk': recipe_id})


class RecipeIngredientDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = RecipeIngredient
    template_name = 'recipe_site/recipe_ingredient_delete.html'

    def test_func(self):
        recipe_ingredient_instance = self.get_object()
        return recipe_ingredient_instance.recipe.owner == self.request.user

    def get_success_url(self):
        messages.success(self.request, _('Deleted successfully'))
        recipe_id=self.object.recipe.id
        return reverse_lazy('recipe', kwargs={'pk': recipe_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete'] = True
        return context


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = RecipeIngredient
    template_name = 'recipe_site/ingredient_create.html'
    form_class = IngredientForm


    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Created successfully'))
        return super().form_valid(form)

    def get_success_url(self):
          return reverse_lazy('my_recipe_list')