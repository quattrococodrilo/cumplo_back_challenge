from django.db import models


class BaseModel(models.Model):
    """
    Clase abstracta para agregar campos de tiempo.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        abstract = True
