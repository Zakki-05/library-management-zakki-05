import qrcode
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Book, Category, Wishlist
from .forms import BookForm

def is_librarian_or_admin(user):
    return user.is_authenticated and (user.is_admin() or user.is_librarian())

@user_passes_test(is_librarian_or_admin)
def book_qr_code(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Generate QR code pointing to the book detail page
    url = request.build_absolute_uri(book.get_absolute_url())
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def toggle_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=book)
    
    if not created:
        wishlist_item.delete()
        messages.info(request, f'"{book.title}" removed from your wishlist.')
    else:
        messages.success(request, f'"{book.title}" added to your wishlist.')
    
    return redirect('books:detail', pk=pk)

@login_required
def my_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'books/wishlist.html', {'wishlist': wishlist})



def book_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query) | 
            Q(isbn__icontains=query)
        )
    
    if category_id:
        books = books.filter(category_id=category_id)
        
    if sort_by == 'latest':
        books = books.order_by('-created_at')
    elif sort_by == 'available':
        books = books.filter(available_quantity__gt=0)
        
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

@user_passes_test(is_librarian_or_admin)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('books:list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@user_passes_test(is_librarian_or_admin)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('books:detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@user_passes_test(is_librarian_or_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('books:list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
