from library_app.admin import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from library_app.views import AuthorViewSet, GenreListView, GenreCreateView, BookListView, BookCreateView, BookDetailView

router = DefaultRouter()
router.register('authors', AuthorViewSet)  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),       
    path('api/genres/', GenreListView.as_view(), name='genre-list'),
    path('api/genres/create/', GenreCreateView.as_view(), name='genre-create'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/create/', BookCreateView.as_view(), name='book-create'),

]
