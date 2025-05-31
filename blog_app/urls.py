
from django.urls import path
from blog_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path("blog_post/",views.blog_post,name = "blog_post"),
    path("get_blog/",views.get_blogs,name="get_blog"),
    path("blog_get/",views.blog_get,name = "blog_get"),
    path("blog_patch/",views.blog_patch,name = "blog_patch"),
    path("blog_put/",views.blog_put,name = "blog_put"),
    path("blog_delete/",views.blog_delete,name = "blog_delete"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



