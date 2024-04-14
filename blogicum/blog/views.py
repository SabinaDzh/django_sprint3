from django.shortcuts import get_object_or_404, render
from django.utils import timezone


from .models import Post, Category


QUANTITY_POSTS = 5


def requesting_post():
    return Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    posts_list = requesting_post()[:QUANTITY_POSTS]
    context = {
        "post_list": posts_list,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        requesting_post(), pk=post_id)

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
    post_list = requesting_post().filter(
        category=category
    )

    context = {
        'category': category, 'post_list': post_list
    }
    return render(request, template, context)
