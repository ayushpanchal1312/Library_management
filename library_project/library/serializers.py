from rest_framework import serializers
from .models import Book, LibraryMember, LibraryTransaction, TransactionItem, LibrarySettings

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class TransectionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        feilds = ['book']

class LibraryTransectionSerializer(serializers.ModelSerializer):
    
    item = TransectionItemSerializer(many=True)

    class Meta:
        model = LibraryTransaction
        feilds = ['id','posting_date','due_date','created_at','member_link_id']

        def create(self,validate_data):

            item_data = validate_data.pop('items')
            member = validate_data['membership_id']

            # rule 1 (unpaid fines)
            if member.total_unpaid_fines > 50:
                raise serializers.ValidationError(
                    "Member has unpaid fines above limit"
                )
            
            # rule 2
            issued_book = TransactionItem.objects.filter(
                transection_member = member,
                transection_due_data_isnull = False
            ).count()

            if issued_book + len(item_data) > 3:
                raise serializers.ValidationError(
                    "Maximum 3 books allowed"
                )
            
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
                    transection=transection,
                    book=book
                )

                book.status = "Issued"
                book.save()

            return transection