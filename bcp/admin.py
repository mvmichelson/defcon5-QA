from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from .models import  Proceso, SubProceso, LogAut, Recursos, Gestor, Tipo_RR, Escenarios, Amenazas, Estrategias, Tipo_Impacto
from .models import  Nivel_Impacto, Indicadores_BIA, Tipo_Indicador, Parametros_G, Incidentes, Grupos, Control_Cambios
from .models import  Drp, Procedimientos, Tipo_Proc, Servicios_PC, Contactos_PC, Pasos_PC, Area, Cod_Area, SubProceso_V
from .models import  LBC, Tipo_Site, Tipo_Disp, Componentes, Tipo_Componente, Impactos_Asig, Indicadores_Asig, Log_Revision
from .models import  Procedimientos_V, Servicios_PC_V, Contactos_PC_V, Pasos_PC_V, Impactos_Asig_v, Indicadores_Asig_v

@admin.register(Proceso)
class AdminProceso(admin.ModelAdmin):

    list_display = ('proceso', 'fecha_crea', 'pk_padre', 'nombre', 'path', 'nro_hijos', 'es_subproceso', 'subproceso')

@admin.register(SubProceso)
class AdminSubProceso(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
    # request.user es el usuario autenticado en ese momento
        #obj.gestor_R = request.user
        #obj.gestor_A = request.user
        #obj.gestor_C = request.user
        #obj.gestor_I = request.user
        super().save_model(request, obj, form, change)

@admin.register(SubProceso_V)
class AdminSubProceso(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
    # request.user es el usuario autenticado en ese momento
        #obj.gestor_R = request.user
        #obj.gestor_A = request.user
        #obj.gestor_C = request.user
        #obj.gestor_I = request.user
        super().save_model(request, obj, form, change)

@admin.register(LogAut)
class AdminLogAut(admin.ModelAdmin):

    list_display = ('cod_proceso','gestor_aprobador','fecha', 'item', 'observacion', 'p_status', 'Aprobado')

@admin.register(Control_Cambios)
class AdminControl_Cambios(admin.ModelAdmin):

    list_display = ('fecha','gestor_aut','descripcion', 'proceso', 'procedimiento')


@admin.register(Recursos)
class AdminRecursos(admin.ModelAdmin):

    list_display = ('nombre','descripcion', 'tipo')

@admin.register(Tipo_RR)
class AdminTipo_RR(admin.ModelAdmin):

    list_display = ('nombre','descripcion')

@admin.register(Gestor)
class AdminGestor(admin.ModelAdmin):

    list_display = ('user_pk','user_gestor','cargo', 'area', 'fono_t', 'fono_c')

@admin.register(Escenarios)
class AdminEscenarios(admin.ModelAdmin):

    list_display = ('titulo', 'descripcion')


@admin.register(Amenazas)
class AdminAmenazas(admin.ModelAdmin):

    list_display = ('titulo', 'descripcion')
    
@admin.register(Estrategias)
class AdminEstrategias(admin.ModelAdmin):

    list_display = ('titulo', 'descripcion')

  
@admin.register(Tipo_Impacto)
class AdminTipo_Impacto(admin.ModelAdmin):

    list_display = ('nombre', 'descripcion', 'ponderacion')
    

@admin.register(Nivel_Impacto)
class AdminNivel_Impacto(admin.ModelAdmin):

    list_display = ( 'nombre', 'tipo', 'cod', 'descripcion', 'valor')

@admin.register(Indicadores_BIA)
class AdminIndicadores_BIA(admin.ModelAdmin):

    list_display = ('tipo', 'cod', 'nivel', 'definicion', 'valor')

@admin.register(Tipo_Indicador)
class AdminTipo_Indicador(admin.ModelAdmin):

    list_display = ('nombre', 'descripcion', 'ponderacion')

@admin.register(Parametros_G)
class AdminParametros_G(admin.ModelAdmin):

    list_display = ('nombre', 'valor_1', 'valor_2')

@admin.register(Incidentes)
class AdminIncidentes(admin.ModelAdmin):

    list_display = ('fecha', 'codigo', 'nombre_r', 'descripcion')

@admin.register(Procedimientos)
class AdminProcedimientos(admin.ModelAdmin):

    list_display = ('codigo','pk_padre', 'fecha_c', 'fecha_ult_mod', 'nombre', 'tipo', 'estrategia', 'resp_proceso', 'bck_resp', 'gestor_ejecutor',
                    'bck_ejecutor', 'enlace_c_crisis', 'bck_enlace', 'esta_activo', 'status',
                      'archivo', 'esta_activo','esta_confirmado')

@admin.register(Procedimientos_V)
class AdminProcedimientos_V(admin.ModelAdmin):

    list_display = ('codigo','pk_padre', 'fecha_c', 'fecha_ult_mod', 'nombre', 'tipo', 'version',
                    'estrategia', 'resp_proceso', 'bck_resp', 'gestor_ejecutor',
                    'bck_ejecutor', 'enlace_c_crisis', 'bck_enlace', 'esta_activo',
                      'archivo', 'esta_activo','esta_confirmado')


@admin.register(Tipo_Proc)
class AdminTipo_Proc(admin.ModelAdmin):

    list_display = ('nombre', 'descripcion' )

@admin.register(Servicios_PC)
class AdminServicios_PC(admin.ModelAdmin):

    list_display = ('nombre', 'objetivo', 'contacto', 'contacto_bck')

@admin.register(Servicios_PC_V)
class AdminServicios_PC_V(admin.ModelAdmin):

    list_display = ('nombre', 'objetivo', 'contacto', 'contacto_bck')
    
@admin.register(Contactos_PC)
class AdminServicios_PC(admin.ModelAdmin):

    list_display = ('nombre', 'cont_int', 'correo', 'tel_lab', 'cel_lab')

@admin.register(Contactos_PC_V)
class AdminServicios_PC_V(admin.ModelAdmin):

    list_display = ('nombre', 'cont_int', 'correo', 'tel_lab', 'cel_lab')


@admin.register(Pasos_PC)
class AdminServicios_PC(admin.ModelAdmin):

    list_display = ('nro_paso', 'descripcion', 'ejecutor', 'tiempo_esp')

@admin.register(Pasos_PC_V)
class AdminServicios_PC_V(admin.ModelAdmin):

    list_display = ('nro_paso', 'descripcion', 'ejecutor', 'tiempo_esp')

@admin.register(Area)
class AdminArea(admin.ModelAdmin):

    list_display = ('nombre', 'nivel')

@admin.register(Cod_Area)
class AdminCod_Area(admin.ModelAdmin):

    list_display = ('codigo', 'ciudad', 'pais')

@admin.register(Grupos)
class AdminGrupos(admin.ModelAdmin):

    list_display = ('grupo', 'descripcion')


@admin.register(Drp)
class AdminDrp(admin.ModelAdmin):

    list_display = ('codigo', 'nombre', 'fecha_c', 'fecha_ult_mod')

@admin.register(Tipo_Site)
class AdminTipo_Site(admin.ModelAdmin):

    list_display = ( 'nombre', 'resumen', 'descripcion')


@admin.register(Tipo_Disp)
class AdminTipo_Disp(admin.ModelAdmin):

    list_display = ( 'nombre', 'resumen', 'descripcion')

@admin.register(Componentes)
class AdminComponentes(admin.ModelAdmin):

    list_display = ( 'codigo', 'identificacion', 'nombre', 'descripcion')

@admin.register(Tipo_Componente)
class AdminTipo_Componente(admin.ModelAdmin):

    list_display = ( 'tipo', 'descripcion')

@admin.register(LBC)
class AdminLBC(admin.ModelAdmin):

    list_display = ( 'nombre', 'codigo', 'descripcion', 'valor')

@admin.register(Impactos_Asig)
class AdminImpactos_Asig(admin.ModelAdmin):
    list_display = ('impacto', 'nivel')

@admin.register(Indicadores_Asig)
class AdminIndicadores_Asig(admin.ModelAdmin):
    list_display = ('indicador', 'nivel')

@admin.register(Impactos_Asig_v)
class AdminImpactos_Asig(admin.ModelAdmin):
    list_display = ('impacto', 'nivel')

@admin.register(Indicadores_Asig_v)
class AdminIndicadores_Asig(admin.ModelAdmin):
    list_display = ('indicador', 'nivel')

@admin.register(Log_Revision)
class AdminLog_Revision(admin.ModelAdmin):
    list_display = ('fecha', 'proceso', 'gestor_aut', 'seccion', 'campo', 'comentario', 'resuelto')




