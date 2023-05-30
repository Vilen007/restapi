
from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,AddBookView,UpdateBookView, \
    DeleteBookView, BookView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('book/', BookView.as_view(), name='book'),
    path('addbook/', AddBookView.as_view(), name='addbook'),
    path('updatebook/<int:id>', UpdateBookView.as_view(), name='updatebook'),
    path('deletebook/<int:id>', DeleteBookView.as_view(), name='deletebook'),
]
