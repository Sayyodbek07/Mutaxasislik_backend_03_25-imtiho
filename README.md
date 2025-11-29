# My Library API

Bu loyiha Django + Django REST Framework asosida qurilgan kitoblar kutubxonasi API’dir.  
Loyihada **Author, Genre, Book** modellari mavjud va ularning CRUD operatsiyalari permissionlar bilan cheklangan.  

---

## 1️⃣ Loyiha tuzilishi

my_library/
├─ manage.py
├─ my_library/
│ ├─ settings.py
│ ├─ urls.py
│ └─ wsgi.py
└─ library/
├─ models.py
├─ serializers.py
├─ views.py
├─ urls.py
├─ pagination.py
└─ permissions.py

python
Копировать код

---

## 2️⃣ Modellar

```python
from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
3️⃣ Serializerlar
python
Копировать код
from rest_framework import serializers
from .models import Author, Genre, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
4️⃣ Pagination (pagination.py)
python
Копировать код
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
Izoh: Bitta sahifada 10 ta element ko‘rinadi, foydalanuvchi ?page_size= orqali o‘zgartirishi mumkin.

5️⃣ Views (views.py)
python
Копировать код
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Author, Genre, Book
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer
from .pagination import CustomPageNumberPagination

# =========================
# Author → ModelViewSet
# =========================
class AuthorViewSet(viewsets.ModelViewSet):
    """
    Faqat adminlar uchun to'liq CRUD
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination

# =========================
# Genre → List + Create
# =========================
class GenreListView(generics.ListAPIView):
    """
    Hammaga ochiq genre list
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

class GenreCreateView(generics.CreateAPIView):
    """
    Faqat adminlar genre qo'shishi mumkin
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]

# =========================
# Book → Full CRUD
# =========================
class BookListView(generics.ListAPIView):
    """
    List → IsAuthenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve → IsAuthenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookCreateView(generics.CreateAPIView):
    """
    Create → IsAdminUser
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BookUpdateView(generics.UpdateAPIView):
    """
    Update → IsAdminUser
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BookDeleteView(generics.DestroyAPIView):
    """
    Delete → IsAdminUser
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
6️⃣ URLs (urls.py)
python
Копировать код
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet,
    GenreListView, GenreCreateView,
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Genre
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/create/', GenreCreateView.as_view(), name='genre-create'),

    # Book
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
7️⃣ Swagger / drf-spectacular
python
Копировать код
# settings.py
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'library.pagination.CustomPageNumberPagination',
}

# project urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
8️⃣ Ishga tushirish
bash
Копировать код
# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Talablarni o'rnatish
pip install -r requirements.txt

# Migrationlar
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
