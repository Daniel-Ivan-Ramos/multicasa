from django.contrib import admin
from django import forms
from .models import Casa, ImagenCasa, ImagenBase

# FORMULARIO PERSONALIZADO para ImagenBase (Galería)
class ImagenBaseForm(forms.ModelForm):
    archivo_imagen = forms.ImageField(
        required=True, 
        help_text="Selecciona una imagen para agregar a la galería central"
    )
    
    class Meta:
        model = ImagenBase
        fields = ['archivo_imagen', 'nombre', 'categoria']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Procesar la imagen subida
        archivo_imagen = self.cleaned_data.get('archivo_imagen')
        if archivo_imagen:
            # Leer los datos binarios de la imagen y guardar en la BD
            instance.imagen_data = archivo_imagen.read()
            instance.tipo_contenido = archivo_imagen.content_type
            # Si no se proporciona nombre, usar el nombre del archivo
            if not instance.nombre:
                instance.nombre = archivo_imagen.name
        
        if commit:
            instance.save()
        return instance


# ADMIN para ImagenBase (Galería Central)
@admin.register(ImagenBase)
class ImagenBaseAdmin(admin.ModelAdmin):
    form = ImagenBaseForm
    list_display = ['nombre', 'categoria', 'fecha_creacion', 'preview_imagen']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['nombre', 'categoria']
    readonly_fields = ['preview_imagen']
    
    def preview_imagen(self, obj):
        if obj.get_image_src():
            return f'<img src="{obj.get_image_src()}" style="max-width: 300px; max-height: 200px;" />'
        return "No hay imagen"
    preview_imagen.allow_tags = True
    preview_imagen.short_description = "Vista previa"


# INLINE para agregar imágenes a las casas desde la galería
class ImagenCasaInline(admin.TabularInline):
    model = ImagenCasa
    extra = 1
    fields = ['imagen_base', 'texto_alternativo', 'orden']
    autocomplete_fields = ['imagen_base']  # Para búsqueda fácil de imágenes


# ADMIN para Casa
@admin.register(Casa)
class CasaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'precio', 'estatus', 'habitaciones', 'banos', 'fecha_publicacion']
    list_filter = ['estatus', 'precio', 'fecha_publicacion']
    search_fields = ['titulo', 'descripcion', 'direccion']
    inlines = [ImagenCasaInline]  # Agrega el selector de imágenes desde galería


# ADMIN para ImagenCasa (opcional - para administración separada)
@admin.register(ImagenCasa)
class ImagenCasaAdmin(admin.ModelAdmin):
    list_display = ['casa', 'imagen_base', 'orden', 'texto_alternativo']
    list_filter = ['casa', 'imagen_base__categoria']
    search_fields = ['casa__titulo', 'imagen_base__nombre']
    autocomplete_fields = ['casa', 'imagen_base']
    readonly_fields = ['preview_imagen']
    
    def preview_imagen(self, obj):
        if obj.get_image_src():
            return f'<img src="{obj.get_image_src()}" style="max-width: 300px; max-height: 200px;" />'
        return "No hay imagen"
    preview_imagen.allow_tags = True
    preview_imagen.short_description = "Vista previa"