from django.db import models
import uuid

# modelo dos tribulais
class Tribunal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sigla = models.CharField(max_length=10)
    nome = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    api_endpoint = models.URLField()
    api_tipo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sigla} - {self.nome}"