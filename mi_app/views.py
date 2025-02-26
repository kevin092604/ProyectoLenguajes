from django.shortcuts import render, redirect
from . import models
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404

# Create your views here.

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario'):
            print(request.session.get('usuario'))
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('inicio_sesion')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def inicio(request):
    return render(request, 'mi_app/inicio.html')
@login_required
def horario(request):
    return render(request, 'mi_app/horario.html')
@login_required
def perfil(request):
    # Obtener el nombre de usuario desde la sesión
    usuario_nombre = request.session.get('usuario')
    
    # Buscar el usuario en la base de datos
    usuario = models.Usuario.objects.get(Usuario=usuario_nombre)
    
    # Pasar los datos del usuario al template
    contexto = {
        'nombre': usuario.Nombre,
        'apellido': usuario.Apellido,
        'usuario': usuario.Usuario,
        'correo': usuario.Correo,
        'ncuenta': usuario.Ncuenta,
    }
    
    return render(request, 'mi_app/perfil.html', contexto)
@login_required
def agregar_clase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clase_nombre = data.get('clase')
            
            if clase_nombre:
                # Guarda la clase en la base de datos
                clase, created = models.Clase.objects.get_or_create(nombre=clase_nombre)

                # Obtén el perfil del usuario
                usuario = request.session.get('usuario')  # Asegúrate de que el usuario esté en la sesión
                if usuario:
                    id = request.session.get('id')
                    models.Perfil.objects.get_or_create(usuario_id = id)
                    perfil = models.Perfil.objects.get(usuario__Usuario=usuario)
                    perfil.clases.add(clase)  # Agrega la clase al perfil

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Nombre de clase no proporcionado'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failure', 'message': 'Error al procesar la solicitud'}, status=400)
        except models.Perfil.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'Perfil de usuario no encontrado'}, status=404)
    return JsonResponse({'status': 'failure', 'message': 'Método no permitido'}, status=405)
@login_required
def eliminar_clase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clase_nombre = data.get('clase')
            
            if clase_nombre:
                # Obtén la clase de la base de datos
                clase = get_object_or_404(models.Clase, nombre=clase_nombre)
                
                # Obtén el perfil del usuario
                usuario = request.session.get('usuario')  # Asegúrate de que el usuario esté en la sesión
                if usuario:
                    id = request.session.get('id')
                    models.Perfil.objects.get_or_create(usuario_id=id)
                    perfil = models.Perfil.objects.get(usuario__Usuario=usuario)
                    
                    # Elimina la clase del perfil
                    perfil.clases.remove(clase)
                    
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Nombre de clase no proporcionado'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failure', 'message': 'Error al procesar la solicitud'}, status=400)
        except models.Perfil.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'Perfil de usuario no encontrado'}, status=404)
        except models.Clase.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'Clase no encontrada'}, status=404)
    return JsonResponse({'status': 'failure', 'message': 'Método no permitido'}, status=405)
@login_required
def recomendaciones(request):
    return render(request, 'mi_app/recomendaciones.html')
@login_required
def mostrar_horario(request):
    if request.method == 'GET':
        # Obtener el usuario en sesión
        usuario_nombre = request.session.get('usuario')
        if usuario_nombre:
            usuario = get_object_or_404(models.Usuario, Usuario=usuario_nombre)
            perfil = get_object_or_404(models.Perfil, usuario=usuario)
            clases = perfil.clases.all()
            # Convertir los objetos de clase en una lista de diccionarios
            clases_list = [{'id': clase.id, 'nombre': clase.nombre} for clase in clases]
            return JsonResponse({'status': 'success', 'clases': clases_list})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Usuario no encontrado'}, status=404)
    return JsonResponse({'status': 'failure', 'message': 'Método no permitido'}, status=405)

def inicio_sesion(request):
    if request.method == "POST":   
        usuario = request.POST.get('Usuario')
        contraseña = request.POST.get('Contraseña')
        user = models.Usuario.objects.filter(Usuario=usuario, Contraseña=contraseña).first()
        if user:
            request.session['id'] = user.id
            request.session['usuario'] = usuario
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('respuestaLogin')
    return render(request, 'mi_app/inicio_sesion.html')

