from .models import Blog, Fav, PostCategory, Save, Tag
from django.contrib.auth.decorators import login_required
from blog.models import Blog, Comment
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Blog
from club.models import Club


from django.core.paginator import Paginator


def posts_list(request, pk=None):
    all_categories = PostCategory.objects.all()
    posts = Blog.objects.get_all_active().order_by('-date_create')
    category = None
    tag = None

    # فیلتر بر اساس دسته‌بندی
    if pk:
        category = get_object_or_404(PostCategory, pk=pk)
        posts = posts.filter(post_cat=category)
    
    # فیلتر بر اساس تگ از کوئری پارامتر
    tag_pk = request.GET.get('tag')
    if tag_pk:
        tag = get_object_or_404(Tag, pk=tag_pk, is_active=True, is_deleted=False)
        posts = posts.filter(post_tag=tag)
        
    club_id = request.GET.get('club')
    if club_id:
        club = get_object_or_404(Club, pk=club_id)
        posts = posts.filter(club=club)

    # صفحه‌بندی
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Fav.objects.filter(user=request.user, blog__in=posts).values_list('blog_id', flat=True)

    saved_posts = []
    if request.user.is_authenticated:
        saved_posts = Save.objects.filter(user=request.user, blog__in=posts).values_list('blog_id', flat=True)

    context = {
        'page_obj': page_obj,
        'category': category,
        'tag': tag,
        'all_categories': all_categories,
        'liked_posts': liked_posts,
        'saved_posts': saved_posts,
    }
    return render(request, "blogs/posts.html", context)


def post_detail(request, slug, pk):
    post = get_object_or_404(Blog, slug=slug, pk=pk, is_active=True)
    latest_posts = Blog.objects.exclude(
        pk=post.pk).order_by('-date_create')[:5]

    if request.user.is_authenticated:
        comments = Comment.objects.filter(blog=post, reply__isnull=True).filter(
            is_show=True
        ).filter(
            is_personal=False
        ) | Comment.objects.filter(blog=post, reply__isnull=True, user=request.user)
    else:
        comments = Comment.objects.filter(
            blog=post, reply__isnull=True, is_show=True, is_personal=False)

    context = {
        "post": post,
        "comments": comments.order_by("-date_create"),
        'latest_posts': latest_posts,
    }
    return render(request, "blogs/post_detail.html", context)


@login_required
def toggle_fav(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    fav, created = Fav.objects.get_or_create(blog=blog, user=request.user)

    if not created:
        # قبلاً وجود داشته -> آن‌لایک
        fav.delete()
        liked = False
    else:
        liked = True

    # تعداد کل لایک‌ها
    likes_count = Fav.objects.filter(blog=blog).count()

    return JsonResponse({
        "status": "success",
        "liked": liked,
        "likes_count": likes_count
    })


@login_required
def toggle_save(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    save, created = Save.objects.get_or_create(blog=blog, user=request.user)

    if not created:
        save.delete()
        saved = False
    else:
        saved = True

    return JsonResponse({
        "status": "success",
        "saved": saved,
    })


@login_required
def add_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        message = request.POST.get("message")
        reply_id = request.POST.get("reply_id")  # اگر پاسخ باشد
        is_personal = request.POST.get("is_personal") == "true"

        post = get_object_or_404(Blog, pk=post_id)

        comment = Comment.objects.create(
            user=request.user,
            blog=post,
            message=message,
            reply_id=reply_id if reply_id else None,
            is_personal=is_personal,
            is_show=False
        )

        return JsonResponse({
            "status": "success",
            "comment_id": comment.id,
            "user_name": request.user.get_full_name() or request.user.username,
            "message": comment.message,
            "date_create": comment.date_create.strftime("%Y/%m/%d %H:%M"),
            "is_personal": comment.is_personal,
        })
    return JsonResponse({"status": "error"}, status=400)
