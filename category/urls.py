# from django.urls import path
# from category import views

# urlpatterns = [
    
#     path("api/",views.register_category,name = 'api'),
#     path("api_list/",views.list_api,name = 'api_list'),
#     path("api_patch/",views.update_patch_api,name = 'api_patch'),
#     path("api_put/",views.update_put_api,name = 'api_put'),
#     path("api_delete/",views.delete_api,name = 'api_delete'),
    
# ]

from django.urls import path
from category import views

urlpatterns = [
    path("api/", views.register_category, name='api'),
    path("api_list/", views.list_api, name='api_list'),
    path("api_patch/<int:pk>/", views.update_patch_api, name='api_patch'),
    path("api_put/", views.update_put_api, name='api_put'),
    path("api_delete/", views.delete_api, name='api_delete'),
]
