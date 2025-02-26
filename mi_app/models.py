from django.db import models

# Create your models here.
class Usuario(models.Model):
    #Campos de texto
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Usuario = models.CharField(max_length=25, unique=True)
    Correo = models.CharField(unique=True, max_length=50)
    Contraseña = models.CharField(max_length=20)
    #Campos numericos
    Ncuenta = models.PositiveBigIntegerField()

class Clase(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    clases = models.ManyToManyField(Clase, related_name='perfiles')  # Relación de muchas clases para un perfil

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    likes = models.IntegerField(default=0)