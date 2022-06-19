from django.shortcuts import render
from django.views import generic
from . models import Recipe
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse_lazy
from . forms import PostForm


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


class RecipeCreateView(generic.CreateView):
    model = Recipe
    template_name = 'recipe_site/post_create.html'
    success_url = reverse_lazy('my_recipe_list')
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

