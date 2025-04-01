import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Post, Reaction
from .forms import UserRegistrationForm  # Import UserRegistrationForm

from .forms import PostForm

# Create a logger
logger = logging.getLogger(__name__)

def home_view(request):
    logger.info('Home view accessed')
    return render(request, 'posts/home.html')

def root_view(request):
    logger.info('Root view accessed')
    return redirect('login')  # Redirect to login page instead of post list

def post_list(request):
    logger.info('Post list view accessed')
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_create(request):
    logger.info('Post create view accessed')
    if not request.user.is_authenticated:
        logger.warning('User is not authenticated')
        return redirect('login')  # Redirect to login if user is not authenticated

    if request.method == 'POST':
        logger.info('Post create form submitted')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info('Post create form is valid')
            post = form.save(commit=False)  # Create the post instance without saving to the database
            post.user = request.user  # Set the user to the currently logged-in user
            post.save()  # Now save the post instance
            logger.info('Post created successfully')
            return redirect('post_list')  # Redirect to the post list
        else:
            logger.error('Post create form is invalid')
    else:
        logger.info('Post create form rendered')
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})

def register_view(request):
    form = UserRegistrationForm()  # Initialize the registration form


    logger.info('Register view accessed')
    if request.method == 'POST':
        logger.info('Register form submitted')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            logger.warning('Username already exists')
            return render(request, 'posts/register.html', {'error': 'Username already exists. Please choose a different one.'})
        
        User.objects.create_user(username=username, email=email, password=password)  # Directly create user


        logger.info('User created successfully')
        return redirect('login')  # Redirect to login after registration
        return redirect('login')  # Redirect to login after registration
    return render(request, 'posts/register.html', {'form': form})


def login_view(request):
    logger.info('Login view accessed')
    if request.method == 'POST':
        logger.info('Login form submitted')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.info('User authenticated successfully')
            login(request, user)
            return redirect('post_list')  # Redirect to post list after login
        else:
            logger.error('Invalid credentials')
            return render(request, 'posts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'posts/login.html')


def react_to_post(request, post_id):
    logger.info('React to post view accessed')
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        logger.error('Post not found')
        return redirect('post_list')  # Redirect to post list if post does not exist

    if request.method == 'POST':
        logger.info('Reaction form submitted')
        reaction_type = request.POST.get('reaction_type')
        Reaction.objects.create(user=request.user, post=post, reaction_type=reaction_type)
        logger.info('Reaction created successfully')
    return redirect('post_list')
