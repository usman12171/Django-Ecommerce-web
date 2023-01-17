from django.contrib import admin
from .models import Customer,Product,cart,category,Comment,palceorder


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('user_id','user','first_name','contact','address','country','city','avatar')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('categori','categori_id','name','price','descrption','discounted_price','productcolor','product_size')

@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display=('id','product','product_id','customer','customer_id','quantity')


@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display=('name','description','category_type')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('product','customer','content','rate')


@admin.register(palceorder)
class placeorderAdmin(admin.ModelAdmin):
    list_display=('product_id','customer_id','order_date','status')