from django.contrib import admin
from library.models import Book,LibraryMember,LibraryTransaction,TransactionItem,LibrarySettings

# Register your models here.
admin.site.register(Book)
admin.site.register(LibraryMember)
admin.site.register(LibraryTransaction)
admin.site.register(TransactionItem)
admin.site.register(LibrarySettings)
