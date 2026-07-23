from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from materials.filters import AdFilter
from materials.models import Ad, Comment
from materials.paginators import AdPaginator
from materials.permissions import IsAdminRole, IsAuthor
from materials.serializers import AdSerializer, CommentSerializer


# Create your views here.
class AdBaseAPIView(generics.GenericAPIView):
    """Базовый класс генериков Объявлений."""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend]


class AdListAPIView(AdBaseAPIView, generics.ListAPIView):
    """Лист объявлений."""

    pagination_class = AdPaginator
    filterset_class = AdFilter
    permission_classes = [permissions.AllowAny]


class AdCreateAPIView(AdBaseAPIView, generics.CreateAPIView):
    """Создать объявление."""

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdDetailAPIView(AdBaseAPIView, generics.RetrieveAPIView):
    """Детали объявления."""

    pass


class AdUpdateAPIView(AdBaseAPIView, generics.UpdateAPIView):
    """Обновить объявление."""

    permission_classes = [IsAuthor | IsAdminRole]


class AdDeleteAPIView(AdBaseAPIView, generics.DestroyAPIView):
    """Удалить объявление."""

    permission_classes = [IsAuthor | IsAdminRole]


class CommentBaseAPIView(generics.GenericAPIView):
    """Базовый класс генериков Комментариев."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(CommentBaseAPIView, generics.ListAPIView):
    """Лист комментариев."""

    pass


class CommentCreateAPIView(CommentBaseAPIView, generics.CreateAPIView):
    """Создать комментарий."""

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailAPIView(CommentBaseAPIView, generics.RetrieveAPIView):
    """Детали комментария."""

    pass


class CommentUpdateAPIView(CommentBaseAPIView, generics.UpdateAPIView):
    """Обновить комментарий."""

    permission_classes = [IsAuthor | IsAdminRole]


class CommentDeleteAPIView(CommentBaseAPIView, generics.DestroyAPIView):
    """Удалить комментарий."""

    permission_classes = [IsAuthor | IsAdminRole]
