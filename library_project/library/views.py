from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .serializers import LibraryTransectionSerializer
from .serializers import LibraryMemberSerializer
from .models import Book , TransactionItem , LibrarySettings,LibraryMember
from django.utils import timezone

@api_view(['POST'])
def add_member(request):
    Serializer = LibraryMemberSerializer(data=request.data)
    if Serializer.is_valid():
        Serializer.save()
        return Response(Serializer.data,status=status.HTTP_201_CREATED)
    return Response(Serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def available_books(request):
    author = request.GET.get('author')

    books = Book.objects.filter(
        author=author,
        status="Available"
    )

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update(request,id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book details updated"},status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response({"error:Book not found"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def search(request,id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({"error:Book Not Found"},status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete(request,id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return Response( {"message": "Book deleted successfully"},status=status.HTTP_201_CREATED)
    except Book.DoesNotExist:
        return Response({"error:Book not found"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def issue_book(request):
    serializer = LibraryTransectionSerializer(data=request.data )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors,status=400)

@api_view(['POST'])
def return_book(request,item_id):
    try:
        item = TransactionItem.objects.get(id=item_id)
    except TransactionItem.DoesNotExist:
        return Response({"error":"Transection item not found"},status=status.HTTP_404_NOT_FOUND)
    
    if item.return_date:
        return Response({"message":"Book already return"})
    
    today = timezone.now().date()
    item.return_date = today

    transaction = item.transaction
    member = transaction.member_link

    settings = LibrarySettings.objects.first()

    fine = 0

    if today > transaction.due_date:
        overdue_days = (today - transaction.due_date).days
        fine = overdue_days * settings.daily_fine_amount

        item.fine_amount = fine

        member.total_unpaid_fines += fine
        member.save()

    item.save()

    book = item.book
    book.status = "Available"
    book.save()

    return Response({"message": "Book returned successfully","fine": fine})