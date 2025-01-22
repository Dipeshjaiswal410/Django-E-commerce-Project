from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm
from .models import Product, Category, Cart, CartProduct, Order
from decimal import Decimal
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.serializers import ProductSerializer, CartSerializer, OrderSerializer



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'registration/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'store/profile.html', {'user': request.user})


def product_list(request):
    query = request.GET.get('q', '')  # Get search query from the request
    category_slug = request.GET.get('category', '')  # Get category filter from the request
    products = Product.objects.all()

    # Apply search filter
    if query:
        products = products.filter(name__icontains=query)  # Search by product name

    # Apply category filter
    if category_slug:
        products = products.filter(category__slug=category_slug)  # Filter by category

    categories = Category.objects.all()  # Fetch all categories for filtering
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Fetch product by primary key or return 404
    return render(request, 'products/product_detail.html', {'product': product})


# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if product is already in the cart
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    # If product already in cart, increase quantity
    if not created:
        cart_product.quantity += 1
        cart_product.save()

    return redirect('cart')

# Update product quantity in cart
@login_required
def update_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)

    # Update quantity
    cart_product.quantity = quantity
    cart_product.save()

    return redirect('cart')

# Remove product from cart
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)

    # Remove the product from the cart
    cart_product.delete()

    return redirect('cart')

# View the cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def create_order(request):
    # Get the user's cart
    cart = Cart.objects.get(user=request.user)
    
    # Calculate the total price for the cart
    total_price = Decimal(0)
    order_details = []
    for item in cart.cartproduct_set.all():
        total_price += item.product.price * item.quantity
        order_details.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price,
            'total': item.product.price * item.quantity
        })
    
    # Create the order
    order = Order.objects.create(
        user=request.user,
        order_details=order_details,  # Store the order details
        total_price=total_price
    )
    
    # Optionally, clear the cart after the order is created
    cart.cartproduct_set.all().delete()

    # Render the order summary page
    return render(request, 'store/order_summary.html', {'order': order})



# Product Listing API
@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Product Detail API
@api_view(['GET'])
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# Cart API: Get Cart and Add Products to Cart
@api_view(['GET', 'POST'])
def cart_view(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Get Cart Details (GET request)
    if request.method == 'GET':
        serializer = CartSerializer(user_cart)
        return Response(serializer.data)

    # Add Products to Cart (POST request)
    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        # Ensure the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the product to the cart
        cart_product, created = CartProduct.objects.get_or_create(cart=user_cart, product=product)
        cart_product.quantity += quantity  # Update quantity
        cart_product.save()

        return Response({"message": "Product added to cart successfully!"}, status=status.HTTP_201_CREATED)

# Order Creation API
@api_view(['POST'])
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_products = CartProduct.objects.filter(cart=cart)

    # Prepare order details
    order_details = []
    total_price = 0
    for cart_product in cart_products:
        order_details.append({
            "product": cart_product.product.name,
            "quantity": cart_product.quantity,
            "price": cart_product.product.price,
        })
        total_price += cart_product.product.price * cart_product.quantity

    # Create order
    order = Order.objects.create(
        user=request.user,
        order_details=order_details,
        total_price=total_price
    )
    
    # Clear the cart after order creation
    cart_products.delete()

    # Serialize and return the order details
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Order Retrieval API
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
