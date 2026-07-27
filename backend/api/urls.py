from django.urls import path
from .views import SummarizeView, HistoryView

urlpatterns=[
    path("summarize/",SummarizeView.as_view()),
    path("history/",HistoryView.as_view()),
]