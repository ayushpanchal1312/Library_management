from django.db import models

# Create your models here.
class Book(models.Model):
    STATUS_CHOICES=[
        ('Available','Available'),
        ('Issued','Issued'),
        ('Maintenance','Maintenance')
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200,unique=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )
    
    valuation_rate=models.DecimalField(max_digits=10,decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LibraryMember(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(unique=True)
    membership_id = models.CharField(max_length=100,unique=True)
    total_unpaid_fines=models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.full_name

class LibraryTransaction(models.Model):
    member_link = models.ForeignKey(
        LibraryMember,
        on_delete=models.CASCADE
    )
    posting_date = models.DateField(auto_now_add=True)
    due_date= models.DateField()

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Transection{self.id}"

class TransactionItem(models.Model):

    transaction = models.ForeignKey(
        LibraryTransaction,
        related_name="items",
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.book.title
    

class LibrarySettings(models.Model):

    max_loan_period = models.IntegerField(
        help_text="Maximum loan period (days)"
    )

    daily_fine_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Library Settings"