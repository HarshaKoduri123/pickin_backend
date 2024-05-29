from django.urls import path
from .views import ReadExcelView,UserRegister, UserLogin, UserLogout, BusinessTypeView, InvoiceFileUploadView, UserView, SalesFileUploadView, index

urlpatterns = [
    path('', index),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('login/', UserLogin.as_view() , name='login'),
    path('logout/', UserLogout.as_view() , name='logout'),
    path('business/', BusinessTypeView.as_view() , name='business'),
    path('user/', UserView.as_view() , name='profile'),
    path('read-excel/', ReadExcelView.as_view(), name='read_excel'),
    path('user/invoicedata/', InvoiceFileUploadView.as_view(), name='invoice-data'),
    path('user/salesdata/', SalesFileUploadView.as_view(), name='sales-data'),
]

