from django.urls import path
from .views import ProductsView,UserRegister, UserLogin, UserLogout, BusinessTypeView, InvoiceView, UserView, SalesView, index, MessageView

urlpatterns = [
    path('', index),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('login/', UserLogin.as_view() , name='login'),
    path('logout/', UserLogout.as_view() , name='logout'),
    path('business/', BusinessTypeView.as_view() , name='business'),
    path('user/', UserView.as_view() , name='profile'),
    path('products/', ProductsView.as_view(), name='read_excel'),
    path('user/invoicedata/', InvoiceView.as_view(), name='invoice-data'),
    path('user/salesdata/', SalesView.as_view(), name='sales-data'),
    path('messages/', MessageView.as_view(), name='message-view'),
]

