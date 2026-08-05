from django.conf import settings
from django.db import models


# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=20, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    description = models.TextField(verbose_name="Описание товара")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор объявления")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} от {self.author}"


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор отзыва")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Объявление отзыва")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзыв"

    def __str__(self):
        return f"Отзыв {self.pk} от {self.author} к {self.ad}"
