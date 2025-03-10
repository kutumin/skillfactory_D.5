from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Category, Post, PostCategory
from django.core.paginator import Paginator
from django.views import View 
from django.shortcuts import render
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protected_index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_auhtor'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostListNews(ListView):
    model = Post
    template_name = 'news.html' 
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type='NW')
    ordering = ['id']
    paginate_by = 1
    
class PostDetail(DetailView):
    model = Post
    template_name = 'details_news.html' 
    context_object_name = 'news'

class PostDetailEdit(DetailView):
    model = Post
    template_name = 'details_news.html' 
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type='news')

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post',)
    template_name = 'add_news.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
class PostDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'delete_news.html'
    queryset = Post.objects.all()
    context_object_name = 'news'
    success_url = '/news/'


class PostSearch(ListView):
    model = Post
    template_name = 'search_news.html' 
    context_object_name = 'news'
    paginate_by = 1
    form_class = PostForm

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['PostCategory'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context
 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        
        if form.is_valid(): 
            form.save()
 
        return super().get(request, *args, **kwargs)

class PostAdd(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_post', )
    model = Post
    template_name = 'add_news.html'
    context_object_name = 'news'
    paginate_by = 1
    form_class = PostForm

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['PostCategory'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        
        if form.is_valid(): 
            form.save()
 
        return super().get(request, *args, **kwargs)
