from django.contrib import admin


from .models import Ejercicio, Medida, Calendario, SesionesGoogle

# class EntrenamientoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'get_ejercicios')
#     save_as = True

class MedidaAdmin(admin.ModelAdmin):
    list_display = ('user','anyo','mes', 'peso', 'imc')

class CalendarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha', 'activo','completado', 'get_ejercicios', 'calories', 'distance')
    save_as = True

    def get_ejercicios(self, obj):
        return "\n".join(['['+ p.nombre + '],' for p in obj.ejercicios.all()])

class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre','zona','nivel')
    save_as = True

class SesionesGoogleAdmin(admin.ModelAdmin):
    list_display = ('id_google','name','description','application','user_google')



admin.site.register(Ejercicio, EjercicioAdmin)
admin.site.register(Medida, MedidaAdmin)
admin.site.register(Calendario, CalendarioAdmin)
admin.site.register(SesionesGoogle, SesionesGoogleAdmin)
