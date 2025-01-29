from django.contrib import admin


from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'address')







@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'tags', 'weight', 'author')  # Fields to display in the list view
    search_fields = ('name', 'category', 'tags')  # Fields to search in the admin interface
    list_filter = ('category', 'tags')  # Fields to filter by in the admin interface
    ordering = ('-price',)  # Default ordering of products by price (descending)

    # To customize the form layout in the admin interface
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'category', 'tags', 'image', 'weight', 'author')
        }),
    )
    # If you want to include image preview in the admin interface
    def image_tag(self, obj):
        if obj.image:
            return '<img src="%s" width="100" height="100"/>' % obj.image.url
        return 'No image'
    image_tag.allow_tags = True
    image_tag.short_description = 'Image Preview'

    # Adding custom methods to the list display
    list_display = ('name', 'price', 'category', 'tags', 'weight', 'image_tag')

    # Customizing the form layout in the add/edit view
    add_fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'category', 'tags', 'image', 'weight')
        }),
    )







admin.site.register(Category)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status', 'total_amount')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'title', 'created_at')




# ForumPost Admin
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'views')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# Reply Admin
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('post__title', 'author__username', 'content')
    list_filter = ('created_at',)
    ordering = ('created_at',)



# Register models to the admin site
admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(Reply, ReplyAdmin)



admin.site.register(FarmerPost)
admin.site.register(Donation)



@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'address', 'phone', 'email', 'transaction_number', 'transaction_id')
