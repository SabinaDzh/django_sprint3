from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Q

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    posts_list = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )[:5]
    context = {
        "post_list": posts_list,
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
        pk=id)
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.filter(
        slug=category_slug,
        is_published=True)
    )
    post_list = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True,
    )

    context = {
        'category': category, 'post_list': post_list
    }
    return render(request, template, context)
