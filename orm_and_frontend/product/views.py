from django.shortcuts import render
from product.models import ProductTable,CartTable
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q

# Create your views here.

def register_user(request):
    data = {}
    if request.method == "POST":
        uname = request.POST['username']
        pswd = request.POST['password']
        cpswd = request.POST['password2']
        if uname == '' or pswd == '' or cpswd == '':
            data['error_msg']='fields cannot be empty'
            return render(request,'myapp/register.html',context=data)
        elif pswd!=cpswd:
            data['error_msg']='password not matched'
            return render(request,'myapp/register.html',context=data)
        elif User.objects.filter(username=uname).exists():
            data['error_msg']=uname + ' already exists'
            return render(request,'myapp/register.html',context=data)
        else:
            user =User.objects.create(username = uname)
            user.set_password(pswd)
            user.save()
            # return HttpResponse("Registration Done")
            return redirect('/user/login')
    return render(request,'myapp/register.html')

def login_user(request):
    data = {}
    if request.method == "POST":
        uname = request.POST['username']
        pswd = request.POST['password']
        if uname == '' or pswd == '':
            data['error_msg']='fields cannot be empty'
            return render(request,'myapp/login.html',context=data)
        
        elif not User.objects.filter(username=uname).exists():
            data['error_msg']=uname + ' user is not registered'
            return render(request,'myapp/login.html',context=data)
        
        else:
            user = authenticate(username=uname,password=pswd)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('/product/product')
            else:
                data['error_msg']='wrong password'
                return render(request,'myapp/login.html',context=data)
    return render(request,'myapp/login.html')

def home(request):
    # user_id =request.user.id
    # user=User.objects.get(id=user_id)
    # print(user_id)
    # return render(request,'myapp/home.html',{'user':user})
    data= {}
    user_authen = request.user.is_authenticated
    # print(user_authen)
    if user_authen:
        user_id =request.user.id
        user=User.objects.get(id=user_id)
        # print(user_id)
        data['user_data']=user.username
        return render(request,'myapp/home.html',context=data)
    else:
        data['user_data']="not logged in"
        return render(request,'myapp/home.html',context=data)
    
def u_logout(request):
    logout(request)
    return render(request,'myapp/login.html',{'user_data':'User'})

# -------------------------------------------------------------------------------------------------------------------

def product(request):
    data ={}
    fetched_products = ProductTable.objects.filter(is_active = True)
    data['products'] = fetched_products
    user_id = request.user.id
    id_specific_cartitems = CartTable.objects.filter(uid=user_id)
    count=id_specific_cartitems.count()
    data['cart_count']=count
    return render(request,'product/product.html',context=data)

def filter_by_category(request,category_value):
    data ={}
    q1 = Q(is_active=True)
    q2 = Q(category = category_value)
    filtered_product=ProductTable.objects.filter(q1 & q2)
    data['products'] = filtered_product
    return render(request,'product/product.html',context=data)

def sort_by_price(request,sort_value):
    data ={}
    if sort_value == 'asc':
        price = 'price'
    else:
        price = '-price'
    sorted_products=ProductTable.objects.filter(is_active = True).order_by(price)
    data['products'] = sorted_products
    return render(request,'product/product.html',context=data)

def sort_by_rating(request,rate_value):
    data ={}
    q1 = Q(is_active=True)
    q2 = Q(rating__gte= rate_value)
    rated_products=ProductTable.objects.filter(q1 & q2)
    data['products'] = rated_products
    return render(request,'product/product.html',context=data)

def sort_by_price_range(request):
    data ={}
    min = request.GET['min']
    max = request.GET['max']
    q1 = Q(is_active=True)
    q2 = Q(price__gte= min)
    q3 = Q(price__lte= max)
    range_products=ProductTable.objects.filter(q1 & q2 & q3)
    data['products'] = range_products
    return render(request,'product/product.html',context=data)

def product_detail(request,pid):
    product = ProductTable.objects.get(id=pid)
    return render(request,'product/self.html',{'product':product})

# _______________________________________________________30/1/2024____________________________________________________________________________
def add_to_cart(request,pid):
    if request.user.is_authenticated:
        uid = request.user.id
        print("user id = " , uid)
        print("product id = " , pid)
        user = User.objects.get(id=uid)
        product = ProductTable.objects.get(id=pid)
        cart = CartTable.objects.create(pid=product,uid=user)
        cart.save()
        # return HttpResponse("product added sucessfully")
        # return render(request,'product/product.html')
        return redirect("/product/product")
    else:
        return redirect("/user/login")
    
def cart_data(request):
    # user = CartTable.objects.all()
    data = {}
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    id_specific_cartitems = CartTable.objects.filter(uid=user_id)
    # product = CartTable.objects.all()
    data['products']=id_specific_cartitems
    data['user']=user

    count = id_specific_cartitems.count()
    data['cart_count']=count
    total_price = 0
    for item in id_specific_cartitems:
        total_price+=item.pid.price
        data['total_price']=total_price
    return render(request,"product/cart.html",context=data)

def remove_item(request,cartid):
    cart = CartTable.objects.get(id=cartid)
    cart.delete()
    return redirect('/product/cartview')

def search_by_sku(request):
    data = {}
    sku = request.GET.get('sku', '',)
    if sku:
        q1 = Q(sku__icontains=sku)
        q2 = Q(is_active=True)
        filter_products = ProductTable.objects.filter(q1 & q2)
        data['products'] = filter_products
    else:
        data['products'] = []
    return render(request, 'product/product.html', context=data)




