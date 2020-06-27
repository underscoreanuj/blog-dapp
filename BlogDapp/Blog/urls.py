from django.urls import path
from .views import BlogList, BlogView

urlpatterns = [
    path('', BlogList.as_view()),
    path('<int:blog_id>', BlogView.as_view()),
]
