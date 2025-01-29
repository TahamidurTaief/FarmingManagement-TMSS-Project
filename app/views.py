from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
from django.http import JsonResponse
import json
from django.contrib import messages



# Create your views here.


def home(request):
    products = Product.objects.all()[:6]

    context = {
        'products': products
    }
    return render(request, 'pages/index.html', context)




def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    rating_range = range(1, 6)  # 1 through 5 stars
    context = {
        'product': product,
        'similar_products': similar_products,
        'rating_range': rating_range,
    }
    return render(request, 'pages/product_detail.html', context)





def allProducts(request):
    # Retrieve all categories for the sidebar filter
    categories = Category.objects.all()
    
    # Get selected category and price range from request
    selected_category = request.GET.get('category')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 1000000)
    
    # Filter products based on selected category and price range
    products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    if selected_category:
        products = products.filter(category__id=selected_category)
    
    # Pass data to the template
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price
    }
    return render(request, 'pages/all_products.html', context)






@login_required
def upload_product(request):
    if request.user:
        categories = Category.objects.all()
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            category = request.POST.get('category')
            tags = request.POST.get('tags')
            weight = request.POST.get('weight')
            image = request.FILES.get('image')
            author = request.user

            Product.objects.create(
                name=name,
                price=price,
                description=description,
                category_id=category,
                tags=tags,
                weight=weight,
                image=image,
                author = author
            )

            return redirect('home')
        else:
            return render(request, 'include/navbar.html', {'categories': categories})
    else:
        return redirect('home')





@login_required
def my_products(request):
    if request.user:
        # Fetch the products uploaded by the logged-in farmer
        products = Product.objects.filter(user=request.user)
        return render(request, 'include/navbar.html', {'products': products})
    else:
        return redirect('home')



@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, author=request.user)  # Ensure author is used correctly
    product.delete()
    return redirect('home')










@login_required
def forum_home(request):
    posts = ForumPost.objects.all()
    return render(request, 'forum/forum_home.html', {'posts': posts})

@login_required
def new_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post = ForumPost(title=title, content=content, author=request.user)
            post.save()
            return redirect('forum_home')
    return render(request, 'forum/new_post.html')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            reply = Reply(post=post, content=content, author=request.user)
            reply.save()
            return redirect('post_detail', post_id=post.id)
    
    return render(request, 'forum/post_detail.html', {'post': post})


@login_required
def forum(request):
    posts = ForumPost.objects.all()  # Retrieve all posts
    context = {
        'posts': posts
    }
    return render(request, 'pages/forum.html', context)

# View to return full content of a post
@login_required
def post_content(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    return JsonResponse({
        'full_content': post.content
    })

# View to return truncated content of a post
@login_required
def post_truncate(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    return JsonResponse({
        'truncated_content': post.content[:100] + '...'  # Truncate to 100 characters
    })







# View to handle post replies

def post_reply(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)

    if request.method == 'POST':
        reply_content = request.POST.get('reply_content')

        if reply_content:
            # Create new reply
            Reply.objects.create(
                post=post,
                author=request.user,
                content=reply_content
            )

            # Redirect to the same page to display the reply
            return redirect('forum')
        else:
            # Add error message if reply content is empty
            error = "Content cannot be empty."
            return render(request, 'pages/forum.html', {'post': post, 'error': error})

    return render(request, 'pages/forum.html', {'post': post})






@login_required
def add_forum_question(request):
    if request.method == 'POST':
        question_content = request.POST.get('forum_question')
        title = request.POST.get('title')

        if question_content:
            ForumPost.objects.create(
                title=title,  # Title should be a truncated version of the content
                content=question_content,
                author=request.user
            )
            return redirect('forum')  # Redirect to the forum page or a success page
        else:
            # Handle empty content case
            return render(request, 'forum.html', {'error': 'Content cannot be empty.'})

    return render(request, 'forum.html')












def farmer_posts(request):
    posts = FarmerPost.objects.all()
    return render(request, 'pages/farmer_posts.html', {'posts': posts})

def donation_page(request, post_id):
    post = get_object_or_404(FarmerPost, id=post_id)

    if request.method == 'POST':
        donor_name = request.POST.get('donor_name')
        donor_phone = request.POST.get('donor_phone')
        donor_email = request.POST.get('donor_email')
        donation_amount = request.POST.get('donation_amount')
        transaction_id = request.POST.get('transaction_id')

        if donor_name and donor_phone and donor_email and donation_amount and transaction_id:
            donation = Donation.objects.create(
                farmer_post=post,
                donor_name=donor_name,
                donor_phone=donor_phone,
                donor_email=donor_email,
                donation_amount=donation_amount,
                transaction_id=transaction_id
            )
            return redirect('farmer_posts')

    return render(request, 'donation_page.html', {'post': post})









def donation_page(request, post_id):
    post = get_object_or_404(FarmerPost, id=post_id)

    if request.method == 'POST':
        donor_name = request.POST.get('donor_name')
        donor_phone = request.POST.get('donor_phone')
        donor_email = request.POST.get('donor_email')
        donation_amount = request.POST.get('donation_amount')
        transaction_id = request.POST.get('transaction_id')

        if donor_name and donor_phone and donor_email and donation_amount and transaction_id:
            donation = Donation.objects.create(
                farmer_post=post,
                donor_name=donor_name,
                donor_phone=donor_phone,
                donor_email=donor_email,
                donation_amount=donation_amount,
                transaction_id=transaction_id
            )
            return redirect('farmer_posts')

    return render(request, 'pages/donation_page.html', {'post': post})








@login_required
def add_donation_post(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            # Create a new FarmerPost object for the donation post
            post = FarmerPost.objects.create(
                author=request.user,
                title=title,
                content=content
            )
            messages.success(request, "Donation post created successfully.")
            return redirect('farmer_posts')  # Redirect to a page showing all posts
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'add_donation_post.html')  # Ensure you have this template set up









@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        transaction_number = request.POST.get('transaction_number')
        transaction_id = request.POST.get('transaction_id')

        # Save checkout details
        Checkout.objects.create(
            product=product,
            full_name=full_name,
            address=address,
            phone=phone,
            email=email,
            transaction_number=transaction_number,
            transaction_id=transaction_id,
            user=request.user
        )

        return redirect('homes')  # After checkout, redirect to success page

    return render(request, 'pages/checkout.html', {'product': product})



def checkout_success(request):
    return render(request, 'pages/checkout_success.html')