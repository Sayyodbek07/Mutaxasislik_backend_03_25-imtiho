
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Author, Genre, Book
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination



class GenreCreateView(generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]


class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
