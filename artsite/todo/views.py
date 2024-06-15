from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout
from .models import User, ArtPost, Message, Conversation, Favorites, File, Review, SubscriberList, Cart, CartItem, \
    Billing
from .forms import modify_credentialsform, DeleteAccount, ArtPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models


# View for the home page
def home(request):
    art_posts = ArtPost.objects.filter(status='approved').order_by('-timestamp')
    context = {
        'art_posts': art_posts
    }
    return render(request, 'home.html', context)


# View for the login page
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # If authentication fails with username, try phone number
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                login(request, user)
                return redirect('home')
        except User.DoesNotExist:
            pass  # Continue to show the error message

        # If authentication fails with both username and phone number
        messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')


# View for the chats page


# View for signing up new members


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            messages.error(request, 'username already exists. please chose another one!')
        elif User.objects.filter(phone=phone).exists():

            messages.error(request, 'Phone number already used!')
        elif User.objects.filter(email=email).exists():

            messages.error(request, 'Email already used!')

        else:
            new_user = User(
                username=username,
                email=email,
                phone=phone,

            )
            new_user.set_password(password)  # Hash the password
            new_user.save()
            login(request, new_user)
            messages.success(request, "account created successfully!")
            return redirect('home')  # Redirect to a success page after form submission

    return render(request, 'signup.html')


# View for logging out
def logoutuser(request):
    logout(request)
    return redirect('home')


# View for the account deletion confirmation
def confirm_delete_account(request):
    return render(request, 'confirm_delete_account.html')


# View for deleting the account
@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccount(request.POST)
        if form.is_valid():
            user = request.user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == user.username and user.check_password(password):
                user.delete()

                messages.success(request, 'account deletion successfull')

                return redirect('loginuser')
            else:
                messages.error(request, 'credentials wrong , logged u out')
                logout(request)
    return redirect('loginuser')


# View for modifying credentials


def find_account(request):
    if request.method == 'POST':

        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            request.session['password_recovery_user_id'] = user.id
            messages.success(request, 'Account found! Please type in your new password.')
            return redirect('change_password')
        except User.DoesNotExist:
            messages.error(request, "There's no such account!")

    return render(request, 'find_account.html')


def change_password(request):
    if 'password_recovery_user_id' not in request.session:
        # Redirect to the appropriate page if session variable is not set
        messages.error(request, 'Password recovery process not initiated.')
        return redirect('find_account')
    if request.method == 'POST':
        user_id = request.session['password_recovery_user_id']
        user = User.objects.get(id=user_id)
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Your password has been changed successfully.')
        del request.session['password_recovery_user_id']

        return redirect('loginuser')

    return render(request, 'change_password.html')


@login_required
def lounge(request):
    user = request.user
    if request.method == 'POST' and user.status == 'seller':
        form = ArtPostForm(request.POST, request.FILES)
        files = request.FILES.getlist('additional_images')

        if form.is_valid():
            art_post = form.save(commit=False)
            art_post.user = user
            art_post.price = request.POST.get('price')
            art_post.title = request.POST.get('title')
            art_post.category = request.POST.get('category')
            art_post.type = request.POST.get('type')
            art_post.save()
            if files is not None:
                for f in files:
                    File.objects.create(
                        art=art_post,
                        file=f
                    )

            messages.success(request, 'File Uploaded.')
            return redirect('lounge')
        else:
            messages.error(request, "Upload Failed!")
    else:
        form = ArtPostForm()

    art_posts = ArtPost.objects.all()
    context = {
        'form': form,
        'art_posts': art_posts
    }
    return render(request, 'uploadpost.html', context)


