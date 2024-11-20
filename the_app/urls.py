from django.urls import path, include
from the_app.views import *
from . import views
from . import api
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


urlpatterns = [
    # I wrote this code
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    # for redirecting @login_required functions
    path('accounts/login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.user_search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('viewing/<str:username>/', views.viewing, name='viewing'),
    path('chats/', views.chats, name='chats'),
    path('chats/<str:chatroom>', views.chatroom, name='chatroom'),
    # path('chats/deleteChatroom/<str:chatroom>', views.deleteChatroom, name='deleteChatroom'),
    # end of code I wrote
    
    path('apischema/', get_schema_view(
        title="thesocialnetwork REST API",
        description="API for interacting with data", version="1.0.0"
    ), name='openapi-schema'),
    path('swaggerdocs/', TemplateView.as_view(
        template_name='swagger-docs.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

    # I wrote this code
    # api for users
    # List and create users
    path('api/users/', views.AppUserList.as_view(), name='users-list'),
    # Retrieve, update, and delete a user by their ID
    path('api/users/<int:pk>/', views.AppUserDetail.as_view(), name='users-detail'),

    # api for posts
    # List all posts and create a new post
    path('api/posts/', views.PostsList.as_view(), name='posts-list'),
    # Retrieve, update, and delete a post by its ID
    path('api/posts/<int:pk>/', views.PostsDetail.as_view(), name='posts-detail'),
    # end of code I wrote
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
