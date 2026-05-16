import os
import django
from datetime import timedelta
from django.utils import timezone

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from books.models import Category, Author, Book
from transactions.models import BorrowRecord

def populate():
    print("Creating users...")
    # Admin User
    admin, _ = User.objects.get_or_create(
        username='admin', 
        defaults={
            'email': 'admin@library.com', 
            'role': 'ADMIN', 
            'is_superuser': True, 
            'is_staff': True,
            'first_name': 'System',
            'last_name': 'Admin'
        }
    )
    admin.set_password('admin123')
    admin.save()
    
    # Librarian User
    librarian, _ = User.objects.get_or_create(
        username='librarian', 
        defaults={
            'email': 'librarian@library.com', 
            'role': 'LIBRARIAN',
            'first_name': 'Sarah',
            'last_name': 'Connor'
        }
    )
    librarian.set_password('lib123')
    librarian.save()
    
    # Student Users
    student1, _ = User.objects.get_or_create(
        username='student1', 
        defaults={
            'email': 'student1@university.com', 
            'role': 'STUDENT',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    )
    student1.set_password('student123')
    student1.save()
    
    student2, _ = User.objects.get_or_create(
        username='student2', 
        defaults={
            'email': 'student2@university.com', 
            'role': 'STUDENT',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
    )
    student2.set_password('student123')
    student2.save()

    print("Creating categories...")
    cat_scifi, _ = Category.objects.get_or_create(name='Science Fiction', description='Futuristic concepts, space exploration, and advanced technology.')
    cat_prog, _ = Category.objects.get_or_create(name='Computer Science', description='Software development, programming languages, and algorithms.')
    cat_fantasy, _ = Category.objects.get_or_create(name='Fantasy', description='Magical and mythical stories, epic adventures.')
    cat_business, _ = Category.objects.get_or_create(name='Business & Finance', description='Economics, personal finance, and entrepreneurship.')

    print("Creating authors...")
    auth_isaac, _ = Author.objects.get_or_create(name='Isaac Asimov', bio='American writer and professor of biochemistry, known for sci-fi works.')
    auth_guido, _ = Author.objects.get_or_create(name='Guido van Rossum', bio='Dutch programmer, best known as the creator of Python.')
    auth_tolkien, _ = Author.objects.get_or_create(name='J.R.R. Tolkien', bio='English writer, poet, and philologist, author of high fantasy works.')
    auth_morgan, _ = Author.objects.get_or_create(name='Morgan Housel', bio='Author and partner at Collaborative Fund.')
    
    print("Creating books...")
    b1, _ = Book.objects.get_or_create(
        isbn='9780553293357',
        defaults={
            'title': 'Foundation',
            'author': auth_isaac,
            'category': cat_scifi,
            'publisher': 'Bantam Books',
            'total_quantity': 5,
            'available_quantity': 4,
            'description': 'The Foundation series is a science fiction book series written by American author Isaac Asimov. It follows a mathematician who predicts the fall of the Galactic Empire.',
            'cover_image': 'books/covers/foundation.png'
        }
    )
    
    b2, _ = Book.objects.get_or_create(
        isbn='9781449355739',
        defaults={
            'title': 'Fluent Python',
            'author': auth_guido,
            'category': cat_prog,
            'publisher': 'O\'Reilly Media',
            'total_quantity': 3,
            'available_quantity': 3,
            'description': 'Clear, concise, and effective programming in Python. This book guides you through Python\'s core language features and libraries.',
            'cover_image': 'books/covers/fluent_python.png'
        }
    )
    
    b3, _ = Book.objects.get_or_create(
        isbn='9780544003415',
        defaults={
            'title': 'The Lord of the Rings',
            'author': auth_tolkien,
            'category': cat_fantasy,
            'publisher': 'Houghton Mifflin',
            'total_quantity': 4,
            'available_quantity': 3,
            'description': 'One Ring to rule them all. An epic high-fantasy novel that follows the quest to destroy the One Ring.',
            'cover_image': 'books/covers/lotr.png'
        }
    )

    b4, _ = Book.objects.get_or_create(
        isbn='9780857197689',
        defaults={
            'title': 'The Psychology of Money',
            'author': auth_morgan,
            'category': cat_business,
            'publisher': 'Harriman House',
            'total_quantity': 10,
            'available_quantity': 10,
            'description': 'Timeless lessons on wealth, greed, and happiness. Doing well with money isn\'t necessarily about what you know. It\'s about how you behave.',
            'cover_image': 'books/covers/psychology_of_money.png'
        }
    )

    # Additional Authors
    auth_herbert, _ = Author.objects.get_or_create(name='Frank Herbert', defaults={'bio': 'American science fiction author.'})
    auth_clear, _ = Author.objects.get_or_create(name='James Clear', defaults={'bio': 'Author and speaker focused on habits and decision-making.'})
    auth_fitzgerald, _ = Author.objects.get_or_create(name='F. Scott Fitzgerald', defaults={'bio': 'American novelist and short story writer.'})
    auth_rowling, _ = Author.objects.get_or_create(name='J.K. Rowling', defaults={'bio': 'British author best known for the Harry Potter series.'})
    auth_martin, _ = Author.objects.get_or_create(name='Robert C. Martin', defaults={'bio': 'Software engineer and author known as Uncle Bob.'})

    # Additional Category
    cat_selfhelp, _ = Category.objects.get_or_create(name='Self-Help', defaults={'description': 'Books focused on personal improvement.'})

    print("Creating more books...")
    
    # Dune
    Book.objects.get_or_create(
        isbn='9780441172719',
        defaults={
            'title': 'Dune',
            'author': auth_herbert,
            'category': cat_scifi,
            'publisher': 'Chilton Books',
            'total_quantity': 7,
            'available_quantity': 7,
            'description': 'Set in the distant future amidst a huge interstellar empire, Dune tells the story of young Paul Atreides.',
            'cover_image': 'books/covers/dune.png'
        }
    )

    # Atomic Habits
    Book.objects.get_or_create(
        isbn='9780735211292',
        defaults={
            'title': 'Atomic Habits',
            'author': auth_clear,
            'category': cat_selfhelp,
            'publisher': 'Avery',
            'total_quantity': 15,
            'available_quantity': 12,
            'description': 'No matter your goals, Atomic Habits offers a proven framework for improving every day.',
            'cover_image': 'books/covers/atomic_habits.png'
        }
    )

    # The Great Gatsby
    Book.objects.get_or_create(
        isbn='9780743273565',
        defaults={
            'title': 'The Great Gatsby',
            'author': auth_fitzgerald,
            'category': cat_fantasy, # Using fantasy/classic loosely
            'publisher': 'Scribner',
            'total_quantity': 5,
            'available_quantity': 5,
            'description': 'The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.',
            'cover_image': 'books/covers/gatsby.png'
        }
    )

    # Harry Potter
    Book.objects.get_or_create(
        isbn='9780439708180',
        defaults={
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': auth_rowling,
            'category': cat_fantasy,
            'publisher': 'Scholastic',
            'total_quantity': 10,
            'available_quantity': 8,
            'description': 'The first novel in the Harry Potter series, featuring the young wizard Harry.',
            'cover_image': 'books/covers/harry_potter.png'
        }
    )

    # Clean Code
    Book.objects.get_or_create(
        isbn='9780132350884',
        defaults={
            'title': 'Clean Code',
            'author': auth_martin,
            'category': cat_prog,
            'publisher': 'Prentice Hall',
            'total_quantity': 8,
            'available_quantity': 7,
            'description': 'A Handbook of Agile Software Craftsmanship.',
            'cover_image': 'books/covers/clean_code.png'
        }
    )

    print("Creating borrow records (Transactions)...")
    now = timezone.now().date()
    
    # Active Borrow (Student 1)
    BorrowRecord.objects.get_or_create(
        user=student1,
        book=b1,
        status='BORROWED',
        defaults={
            'borrow_date': now - timedelta(days=5),
            'due_date': now + timedelta(days=9),
        }
    )

    # Returned Late Borrow with Fine (Student 2)
    BorrowRecord.objects.get_or_create(
        user=student2,
        book=b3,
        status='RETURNED',
        defaults={
            'borrow_date': now - timedelta(days=20),
            'due_date': now - timedelta(days=6),
            'return_date': now - timedelta(days=1),
            'fine_amount': 50.00
        }
    )
    
    # Overdue Borrow (Student 1)
    BorrowRecord.objects.get_or_create(
        user=student1,
        book=b3, # Let's say we have 4 total, 1 returned, 1 overdue, 2 available
        status='OVERDUE',
        defaults={
            'borrow_date': now - timedelta(days=25),
            'due_date': now - timedelta(days=11),
        }
    )

    # Returned Late Borrow with Fine (Student 2)
    BorrowRecord.objects.get_or_create(
        user=student2,
        book=b4,
        status='RETURNED',
        defaults={
            'borrow_date': now - timedelta(days=15),
            'due_date': now - timedelta(days=5),
            'return_date': now,
            'fine_amount': 50.00
        }
    )
    
    # Adjust b3 availability logic based on dummy records
    b3.available_quantity = b3.total_quantity - 1 # 1 overdue, 1 returned (so +1 available again)
    b3.save()

    print("\n" + "="*40)
    print("✅ Database populated successfully!")
    print("="*40)
    print("\nDefault Accounts Created:")
    print("  Admin:      admin / admin123")
    print("  Librarian:  librarian / lib123")
    print("  Student 1:  student1 / student123")
    print("  Student 2:  student2 / student123")

if __name__ == '__main__':
    populate()
