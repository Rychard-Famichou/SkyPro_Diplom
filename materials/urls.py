from django.urls import path

from materials.views import (
    AdCreateAPIView,
    AdDeleteAPIView,
    AdDetailAPIView,
    AdListAPIView,
    AdUpdateAPIView,
    CommentCreateAPIView,
    CommentDeleteAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    CommentUpdateAPIView,
)

app_name = "materials"

urlpatterns = [
    path("ads/", AdListAPIView.as_view(), name="ad-list"),
    path("ads/create/", AdCreateAPIView.as_view(), name="ad-create"),
    path("ads/<int:pk>/", AdDetailAPIView.as_view(), name="ad-detail"),
    path("ads/<int:pk>/update/", AdUpdateAPIView.as_view(), name="ad-update"),
    path("ads/<int:pk>/delete/", AdDeleteAPIView.as_view(), name="ad-delete"),
    path("comments/", CommentListAPIView.as_view(), name="comment-list"),
    path("comments/create/", CommentCreateAPIView.as_view(), name="comment-create"),
    path("comments/<int:pk>/", CommentDetailAPIView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/update/", CommentUpdateAPIView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteAPIView.as_view(), name="comment-delete"),
]
