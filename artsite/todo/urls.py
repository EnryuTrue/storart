from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginuser, name='loginuser'),

    path('signup/', views.signup, name='signup'),

    path('chats/', views.chats, name='chats'),

    path('logout/', views.logoutuser, name='logoutuser'),

    path('delete_account/', views.confirm_delete_account, name='confirm_delete_account'),

    path('delete_account/delete/', views.delete_account, name='delete_account'),

    path('member/<int:member_id>/', views.member_details, name='member_details'),

    path('find_account/', views.find_account, name='find_account'),

    path('change_password/', views.change_password, name='change_password'),

    path('upload/', views.lounge, name='lounge'),

    path('mesaging/', views.messaging, name='messaging'),

    path('browse/', views.browse, name='browse'),

    path('results/', views.filtering, name='filtering'),

    path('aboutus/', views.aboutus, name='aboutus'),

    path('contact/', views.contact, name='contact'),

    path('profile/', views.profile_info, name='profile_info'),

    path('product_page/<int:post_id>/', views.product_page, name='product_page'),

    path('categories/', views.categories, name='categories'),

    path('favorites/<int:post_id>/', views.favorite, name='favorite'),

    path('review/<int:post_id>/', views.review, name='review'),

    path('subscribe/', views.subscribe, name='subscribe'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('settings/', views.settings, name='settings'),

    path('change_pass/', views.change_pass, name='change_pass'),

    path('add_to_cart/<int:post_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart_detail/', views.cart_detail, name='cart_detail'),

    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    path('update_cart/', views.update_cart, name='update_cart'),

    path('checkout/', views.check_out, name='check_out'),

    path('billing/', views.billing, name='billing'),

    path('view_messages/', views.view_messages, name='view_messages'),

    path('payment_successful', views.success, name='success'),





]

