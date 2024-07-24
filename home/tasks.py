from celery import shared_task
from .models import Book, Category
from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
def upload_books(user_id, books_data):
    user = User.objects.get(id=user_id)
    book_titles = []
    for book_data in books_data:
        categories = book_data.pop('category')
        book = Book.objects.create(**book_data, user=user)
        book.category.set(Category.objects.filter(slug__in=categories))
        book.save()
        book_titles.append(book.title)

    book_titles_str = ", ".join(book_titles)
    subject = "Загруженные книги"
    message = f"Вы успешно загрузили следующие книги: {book_titles_str}"
    from_email = 'no-reply@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)