def logout(request):
    # Elimina la información de la sesión
    if 'usuario' in request.session:
        del request.session['usuario']
        messages.success(request, 'Has cerrado sesión correctamente.')
    # Redirige a la página de inicio de sesión u otra página deseada
    return redirect('inicio_sesion')

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get('Nombre')
        apellido = request.POST.get('Apellido')
        email = request.POST.get('Correo')
        usuario = request.POST.get('Usuario')
        contraseña = request.POST.get('Contraseña')
        nCuenta = request.POST.get('Ncuenta')
        print(models.Usuario.objects.filter(Usuario =  usuario).exists())
        # Aquí iría la lógica para guardar los datos en la base de datos
        if models.Usuario.objects.filter(Usuario =  usuario).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('respuestaRegistro')
        elif models.Usuario.objects.filter(Correo = email).exists():
            messages.error(request, 'El correo ya existe')
            return redirect('respuestaRegistro')
        else:
            user = models.Usuario(
             Nombre=nombre,
            Apellido=apellido,
            Usuario=usuario,
            Correo=email,
            Contraseña=contraseña,
            Ncuenta=nCuenta)
        user.save()
        #return JsonResponse({'message': 'Usuario creado con éxito'})
        messages.success(request, 'Usuario creado con exito')
        return redirect('respuestaRegistro/')

    return render(request, 'mi_app/registro.html')            

def respuestaRegistro(request):
    return render(request, 'mi_app/respuestaRegistro.html')
def respuestaLogin(request):
    return render(request, 'mi_app/respuestaLogin.html')

@login_required
def Español(request):
    return render(request, 'mi_app/clases/EG-011.html')
@login_required
def Electiva1(request):
    return render(request, 'mi_app/clases/Electiva1.html')
@login_required
def InglesI(request):
    return render(request, 'mi_app/clases/IN-101.html')
@login_required
def InglesII(request):
    return render(request, 'mi_app/clases/IN-102.html')
@login_required
def Introduccion(request):
    return render(request, 'mi_app/clases/IS-110.html')
@login_required
def MateI(request):
    return render(request, 'mi_app/clases/MM-110.html')
@login_required
def Geometria(request):
    return render(request, 'mi_app/clases/MM-111.html')
@login_required
def Vectores(request):
    return render(request, 'mi_app/clases/MM-211.html')
@login_required
def CalculoI(request):
    return render(request, 'mi_app/clases/MM-201.html')
@login_required
def CalculoII(request):
    return render(request, 'mi_app/clases/MM-202.html')
@login_required
def Programacion1(request):
    return render(request, 'mi_app/clases/MM-314.html')
@login_required
def Sociologia(request):
    return render(request, 'mi_app/clases/SC-101.html')
@login_required
def PlanEstudio(request):
    return render(request, 'mi_app/Plan_Estudio.html')
@login_required
def guardar_comentario(request):
    if request.method == 'POST':
        # Cargar los datos del cuerpo de la solicitud como JSON
        data = json.loads(request.body)

        # Obtener los valores del JSON
        nombre_clase = data.get('nombre_clase')
        comentario_texto = data.get('comentario')
        print("Clase: "+nombre_clase)
        # Obtener la clase por nombre
        clase = get_object_or_404(models.Clase, nombre=nombre_clase)
        usuario_id = request.session.get('id')

        # Obtener el objeto Usuario basado en el ID
        usuario = get_object_or_404(models.Usuario, id=usuario_id)
        # Crear el comentario
        comentario = models.Comentario.objects.create(
            usuario=usuario,
            clase=clase,
            texto=comentario_texto
        )
        
        comentario.save()
        # Devolver la respuesta en formato JSON
        return JsonResponse({
            'status': 'success',
            'comentario': {
                'usuario': comentario.usuario.Usuario,  # Asumiendo que `username` es el campo que quieres mostrar
                'texto': comentario.texto,
            }
        })
    
    return JsonResponse({'status': 'failure', 'message': 'Método no permitido'}, status=405)
def mostrar_comentario(request):
    if request.method == 'GET':
        nombre_clase = request.GET.get('nombre_clase')
        # Obtener la clase basada en el nombre
        clase = get_object_or_404(models.Clase, nombre=nombre_clase)
    
        # Obtener los comentarios asociados con esta clase
        comentarios = models.Comentario.objects.filter(clase=clase).order_by('-likes')

        # Crear una lista de comentarios en formato JSON serializable
        comentarios_lista = []
        for comentario in comentarios:
            comentarios_lista.append({
                'usuario': comentario.usuario.Usuario,  # Asumiendo que `Usuario` es el campo de nombre de usuario
                'texto': comentario.texto,
                'likes' : comentario.likes,
                'id' : comentario.id,
            })
        
        # Imprimir la lista de comentarios para debugging
        print(comentarios_lista)
        
        # Enviar la respuesta como JSON
        return JsonResponse({'comentarios': comentarios_lista})
    
def incrementar_likes(request):
    try:
        data = json.loads(request.body)
        comentario_id = data.get('comentario_id')

        comentario = models.Comentario.objects.get(id=comentario_id)
        comentario.likes += 1
        comentario.save()

        return JsonResponse({'success': True, 'likes': comentario.likes})
    except models.Comentario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comentario no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
