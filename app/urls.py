
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_details'),
    path('products/', views.allProducts, name='all_products'),
    path('upload-product/', views.upload_product, name='upload_product'),

    path('my-products/', views.my_products, name='my_products'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('new/post/', views.new_post, name='new_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    path('forum/', views.forum, name='forum'),  # Main forum view
    path('post/<int:post_id>/content/', views.post_content, name='post_content'),  # AJAX to get full post content
    path('post/<int:post_id>/truncate/', views.post_truncate, name='post_truncate'),  # AJAX to get truncated post content
    path('post/<int:post_id>/reply/', views.post_reply, name='post_reply'),  # AJAX to post a reply
    path('add-question/', views.add_forum_question, name='add_forum_question'),



    path('donation', views.farmer_posts, name='farmer_posts'),
    path('donate/<int:post_id>/', views.donation_page, name='donation_page'),
    path('add-donation-post/', views.add_donation_post, name='add_donation_post'),


    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('checkout-success/', views.checkout_success, name='checkout_success'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)