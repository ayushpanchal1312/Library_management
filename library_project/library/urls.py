from django.urls import path
from .views import book_list, add_book, search,update,delete,return_book

urlpatterns = [
    path('books/',book_list),
    path('add-books/',add_book),
    path('search/<int:id>/',search),
    path('update/<int:id>/',update),
    path('delete/<int:id>/',delete),
    path('return/<int:item_id>/', return_book),
]   