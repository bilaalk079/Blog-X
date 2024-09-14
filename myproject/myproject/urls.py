"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myblog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage, name='HomePage'),
    path('about', views.About, name='About'),
    path('discover', views.Discover, name='Discover'),
    path('login', views.Login, name='Login'),
    path('signup', views.Signup, name='Signup'),
    path('user_home', views.User_home, name='User_home'),
    path('logout', views.Logout , name='logout'),
    path('user_discover', views.User_discover, name='User_discover'),
    path('user_profile', views.User_profile, name='User_profile'),
    path('edit_profile', views.Edit_profile, name='Edit_profile'),
    path('admin_register', views.Reg_Admin, name='admin_register'),
    path('admin_registration', views.Admin_Registration, name='Admin_Registration'),
    path('admin_dashboard',views.Admin_Dashboard, name='Admin_Dashboard'),
    path('all_users', views.All_Users, name='All_users'),
    path('single_user/<int:id>', views.Single_User, name='Single_User'),
    path('block/<int:id>' , views.Block, name='Block'),
    path('unblock/<int:id>', views.Unblock , name='Unblock'),
    path('delete/<int:id>', views.Delete, name='Delete'),
    path('new_post',views.NewPost, name='NewPost'),
    path('all_posts',views.All_Posts,name='All_Posts'),
    path('single_post/<int:id>', views.Single_Post, name='Single_Post'),
    path('edit_post/<int:id>', views.Edit_Post, name='Edit_Post'),
    path('delete_post/<int:id>', views.DeletePost, name='DeletePost'),
    path('my_post', views.MyPost,name='MyPost'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comments/<int:post_id>/', views.fetch_comments, name='fetch_comments'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)