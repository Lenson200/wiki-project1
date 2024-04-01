from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_detail, name="entry_detail"),
    path("search", views.search_results, name="search_results"),
    path("query", views.entry_detail, name="entry_detail_query"),
    path("create_new", views.create_new, name="create_new"),
    path("wiki/edit_content/<str:title>", views.edit_content, name="edit_content"),
    path("random", views.random_page, name="random_page"),
   
    
]
