from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import make_password
from django.contrib import messages
from django.conf import settings
from myblog.models import *
from django.http import JsonResponse

# Create your views here.
def HomePage(request):
    latest_posts = Posts.objects.all().order_by('-created_at')[:6] 
    return render(request,'index.html', {'posts': latest_posts})
def About(request):
    return render(request,'about.html')
def Discover(request):
    user = request.user
    posts = Posts.objects.all().order_by('-id')
    return render(request, 'discover.html',{'posts':posts})
def Signup(request):
    if request.method == 'POST':
        get_email = request.POST.get('email')
        get_password = request.POST.get('password')
        get_username = request.POST.get('username')
        if User.objects.filter(email = get_email).exists():
            messages.error(request, 'E-mail Already Exists')
        elif User.objects.filter(username = get_username).exists():
            messages.error(request, 'Username Already exists')
        else:
           user =  User.objects.create_user(email = get_email, password = get_password, username = get_username)
           user.save()
           userinfo = Userinfo.objects.create(user = user)
           userinfo.save()
           messages.success(request, f'Thank You {get_username} for registering with us')
           return redirect('/login')
    return render(request, 'signup.html')
def Login(request):
    if request.method == 'POST':
        get_username = request.POST.get('username')
        get_password = request.POST.get('password')
        
        user = auth.authenticate(username = get_username,password = get_password)
        if user is None:
            messages.error(request, 'Authentication Failed')
            return redirect('/login')
        else:
            auth.login(request,user)
            get_user = request.user
            is_superuser = get_user.is_superuser
            if is_superuser == 1:
                return redirect('/admin_dashboard')
            else:
               return redirect('/user_home')

    return render(request, 'login.html')
def Logout(request):
    auth.logout(request)
    return redirect('/login')
@login_required(login_url='/login')
def User_home(request):
    latest_posts = Posts.objects.all().order_by('-created_at')[:6] 
    return render(request, 'user_home.html', {'posts': latest_posts})
@login_required(login_url='/login')
def User_discover(request):
    query = request.GET.get('q')  # Get the search query if it exists
    if query:
        posts = Posts.objects.filter(content__icontains=query)  # Filter posts by content
    else:
        posts = Posts.objects.all()  # If no search query, return all posts
    
    post_data = []
    for post in posts:
        like_count = post.like_set.filter(is_liked=True).count()
        comment_count = Comment.objects.filter(post=post,).count()
        user_liked = post.like_set.filter(user=request.user, is_liked=True).exists()
        post_data.append({
            'post': post,
            'like_count': like_count,
            'user_liked': user_liked,
            'comment_count':comment_count,
        })
    
    return render(request, 'user_discover.html', {'post_data': post_data})
@login_required(login_url='/login')
def User_profile(request):
    return render(request, 'user_profile.html')
@login_required(login_url='/login')
def Edit_profile(request):
    if request.method == 'POST':
        get_username2 = request.POST.get('username')
        get_email2 = request.POST.get('email')
        get_password2 = request.POST.get('password')
        get_id = request.POST.get('user_id')
        get_bio = request.POST.get('bio')
        profilepic = request.FILES.get('profilepic')
        user = User.objects.get(id = get_id)
        userinfo = Userinfo.objects.get(user = user)
        if User.objects.filter(email = get_email2).exclude(id = get_id).exists():
            messages.error(request, 'E-mail Already Exists')
            return redirect('/edit_profile')
        elif User.objects.filter(username = get_username2).exclude(id = get_id).exists():
            messages.error(request, 'Username Already exists')
            return redirect('/edit_profile')
        else:
           user.username = get_username2
           user.email = get_email2
           if get_password2:
            user.password = make_password(get_password2)
           user.save()
           userinfo.bio = get_bio
           if profilepic:
                userinfo.image = profilepic
           userinfo.save()
           messages.success(request, f'{get_username2} Your Profile was updated Successfully')
           return redirect('/login')    
    return render(request, 'edit_profile.html')
