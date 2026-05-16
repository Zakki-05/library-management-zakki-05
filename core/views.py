from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.models import Book
from users.models import User
from transactions.models import BorrowRecord
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


def home(request):
    books = Book.objects.order_by('-created_at')[:6]
    return render(request, 'core/home.html', {'latest_books': books})

@login_required
def dashboard(request):
    if request.user.is_admin() or request.user.is_librarian():
        return admin_dashboard(request)
    else:
        return student_dashboard(request)

def admin_dashboard(request):
    total_books = Book.objects.aggregate(total=Sum('total_quantity'))['total'] or 0
    total_users = User.objects.filter(role='STUDENT').count()
    issued_books = BorrowRecord.objects.filter(status='BORROWED').count()
    returned_books = BorrowRecord.objects.filter(status='RETURNED').count()
    overdue_books = BorrowRecord.objects.filter(status='OVERDUE').count()
    
    total_fine = BorrowRecord.objects.aggregate(total=Sum('fine_amount'))['total'] or 0
    recent_activities = BorrowRecord.objects.order_by('-borrow_date')[:5]
    
    # Chart Data: Last 7 days transactions
    last_7_days = []
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        count = BorrowRecord.objects.filter(borrow_date=day).count()
        last_7_days.append(day)
        chart_labels.append(day.strftime('%a'))
        chart_data.append(count)

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'issued_books': issued_books,
        'returned_books': returned_books,
        'overdue_books': overdue_books,
        'total_fine': total_fine,
        'recent_activities': recent_activities,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'core/admin_dashboard.html', context)

def student_dashboard(request):
    borrowed_books = BorrowRecord.objects.filter(user=request.user, status='BORROWED')
    total_fine = BorrowRecord.objects.filter(user=request.user).aggregate(total=Sum('fine_amount'))['total'] or 0
    recently_added = Book.objects.order_by('-created_at')[:3]
    
    context = {
        'borrowed_books': borrowed_books,
        'total_fine': total_fine,
        'recently_added': recently_added,
    }
    return render(request, 'core/student_dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
