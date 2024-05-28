from django.urls import path
from .views import ReadExcelView,UserRegister, UserLogin, UserLogout, BusinessTypeView, UserFileUploadView, UserView, index

urlpatterns = [
    path('', index),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('login/', UserLogin.as_view() , name='login'),
    path('logout/', UserLogout.as_view() , name='logout'),
    path('business/', BusinessTypeView.as_view() , name='business'),
    path('user/', UserView.as_view() , name='profile'),
    path('read-excel/', ReadExcelView.as_view(), name='read_excel'),
    path('user/upload-file/', UserFileUploadView.as_view(), name='user-upload-file'),
]

