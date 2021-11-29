from django.forms import ModelForm
from .models import Post
 
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['id', 'post_author', 'post_type', 'category', 'post_raiting','article_text']