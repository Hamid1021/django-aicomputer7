from django.urls import path
from blog.views import add_comment, post_detail, posts_list, toggle_fav, toggle_save

app_name = "blogs"

urlpatterns = [
    path("", posts_list, name="blogs"),
    path("category/<int:pk>/", posts_list, name="category"),
    path("post_detail/<slug:slug>/<int:pk>/", post_detail, name="blog"),
    path("add_comment/", add_comment, name="add_comment"),
    path('blog/<int:blog_id>/fav/', toggle_fav, name='blog_fav'),
    path('blog/<int:blog_id>/save/', toggle_save, name='blog_save'),
]
