from django.shortcuts import render
from django.shortcuts import render,redirect
import random
from django.contrib import messages
from . models import Client,Delivery,Notification,Delivery1,Orders,Product,Cart
from django.shortcuts import render, get_object_or_404
from . models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from email import message
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
import os
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})

def loginn(request):
    return render(request,'login.html')

# client signup page 
def client_signup(request):
    return render(request,'client_signup.html')

# delivery signup page
def delivery_signup(request):
    return render(request,'delivery_signup.html')

# admin home page
@login_required(login_url='login1')
def admin(request):
    return render(request,'admin.html')

# client home page
@login_required(login_url='login1')
def client(request):
    products=Product.objects.all()
    user = request.user.id
    client = Client.objects.get(user_id=user)
    carts = Cart.objects.filter(customer_id=client.id)
    product_count_in_cart = carts.count()
    return render(request,'client.html',{'products':products,'product_count_in_cart': product_count_in_cart})

# delivery home page
@login_required(login_url='login1')
def delivery(request):
    return render(request,'delivery.html')

# client signup function
def client_reg(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        age = request.POST['age']
        address=request.POST['address']
        contact = request.POST['contact']
        image = request.FILES['photo'] 
        password='123'
        # password=request.POST['password']
        # password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('client_signup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email_id,user_type=user_type)
            user.save()
                
            
            member=Client(age=age,number=contact,photo=image,address=address,user=user)
            member.save()
            # subject='Your Approval has been Successfull'
            # message=f'We have received your application and the admin has approved your application. Your username and password are:\nUsername:{user_name}\nPassword:{password}'
            # recipient=email_id
            # send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return redirect('/')
                # messages.info(request, 'You have successfully registered')
          
    return render(request,'client_signup.html')

# client approve function
def client_approve(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email'] 
        contact = request.POST['contact']
        image = request.FILES['photo'] 
        address=request.POST['address']
        
        # password=request.POST['password']
        # password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return render(request,'client_signup.html') 
        else:
        
            user=Delivery1(first_name=first_name,last_name=last_name,username=user_name,email=email_id,number=contact,user_type=user_type,client=True,image=image,address=address)
            user.save() 
            a=Notification(message=f'{first_name}{last_name} is waiting for approval',sender_id=user.id)
            a.save()
            messages.info(request, 'Registered Successfully...Please wait for approval')
            return redirect('loginn')
                # messages.info(request, 'You have successfully registered')
          
    return render(request,'client_signup.html')

# def approvedetails(request):
#     a=Client1.objects.all()
#     return render(request,'approve.html',{'a':a})

def approval(request,pk):
    
    c=Delivery1.objects.get(id=pk)
    if c.client==True:
        pas=str(random.randint(100000,999999))
        use=CustomUser.objects.create_user(email=c.email,username=c.username,password=pas,first_name=c.first_name,last_name=c.last_name,user_type=c.user_type)
        usr=Client(number=c.number,photo=c.image,age=1,address=c.address) 
        c.is_approved=True
        c.save()
        s=Notification.objects.get(sender_id=pk)
        s.is_read=True 
        s.save() 
        usr.user=use 
        usr.save() 
        c.delete() 
        
        subject="Your Approval has been Successful"
        message=f'Dear {use.first_name} {use.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username: {use.username} ''\n password={}'.format(pas)
        recipient=use.email 
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        return render(request,'admin.html',locals())
    elif c.delivery==True:
        pas=str(random.randint(100000,999999))
        use=CustomUser.objects.create_user(email=c.email,username=c.username,password=pas,first_name=c.first_name,last_name=c.last_name,user_type=c.user_type)
        usr=Delivery(number=c.number,image=c.image)
        c.is_approved=True
        c.save()
        s=Notification.objects.get(sender_id=pk)
        s.is_read=True
        s.save()
        usr.user=use 
        usr.save()
        c.delete()
        subject="Your Approval has been Successful"
        message=f'Dear {use.first_name} {use.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username: {use.username} ''\n password={}'.format(pas)
        recipient=use.email 
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        return render(request,'admin.html',locals())

def disapproval(request,pk):
    a=Notification.objects.get(sender_id=pk)
    a.is_read=True
    a.save() 
    p=Delivery1.objects.get(id=pk) 
    p.delete()
    return redirect('approvedetails') 

def show_notification(request):
    s=Client.objects.all()
    d=Notification.objects.all().count()
    return render(request,'approve.html',{'s':s,'d':d}) 

# delivery approve function
def delivery_approve(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        contact = request.POST['contact']
        image = request.FILES.get('image')
        
        # password = str(random.randint(100000, 999999))
        user_type = '2'
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('delivery_signup') 
        else:
            user=Delivery1(first_name=first_name,last_name=last_name,username=user_name,email=email_id,number=contact,image=image,user_type=user_type,delivery=True)
            user.save() 
            a=Notification(message=f'{first_name}{last_name} is waiting for approval',sender_id=user.id)
            a.save()
            messages.info(request, 'Registered Successfully...Please wait for approval')
            # send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return redirect('loginn')
    return render(request,'delivery_signup.html') 

# delivery sign up original 
def delivery_reg(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        contact = request.POST['contact']
        password='123'
        image = request.FILES.get('image')
        
        # password = str(random.randint(100000, 999999))
        user_type ='2' 
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('delivery_signup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email_id,user_type=user_type)
            user.save()      
            member=Delivery(number=contact,image=image,user=user)
            member.save()
            return redirect('/')
    return render(request,'delivery_signup.html')

@login_required(login_url='login1')
def approvedetails(request):
    a=Delivery1.objects.filter(is_approved=False) 
    # count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request,'approve.html',{'a':a})

    

# login function
def login1(request):
    if request.method=='POST':
        user_name=request.POST.get('username')
        print(user_name)
        password1=request.POST.get('password')
        print(password1)
        user=authenticate(username=user_name,password=password1)
           
        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return redirect('admin') 
            elif user.user_type == '2':
                auth.login(request,user)
                return redirect('delivery')
            else:
                auth.login(request,user)
                return redirect('client')
        else:
            messages.info(request,"Invalid username or password")
            return redirect('/')
    return render(request,'login.html') 
    
def show_nofification(request):
    s=Notification.objects.all()
    return render(request,'notification.html',{'s':s})

def approveaction(request,pk):
           n=Notification.objects.get(id=pk)
           n.sender.password = str(random.radint(100000,999999))
           n.save()
           subject='Your Approval has been successful'
           message=f' Dear {n.sender.first_name}{n.sender.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username{n.sender.username} \n  password :{n.sender.password} thanku for joining'
           recipient=n.sender.email
           send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
           message.info(request,)

@login_required(login_url='login1')          
def logoutt(request):
    logout(request)
    return redirect('home')

#########################################
###########  Admin Views ################
#########################################
@login_required(login_url='login1')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=Client.objects.all().count()
    productcount=Product.objects.all().count()
    ordercount=Orders.objects.all().count()

    # for recent order tables
    orders=Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    # for order in orders:
    #     ordered_product=Product.objects.filter(id=order.product.id)
    #     ordered_by=Client.objects.all().filter(id = order.client.id)
    #     ordered_products.append(ordered_product)
    #     ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'admin.html',context=mydict)

@login_required(login_url='login1')
def admin_products_view(request):
    products=Product.objects.all()
    return render(request,'add_product.html',{'products':products})

@login_required(login_url='login1')
def admin_add_product_view(request):
    if request.method=='POST':
        pname = request.POST['pname']
        des = request.POST['des']
        price = request.POST['price']
        qty=request.POST['qty']
        image = request.FILES.get('image')
        product=Product(name=pname,description=des,price=price,pimage=image,qty=qty)
        product.save()
        return redirect('admin_products_view')
    return render(request,'add_pro.html')

@login_required(login_url='login1')
def delete_product_view(request,pk):
    product=Product.objects.get(id=pk)
    product.delete()
    return redirect('admin_products_view')


@login_required(login_url='login1')
def update_product_view(request,pk):
    product=Product.objects.get(id=pk)
    if request.method=='POST':
        product=Product.objects.get(id=pk)
        product.name=request.POST['pname']
        product.description=request.POST['des']
        product.price=request.POST['price']
        product.qty=request.POST['qty']
        if len(request.FILES)!=0:
            if len(product.pimage)>0: 
                os.remove(product.pimage.path)
            else:
                product.pimage = request.FILES['image']
            product.pimage=request.FILES['image']
        product.save()
        return redirect('admin_products_view')
    return render(request,'edit_product.html',{'prd':product})

@login_required(login_url='login1')
def admin_view_booking_view(request):
    orders = Orders.objects.all()

    # No need to manually iterate over orders to fetch related information
    # Use relationships defined in models to access related data directly in the template

    return render(request, 'listoforders.html', {'orders': orders})


@login_required(login_url='login1')
def delete_order_view(request,pk):
    order=Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin_view_booking_view')

@login_required(login_url='login1')
def view_customer_view(request):
    customers=Client.objects.all()
    return render(request,'customer.html',{'customers':customers}) 

# admin delete customer
@login_required(login_url='login1')
def delete_customer_view(request,pk):
    customer=Client.objects.get(id=pk)
    user=CustomUser.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view_customer_view')

@login_required(login_url='login1')
def view_delivery_view(request):
    delivery=Delivery.objects.all()
    return render(request,'admin_delivery.html',{'delivery':delivery})

@login_required(login_url='login1')
def delete_delivery_view(request,pk):
    delivery=Delivery.objects.get(id=pk)
    user=CustomUser.objects.get(id=delivery.user_id)
    user.delete()
    delivery.delete()
    return redirect('view_delivery_view')

@login_required(login_url='login1')
def delivery_assign(request):
    orders=Orders.objects.all()
    delivery=Delivery.objects.all()
    customer=Client.objects.all() 
    return render(request,'admin_delivery_assign.html',{'orders':orders,'delivery':delivery,'customers':customer})

@login_required(login_url='login1')
def assign(request,pk):
    o=Orders.objects.get(id=pk)
    if request.method=='POST':
        deliveryboy=request.POST['delivery']
        o.deliveryboy_id=deliveryboy
        o.save() 
        return redirect('delivery_assign') 
    
@login_required(login_url='login1')
def status_admin(request):
    s=Orders.objects.all()
    return render(request,'admin_status.html',{'s':s}) 


########################################################
########### Client Views ###############################
########################################################
def search_view(request):
    query = request.GET['query']
    products = Product.objects.filter(name__contains=query)
    if request.user.is_authenticated:
        return render(request,'client.html',{'products':products})
    return render(request,'home.html',{'products':products}) 
    
@login_required(login_url='login1')
def Cart_view(request):
    total = 0
    product_count_in_cart = 0  # Initialize product count

    try:
        user = request.user.id
        client = Client.objects.get(user_id=user)

        # Assuming there is a ForeignKey relationship from Cart to Product named 'products'
        carts = Cart.objects.filter(customer_id=client.id)
        products_in_cart = [cart.products for cart in carts]

        for item in carts:
            total += item.quantity * item.products.price

        product_count_in_cart = carts.count()

    except Client.DoesNotExist:
        products_in_cart = []

    return render(request, 'Cart.html', {'cart': carts, 'total': total, 'product_count_in_cart': product_count_in_cart})

@login_required(login_url='login1')
def AddCart(request, p):
    product = Product.objects.get(id=p)
    user = request.user.id
    a = Client.objects.get(user_id=user)

    try:
        cart_entry = Cart.objects.get(products=product, products_id=product.id, customer_id=a.id)
        messages.info(request, product.name + ' added to cart successfully!')
        if cart_entry.quantity < cart_entry.products.qty:
            cart_entry.quantity += 1
            cart_entry.save()
    except Cart.DoesNotExist:
        cart_entry = Cart.objects.create(products=product, quantity=1, products_id=product.id, customer_id=a.id)
        messages.info(request, product.name + ' added to cart successfully!')
        cart_entry.save()

    return redirect('client')  # Redirect to the Cart view after adding to the Cart


@login_required(login_url='login1')
def addplus(request, p):
    product = Product.objects.get(id=p)
    user = request.user.id
    a = Client.objects.get(user_id=user)

    try:
        cart_entry = Cart.objects.get(products=product, products_id=product.id, customer_id=a.id)
        if cart_entry.quantity < cart_entry.products.qty:
            cart_entry.quantity += 1
            cart_entry.save()
    except Cart.DoesNotExist:
        cart_entry = Cart.objects.create(products=product, quantity=1, products_id=product.id, customer_id=a.id)
        cart_entry.save()

    return redirect('Cart_view')  # Redirect to the Cart view after adding to the Cart


@login_required(login_url='login1')
def decreaser(request,p):
    product = Product.objects.get(id=p)
    user=request.user.id
    try:
      Cartitem=Cart.objects.get(products=product,products_id=product.id)
      if Cartitem.quantity>1:
         Cartitem.quantity-=1
         Cartitem.save()
      else:
          Cartitem.delete()
    except:
        pass
    return redirect('Cart_view')

@login_required(login_url='login1')
def dele(request,p):
    product = Product.objects.get(id=p)
    user=request.user
    try:
       item= Cart.objects.get(products=product,products_id=product.id)
       item.delete()
    except:
        pass
    return redirect('Cart_view')

@login_required(login_url='login1')
def accnt(request):
    total=0
    items=0
    msg=0
    if (request.method=='POST'):
        a = request.POST['a']
        ph = request.POST['p']
        delivery = request.POST['delivery']
        user=request.user.id
        c=Client.objects.get(user_id=request.user.id)
        cart=Cart.objects.all()
        pas=str(random.randint(100000,999999))
        for i in cart:
            total +=i.quantity*i.products.price
            items +=i.quantity
            for i in cart:
                o = Orders.objects.create(client_id=c.id, product=i.products, address=a, mobile=ph, status="Pending",
                                         noofitems=i.quantity,deliverymethod=delivery,tracking_id=pas)
                o.save()
            cart.delete()
            subject="Your Order is placed"
            message=f'Dear Sir/Madam, \n We have received your Order. ''\n Here is your tracking ID :{}'.format(pas)
            recipient=c.user.email 
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return render(request, 'payment_success.html', {'msg': msg, 'total': total, 'items': items})
    return render(request, 'address.html')

@login_required(login_url='login1')
def orderview1(request):
    customer=Client.objects.get(user_id=request.user.id)
    orders=Orders.objects.all().filter(client_id = customer)
    user = request.user.id
    client = Client.objects.get(user_id=user)
    carts = Cart.objects.filter(customer_id=client.id)
    product_count_in_cart = carts.count()
    ordered_products=[]
    for order in orders:
        ordered_product=Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product) 

    return render(request,'myorder.html',{'data':zip(ordered_products,orders),'product_count_in_cart': product_count_in_cart})


@login_required(login_url='login1')
def searchh(request):
    user = request.user.id
    client = Client.objects.get(user_id=user)
    carts = Cart.objects.filter(customer_id=client.id)
    product_count_in_cart = carts.count()
    # o=Orders.objects.filter(tracking_id=pk)
    return render(request,'search.html',{'product_count_in_cart': product_count_in_cart}) 


@login_required(login_url='login1')
def searchid(request):
    product_count_in_Cart=Cart.objects.all().count()
    abc = Cart.objects.values('products').annotate(total_count=Count('products'))
    query=request.GET['search'] 
    order=Orders.objects.filter(tracking_id=query) 
    return render(request,'search.html',{'order':order,'product_count_in_Cart':product_count_in_Cart,'abc':abc})

@login_required(login_url='login1')
def receive(request,pk):
    o=Orders.objects.get(id=pk)
    oo=Orders.objects.filter(id=pk)
    if request.method=='POST':
        receive=request.POST['receive']
        if receive=='receive':
            o.is_receive=True
            o.save() 
            return render(request,'search.html',{'order':oo}) 
        elif receive=='pending':
            o.is_receive=False
            o.save() 
            return render(request,'search.html',{'order':oo})
        else:
            return redirect('searchh')

# def paymentt(request):
#     return render(request,'payment.html')

# def payment_sucess(request,p):
#     c=Client.objects.get(user_id=request.user.id)
#     product = Product.objects.get(id=p)
#     pas=str(random.randint(100000,999999)) 
#     item= Cart.objects.get(products=product,products_id=product.id)
#     item.delete()
#     subject="Your Order is placed"
#     message=f'Dear Sir/Madam, \n We have received your Order. ''\n Here is your tracking ID :{}'.format(pas)
#     recipient=c.user.email 
#     send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
#     return render(request,'payment_success.html') 



@login_required(login_url='login1')
def my_profile_view(request):
    user = request.user.id
    client = Client.objects.get(user_id=user)
    carts = Cart.objects.filter(customer_id=client.id)
    product_count_in_cart = carts.count()
    customer=Client.objects.get(user_id=request.user.id)
    return render(request,'my_profile.html',{'customer':customer,'product_count_in_cart': product_count_in_cart})


@login_required(login_url='login1') 
def edit_profile_view(request):
    c=Cart.objects.all().count()
    customer=Client.objects.get(user_id=request.user.id) 
    # user=CustomUser.objects.get(id=customer.user_id)
    nam = request.user.first_name
    lname = request.user.last_name
    username = request.user.username
    age = customer.age
    email = request.user.email
    add = customer.address
    photo = customer.photo
    number=customer.number
    context = {
        'photo':photo,'name':nam,'age':age,'mail':email,'address':add,'lname':lname,'username':username,'number':number,'product_count_in_Cart':c
    }
    return render(request,'edit_profile.html',context)

@login_required(login_url='login1')
def update_profile(request):
    if request.method == 'POST':
        usr = CustomUser.objects.get(id=request.user.id)
        tec = Client.objects.get(user_id=request.user.id)
        usr.first_name = request.POST['fname']
        usr.last_name = request.POST['lname']
        usr.username = request.POST['uname']
        usr.email = request.POST['email']
        tec.address = request.POST['address']
        tec.age = request.POST['age']
        tec.number = request.POST['contact']
        if len(request.FILES)!=0:
            if len(tec.photo)>0: 
                os.remove(tec.photo.path)
            else:
                tec.photo = request.FILES['photo']
            tec.photo=request.FILES['photo'] 
        usr.save()
        tec.save()
        return redirect('my_profile_view') 
    
@login_required(login_url='login1')
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Ensure the user is authenticated before checking the password
        if request.user.is_authenticated:

            if request.user.check_password(current_password):
                
                if new_password == confirm_new_password:
                    
                    request.user.set_password(new_password)
                    request.user.save()

                    update_session_auth_hash(request, request.user)

                    messages.success(request, 'Your password was successfully updated!')
                    return render(request,'reset_paswd.html')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Incorrect current password.')
        else:
            messages.error(request, 'User is not authenticated.')  # Add an appropriate message

    return render(request, 'reset_paswd.html')

@login_required(login_url='login1')
def update_deliverypass(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Ensure the user is authenticated before checking the password
        if request.user.is_authenticated:

            if request.user.check_password(current_password):
                
                if new_password == confirm_new_password:
                    
                    request.user.set_password(new_password)
                    request.user.save()

                    update_session_auth_hash(request, request.user)

                    messages.success(request, 'Your password was successfully updated!')
                    return render(request,'reset_delivery.html') 
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Incorrect current password.')
        else:
            messages.error(request, 'User is not authenticated.')  # Add an appropriate message

    return render(request, 'reset_delivery.html')


#################################################################
#------------Delivery module views------------------------------#
#################################################################
@login_required(login_url='login1')
def delivery_order(request):
    orders=Orders.objects.all()
    # ordered_products=[] 
    # ordered_bys=[] 
    # for order in orders:
    a=Delivery.objects.get(user_id=request.user.id)
    d=Orders.objects.filter(deliveryboy_id=a.id)
    return render(request,'delivery_order.html',{'d':d})
        # ordered_product=Product.objects.all().filter(id=order.product.id)
        # ordered_by=Client.objects.all().filter(id = order.client.id)
        # ordered_products.append(ordered_product)
        # ordered_bys.append(ordered_by)
    # return render(request,'delivery_order.html',{'data':zip(ordered_products,ordered_bys,orders,d)}) 

@login_required(login_url='login1')
def update_order_view(request,pk):
    order=Orders.objects.get(id=pk) 
    if request.method=='POST':
        status=request.POST['status']
        order.status=status
        order.save() 
        return redirect('delivery_order') 
    return render(request,'status_update.html',{'order':order})

@login_required(login_url='login1')    
def delivery_status(request):
    orders=Orders.objects.all()
    ordered_products=[] 
    ordered_bys=[]
    for order in orders:
        ordered_product=Product.objects.all().filter(id=order.product.id)
        ordered_by=Client.objects.all().filter(id = order.client.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'delivery_status.html',{'data':zip(ordered_products,ordered_bys,orders)})

@login_required(login_url='login1')
def locationn(request,pk):
    order=Orders.objects.get(id=pk)
    if request.method == 'POST':
        location = request.POST['locationn']
        order.place = location
        order.save()
        return redirect('delivery_order')  
    return render(request,'delivery_order.html',{'order':order})
    

@login_required(login_url='login1')
def update_status_view(request,pk):
    order=Orders.objects.get(id=pk) 
    if request.method=='POST':
        status=request.POST['status']
        order.status=status
        order.save() 
        return redirect('delivery_order')
    return render(request,'delivery_status_update.html',{'order':order}) 

@login_required(login_url='login1')
def delivery_profile(request):
    delivery=Delivery.objects.get(user_id=request.user.id)
    return render(request,'delivery_profile.html',{'delivery':delivery})