def Reg_Admin(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if token != settings.ADMIN_REGISTER_TOKEN:
            messages.error(request, 'Invalid Token')
            return redirect('/admin_register')
        else:
            request.session['admin_registration_token_valid'] = True
            return redirect('/admin_registration')
    return render(request, 'admin_register.html')
def Admin_Registration(request):
    if not request.session.get('admin_registration_token_valid'):
        messages.error(request, 'Unauthorized access')
        return redirect('/admin_register')
    if request.method == 'POST':
        get_username = request.POST.get('username')
        get_email = request.POST.get('email')
        get_password = request.POST.get('password')
        if User.objects.filter(email = get_email).exists():
            messages.error(request, 'E-mail Already Exists')
            return redirect('/admin_registration')
        elif User.objects.filter(username = get_username).exists():
            messages.error(request, 'Username Already exists')
            return redirect('/admin_registration')
        else:
            user =  User.objects.create_user(email = get_email, password = get_password, username = get_username, is_superuser = 1)
            user.save()
            userinfo = Userinfo.objects.create(username = get_username,user = user,is_superuser =1)
            userinfo.save()
            messages.success(request, f'Thank You {get_username} for registering As an Admin')
            request.session.pop('admin_registration_token_valid', None)
            return redirect('/login')
    return render(request, 'admin_register_form.html')
@login_required(login_url='/login')
def Admin_Dashboard(request):
    latest_posts = Posts.objects.all().order_by('-created_at')[:6] 
    user = request.user
    if user.is_superuser == 1:
     return render(request, 'admin_dashboard.html',{'posts': latest_posts})
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def All_Users(request):
    user = request.user
    if user.is_superuser == 1:
      users = User.objects.filter(is_superuser = 0)
      return render(request, 'all_users.html', {'users':users})
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def Single_User(request,id):
    user = request.user
    if user.is_superuser == 1:
      single_user = User.objects.get(id = id)
      return render(request, 'single_user.html', {'single_user':single_user})
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def Delete(request, id):
     user = request.user
     if user.is_superuser == 1:
       get_id = User.objects.get(id = id)
       get_id.delete()
       return redirect('/all_users')
     else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def Unblock(request, id):
    user = request.user
    if user.is_superuser == 1:
      get_id = User.objects.get(id = id)
      get_id.is_active = 1
      get_id.save()
      return redirect('/all_users')
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def Block(request, id):
    user = request.user
    if user.is_superuser == 1:
      get_id = User.objects.get(id = id)
      get_id.is_active = 0
      get_id.save()
      return redirect('/all_users')
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def NewPost(request):
    if request.method == 'POST':
        user = request.user
        category = request.POST.get('category')
        title = request.POST.get('title')
        image = request.POST.get('postimage')
        content = request.POST.get('content')

        newpost = Posts.objects.create(title = title, content = content, author = user,category = category)
        newpost.save()
       
        if user.is_superuser == 1:
            return redirect('/admin_dashboard')
        else:
            return redirect('/user_home')
    return render(request, 'newpost.html')
@login_required(login_url='/login')
def All_Posts(request):
    user = request.user
    if user.is_superuser == 1:
      posts = Posts.objects.all()
      users = Userinfo.objects.all()
      return render(request, 'all_posts.html', {'posts':posts, 'users':users})
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
def Single_Post(request,id):
    user = request.user
    post = Posts.objects.get(id = id)
    return render(request, 'singlepost.html', {'post':post})
@login_required(login_url='/login')
def Edit_Post(request,id):
    user = request.user
    post = Posts.objects.get(id = id)
    if post.author == user:
      if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        image = request.POST.get('postimage')
        content = request.POST.get('content')

        post.title = title
        post.category = category
        post.content = content
        post.save()
        
        return redirect(f'/single_post/{id}')
      return render(request, 'edit_post.html',{'post':post})
@login_required(login_url='/login')
def DeletePost(request,id):
    user = request.user
    if user.is_superuser == 1:
       get_id = Posts.objects.get(id = id)
       get_id.delete()
       return redirect('/all_posts')
    else:
        messages.error(request, 'Forbidden')
        return redirect('/login')
@login_required(login_url='/login')
def MyPost(request):
    user = request.user
    posts = Posts.objects.filter(author = user)
    return render(request, 'my_post.html',{'posts':posts})
@login_required(login_url='/login')
def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Posts, id=post_id)
        user = request.user

        # Get or create a Like object
        like, created = Like.objects.get_or_create(user=user, post=post)

        # Toggle the like status
        like.is_liked = not like.is_liked
        like.save()

        # Count the number of likes where is_liked=True
        like_count = Like.objects.filter(post=post, is_liked=True).count()

        # Return the updated like status and like count
        return JsonResponse({
            'is_liked': like.is_liked,
            'like_count': like_count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required(login_url='/login')
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Posts, id=post_id)

        # Create and save the comment
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=content
        )

        return JsonResponse({
            'user': request.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='/login')
def fetch_comments(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Send back comment data as JSON
    comments_data = [{
        'user': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')

    } for comment in comments]

    return JsonResponse(comments_data, safe=False)