@login_required
def messaging(request):
    user1 = request.user
    member_id = request.GET.get('member_id')
    user2 = get_object_or_404(User, id=member_id)
    
    all_conversations = Conversation.objects.filter(
        (models.Q(user1=user1) | models.Q(user2=user1))
    )

    conversation = Conversation.objects.filter(
        models.Q(user1=user1, user2=user2) | models.Q(user1=user2, user2=user1)
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(user1=user1, user2=user2)

    messages = Message.objects.filter(fk_msg=conversation).order_by('id')
    lstmessage = messages[:1]

    if request.method == 'POST':
        new_msg = request.POST.get('msg')
        if new_msg:
            Message.objects.create(
                fk_sender=user1,
                fk_msg=conversation,
                msg=new_msg
            )
            # Update messages and lstmessage after creating a new message
            messages = Message.objects.filter(fk_msg=conversation).order_by('-id')
            lstmessage = messages[:1]

    context = {
        'member1': user1,
        'member2': user2,
        'messages': messages,
        'lstmessage': lstmessage,
        'all_conversations': all_conversations
    }

    return render(request, 'messages.html', context)


def view_messages(request):
    user1 = request.user

    all_conversations = Conversation.objects.filter(
        (models.Q(user1=user1) | models.Q(user2=user1))
    )
    context = {
        'all_conversations': all_conversations
    }
    return render(request,'messages.html',context)


@login_required
def browse(request):
    filter_conditions = {
        'status': 'approved'
    }

    art_posts = ArtPost.objects.filter(**filter_conditions).order_by('-timestamp')
    paginator = Paginator(art_posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = range(1, page_obj.paginator.num_pages + 1)
    context = {
        'page_obj': page_obj,
        'num_pages': num_pages

    }
    return render(request, 'browse.html', context)



def filtering(request):
    filter_conditions = {'status': 'approved'}

    search_query = request.POST.get('search')
    category = request.POST.get('category') or request.GET.get('category')
    art_type = request.POST.get('type') or request.GET.get('type')
    min_price = request.POST.get('min_price') or request.GET.get('min_price')
    max_price = request.POST.get('max_price') or request.GET.get('max_price')

    if search_query:
        filter_conditions['title__icontains'] = search_query
    if category:
        filter_conditions['category'] = category
    if art_type:
        filter_conditions['type'] = art_type
    if min_price:
        try:
            filter_conditions['price__gte'] = int(min_price)
        except ValueError:
            pass  # ignore if conversion fails
    if max_price:
        try:
            filter_conditions['price__lte'] = int(max_price)
        except ValueError:
            pass  # ignore if conversion fails

    art_posts = ArtPost.objects.filter(**filter_conditions).order_by('-timestamp')
    paginator = Paginator(art_posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = range(1, page_obj.paginator.num_pages + 1)

    context = {
        'page_obj': page_obj,
        'num_pages': num_pages,
        'filter_conditions': filter_conditions
    }

    return render(request, 'results.html', context)


def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    return render(request, 'contact.html')


@login_required
def profile_info(request):
    user = request.user
    art_posts = ArtPost.objects.filter(user=user)
    favorites = Favorites.objects.filter(user=user)
    context = {
        'user': user,
        'art_posts': art_posts,
        'favorites': favorites,
    }

    return render(request, 'profile.html', context)


@login_required
def chats(request):
    user = request.user
    members = User.objects.all()
    return render(request, 'chats.html', {'user': user, 'members': members})


def member_details(request, member_id):
    user = get_object_or_404(User, id=member_id)
    user_art_posts = ArtPost.objects.filter(user=user)
    context = {
        'member': user,
        'art_posts': user_art_posts
    }

    return render(request, 'member_details.html', context)


def product_page(request, post_id):
    post = ArtPost.objects.get(id=post_id)
    additional_images = File.objects.filter(art=post_id)
    reviews = Review.objects.filter(art=post_id)
    context = {
        'post': post,
        'post_id': post_id,
        'additional_images': additional_images,
        'reviews': reviews
    }

    return render(request, 'product_page.html', context)


def categories(request):
    return render(request, 'categories.html')


def favorite(request, post_id):
    user = request.user
    art = ArtPost.objects.get(id=post_id)
    if Favorites.objects.filter(user=user, art=art).exists():
        messages.warning(request, 'This post is already in your favorites.')
    else:
        new_fav = Favorites(
            user=user,
            art=art
        )
        new_fav.save()
        messages.success(request, 'This post has been added to your favorites.')

    return redirect('product_page', post_id=post_id)


def review(request, post_id):
    user = request.user
    review_text = request.POST.get('review')
    art = ArtPost.objects.get(id=post_id)
    new_review = Review(
        user=user,
        art=art,
        review=review_text

    )
    new_review.save()

    return redirect('product_page', post_id=post_id)


def subscribe(request):
    email = request.POST.get('email')
    if SubscriberList.objects.filter(email=email).exists():
        messages.error(request, 'Your email is already in the subscriber list')
    else:
        new_subscriber = SubscriberList(
            email=email
        )
        new_subscriber.save()
        messages.success(request, 'Your email has been added to the subscriber list')
    return redirect('home')


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        new_username = request.POST.get('user')
        new_bio = request.POST.get('bio')
        new_profile_picture = request.FILES.get('new_pic')

        if new_username:
            user.username = new_username
        if new_bio:
            user.bio = new_bio
        if new_profile_picture:
            user.profile_picture = new_profile_picture

        user.save()
        messages.success(request, 'Your info has been changed successfully')

    context = {
        'user': user
    }
    return render(request, 'update-profile.html', context)


def settings(request):
    user = request.user
    new_fullname = request.POST.get('fullname')
    new_address = request.POST.get('address')
    new_phone = request.POST.get('phone')
    new_email = request.POST.get('email')
    billing = Billing.objects.filter(user=user)
    context = {
        'billing': billing
    }
    if new_fullname:
        user.full_name = new_fullname
    if new_address:
        user.address = new_address
    if new_phone:
        user.phone = new_phone
    if new_email:
        user.email = new_email
    user.save()
    return render(request, 'settings.html', context)


def change_pass(request):
    user = request.user
    old_pass = request.POST.get('curr_pass')
    new_pass1 = request.POST.get('pass1')
    new_pass2 = request.POST.get('pass2')
    if user.check_password(old_pass):
        if new_pass2 == new_pass1:
            user.set_password(new_pass1)
            user.save()
            messages.success(request, 'Your password was changed successfully')
        else:
            messages.error(request, "The entered Passwords don't match")

    return redirect('home')


def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart


def add_to_cart(request, post_id):
    art_post = get_object_or_404(ArtPost, id=post_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, art_post=art_post)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('product_page', post_id=post_id)


def cart_detail(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)


def remove_from_cart(request):
    cart_item_id = request.GET.get('cart_item')
    cart_item = get_object_or_404(CartItem, art_post_id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')


def update_cart(request):
    cart_item_id = request.GET.get('cart_item')
    cart_item = get_object_or_404(CartItem, art_post=cart_item_id)
    cart_item.quantity += + int(request.GET.get('quantity'))
    cart_item.save()
    return redirect('cart_detail')


def check_out(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    total = 0
    for item in cart_items:
        total += item.art_post.price * item.quantity

    context = {
        'total': total,
        'items': cart_items
    }
    return render(request, 'checkout.html', context)


def billing(request):
    user = request.user
    card = request.POST.get('card_num')

    expiry_date = request.POST.get('expiry_date')
    cvv = request.POST.get('cvv')
    address = request.POST.get('address')
    new_billing = Billing(
        user=user,
        credit_number=card,
        expiry_date=expiry_date,
        cvv=cvv,
        address=address,
    )
    new_billing.save()
    messages.success(request, 'Your billing information has been updated')
    return redirect('settings')


def success(request):
    return render(request, 'success.html')

