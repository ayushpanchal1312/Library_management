from rest_framework import serializers
from .models import Book,  LibraryTransaction, TransactionItem, LibraryMember

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class LibraryMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryMember
        fields =  '__all__'
        
class TransectionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = ['book']

class LibraryTransectionSerializer(serializers.ModelSerializer):
    
    items = TransectionItemSerializer(many=True)

    class Meta:
        model = LibraryTransaction
        fields = ['id','member_link','due_date','items']

    def create(self,validate_data):

            item_data = validate_data.pop('items')
            member = validate_data['member_link']

            # rule 1 (unpaid fines)
            if member.total_unpaid_fines > 50:
                raise serializers.ValidationError("Member has unpaid fines above limit")
            
            # rule 2
            issued_book = TransactionItem.objects.filter(
                transaction__member_link=member,
                return_date__isnull=True
            ).count()

            if issued_book + len(item_data) >= 3:
                raise serializers.ValidationError("Maximum 3 books allowed")
            
            # transection
            transection = LibraryTransaction.objects.create(
                **validate_data
            )

            for item in item_data:

                book = item['book']

                if book.status != 'Available':
                    raise serializers.ValidationError(
                        f"{book.title} not Available"
                    )
                TransactionItem.objects.create(
                    transaction=transection,
                    book=book
                )

                book.status = "Issued"
                book.save()

            return transection