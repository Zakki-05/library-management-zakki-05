from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal
from reportlab.pdfgen import canvas
from .models import BorrowRecord
from books.models import Book
from .forms import IssueBookForm

def is_librarian_or_admin(user):
    return user.is_authenticated and (user.is_admin() or user.is_librarian())

@login_required
@user_passes_test(is_librarian_or_admin)
def export_transactions_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="library_transactions.pdf"'
    
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Library Management System - Transaction Report")
    
    p.setFont("Helvetica", 12)
    y = 750
    records = BorrowRecord.objects.all().order_by('-borrow_date')
    
    p.drawString(50, y, "ID")
    p.drawString(100, y, "Student")
    p.drawString(200, y, "Book")
    p.drawString(400, y, "Date")
    p.drawString(500, y, "Status")
    y -= 20
    
    for record in records:
        if y < 50:
            p.showPage()
            y = 800
        p.drawString(50, y, str(record.id))
        p.drawString(100, y, record.user.username[:15])
        p.drawString(200, y, record.book.title[:30])
        p.drawString(400, y, str(record.borrow_date))
        p.drawString(500, y, record.status)
        y -= 20
        
    p.showPage()
    p.save()
    return response


@login_required
@user_passes_test(is_librarian_or_admin)
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            book = borrow_record.book
            
            if book.available_quantity > 0:
                book.available_quantity -= 1
                book.save()
                borrow_record.save()
                messages.success(request, f'Book "{book.title}" successfully issued to {borrow_record.user.username}.')
                return redirect('transactions:record_list')
            else:
                messages.error(request, 'This book is currently out of stock.')
    else:
        book_id = request.GET.get('book_id')
        initial_data = {}
        if book_id:
            initial_data['book'] = get_object_or_404(Book, pk=book_id)
        form = IssueBookForm(initial=initial_data)
        
    return render(request, 'transactions/issue_book.html', {'form': form})

@login_required
@user_passes_test(is_librarian_or_admin)
def return_book(request, record_id):
    record = get_object_or_404(BorrowRecord, pk=record_id)
    if record.status != 'RETURNED':
        record.status = 'RETURNED'
        record.return_date = timezone.now().date()
        
        # Calculate Fine (10 currency units per day late)
        if record.return_date > record.due_date:
            days_late = (record.return_date - record.due_date).days
            record.fine_amount = Decimal(days_late * 10)
            messages.warning(request, f'Book returned late. Fine amount: ${record.fine_amount}')
        else:
            messages.success(request, 'Book returned successfully on time.')
            
        record.save()
        
        # Increase book availability
        book = record.book
        book.available_quantity += 1
        book.save()
        
    return redirect('transactions:record_list')

@login_required
@user_passes_test(is_librarian_or_admin)
def record_list(request):
    records = BorrowRecord.objects.all().order_by('-borrow_date')
    return render(request, 'transactions/record_list.html', {'records': records})

@login_required
def my_borrowed_books(request):
    records = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'transactions/my_books.html', {'records': records})
