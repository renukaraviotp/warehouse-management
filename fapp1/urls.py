from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('loginn',views.loginn,name='loginn'),
    path('client_signup',views.client_signup,name='client_signup'),
    path('delivery_signup',views.delivery_signup,name='delivery_signup'),
    path('admin',views.admin,name='admin'),
    path('client',views.client,name='client'),
    path('delivery',views.delivery,name='delivery'),
    path('client_signup',views.client_signup,name='client_signup'),
    path('delivery_signup',views.delivery_signup,name='delivery_signup'),
    path('client_reg',views.client_reg,name='client_reg'),
    path('client_approve',views.client_approve,name='client_approve'),
    path('approval/<int:pk>',views.approval,name='approval'),
    path('disapproval/<int:pk>',views.disapproval,name='disapproval'),
    path('delivery_reg',views.delivery_reg,name='delivery_reg'),
    path('show_notification',views.show_notification,name='show_notification'),
    path('delivery_approve',views.delivery_approve,name='delivery_approve'),
    path('approvedetails',views.approvedetails,name='approvedetails'),
    path('login1',views.login1,name='login1'),
    path('logoutt',views.logoutt,name='logoutt'),
    path('admin_dashboard_view',views.admin_dashboard_view,name='admin_dashboard_view'),
    path('admin_add_product_view',views.admin_add_product_view,name='admin_add_product_view'),
    path('delete_product_view/<int:pk>',views.delete_product_view,name='delete_product_view'),
    path('update_product_view/<int:pk>',views.update_product_view,name='update_product_view'),
    path('admin_view_booking_view',views.admin_view_booking_view,name='admin_view_booking_view'),
    path('delete_order_view/<int:pk>',views.delete_order_view,name='delete_order_view'),
    path('view_customer_view',views.view_customer_view,name='view_customer_view'),
    path('delete_customer_view/<int:pk>',views.delete_customer_view,name='delete_customer_view'),
    path('view_delivery_view',views.view_delivery_view,name='view_delivery_view'),
    path('delete_delivery_view/<int:pk>',views.delete_delivery_view,name='delete_delivery_view'),
    path('delivery_assign',views.delivery_assign,name='delivery_assign'),
    path('assign/<int:pk>',views.assign,name='assign'),
    path('admin_products_view',views.admin_products_view,name='admin_products_view'),
    path('status_admin',views.status_admin,name='status_admin'),
    path('AddCart/<int:p>',views.AddCart,name='AddCart'),
    path('addplus/<int:p>',views.addplus,name='addplus'),
    path('Cart_view',views.Cart_view,name='Cart_view'),
    path('decreaser/<int:p>',views.decreaser,name='decreaser'),
    path('dele/<int:p>',views.dele,name='dele'),
    path('accnt',views.accnt,name='accnt'),
    path('orderview1',views.orderview1,name='orderview1'),
    # path('paymentt',views.paymentt,name='paymentt'),
    # path('payment_success/<int:p>',views.payment_sucess,name='payment_success'),
    path('orderview1',views.orderview1,name='orderview1'),
    path('searchh',views.searchh,name='searchh'),
    path('searchid',views.searchid,name='searchid'),
    path('receive/<int:pk>',views.receive,name='receive'),
    path('my_profile_view',views.my_profile_view,name='my_profile_view'),
    path('edit_profile_view',views.edit_profile_view,name='edit_profile_view'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('update_password',views.update_password,name='update_password'),
    path('update_deliverypass',views.update_deliverypass,name='update_deliverypass'),
    path('delivery_order',views.delivery_order,name='delivery_order'),
    path('update_order_view<int:pk>',views.update_order_view,name='update_order_view'),
    path('delivery_status',views.delivery_status,name='delivery_status'),
    path('update_status_view/<int:pk>',views.update_status_view,name='update_status_view'),
    path('delivery_profile',views.delivery_profile,name='delivery_profile'),
    path('locationn',views.locationn,name='locationn'),
    path('search_view',views.search_view,name='search_view'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)