from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('add/', views.create_comic_book, name='create_comic_book'),
    path('inventory/', views.comic_list, name='comic_list'),
    path('details/<int:comic_id>', views.comic_details, name='comic_details'),
    path('delete/<int:comic_id>/', views.delete_comic, name='delete_comic'),
    path('edit/<int:comic_id>/', views.edit_comic, name='edit_comic'),
    path('superhero/<int:hero_id>/', views.superhero_api_view, name='superhero_api'),
    path('marvel-scrape/', views.marvel_scrape, name='marvel_scrape'),
    path('dc-scrape/', views.dc_scrape, name='dc_scrape'),

]
