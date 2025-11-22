from django.db import models
from django.contrib.auth.models import User
import base64

class Casa(models.Model):
    """
    Modelo que representa una propiedad o vivienda en la base de datos.
    """
    ESTATUS_CHOICES = [
        ('en venta', 'En Venta'),
        ('vendida', 'Vendida'),
    ]

    id_casa = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default='en venta')
    habitaciones = models.IntegerField(null=True, blank=True)
    banos = models.IntegerField(null=True, blank=True)
    superficie_m2 = models.IntegerField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Casa"
        verbose_name_plural = "Casas"


class ImagenBase(models.Model):
    """
    Galería central de imágenes disponibles para todas las casas
    """
    id_imagen = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, help_text="Nombre descriptivo de la imagen")
    imagen_data = models.BinaryField(verbose_name="Datos de la imagen")
    tipo_contenido = models.CharField(max_length=100, help_text="Tipo MIME (ej: image/jpeg, image/png)")
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Categoría (ej: exterior, interior, jardín)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    def get_image_src(self):
        """
        Genera el src para usar en etiquetas img HTML
        """
        if self.imagen_data and self.tipo_contenido:
            base64_data = base64.b64encode(self.imagen_data).decode('utf-8')
            return f"data:{self.tipo_contenido};base64,{base64_data}"
        return None

    class Meta:
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Imágenes de Galería"
        ordering = ['nombre']


class ImagenCasa(models.Model):
    """
    Relación entre casas e imágenes de la galería central
    """
    id_imagen_casa = models.AutoField(primary_key=True)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='imagenes')
    
    # TEMPORAL: Permitir null para la migración
    imagen_base = models.ForeignKey(ImagenBase, on_delete=models.CASCADE, verbose_name="Imagen de la galería", null=True, blank=True)
    
    texto_alternativo = models.CharField(max_length=100, null=True, blank=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        if self.imagen_base:
            return f"Imagen de {self.casa.titulo} - {self.imagen_base.nombre}"
        return f"Imagen de {self.casa.titulo} (Sin imagen base)"

    def get_image_src(self):
        """
        Hereda la fuente de imagen de ImagenBase
        """
        if self.imagen_base:
            return self.imagen_base.get_image_src()
        return None

    class Meta:
        verbose_name = "Imagen de Casa"
        verbose_name_plural = "Imágenes de Casas"
        ordering = ['orden']