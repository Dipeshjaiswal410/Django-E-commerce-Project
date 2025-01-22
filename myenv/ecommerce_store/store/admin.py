from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Product, Profile, Order, Cart, CartProduct

# Register UserProfile model
#admin.site.register(UserProfile)

# Register and customize Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Display name and slug in the list view
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug based on name

# Register and customize Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'category')  # Display product details
    list_filter = ('category',)  # Filter by category
    search_fields = ('name',)  # Search by product name
    list_editable = ('price', 'stock_quantity')  # Allow price and stock updates in list view

# Register and customize Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')  # Display user-related information
    search_fields = ('user__username',)  # Search by username

# Register and customize Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')  # Display order details
    list_filter = ('status', 'created_at')  # Filter by status and creation date
    search_fields = ('user__username', 'id')  # Search by username or order ID
    readonly_fields = ('total_price', 'created_at')  # Make these fields read-only
    fieldsets = (  # Organize fields into sections
        (None, {'fields': ('user', 'order_details', 'total_price', 'status')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

# Register and customize Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the associated user
    search_fields = ('user__username',)  # Search by username

# Register and customize CartProduct model
@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  # Display cart, product, and quantity
    search_fields = ('cart__user__username', 'product__name')  # Search by username or product name
