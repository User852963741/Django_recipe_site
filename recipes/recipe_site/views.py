from django.shortcuts import render
from django.views import generic
from . models import Recipe, UserRecipe
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse_lazy
from . forms import RecipeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request, 'base.html')


class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipe_site/recipe.html'


class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10
    template_name = 'recipe_site/recipe_list.html'
    

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.request.GET.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner=owner_id)
        return queryset


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
    template_name = 'recipe_site/post_create.html'
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