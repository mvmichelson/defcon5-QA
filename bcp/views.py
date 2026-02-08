#Programa PYTHON
#Definicion de Vistas para el Sistema bcp del Proyecto DEFCON5
#Programado por Marco A. Villalobos Michelson
#==============================================================

#========
# Indice
#========

# 1. Listas y Detalles
#=======================

# 1.1 Lista de Procesos
# 1.2 Lista de Procesos para asociar Activos
# 1.3 Lista de Procesos para asociar Escenarios
# 1.4 Lista de Procesos para asociar Evaluacion
# 1.5 Detalle de Proceso
# 1.6 Detalle de Politicas de Evaluacion BIA
# 1.7 Lista de log de autorizaciones
# 

# 2. Creacion/Borrado de Entidades
#===================================
# 2.1 Creacion de Procesos y Subproceso
# 2.1.2 Borra  Proceso

# 2.4 Crea Activo o Recurso
# 


# 3. Gestion de Autorizaciones
# =============================
# 3.1 Asignacion  RACI
# 3.2 Autorizacion RACI de Proceso
# 3.3  Autorizacion RACI de Asignacion   BIA  a Proceso

#    3.10 Autorizacion RACI de Procedimiento de Contingencia
# 4. Asignacion de Relaciones a Procesos
# 5.
 


# 6. DRP
#==================

# 6.1 Lista los DRPs 
# 6.2 Muestra el Indice con las Secciones del DRP 
# 6.3 Crea un DRP
# 6.4 Borra un DRP

# 6.5 registra Objetivo del  DRP
# 6.6 registra Equipo Gestores  DRP
# 6.7 Definicion Alcance del   DRP
# 6.8 Definicion la Estrategia del   DRP

# 6.9 Especificacion Tecnica  del DRP
# 6.9.1 Lista Componentes del DRP
# 6.9.2 Asigna Componentes a un  DRP

# 6.9.3.1 Crea Componentes en la BD
# 6.9.3.2 Borra Componentes de la BD (no implementado)
# 6.9.3.3  Lista la LBC DRP
# 6.9.3.4 Crea  la LBC
# 6.9.3.5 Borra la LBC

# 6.10 Servicios Criticos DRP
# 6.10.1 Lista  Servicios Criticos DRP
# 6.10.2 Crea Servicios Criticos DRP
# 6.10.2 Borra Servicios Criticos DRP

# 6.11 Procedimiento del  DRP
# 6.11.1 Lista Pasos del  Procedimiento del  DRP

# 6.12 Datos de Contacto  del  DRP
# 6.12.1 Lista Contactos del  Procedimiento del  DRP
   
# 6.13  Autorizaciones  del DRP

# 6.14  Revision de Observaciones  del DRP
# 6.14.1   Revision de Responsables
# 6.14.2   Revision de Objetivo  del DRP
# 6.14.3   Revision de Alcance  del DRP
# 6.14.5 Revision Especificacion Tecnica Site de Contingencias 

# 6.15  Detalle del DRP en Desarrollo/Actualizacion


# 6. Maestros
# Administracion de Riesgo/Impacto 

#7. Administracion de Incidentes
# ==============================
# Declara Incidente
# Plan de Pruebas
# Switchs de Activacion / Desactivacion
# Reportes de Incidentes


# 8. Proposito General
#=======================

# Manda correo de Notificacion
# Manejo de Errores
# Valida el acceso de la sesion
# Manejo de Graficos
# Reinicia BD

# Respaldo / Recuperacion de la BD


# ============================================================================================
# ============================================================================================


from queue import Full
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Modelos del Sistema.

from .models import Proceso, SubProceso, LogAut, Recursos, Tipo_RR, Gestor, Escenarios, Amenazas, Estrategias, Tipo_Impacto, Nivel_Impacto, Tipo_Impacto_P, Nivel_Impacto_P
from .models import Drp, Indicadores_BIA, Tipo_Indicador, Parametros_G, Incidentes, Procedimientos, Tipo_Proc, Servicios_PC, Contactos_PC, Pasos_PC 
from .models import Componentes, Tipo_Componente, LBC, Tipo_Disp, Tipo_Site, Impactos_Asig, Contactos_PC_V, Pasos_PC_V
from .models import Indicadores_Asig, Log_Revision, SubProceso_V, Control_Cambios, Procedimientos_V, Servicios_PC_V, Impactos_Asig_v, Indicadores_Asig_v
from .models import CheckList, Check_Pasos, PruebaContingencia, PruebaContingencia_V, CasoPrueba, CasoPrueba_V, EjecucionPrueba, EjecucionCasoPrueba

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.auth.hashers import make_password

from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from django.http import HttpResponseRedirect
from django.urls import reverse 
import datetime

from django.contrib.auth.decorators import permission_required

#from django.contrib.sites.models import Site
from django.core.mail import send_mail

from .utils import substring, extraer_desde_char, resta_string



#Variables Globales

url_ant= ''
url_ant_obs_aut=''
Drp_Sec_3_url_ant =''
Drp_Sec_4_url_ant =''
Asigna_CMP_ult_url=''

Crea_LBC_url_ant=''
cr_drp_P5_url_ant=''
defcon_est=''

selec_Autorizadores = []
selec_Ejecutores =[]
selec_Gestion_de_Crisis = []
selec_TI=[]

# Fin variables Globales

# ===============================================================================================
# 
#================================================================================================



class Base_GenericPageView(TemplateView):
    
    model = Parametros_G
    template_name = '/bcp/base_generic.html'

    def get_context_data(self, **kwargs):
        #global defcon_est
    
        #parametro_g = get_object_or_404(Parametros_G , pk=1)
        #self.defcon_est = get_object_or_404(Parametros_G , pk=1)

        context = super(Base_GenericPageView, self).get_context_data(**kwargs)
        context['defcon'] = get_object_or_404(Parametros_G , pk=1)
        #get_object_or_404(Parametros_G , pk=1)
        #print('base_generic', defcon_est)
        return context

def index(request):
    """
    Función de vista para la página inicio del sitio.
    """
    print('>>>>> Index')

    #usr=request.user
    #if not usr.is_authenticated:
        #return HttpResponseRedirect(reverse('error-sesion-mgm', args=[500] ))

    # Genera contadores de algunos de los objetos principales
    #num_proc=Proceso.objects.all().count()
    #num_sproc=SubProceso.objects.all().count()
    #num_proced=Procedimientos.objects.all().count()
    nro_procesos=SubProceso_V.objects.all().count()
    nro_proced=Procedimientos_V.objects.all().count()
    nro_proced_act=Procedimientos_V.objects.filter(esta_activo=True).count()
    nro_incidentes=Incidentes.objects.filter(estado=True).count()
    incidentes_activos = False
    if nro_incidentes > 0:
        incidentes_activos=True
    
    print('---- nro_proced_act:', nro_proced_act, '/', nro_proced)

    # Numero de visitas a esta view, como está contado en la variable de sesión.
    #num_visits = request.session.get('num_visits', 0)
    #request.session['num_visits'] = num_visits + 1
    #defcon = get_object_or_404(Parametros_G , pk=1)

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    #return render(request, 'index.html')

    return render(request, 'index.html', context={'nro_procesos':nro_procesos,
                                                  'nro_proced':nro_proced, 
                                                  'nro_proced_act':nro_proced_act,
                                                  'nro_incidentes':nro_incidentes,
                                                  'incidentes_activos':incidentes_activos
                                                  })


def En_Construccion(request):
    return render(request, 'bcp/mensajes/en_construccion.html')


def Mapeo(request):
    """
    Despliega Grafico con la Metodologia de Mapeo 
    """

    return render(request, 'bcp/mapeo.html')

def Mapa_RIA(request):
    """
    Despliega Grafico con la Metodologia de Evaluacion RIA 
    """

    return render(request, 'bcp/ria/diagrama_ria.html')



#******************************************************************************************************************************************
#************************************************************* 1. Listas y Detalles *******************************************************
#******************************************************************************************************************************************


#***********************
# 1.1 Lista de Procesos *
#***********************
@login_required
def Lista_Procesos(request):
    """
    Lista Procesos 
    """
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, nombre = 'BIA_BAJO')
    bia_medio = get_object_or_404(Parametros_G, nombre = 'BIA_MEDIO')
    bia_max   = get_object_or_404(Parametros_G, nombre = 'BIA_MAX')

    tramo_1 = float(bia_bajo.valor_2)/100
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100
    valor_max=float(bia_max.valor_2)
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2)
    print('valor_max:', valor_max) 

    lista_procesos = Proceso.objects.all()
    
    return render(request, 'bcp/proceso_list.html',
                  context={'lista_procesos':lista_procesos,
                           'tramo_1':tramo_1, 
                           'tramo_2':tramo_2,
                           'valor_max':valor_max})
 

#********************************************
# 1.2 Lista de Procesos para asociar Activos*
#********************************************
@login_required
def Lista_Recursos(request):
    """
    Lista Procesos para asociar Servicios Criticos
    """
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, nombre = 'BIA_BAJO')
    bia_medio = get_object_or_404(Parametros_G, nombre = 'BIA_MEDIO')
    bia_max   = get_object_or_404(Parametros_G, nombre = 'BIA_MAX')

    tramo_1 = float(bia_bajo.valor_2)/100
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100
    valor_max=float(bia_max.valor_2)
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2)
    print('valor_max:', valor_max) 

    lista_procesos = Proceso.objects.all()
    return render(request, 'bcp/map_act/map_activos__list.html',
                  context={'lista_procesos':lista_procesos,
                           'tramo_1':tramo_1,
                           'tramo_2':tramo_2,
                           'valor_max':valor_max})
    


#***********************************************
# 1.3 Lista de Procesos para asociar Escenarios*
#***********************************************
@login_required
def Lista_Escenarios(request):
    """
    Lista Procesos para asignar Escenarios.
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, nombre = 'BIA_BAJO')
    bia_medio = get_object_or_404(Parametros_G, nombre = 'BIA_MEDIO')
    bia_max   = get_object_or_404(Parametros_G, nombre = 'BIA_MAX')

    tramo_1 = float(bia_bajo.valor_2)/100
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100
    valor_max=float(bia_max.valor_2)
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2)
    print('valor_max:', valor_max) 

    lista_procesos = Proceso.objects.all()
    
    return render(request, 'bcp/map_esc/map_esc_list.html',
                  context={'lista_procesos':lista_procesos,
                           'tramo_1':tramo_1,
                           'tramo_2':tramo_2,
                           'valor_max':valor_max})
    


#***********************************************
# 1.4 Lista de Procesos para asociar Evaluacion*
#***********************************************
@login_required
def Lista_Evaluaciones(request):
    """
    Lista Procesos para Evaluacion BIA.
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, nombre = 'BIA_BAJO')
    bia_medio = get_object_or_404(Parametros_G, nombre = 'BIA_MEDIO')
    bia_max   = get_object_or_404(Parametros_G, nombre = 'BIA_MAX')

    tramo_1 = float(bia_bajo.valor_2)/100
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100
    valor_max=float(bia_max.valor_2)
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2)
    print('valor_max:', valor_max) 

    lista_procesos = Proceso.objects.all()
    
    return render(request, 'bcp/map_eval/map_eval__list.html',
                  context={'lista_procesos':lista_procesos,
                           'tramo_1':tramo_1,
                           'tramo_2':tramo_2,
                           'valor_max':valor_max})


    
#***********************
#1.5 Detalle de Proceso*
#***********************
class ProcesoDetailView(generic.DetailView):
    model = Proceso

@login_required
def Detalle_Proceso(request, pk):
    """
    muestra todos los datos asociados al proceso pk
    """
    print('------- Detalle del Proceso -----------------')
    proceso=get_object_or_404(Proceso, pk=pk)
    print('proceso=', proceso.proceso)
    comentarios=Log_Revision.objects.filter(proceso=proceso)
    print('comentarios=', comentarios)

    return render(request, 'bcp/proceso_detail.html',
                  context={'proceso':proceso, 'comentarios':comentarios})

@login_required
def Detalle_Proceso_V(request, pk):
    """
    muestra todos los datos asociados al proceso vigente
    pk: Recibe identificacion del Proceso 
    """
    print('------- Detalle del Proceso Vigente -----------------')

    proceso=get_object_or_404(Proceso, pk=pk)
    print('proceso=', proceso.proceso)

    control_cambios=Control_Cambios.objects.filter(proceso=proceso.subproceso_v)
    print('comentarios=', control_cambios)

    return render(request, 'bcp/proceso_detail_v.html',
                  context={'proceso':proceso, 'control_c':control_cambios})

@login_required
def Detalle_Proceso_V2(request, pk):
    """
    muestra todos los datos asociados al proceso vigente
    pk: Recibe identificacion del subproceso vigente (proceso.subproceso_v)
    """
    print('------- Detalle del Proceso Vigente 2 -----------------')

    spv=get_object_or_404(SubProceso_V,pk=pk)
    proceso=spv.proceso
    print('pk del proceso=', proceso.pk)

    control_cambios=Control_Cambios.objects.filter(proceso=proceso.subproceso_v)
    print('comentarios=', control_cambios)

    return render(request, 'bcp/proceso_detail_v.html',
                  context={'proceso':proceso, 'control_c':control_cambios})


#********************************************
#1.6 Detalle de Politicas de Evaluacion BIA *
#********************************************
class Pol_Eval_BIA_DetailView(generic.DetailView):
    model = Nivel_Impacto, Indicadores_BIA


#***********************************
#1.7 Lista de log de autorizaciones*
#***********************************
class LogAutRevListView(generic.ListView):
    model = LogAut




#****************************************************** Fin Listas ************************************************************************

#********************************************************************************************************************************************
#*********************************************** 2. Creacion/Borrado de Entidades ************************************************************
#********************************************************************************************************************************************


#***************************************
# 2.1 Creacion de Procesos y Subproceso*
#***************************************

from .forms import CreaProcesoForm

@login_required
def crea_proceso(request, pk):
    """
    Funcio de vista para crear un Proceso
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))


    model = Proceso
    
    proc_padre=get_object_or_404(Proceso, pk = pk)
    #proc_hijo=Proceso.object.create()

    # Determinacion de Codigo a asignar.
    cod = proc_padre.proceso
    codigo = cod.strip()+"." 
    hijos_i = proc_padre.nro_hijos+1
        
    if hijos_i<10:
        codigo=codigo+"0"+str(hijos_i)
    else:
        codigo=codigo+str(hijos_i)

            

    #Asigna el formulario creado en Forrms
    form=CreaProcesoForm()

    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProcesoForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            proc_hijo=Proceso()
            
            proc_hijo.proceso_padre = cod
            proc_hijo.pk_padre=pk
            proc_hijo.proceso = codigo
            proc_hijo.nombre = form.cleaned_data['nombre']
            proc_hijo.objetivo=form.cleaned_data['objetivo']
            proc_hijo.fecha_crea=datetime.date.today()
            proc_hijo.es_subproceso=form.cleaned_data['es_subproceso']

            path = proc_padre.path
            path=path.strip()
            path=path + './. ' + form.cleaned_data['nombre'].strip()
            proc_hijo.path=path
            
            #proc_hijo.ni='&emsp;'

            for i in codigo:
                proc_hijo.ni=proc_hijo.ni+'.'
                
                      
            #Crea registro del SubProceso
            if proc_hijo.es_subproceso:
                proc_hijo.subproceso=SubProceso()

                proc_hijo.subproceso.pk_padre = pk
                proc_hijo.subproceso.codigo=codigo
                proc_hijo.subproceso.path=path
                
                #Asigna valores de estado del Proceso                                         
                proc_hijo.subproceso.status='C'
                proc_hijo.subproceso.fase_status='M'

                #Asigna valores iniciales RACI (todos quedan asignados al usuario de sesion)
                usuario_sesion = request.user.pk
                print('usr_ses=',usuario_sesion)
           
                          
                #usuario_a=Gestor.objects.get(cargo=='Gerente TI')
                
                usuario_ges=get_object_or_404(Gestor, user_pk=usuario_sesion)

                print('usuario_gestor', usuario_ges)
                
                proc_hijo.subproceso.gestor_R=usuario_ges
                proc_hijo.subproceso.gestor_A=usuario_ges
                proc_hijo.subproceso.gestor_C=usuario_ges
                #proc_hijo.subproceso.gestor_I=usuario_ges
                #proc_hijo.subproceso.subproceso_r
                

                #Graba registro del SubProceso
                proc_hijo.subproceso.save()


            proc_hijo.nro_hijos=0
            proc_padre.nro_hijos=hijos_i

                        
            proc_hijo.save()           
            proc_padre.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Procesos') )

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            


    # If this is a GET (or any other method) create the default form.
    else:
    
        return render(request, 'bcp/proceso_crea.html', {'form': form, 'proceso':proc_padre})

#***********************
# 2.1.2 Borra  Proceso *
#***********************

#@permission_required('Catalogo.can_mark_returned')
@login_required
def borra_proceso(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))


    proceso = get_object_or_404(Proceso, pk = pk)
    pk2 = proceso.pk_padre
    proceso_padre = get_object_or_404(Proceso, pk = pk2)



    if proceso.es_subproceso:
            
            if proceso.subproceso.status=='C' and proceso.subproceso.fase_status == 'M':
                
                proceso.subproceso.delete()
                proceso.delete()
                proceso_padre.nro_hijos = proceso_padre.nro_hijos - 1
                proceso_padre.save()
                print('SubProceso Borrado')
            else:
                print('Proceso no se puede borrar')
                

    else:

        if proceso.nro_hijos == 0:
            proceso.delete()
            if proceso.proceso != 'root':
                proceso_padre.nro_hijos = proceso_padre.nro_hijos - 1
            proceso_padre.save()
            print('Proceso Borrado')

        else:
            print('Proceso no se puede borrar')
        

    # redirect to a new URL:
    return HttpResponseRedirect(reverse('Lista-Procesos') )



#**************************
#2.4 Crea Activo o Recurso*
#**************************
@login_required
def Lista_SRV(request, pk_proc, origen):

    """Lista los Servicios o Recursos definidos en la Base de Servicios
    
        pk_proc: 
            Si <> 0 Trae el pk del Proceso 
            0 si viene de la Lista de Asignacion de Activos
        origen: 
            0: si viene de la Lista 
            1: si viene de Asignar el Servicios/Recurso
            2: si viene de Corregir el Servicios/Recurso
    """

    print('----- Lista SRV----')

    if pk_proc != 0:
        proceso=get_object_or_404(Proceso, pk=pk_proc)
    else:
        srv=0

    lista_srv=Recursos.objects.all() 

    #url_comp=Componentes.get_absolute_url
    print('url ant=', url_ant)

    return render(request, 'bcp/map_act/lista_srv.html', context={'lista_srv':lista_srv,
                                                              'proceso':proceso,
                                                              'origen':origen
                                                              })

from .forms import CreaActivoForm
#@permission_required('Catalogo.can_mark_returned')
#def Crea_Activo(request):
@login_required
def Crea_SRV(request):
    """
    Crea un Servicio / Recurso en la Base de Datos.
    """
    print("=== Entra a Crea_SRV ===")
    print("Método:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)
    print('--- CREA CMP ----')

    # Determina el URL al que volver
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    print(">>> next_url:", next_url)

    if request.method == 'POST':
        form = CreaActivoForm(request.POST)

        if form.is_valid():

            # Genera el código solo al grabar
            cod = get_object_or_404(Parametros_G, nombre='CORRELATIVO SERVICIOS/REC')
            codigo = f"SRV-{cod.valor_2}"
            cod.valor_2 += 1
            cod.save()

            # Crea en BD
            srv = Recursos(
                cod_rec=codigo,
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                tipo=form.cleaned_data['tipo'],
            )
            srv.save()

            print('>>> Componente creado, redirigiendo a:', next_url)
            return redirect(next_url)

        else:
            print('>>> Error de formulario:', form.errors)
            return render(
                request,
                'bcp/mensajes/mensajes_error_Form.html',
                {'form': form.errors}
            )

    else:
        form = CreaActivoForm()

    return render(request, 'bcp/map_act/crea_srv.html', {
        'form': form,
        'next': next_url
    })


from .forms import CreaActivoForm
#@permission_required('Catalogo.can_mark_returned')
#def Crea_Activo(request):
@login_required
def Mod_SRV(request, pk):
    """
    Modifica un Servicio / Recurso en la Base de Datos.
    pk: pk del Servicio
    """
    print("=== Entra a Mod_SRV ===")
    print("Método:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)
    print('--- CREA CMP ----')

    # Determina el URL al que volver
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    print(">>> next_url:", next_url)

    srv=get_object_or_404(Recursos, pk=pk)
    if request.method == 'POST':
        form = CreaActivoForm(request.POST)

        if form.is_valid():

            # Modifica en BD
            srv.nombre=form.cleaned_data['nombre']
            srv.descripcion=form.cleaned_data['descripcion']
            srv.tipo=form.cleaned_data['tipo']
            srv.save()

            print('>>> Componente modificado, redirigiendo a:', next_url)
            return redirect(next_url)

        else:
            print('>>> Error de formulario:', form.errors)
            return render(
                request,
                'bcp/mensajes/mensajes_error_Form.html',
                {'form': form.errors}
            )

    else:
        form = CreaActivoForm(initial={'nombre':srv.nombre,
                                       'descripcion':srv.descripcion,
                                       'tipo':srv.tipo
                                       })

    return render(request, 'bcp/map_act/mod_srv.html', {
        'form': form,
        'next': next_url
    })

@login_required
def Borra_SRV(request, pk):
    """
    Borra el Servicio / Recurso de la Base """
     
    # Borra el Componente 
    srv=get_object_or_404(Recursos, pk=pk)
    srv.delete()

    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


#************************************************** Fin Creacion/Borrado de Entidades *****************************************************    

#*********************************************************************************************************************************************
#*********************************************** 3. Gestion de Autorizaciones *** ************************************************************
#*********************************************************************************************************************************************

#****************
# Actualizacion *
#****************
@login_required
def Actualiza_Mapeo(request, pk):
    """
    Cambia el estado de un Proceso autorizado en todas sus fases para su actualizacion
    """
    print('-- Actualiza Mapeo :')

    proceso=get_object_or_404(Proceso, pk=pk)
    print('--- Proceso :', proceso)
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)

    proceso.subproceso.status="C"
    proceso.subproceso.fase_status="M"
    proceso.subproceso.actualiza=True
    print('--- en_actua.. : ', proceso.subproceso.actualiza )
    proceso.subproceso.save()

     # Crea Log de Rechazo de Autorizador
    log=Log_Revision()
    log.fecha = datetime.date.today()
    log.proceso= proceso
    log.gestor_aut=proceso.subproceso.gestor_C
    log.seccion="M"
    log.campo="Autorizado por:"+aut
    log.comentario="Inicio Ciclo de Actualizacion del Proceso."
    log.resuelto=True
    log.save()

    return HttpResponseRedirect(reverse('Lista-Procesos') )


#**********************
# 3.1 Asignacion  RACI*
#**********************
from .forms import AsignaRaciForm
@login_required
def Asigna_Raci(request, pk, etapa):
    """
    Funcion de vista para asignar usuarios a esquema RACI
    """
    print ('---- view Asigna Raci -----')

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    global url_ant
    
    print('Etapa:',etapa)
    model = Proceso
    proc_raci=get_object_or_404(Proceso, pk = pk)
    ruta_p=proc_raci.path
    
    nom_proc=extraer_desde_char(ruta_p,'/')
    ruta=resta_string(ruta_p,nom_proc)
    print('---- nombre proceso :', nom_proc)
    #form = AsignaRaciForm()
    
        
    if request.method =='POST':
        print('--Entra a metodo POST ---')
        form = AsignaRaciForm(request.POST)

        v= form.is_valid()
        print ('Formato valido =', v)
        print ('Errores = ', form.errors)
        
        if form.is_valid():
            
            #Graba intancias en Registro
                       
            proc_raci.subproceso.gestor_R =form.cleaned_data['gestor_R']
            proc_raci.subproceso.gestor_A =form.cleaned_data['gestor_A']
            #proc_raci.subproceso.gestor_C =form.cleaned_data['gestor_C']
            proc_raci.subproceso.gestor_I =form.cleaned_data['gestor_I']

            notifica=form.cleaned_data['notifica']
            
            # Cambia status del Proceso a x Aprobar

            proc_raci.subproceso.status='A'

            # Notifica por correo a Gestor A            
            #if notifica:
            #    email = proc_raci.subproceso.gestor_A.email
            #    cc_email= proc_raci.subproceso.gestor_C.email
            #    nombre=proc_raci.subproceso.gestor_C.last_name
            #    proceso=proc_raci.path
            #    accion='revisar definicion y aprobar o requerir cambios al '
                
            #    Manda_Correo(email, cc_email, nombre, proceso, accion)

                  
            proc_raci.subproceso.save()

            # Crea Log de aprobacion de [R]utorizador
            log=Log_Revision()
            log.fecha = datetime.date.today()
            log.proceso= proc_raci
            log.gestor_aut=proc_raci.subproceso.gestor_C
            log.seccion=proc_raci.subproceso.fase_status
            log.campo="Asignacion RACI"
            log.comentario =  "A: "+proc_raci.subproceso.gestor_A.user_gestor.last_name+', '
            log.comentario += proc_raci.subproceso.gestor_A.user_gestor.first_name+' - '
            log.comentario += ", R: "+proc_raci.subproceso.gestor_R.user_gestor.last_name+', '
            log.comentario += proc_raci.subproceso.gestor_R.user_gestor.first_name+' - '
            if proc_raci.subproceso.gestor_I:
                log.comentario += ", R: "+proc_raci.subproceso.gestor_I.user_gestor.last_name+', '
                log.comentario += proc_raci.subproceso.gestor_I.user_gestor.first_name
            else:
                log.comentario += ", No se asigna Persona Interesada"
                
            log.resuelto=True
            log.save()
     
            
            # redirect to a new URL:

            print ('url anterior 0 POST =', url_ant)
                         
            return HttpResponseRedirect(url_ant)

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
        
    else:
        
        url_ant=request.META['HTTP_REFERER']
        print ('url anterior 0 GET=', url_ant)

        
        form = AsignaRaciForm(initial= {
                                        'gestor_R':proc_raci.subproceso.gestor_R,
                                        'gestor_A':proc_raci.subproceso.gestor_A,
                                        'gestor_C':proc_raci.subproceso.gestor_C,
                                        'gestor_I':proc_raci.subproceso.gestor_I,
                                        'notifica':False,
                                        }
                             )
                                        
        return render(request, 'bcp/raci_asigna.html', {'form': form,
                                                        'proc_raci':proc_raci,
                                                        'ruta':ruta,
                                                        'n_proceso':nom_proc,
                                                        'etapa':etapa})


#*********************************
#3.2 Autorizacion RACI de Proceso*
#*********************************
from .forms import AutorizaRaciForm
import datetime
@login_required
def Autoriza_M(request, pk):
    
    proc = get_object_or_404(Proceso, pk = pk)
    
    comentarios_proceso=Log_Revision.objects.filter(proceso=proc)
    comentarios_m=[]
    for com in comentarios_proceso:
        if com.seccion == "M":
            comentarios_m.append(com)
            

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)

    if request.method=='POST':

        form = AutorizaRaciForm(request.POST)
        
        
        if form.is_valid():
            
            #Registra autorizacion en Log.  
           
            notifica=form.cleaned_data['notifica']
            aprobado=form.cleaned_data['aprobacion']
            
                        
            if proc.subproceso.status=='A': # (Si es primera revision ...)
                
                if aprobado:
                    print('aprobo A->r')
                    proc.subproceso.status='r' # (Manda a revision del [R]esponsable)

                    # Crea Log de aprobacion de [A]utorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc
                    log.gestor_aut=usr_aut
                    log.seccion="M"
                    log.campo="Autorizado por:"+aut
                    log.comentario="Proceso aprobado por Gestor Autorizador"
                    log.resuelto=True
                    log.save()
                    
                    # Prepara datos del correo 
                    nombre=proc.subproceso.gestor_R.user_gestor.last_name
                    email = proc.subproceso.gestor_R.user_gestor.email
                    accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    proc.subproceso.status='x' # (Devuelve a [C]onsultor)
                    print ('rechazo A->x')

                    # Crea Log de Rechazo de Autorizador.
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc
                    log.gestor_aut=usr_aut
                    log.seccion="M"
                    log.campo="Observado por:"+aut
                    log.comentario="Proceso observado por Gestor Autorizador. Se envia a Gestor Consultor para su Revision. "
                    log.resuelto=True
                    log.save()


                    email = proc.subproceso.gestor_C.user_gestor.email
                    accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proc.subproceso.status=='r': # (Si es una revision ... )

                    if aprobado:
                        """ Pasa a estado Vigenteado"""
                        print('aprobo A->R')
                        proc.subproceso.status='R'

                        # Crea Log de aprobacion de [R]esponsable
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proc
                        log.gestor_aut=usr_aut
                        log.seccion="M"
                        log.campo="Autorizado por:"+aut
                        log.comentario="Proceso aprobado por Nivel [R]esponsable"
                        log.resuelto=True
                        log.save()
                    
                        if proc.subproceso.gestor_I:
                            nombre=proc.subproceso.gestor_I.user_gestor.last_name
                            email = proc.subproceso.gestor_C.user_gestor.email
                            accion='tomar conocimiento de la puesta en vigencia del '
                            
                    else:
                        """ Pasa a revision por C """
                        proc.subproceso.status='x'

                        # Crea Log de Observacion de [R]esponsable
                        #log=Log_Revision()
                        #log.fecha = datetime.date.today()
                        #log.proceso= proc
                        #log.gestor_aut=usr_aut
                        #log.seccion="M"
                        #log.campo="Observado por:"+aut
                        #log.comentario="Proceso observado por Gestor Responsable. Se envia a Revision por Gestor Autorizador."
                        #log.resuelto=True
                        #log.save()


                
            #Notificar a Gestor I por email
            if notifica:
                if aprobado:
                    cc_email= proc.subproceso.gestor_C.user_gestor.email
                    proceso=proc.path
                    Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
                           
            proc.subproceso.save()
            
             
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Procesos') )

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'bcp/proceso_auth.html', {'form': form,
                                                         'autorizador':aut, 
                                                         'proceso':proc,
                                                         'comentarios':comentarios_m})
    

#********************************************************
#3.3  Autorizacion RACI de Asignacion   BIA  a Proceso **
#********************************************************
from .forms import Autoriza_BIA_Form
#import datetime
@login_required
def Aut_Asig_BIA(request, pk):
    """ Los comentarios se registran mediante un script (main.js) en el Template y se cargan a la 
    base con la vista "Crea_Rev_OC" """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    proceso=get_object_or_404(Proceso, pk = pk)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)

    # Selecciona observaciones del proceso de asignacion ("V")
    comentarios_proceso=Log_Revision.objects.filter(proceso=proceso)
    comentarios_v=[]
    for com in comentarios_proceso:
        if com.seccion == "V":
            comentarios_v.append(com)

    print('comentarios_v=', comentarios_v)
    #.objects.filter(seccion="V") # Observaciones de Asignacion BIA
    #impactos=proceso.subproceso.impact_subp
    #indicadores=proceso.subproceso.indicadores_subp


    if request.method=='POST':

        form = Autoriza_BIA_Form(request.POST)
        
        
        if form.is_valid():
            
            #Registra autorizacion en log
                             
         
            notifica=form.cleaned_data['notifica']
            aprobado=form.cleaned_data['aprobacion']

                        
            #Cambia Estado de Aprobacion
            print(proceso.subproceso.status)
            if proceso.subproceso.status=='A':
            # Si el estado esta en x Aprobar 
                
                if aprobado:
                    print('aprobo A->r')
                    # Si es aprobado cambia a  x Vigentear
                    proceso.subproceso.status='r'

                    # Crea Log de aprobacion de Autorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proceso
                    log.gestor_aut=usr_aut
                    log.seccion="V"
                    log.campo="Autorizado por:"+aut
                    log.comentario="BIA Aprobado por Gestor Autorizador"
                    log.resuelto=True
                    log.save()

                    # Prepara correo informativo
                    nombre=proceso.subproceso.gestor_R.user_gestor.last_name
                    email = proceso.subproceso.gestor_R.user_gestor.email
                    accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    # Si no es aprobado cambia a En Revision
                    proceso.subproceso.status='x'

                    # Crea Log de rechazo de Autorizador
                    #log=Log_Revision()
                    #log.fecha = datetime.date.today()
                    #log.proceso= proceso
                    #log.gestor_aut=usr_aut
                    #log.seccion="V"
                    #log.campo="Observado por:"+aut
                    #log.comentario="BIA observado por Gestor Autorizador. Se envia a revision por Gestor Consultor"
                    #log.resuelto=True
                    #log.save()

                    email = proceso.subproceso.gestor_C.user_gestor.email
                    accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proceso.subproceso.status=='r': 

                    if aprobado:
                        print('aprobo r->R')
                        proceso.subproceso.status='R'
                        # Crea Log de aprobacion de Responsable
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proceso
                        log.gestor_aut=usr_aut
                        log.seccion="V"
                        log.campo="Aprobado por:"+aut
                        log.comentario="BIA Aprobado por Gestor Responsable"
                        log.resuelto=True
                        log.save()

                    
                        if  proceso.subproceso.gestor_I:
                            nombre=proceso.subproceso.gestor_I.user_gestor.last_name
                            email = proceso.subproceso.gestor_C.user_gestor.email
                            accion='tomar conocimiento de la puesta en vigencia del '
                    else:
                        proceso.subproceso.status='x'
                        # Crea Log de rechazo de Responsable
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proceso
                        log.gestor_aut=usr_aut
                        log.seccion="V"
                        log.campo="Observado por:"+aut
                        log.comentario="BIA observado por Gestor Responsable"
                        log.resuelto=True
                        log.save()


            #Notificar a Gestor I por email
            if notifica:
                if aprobado:
                    cc_email= proceso.subproceso.gestor_C.user_gestor.email
                    proceso=proceso.path
                    Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
            
                             
            proceso.subproceso.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Evaluaciones'))            

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

        
    else:
    
        form = AutorizaRaciForm(initial= {'aprobacion':False, 'notifica':False }
                             )
                                        
        return render(request, 'bcp/map_eval/asig_eval_auth.html', {'form': form,
                                                                    'autorizador':aut,
                                                                    'proceso':proceso,
                                                                    'comentarios':comentarios_v})
    
# OBSOLETO (BORRAR) 
def aut_obs_proceso(request, item, pk, valor):
    """
    Registra observaciones por item a la
    Autorizacion de Procesos
    """

    global  url_ant_obs_aut

    print('item:', item)
    print('pk :', pk)
    print('valor:', valor)
    
    proc = get_object_or_404(Proceso, pk = pk)
        
    aut=LogAut()
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    print('usuario de sesion',aut.gestor_aprobador.user_gestor.username)
    print('usr sesion pk :', pk_usr_sesion)
    print('gestor_ap     :', aut.gestor_aprobador.pk)


    if item=='SCS':
        item='Servicio Critico seleccionado..:.'+valor
        valor=''
                
    elif item=='SCNS':
        item='Servicio Critico NO seleccionado..:.'+valor
        valor=''
                
    elif item=='ERS':
        item='Escenario de Riesgo seleccionado..:.'+ valor
        valor=''
                
    elif item=='ERNS':
        item='Escenario de Riesgo  NO Seleccionado..:.'+ valor
        valor=''

    if request.method=='POST':

        form = Autoriza_obs_Proced_C_Form(request.POST)
        
        print('FORMATO VALID0?',form.is_valid())
        
        if form.is_valid():
            
            #Registra autorizacion en log
                                
            aut.cod_proceso=proc.proceso  
            aut.fecha=datetime.date.today()
            aut.p_status=proc.subproceso.status+proc.subproceso.fase_status
            aut.item=item
            aut.observacion=form.cleaned_data['comentario']  
        
            #Graba en Base de Datos                
            aut.save()
            proc.log_auth.add(aut)      
            proc.save()
            
                
            # redirect to a new URL:
            return HttpResponseRedirect(url_ant_obs_aut)

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        url_ant_obs_aut =request.META['HTTP_REFERER']
        form= Autoriza_obs_Proced_C_Form()
        
        return render(request, 'bcp/proceso_obs_auth.html', {'form': form, 'proc':proc, 'item':item, 'valor':valor})

@login_required
def borra_obs_proceso(request, pk):
    """
    Borra observacion a nivel de item
    """

    url_ant= request.META['HTTP_REFERER']
    
    item_auth=get_object_or_404(LogAut, pk = pk)
    item_auth.delete()
    
    return HttpResponseRedirect(url_ant)



#*********************************************************
#3.4 Autorizacion de Asignacion de Activos a Proceso     *
#*********************************************************
from .forms import Autoriza_Act_x_Proc_Form
import datetime
@login_required
def Aut_Asig_Act(request, pk):

    print('--- Entra a Vista: Autorizacion de ASignacion Aut_Asig_Act')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[300] ))
    
    model = Proceso
    proc = get_object_or_404(Proceso, pk = pk)
    subproceso=proc.subproceso
    activos=proc.subproceso.recursos
    activos_disp=Recursos.objects.all().order_by('tipo')
    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)



    form = Autoriza_Act_x_Proc_Form()
    #aut=LogAut()

    # Selecciona observaciones del proceso de asignacion ("V")
    comentarios_proceso=Log_Revision.objects.filter(proceso=proc)
    comentarios_a=[]
    for com in comentarios_proceso:
        if com.seccion == "B":
            comentarios_a.append(com)

    print('comentarios_a=', comentarios_a)

    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    #aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    #print('usuario de sesion',aut.gestor_aprobador)


    
    #aut.cod_proceso=proc.proceso 

    if request.method=='POST':

        form = Autoriza_Act_x_Proc_Form(request.POST)
        
        
        if form.is_valid():

            
            notifica=form.cleaned_data['notifica']
            aprobado=form.cleaned_data['aprobacion']            

            #Gestiona los Estados del Proceso        
                        
            if proc.subproceso.status=='A':
                
                if aprobado:
                    print('aprobo A->r')
                    proc.subproceso.status='r'
                    # Crea Log de aprobacion de Autorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc
                    log.gestor_aut=usr_aut
                    log.seccion="B"
                    log.campo="Autorizado por:"+aut
                    log.comentario="Asignacion de Servicios Criticos Aprobado por Gestor Autorizador"
                    log.resuelto=True
                    log.save()
                    
                    # Prepara correo al Gestor Responsable
                    #nombre=proc.subproceso.gestor_R.user_gestor.last_name
                    #email = proc.subproceso.gestor_R.user_gestor.email
                    #accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    proc.subproceso.status='x'
                    # Crea Log de aprobacion de Autorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc
                    log.gestor_aut=usr_aut
                    log.seccion="B"
                    log.campo="Observado por:"+aut
                    log.comentario="Asignacion de Servicios Criticos observado por Gestor Autorizador. Se envia a Gestor Consultor para su Revision."
                    log.resuelto=True
                    log.save()

                    # Prepara correo para Gestor Consultor
                    #email = proc.subproceso.gestor_C.user_gestor.email
                    #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proc.subproceso.status=='r':

                    if aprobado:
                        print('aprobo r->R')
                        proc.subproceso.status='R'
                        # Crea Log de aprobacion de Autorizador
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proc
                        log.gestor_aut=usr_aut
                        log.seccion="B"
                        log.campo="Autorizado por:"+aut
                        log.comentario="Asignacion de Servicios Criticos Aprobado por Gestor Responsable"
                        log.resuelto=True
                        log.save()
                   
                        # Prepara correo a Gestor Interesado
                        #if proc.subproceso.gestor_I:
                        #    nombre=proc.subproceso.gestor_I.user_gestor.last_name
                        #    email = proc.subproceso.gestor_C.user_gestor.email
                        #    accion='tomar conocimiento de la puesta en vigencia del '
                    else:
                        proc.subproceso.status='x'
                        # Crea Log de aprobacion de Autorizador
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proc
                        log.gestor_aut=usr_aut
                        log.seccion="B"
                        log.campo="Observado por:"+aut
                        log.comentario="Asignacion de Servicios Criticos observada por Gestor Responsable. Se envia a Gestor Consultor para su Revision."
                        log.resuelto=True
                        log.save()

                
            #Notificar a Gestor I por email
            if notifica:
                if aprobado:
                    print('**** Envia Correo ****')
                    #cc_email= proc.subproceso.gestor_C.user_gestor.email
                    #proceso=proc.path
                    #Manda_Correo(email, cc_email, nombre, proceso, accion)
                    

            #Registra autorizacion en log
                                
            #aut.fecha=datetime.date.today()
            #aut.p_status=proc.subproceso.status+proc.subproceso.fase_status
            #aut.item = 'Conclusion etapa Autorizacion.:'
            #aut.observacion=form.cleaned_data['comentario']
            #aut.Aprobado=form.cleaned_data['aprobacion']
            
            notifica=form.cleaned_data['notifica']
            aprobado=form.cleaned_data['aprobacion']            

            #Graba en la BD                             
            #aut.save()
            #proc.log_auth.add(aut)      
            proc.subproceso.save()
            
             
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Recursos') )

        else:

            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )

        # Cargar recursos disponibles y asignados
        recursos_disponibles = Recursos.objects.exclude(id__in=subproceso.recursos.values_list('id', flat=True))
        recursos_asignados = subproceso.recursos.all()
        print('---- recursos_asignados=', recursos_asignados)


        return render(request, 'bcp/map_act/asig_act_auth.html', {'form': form,
                                                                  'proceso':proc,
                                                                  'recursos_disponibles':recursos_disponibles,
                                                                  'recursos_asignados':recursos_asignados,
                                                                  'activos':activos,
                                                                  'activos_disp':activos_disp,
                                                                  'comentarios':comentarios_a})


#********************************************************
#3.5 Autorizacion de Asignacion de Escenario a Proceso  *
#********************************************************
from .forms import Autoriza_Asig_Escenarios_Form
import datetime

@login_required
def auth_asig_SCER(request, pk): 
    """
    Autorizacion de los Servicios Criticos y Escenarios de Riesgo asignados
    """

    print('----Entra a View  Autorizacion Asignacion Servicios y Escenario (Aut_Asig_Esc) ----')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[300] ))

    # Datos de Servicios asociados al Proceso
    proc = get_object_or_404(Proceso, pk = pk)
    subproceso=proc.subproceso
    activos=proc.subproceso.recursos
    activos_disp=Recursos.objects.all().order_by('tipo')

    # Datos de Escenarios asociados al Proceso
    #model = Proceso
    escenarios=proc.subproceso.escenarios
    esc_disp=Escenarios.objects.all()
    

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)

    form = Autoriza_Asig_Escenarios_Form()
    #aut=LogAut()

    # Selecciona los comentarios sobre Servicios y Escenarios
    comentarios_proceso=Log_Revision.objects.filter(proceso=proc)
    comentarios_e=[]
    for com in comentarios_proceso:
        if com.seccion == "E" or com.seccion == "B" :
            comentarios_e.append(com)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    #aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    #print('usuario de sesion',aut.gestor_aprobador)

   
    #aut.cod_proceso=proc.proceso 

    if request.method=='POST':

        form = Autoriza_Asig_Escenarios_Form(request.POST)
        
        
        if form.is_valid():
            
            
            notifica=form.cleaned_data['notifica']
            aprobado=form.cleaned_data['aprobacion']
            
            #---
            print(proc.subproceso.status)
            if proc.subproceso.status=='A':
                
                if aprobado:
                    print('aprobo A->r')
                    proc.subproceso.status='r'  # Cambia Status a "Por Vigentear"

                    # Crea Log de aprobacion de Autorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc
                    log.gestor_aut=usr_aut
                    log.seccion="E"
                    log.campo="Autorizado por:"+aut
                    log.comentario="Asignacion de Escenarios de Riesgo Aprobado por Gestor Autorizador"
                    log.resuelto=True
                    log.save()

                    
                    # Prepara email para Gestor Responsable 
                    #nombre=proc.subproceso.gestor_R.user_gestor.last_name
                    #email = proc.subproceso.gestor_R.user_gestor.email
                    #accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    # Cambia Status a "Revisar"
                    proc.subproceso.status='x' 

                    # Crea Log de Rechazo de Autorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc
                    log.gestor_aut=usr_aut
                    log.seccion="E"
                    log.campo="Observada por:"+aut
                    log.comentario="Asignacion de Escenarios de Riesgo observada por Gestor Autorizador. Se envia a Gestor Consultor para Revision."
                    log.resuelto=True
                    log.save()

                    
                    #Prepara email para Gestor Consultor
                    #email = proc.subproceso.gestor_C.user_gestor.email
                    #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proc.subproceso.status=='r':

                    if aprobado:
                        print('aprobo r->R')
                        proc.subproceso.status='R'
                        proc.subproceso.fase_status='E'
                        proc.subproceso.actualiza=False

                        # Crea Log de aprobacion de Autorizador
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proc
                        log.gestor_aut=usr_aut
                        log.seccion="E"
                        log.campo="Autorizado por:"+aut
                        log.comentario="Asignacion de Servicios Criticos y Escenarios de Riesgo Aprobado por Gestor Responsable."
                        log.resuelto=True
                        log.save()


                        # Crea o Modifica Proceso (SubProceso) Vigente
                        # Crea una entrada al log de Control de Cambios
                        # =============================================

                        p_vigente_existe=SubProceso_V.objects.filter(codigo=proc.subproceso.codigo).exists()
                        hay_cambios=False


                        if not p_vigente_existe:
                            # Si el Proceso Vigente no existe, lo crea.

                            # Crea Log de Creacion de Proceso Vigente 
                            log=Log_Revision()
                            log.fecha = datetime.date.today()
                            log.proceso= proc
                            log.gestor_aut=usr_aut
                            log.seccion="E"
                            log.campo="Autorizado por:"+aut
                            log.comentario="Se crea un Proceso vigente (sujeto a Contingenciar)"
                            log.resuelto=True
                            log.save()


                            sub_proceso_v=SubProceso_V()
                            print('Crea version inicial del Subproceso vigente.')
                            detalle_log="Version Inicial"

                            sub_proceso_v.nombre=proc.nombre
                            sub_proceso_v.objetivo=proc.objetivo
                            sub_proceso_v.version=1


                            sub_proceso_v.fecha_ult_aut=datetime.date.today()
                            sub_proceso_v.pk_padre = proc.subproceso.pk_padre
                            sub_proceso_v.codigo   = proc.subproceso.codigo
                            sub_proceso_v.path = proc.subproceso.path

                            sub_proceso_v.gestor_R = proc.subproceso.gestor_R
                            sub_proceso_v.gestor_A = proc.subproceso.gestor_A
                            sub_proceso_v.gestor_C = proc.subproceso.gestor_C
                            sub_proceso_v.gestor_I = proc.subproceso.gestor_I

                            sub_proceso_v.save()

                            # Asigna Impactos

                            impactos_asig = proc.subproceso.impact_subp.all()
                            impactos_asig_v = []
                            print('-- impactos asignados :', impactos_asig)


                            for imp in impactos_asig:
                                try:
                                    imp_v, created = Impactos_Asig_v.objects.get_or_create(
                                        impacto=imp.impacto,
                                        nivel=imp.nivel
                                    )
                                    impactos_asig_v.append(imp_v)
                                    if created:
                                        print(f"Creado nuevo Impactos_Asig_v: {imp_v}")
                                        
                                except Exception as e:
                                    print(f"Error al crear o recuperar impacto: {imp.impacto} / {imp.nivel} -> {e}")

                            # Relaciona al subproceso vigente
                            sub_proceso_v.impact_subp.set(impactos_asig_v)

                           
                            # Asigna Indicadores
                            # Obtener los indicadores asignados al proceso editable
                            indicadores_asig = proc.subproceso.indicador_subp.all()
                            indicadores_asig_v = []
                            print('-- indicadores asignados: ', indicadores_asig)

                            # Buscar sus equivalentes en Indicadores_Asig_v
                            for ind in indicadores_asig:
                                try:
                                    ind_v, created = Indicadores_Asig_v.objects.get_or_create(
                                        indicador=ind.indicador,
                                        nivel=ind.nivel
                                    )
                                    indicadores_asig_v.append(ind_v)
                                    if created:
                                        print(f"Creado nuevo Indicadores_Asig_v: {ind_v}")
                                except Exception as e:
                                    print(f"Error al crear o recuperar indicador: {ind.indicador} / {ind.nivel} -> {e}")

                            # Asignar la lista encontrada al ManyToManyField del modelo vigente
                            sub_proceso_v.indicador_subp.set(indicadores_asig_v)


                            sub_proceso_v.ranking =  proc.subproceso.ranking
                            sub_proceso_v.recursos.set(proc.subproceso.recursos.all())
                            sub_proceso_v.escenarios.set(proc.subproceso.escenarios.all())

                            sub_proceso_v.save()
                            proc.subproceso_v = sub_proceso_v
                            proc.save()
                            print('Actualiza tabla de procesos')


                        else:
                            # Si el Proceso vigente ya existe

                            # Cambios en Proceso Vigente 
                            # ============================

                            print('Modifica el Proceso vigente existente')

                            sub_proceso_v=get_object_or_404(SubProceso_V, codigo=proc.subproceso.codigo)
                            sub_proceso_v.fecha_ult_aut=datetime.date.today()
                            detalle_log="Cambios implementados a version "+str(sub_proceso_v.version)+" :-> "

                            # Crea "Log de Creacion" de Proceso Vigente  en log de Revision 
                            log=Log_Revision()
                            log.fecha = datetime.date.today()
                            log.proceso= proc
                            log.gestor_aut=usr_aut
                            log.seccion="E"
                            log.campo="Autorizado por:"+aut
                            log.comentario="Se modifica version "+str(sub_proceso_v.version)+" del Proceso"
                            log.resuelto=True
                            log.save()
                         
                            sub_proceso_v.version=sub_proceso_v.version+1


                            
                            # Deteccion de Cambios y actualizacion de Control de Cambios
                            # ==========================================================

                            # Datos Sub Proceso
                            # -----------------

                            if sub_proceso_v.nombre != proc.nombre:
                                print('Cambio a Nombre del Proceso')
                                sub_proceso_v.nombre = proc.nombre
                                detalle_log=detalle_log+'Cambio a nombre del Proceso. De :'+sub_proceso_v.nombre+' a: '+proc.nombre+'.//'

                            if sub_proceso_v.objetivo != proc.objetivo:
                                print('Cambio descripcion de objetivo')
                                sub_proceso_v.objetivo = proc.objetivo
                                detalle_log=detalle_log+'Cambio en la descripcion del objetivo. De : '+sub_proceso_v.objetivo+' a: '+proc.objetivo+'.//'
     
                            # Gestores
                            # --------

                            if sub_proceso_v.gestor_R != proc.subproceso.gestor_R:
                                print('Cambio al Gestor Responsable')
                                detalle_log=detalle_log+'Cambio al Gestor Responsable de: '+sub_proceso_v.gestor_R.user_gestor.last_name+','+sub_proceso_v.gestor_R.user_gestor.first_name+', por :'+proc.subproceso.gestor_R.user_gestor.last_name+','+proc.subproceso.gestor_R.user_gestor.first_name+'.//'
                                sub_proceso_v.gestor_R = proc.subproceso.gestor_R
                                hay_cambios=True

                            if sub_proceso_v.gestor_A != proc.subproceso.gestor_A:
                                print('Cambio al Gestor Autorizador')
                                detalle_log=detalle_log+'Cambio al Gestor Autorizador de: '+sub_proceso_v.gestor_A.user_gestor.last_name+','+sub_proceso_v.gestor_A.user_gestor.first_name+', por :'+proc.subproceso.gestor_A.user_gestor.last_name+','+proc.subproceso.gestor_A.user_gestor.first_name+'.//'
                                sub_proceso_v.gestor_A = proc.subproceso.gestor_A
                                hay_cambios=True


                            if sub_proceso_v.gestor_I != proc.subproceso.gestor_I:
                                print('Cambio Persona Interesada')

                                if sub_proceso_v.gestor_I:
                                    detalle_log=detalle_log+'Cambio a la Persona Interesada de: '+sub_proceso_v.gestor_I.user_gestor.last_name+','+sub_proceso_v.gestor_I.user_gestor.first_name+', por :'+proc.subproceso.gestor_I.user_gestor.last_name+','+proc.subproceso.gestor_I.user_gestor.first_name+'.//'
                                else:
                                     detalle_log=detalle_log+'Se asigna Pesona Interesada: '+proc.subproceso.gestor_I.user_gestor.last_name+','+proc.subproceso.gestor_I.user_gestor.first_name+'.//'
            
                                sub_proceso_v.gestor_I = proc.subproceso.gestor_I
                                hay_cambios=True


                            # === Versión 4.1 - Sincronización de Impactos e Indicadores ===
                            # Fecha: 2025-06-19  Hora: 20:53
                            # - Distingue correctamente entre agregados/eliminados y cambios de nivel.
                            # - Crea automáticamente registros faltantes en Impactos_Asig_v e Indicadores_Asig_v si no existen.
                            # - No elimina impactos ni indicadores por cambios de nivel.

                            # --- Sincronización de Impactos ---
                            impactos_p = list(proc.subproceso.impact_subp.all())
                            impactos_v = list(sub_proceso_v.impact_subp.all())

                            # Diccionarios por nombre de impacto
                            dict_p = {imp.impacto.nombre: imp for imp in impactos_p}
                            dict_v = {imp.impacto.nombre: imp for imp in impactos_v}

                            nombres_p = set(dict_p.keys())
                            nombres_v = set(dict_v.keys())

                            impactos_agregados = nombres_p - nombres_v
                            impactos_eliminados = nombres_v - nombres_p
                            impactos_comunes = nombres_p & nombres_v

                            # Detectar cambios de nivel (solo si están en ambos)
                            cambios_nivel = [
                                nombre for nombre in impactos_comunes
                                if dict_p[nombre].nivel.nombre != dict_v[nombre].nivel.nombre
                            ]

                            impactos_asig_v = []

                            # 1. Mantener impactos comunes sin cambios de nivel
                            for nombre in impactos_comunes:
                                if nombre not in cambios_nivel:
                                    impactos_asig_v.append(dict_v[nombre])

                            # 2. Agregar impactos nuevos
                            for nombre in impactos_agregados:
                                imp_p = dict_p[nombre]
                                imp_v, created = Impactos_Asig_v.objects.get_or_create(
                                    pk_proc=pk,
                                    impacto=imp_p.impacto,
                                    nivel=imp_p.nivel
                                )
                                impactos_asig_v.append(imp_v)

                            # 3. Reemplazar nivel de impactos con cambio de nivel
                            for nombre in cambios_nivel:
                                imp_p = dict_p[nombre]
                                imp_v, created = Impactos_Asig_v.objects.get_or_create(
                                    pk_proc=pk,
                                    impacto=imp_p.impacto,
                                    nivel=imp_p.nivel
                                )
                                impactos_asig_v.append(imp_v)

                            # 4. Asignar solo si hay cambios reales
                            if impactos_agregados or impactos_eliminados or cambios_nivel:
                                sub_proceso_v.impact_subp.set(impactos_asig_v)
                                sub_proceso_v.save()
                                hay_cambios = True

                                detalle_log += "Cambios en impactos:\n"
                                for nombre in impactos_agregados:
                                    imp = dict_p[nombre]
                                    detalle_log += f"+ Nuevo impacto: {imp.impacto.nombre} (nivel: {imp.nivel.nombre})\n"
                                for nombre in impactos_eliminados:
                                    imp = dict_v[nombre]
                                    detalle_log += f"- Impacto eliminado: {imp.impacto.nombre} (nivel: {imp.nivel.nombre})\n"
                                for nombre in cambios_nivel:
                                    imp_p = dict_p[nombre]
                                    imp_v = dict_v[nombre]
                                    detalle_log += (
                                        f"* Cambio de nivel: {imp_p.impacto.nombre}, "
                                        f"de {imp_v.nivel.nombre} a {imp_p.nivel.nombre}\n"
                                    )
                                detalle_log += ".//"
                            else:
                                print("Sin cambios en impactos.")

                            # --- Sincronización de Indicadores ---
                            indicadores_p = list(proc.subproceso.indicador_subp.all())
                            indicadores_v = list(sub_proceso_v.indicador_subp.all())

                            dict_ip = {ind.indicador.nombre: ind for ind in indicadores_p}
                            dict_iv = {ind.indicador.nombre: ind for ind in indicadores_v}

                            nombres_ip = set(dict_ip.keys())
                            nombres_iv = set(dict_iv.keys())

                            indicadores_agregados = nombres_ip - nombres_iv
                            indicadores_eliminados = nombres_iv - nombres_ip
                            indicadores_comunes = nombres_ip & nombres_iv

                            cambios_nivel_ind = [
                                nombre for nombre in indicadores_comunes
                                if dict_ip[nombre].nivel.nivel != dict_iv[nombre].nivel.nivel
                            ]

                            indicadores_asig_v = []

                            # 1. Mantener indicadores comunes sin cambios de nivel
                            for nombre in indicadores_comunes:
                                if nombre not in cambios_nivel_ind:
                                    indicadores_asig_v.append(dict_iv[nombre])

                            # 2. Agregar nuevos
                            for nombre in indicadores_agregados:
                                ind_p = dict_ip[nombre]
                                ind_v, created = Indicadores_Asig_v.objects.get_or_create(
                                    pk_proc=pk,
                                    indicador=ind_p.indicador,
                                    nivel=ind_p.nivel
                                )
                                indicadores_asig_v.append(ind_v)

                            # 3. Reemplazar nivel si cambió
                            for nombre in cambios_nivel_ind:
                                ind_p = dict_ip[nombre]
                                ind_v, created = Indicadores_Asig_v.objects.get_or_create(
                                    pk_proc=pk,
                                    indicador=ind_p.indicador,
                                    nivel=ind_p.nivel
                                )
                                indicadores_asig_v.append(ind_v)

                            # 4. Asignar si hubo cambios
                            if indicadores_agregados or indicadores_eliminados or cambios_nivel_ind:
                                sub_proceso_v.indicador_subp.set(indicadores_asig_v)
                                sub_proceso_v.save()
                                hay_cambios = True

                                detalle_log += "Cambios en indicadores:\n"
                                for nombre in indicadores_agregados:
                                    ind = dict_ip[nombre]
                                    detalle_log += f"+ Nuevo indicador: {ind.indicador.nombre} (nivel: {ind.nivel.nivel})\n"
                                for nombre in indicadores_eliminados:
                                    ind = dict_iv[nombre]
                                    detalle_log += f"- Indicador eliminado: {ind.indicador.nombre} (nivel: {ind.nivel.nivel})\n"
                                for nombre in cambios_nivel_ind:
                                    ind_p = dict_ip[nombre]
                                    ind_v = dict_iv[nombre]
                                    detalle_log += (
                                        f"* Cambio de nivel: {ind_p.indicador.nombre}, "
                                        f"de {ind_v.nivel.nivel} a {ind_p.nivel.nivel}\n"
                                    )
                                detalle_log += ".//"
                            else:
                                print("Sin cambios en indicadores.")


                            # Puntaje (Ranking) de Evaluacion
                            # ------------------------------- 

                            if sub_proceso_v.ranking !=  proc.subproceso.ranking:
                                print('Cambio en el puntaje')
                                detalle_log=detalle_log+'Se produjo un cambio en el puntaje de :'+str(sub_proceso_v.ranking) +'a :'+str(proc.subproceso.ranking)+'.//'
                                sub_proceso_v.ranking =  proc.subproceso.ranking
                                hay_cambios=True

                            # Servicios/Recursos criticos
                            # -----------------------------
                            
                            # Obtener recursos como conjuntos
                            recursos_p = set(proc.subproceso.recursos.all())
                            recursos_v = set(sub_proceso_v.recursos.all())

                            # Detectar diferencias
                            recursos_agregados = recursos_p - recursos_v
                            recursos_eliminados = recursos_v - recursos_p

                            # Si hay cambios
                            if recursos_agregados or recursos_eliminados:
                                sub_proceso_v.recursos.set(recursos_p)
                                sub_proceso_v.save()
                                hay_cambios = True

                                detalle_log += "Cambios en recursos:\n"

                                for recurso in recursos_agregados:
                                    detalle_log += f"+ Recurso agregado: {recurso.nombre}\n"

                                for recurso in recursos_eliminados:
                                    detalle_log += f"- Recurso eliminado: {recurso.nombre}\n"

                                detalle_log +='.//'
                                print("CAMBIOS EN RECURSOS:\n", detalle_log)

                            else:
                                print("Sin cambios en recursos.")


                            # Escenarios
                            # -----------

                            # Obtener los conjuntos de escenarios
                            escenarios_p = set(proc.subproceso.escenarios.all())
                            escenarios_v = set(sub_proceso_v.escenarios.all())

                            # Comparar si hay diferencias
                            if escenarios_p != escenarios_v:
                                sub_proceso_v.escenarios.set(escenarios_p)  # Actualiza la relación
                                sub_proceso_v.save()

                                detalle_log += "Cambio en escenarios:\n"
                                detalle_log += f"De: {[esc.titulo for esc in escenarios_v]}\n"
                                detalle_log += f"A: {[esc.titulo for esc in escenarios_p]}\n"
                                hay_cambios = True
                                print("CAMBIO en escenarios:", escenarios_v, "->", escenarios_p, "--", detalle_log)
                                detalle_log += './/'
                            else:
                                print("Sin cambios en escenarios:", [esc.titulo for esc in escenarios_v])


                            if not hay_cambios:
                                detalle_log=detalle_log+'Vigenteo sin cambios'

                            sub_proceso_v.save()

                        # Actualiza Base 
                        # proc.subproceso_v=sub_proceso_v
                        proc.save()
                        print('--- Actualiza Tabla de Procesos')

                        # Crea entrada para el Control de Cambios
                        # =======================================

                        log=Control_Cambios()

                        # Crea entrada
                        log.fecha=datetime.date.today()
                        log.proceso=sub_proceso_v
                        log.gestor_aut=sub_proceso_v.gestor_R
                        log.descripcion=detalle_log
                        log.save()


                        # Prepara email para Gestor Consultor
                        # ===================================
                        #  
                        # nombre=proc.subproceso.gestor_C.user_gestor.last_name
                        # email = proc.subproceso.gestor_C.user_gestor.email
                        # accion='tomar conocimiento de la puesta en vigencia del '

                    else:
                    # Si no esta aprobado
                        proc.subproceso.status='x'

                        # Crea Log de Rechazo de Autorizador
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proc
                        log.gestor_aut=usr_aut
                        log.seccion="E"
                        log.campo="Observada por:"+aut
                        log.comentario="Asignacion de Servicios Criticos y Escenarios de Riesgo observada por Gestor Responsable. Se envia a Gestor Consultor para Revision."
                        log.resuelto=True
                        log.save()

                
            #Notificar a Gestor I por email
            if notifica:
                if aprobado:
                    print('***** Envio de Correo Deshabilitado ******')
                    # Envia Correo
                    # cc_email= proc.subproceso.gestor_C.user_gestor.email
                    # proceso=proc.path
                    # Manda_Correo(email, cc_email, nombre, proceso, accion)

            #Registra autorizacion en log
                                
            #aut.fecha=datetime.date.today()
            #aut.p_status=proc.subproceso.status+proc.subproceso.fase_status
            #aut.item = 'Conclusion etapa Autorizacion.:'
            #aut.observacion=form.cleaned_data['comentario']
            #aut.Aprobado=form.cleaned_data['aprobacion']                    
            
            #Graba en Base de Datos                
            #aut.save()
            #proc.log_auth.add(aut)
                  
            proc.subproceso.save()
            
             
            # redirect to a new URL:
            #return HttpResponseRedirect(reverse('Lista-Escenarios') )
            return HttpResponseRedirect(reverse('Lista-Recursos') )

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'bcp/map_esc/aut_asig_SCER.html', {'form': form, 'proc':proc,
                                                                  'escenarios':escenarios,
                                                                  'comentarios':comentarios_e,
                                                                  'esc_disp':esc_disp,
                                                                  'activos':activos,
                                                                  'activos_disp':activos_disp})


    activos=proc.subproceso.recursos
    activos_disp=Recursos.objects.all().order_by('tipo')



#*********************************************************
#3.6  Revision de Proceso con autorizazion RACI rechazada*
#*********************************************************
from .forms import RevisaProcesoForm
@login_required
def Revisa_Proceso(request, pk):
    """
    Funcion de vista para ingresar cambios a los Procesos
    producto de Autorizacion RACI
    """
    print('--------- Entra a Revisa_Proceso -----------')

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))
    
    proc_rev=get_object_or_404(Proceso, pk = pk)

    comentarios_proceso=Log_Revision.objects.filter(proceso=proc_rev)
    comentarios_m=[]
    for com in comentarios_proceso:
        if com.seccion == "M":
            comentarios_m.append(com)

    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)


    if request.method=='POST':

        form = RevisaProcesoForm(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            print('-------- Graba instancia de Revision ---------')

            # Cambia el Path si se le cambio el nombre al Proceso.
            nombre_act=form.cleaned_data['nombre']
            if  proc_rev.nombre != nombre_act:

                proc_rev.nombre=form.cleaned_data['nombre']
                proc_padre=get_object_or_404(Proceso, pk = proc_rev.pk_padre)
                proc_rev.path=proc_padre.path+'/'+nombre_act

                
            proc_rev.objetivo=form.cleaned_data['objetivo']

            gestor_r = form.cleaned_data['gestor_R']
            gestor_i = form.cleaned_data['gestor_I']

            print(f"Antes de asignar: gestor_R = {proc_rev.subproceso.gestor_R}, gestor_I = {proc_rev.subproceso.gestor_I}")
            print(f"Datos del formulario: gestor_r = {gestor_r}, gestor_i = {gestor_i}")

            proc_rev.subproceso.gestor_R = gestor_r
            proc_rev.subproceso.gestor_I = gestor_i

            print(f"Después de asignar: gestor_R = {proc_rev.subproceso.gestor_R}, gestor_I = {proc_rev.subproceso.gestor_I}")


            proc_rev.subproceso.gestor_A =form.cleaned_data['gestor_A']
            proc_rev.subproceso.save()

            notifica=form.cleaned_data['notifica']

            #Cambia status del Proceso a x Aprobar
            if proc_rev.subproceso.gestor_C == form.cleaned_data['gestor_A']:
                
                if proc_rev.subproceso.gestor_C == form.cleaned_data['gestor_R']:
                    #Aprobada por Responsable area 
                    proc_rev.subproceso.status='R'
                    

                    #Notificar a Gestor I por email
                    if notifica:
                        email = proc_rev.subproceso.gestor_I.email
                        cc_email= proc_rev.subproceso.gestor_C.email
                        nombre=proc_rev.subproceso.gestor_C.last_name
                        proceso=proc_rev.path
                        accion='tomar conocimiento de la puesta en vigencia del '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
                else:
                    #Por Vigentear
                    proc_rev.subproceso.status='r'

                    #Notificar a Gestor R por email           
                    if notifica:
                        email = proc_rev.subproceso.gestor_R.email
                        cc_email= proc_rev.subproceso.gestor_C.email
                        nombre=proc_rev.subproceso.gestor_C.last_name
                        proceso=proc_rev.path
                        accion='dar visto bueno o requerir cambios para el '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                        
            else:
                #Por Aprobar
                proc_rev.subproceso.status='A'

                #Notifica por correo a Gestor A            
                if notifica:
                    email = proc_rev.subproceso.gestor_A.email
                    cc_email= proc_rev.subproceso.gestor_C.email
                    nombre=proc_rev.subproceso.gestor_C.last_name
                    proceso=proc_rev.path
                    accion='revisar definicion y aprobar o requerir cambios al '
                
                    Manda_Correo(email, cc_email, nombre, proceso, accion)


            #Graba registro
            proc_rev.subproceso.save()
            proc_rev.save()
            
            # Crea log de revision

                    
            log=Log_Revision()
            log.fecha = datetime.date.today()
            log.proceso= proc_rev
            log.gestor_aut=usr_aut
            log.seccion="M"
            log.campo="Modificada por:"+aut
            log.comentario="Se implementaron las Observaciones. Se devuelve a Gestor Autorizador."
            log.resuelto=True
            log.save()


            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Procesos') )

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = RevisaProcesoForm(initial= {
                                        'nombre':proc_rev.nombre,
                                        'objetivo':proc_rev.objetivo,
                                        'gestor_R':proc_rev.subproceso.gestor_R,
                                        'gestor_A':proc_rev.subproceso.gestor_A,
                                         #'gestor_C':proc_rev.subproceso.gestor_C,
                                        'gestor_I':proc_rev.subproceso.gestor_I,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'bcp/proceso_revisa.html', {'form': form,
                                                           'proceso':proc_rev,
                                                           'comentarios':comentarios_m})



#*********************************************************************************
#3.7  Revision de Asignacion de Activos a Proceso con autorizazion RACI rechazada*
#*********************************************************************************
from .forms import Revisa_AsigAct_x_Proc_Form
@login_required
def Revisa_AsigActxProceso(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))
    
    model = Proceso
    proc_rev=get_object_or_404(Proceso, pk = pk)

    
    form = Revisa_AsigAct_x_Proc_Form()


    if request.method=='POST':

        form = Revisa_AsigAct_x_Proc_Form(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            p1= form.cleaned_data['activos']
            proc_rev.subproceso.recursos.set(p1)
            

            notifica=form.cleaned_data['notifica']

            #Cambia status del Proceso a x Aprobar
            if proc_rev.subproceso.gestor_C == proc_rev.subproceso.gestor_A:
                
                if proc_rev.subproceso.gestor_C == proc_rev.subproceso.gestor_R:
                    #Aprobada por Responsable area 
                    proc_rev.subproceso.status='R'
                    

                    #Notificar a Gestor I por email
                    if notifica:
                        email = proc_rev.subproceso.gestor_I.user_gestor.email
                        cc_email= proc_rev.subproceso.gestor_C.user_gestor.email
                        nombre=proc_rev.subproceso.gestor_C.user_gestor.last_name
                        proceso=proc_rev.path
                        accion='tomar conocimiento de la puesta en vigencia del '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
                else:
                    #Por Vigentear
                    proc_rev.subproceso.status='r'

                    #Notificar a Gestor R por email           
                    if notifica:
                        email = proc_rev.subproceso.gestor_R.user_gestor.email
                        cc_email= proc_rev.subproceso.gestor_C.user_gestor.email
                        nombre=proc_rev.subproceso.gestor_C.user_gestor.last_name
                        proceso=proc_rev.path
                        accion='dar visto bueno o requerir cambios para el '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                        
            else:
                #Por Aprobar
                proc_rev.subproceso.status='A'

                #Notifica por correo a Gestor A            
                if notifica:
                    email = proc_rev.subproceso.gestor_A.email
                    cc_email= proc_rev.subproceso.gestor_C.email
                    nombre=proc_rev.subproceso.gestor_C.last_name
                    proceso=proc_rev.path
                    accion='revisar definicion y aprobar o requerir cambios al '
                
                    Manda_Correo(email, cc_email, nombre, proceso, accion)
                
                   
            proc_rev.subproceso.save()
            proc_rev.save()
     
          
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Recursos') )

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:

        p2=proc_rev.subproceso.recursos.all()
        form = Revisa_AsigAct_x_Proc_Form(initial= {'activos':set(p2),
                                                    'notifica':False}
                                          )

                                               
        return render(request, 'bcp/map_act/asigna_act_revisa.html', {'form': form, 'proceso':proc_rev})


@login_required
def rev_asigna_servicio(request, pk):
    """ ----------------------------------------------------------------------------------
    Presenta los Comentarios realizados por los Supervisores durante la Autorizacion
    y permite la modificacion de las asignaciones de Servicios criticos para su correccion.

    Esta version utiliza el script Java de asignacion basado en el traspaso 
    entre un box de Disponibles a otro de Asignados (y viceversa).

    pk: Pk del Proceso.
    ---------------------------------------------------------------------------------------
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))

    proceso = get_object_or_404(Proceso, pk=pk)
    subproceso = proceso.subproceso



    # Rescata los Comentarios 
    comentarios_proceso=Log_Revision.objects.filter(proceso=proceso)
    comentarios_b=[]
    for com in comentarios_proceso:
        if com.seccion == "B":
            comentarios_b.append(com)

    if request.method == "POST":
        recursos_ids = request.POST.get("recursos", "").split(",")  # Obtener los recursos seleccionados
        recursos_ids = [int(r) for r in recursos_ids if r.isdigit()]  # Filtrar solo los números válidos

        if recursos_ids:
            subproceso.recursos.set(Recursos.objects.filter(id__in=recursos_ids))  # Asignar recursos
        #else:
            #subproceso.recursos.clear()  # Si no hay recursos, limpiar asignaciones



        subproceso.save()  # Guardar los cambios

        #return HttpResponseRedirect(reverse('Lista-Servicios', args=[pk]))
        #return HttpResponseRedirect(reverse('Lista-Recursos'))
        return HttpResponseRedirect(reverse('Rev-Asigna-Escenarios', args=[pk]))


    # Cargar recursos disponibles y asignados
    recursos_disponibles = Recursos.objects.exclude(id__in=subproceso.recursos.values_list('id', flat=True))
    recursos_asignados = subproceso.recursos.all()

    return render(request, 'bcp/map_act/rev_asigna_activos_v2.html', {
        'form': ServicioForm(),
        'proceso': proceso,
        'subproceso': subproceso,
        'comentarios': comentarios_b,
        'recursos_disponibles': recursos_disponibles,
        'recursos_asignados': recursos_asignados
    })


#*************************************************************************************
# 3.8 Revision de Asignacion de Escenarios a Proceso con autorizazion RACI rechazada *
#*************************************************************************************
from .forms import Revisa_Asig_Esc_Form
@login_required
def Revisa_Asig_Esc(request, pk): 

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))
    
    model = Proceso
    proc_rev=get_object_or_404(Proceso, pk = pk)


    # Rescata los Comentarios 
    comentarios_proceso=Log_Revision.objects.filter(proceso=proc_rev)
    comentarios_m=[]
    for com in comentarios_proceso:
        if com.seccion == "E":
            comentarios_m.append(com)


    form = Revisa_Asig_Esc_Form()


    if request.method=='POST':

        form = Revisa_Asig_Esc_Form(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            p1= form.cleaned_data['escenarios']
            proc_rev.subproceso.escenarios.set(p1)
            

            notifica=form.cleaned_data['notifica']

            #Cambia status del Proceso a x Aprobar
            if proc_rev.subproceso.gestor_C == proc_rev.subproceso.gestor_A:
                
                if proc_rev.subproceso.gestor_C == proc_rev.subproceso.gestor_R:
                    #Aprobada por Responsable area 
                    proc_rev.subproceso.status='R'
                    

                    #Notificar a Gestor I por email
                    if notifica:
                        email = proc_rev.subproceso.gestor_I.user_gestor.email
                        cc_email= proc_rev.subproceso.gestor_C.user_gestor.email
                        nombre=proc_rev.subproceso.gestor_C.user_gestor.last_name
                        proceso=proc_rev.path
                        accion='tomar conocimiento de la puesta en vigencia del '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
                else:
                    #Por Vigentear
                    proc_rev.subproceso.status='r'

                    #Notificar a Gestor R por email           
                    if notifica:
                        email = proc_rev.subproceso.gestor_R.user_gestor.email
                        cc_email= proc_rev.subproceso.gestor_C.user_gestor.email
                        nombre=proc_rev.subproceso.gestor_C.user_gestor.last_name
                        proceso=proc_rev.path
                        accion='dar visto bueno o requerir cambios para el '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                        
            else:
                #Por Aprobar
                proc_rev.subproceso.status='A'

                #Notifica por correo a Gestor A            
                if notifica:
                    email = proc_rev.subproceso.gestor_A.email
                    cc_email= proc_rev.subproceso.gestor_C.email
                    nombre=proc_rev.subproceso.gestor_C.last_name
                    proceso=proc_rev.path
                    accion='revisar definicion y aprobar o requerir cambios al '
                
                    Manda_Correo(email, cc_email, nombre, proceso, accion)
                
                   
            proc_rev.subproceso.save()
            proc_rev.save()
     
          
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Escenarios') )

        else:

            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

            
        
    else:

        p2=proc_rev.subproceso.escenarios.all()
        form = Revisa_Asig_Esc_Form(initial= {'escenarios':set(p2),
                                              'notifica':False} )

                                               
        return render(request, 'bcp/map_esc/asigna_esc_revisa.html', {'form': form,
                                                                      'proceso':proc_rev,
                                                                      'comentarios':comentarios_m})

@login_required   
def rev_asigna_escenarios(request, pk):
    """ ----------------------------------------------------------------
    Presenta los Comentarios realizados por los Supervisores durante la 
    Autorizacion y permite la reasignacion de Escenarios.

    Esta version utiliza el script Java de asignacion basado en el traspaso 
    entre un box de Disponibles a otro de Asignados (y viceversa).

    pk: Pk del Proceso.
    --------------------------------------------------------------------
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))

    proceso = get_object_or_404(Proceso, pk=pk)
    subproceso = proceso.subproceso

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)


    # Rescata los Comentarios 
    comentarios_proceso=Log_Revision.objects.filter(proceso=proceso)
    comentarios_b=[]
    for com in comentarios_proceso:
        if com.seccion == "E":
            comentarios_b.append(com)
            

    if request.method == "POST":
        escenarios_ids = request.POST.get("escenarios", "").split(",")
        escenarios_ids = [int(e) for e in escenarios_ids if e.isdigit()]

        if escenarios_ids:
            subproceso.escenarios.set(Escenarios.objects.filter(id__in=escenarios_ids))
        #else:
            #subproceso.escenarios.clear()



        #Cambia el estado para inicio de las autorizaciones
        #subproceso.status='A' # Aprobacion Gestor Autorizador
        #subproceso.fase_status='E'
        subproceso.save()

        #return HttpResponseRedirect(reverse('Asigna-Escenarios', args=[pk]))
        return HttpResponseRedirect(reverse('Lista-Recursos') )


    escenarios_disponibles = Escenarios.objects.exclude(id__in=subproceso.escenarios.values_list('id', flat=True))
    escenarios_asignados = subproceso.escenarios.all()

    return render(request, 'bcp/map_esc/asigna_esc_revisa.html', {
        'form': EscenarioForm(),
        'proceso': proceso,
        'subproceso': subproceso,
        'comentarios':comentarios_b,
        'escenarios_disponibles': escenarios_disponibles,
        'escenarios_asignados': escenarios_asignados,
    })
  

#****************************************************************************
# 3.9 Revision de Asignacion BIA  a Proceso con autorizazion RACI rechazada *
#****************************************************************************
from .forms import Revisa_Asig_BIA_Form
@login_required
def Revisa_Asig_BIA(request, pk):

    print('-- Revisa Asignacion BIA (Revisa_Asig_BIA)')
    print('------------------------------------------')

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))


    proceso = get_object_or_404(Proceso, pk = pk)
    total_pro_ant=proceso.subproceso.ranking

    impactos_pc = proceso.subproceso.impact_subp
    nro_impactos_pc=impactos_pc.count()

    indicador_pc=proceso.subproceso.indicador_subp
    nro_indicador_pc=indicador_pc.count()

    #print('impactos_pc=', impactos_pc)
    #print(not impactos_pc)


    if  nro_impactos_pc == 0:
        #print('entra')
        impactos = Tipo_Impacto.objects.all()
        #print('Tipo de Impacto Maestro =', impactos)

        for imp in impactos:
            asigna_imp=Impactos_Asig()
            asigna_imp.pk_proc=pk
            asigna_imp.impacto = get_object_or_404(Tipo_Impacto, pk=imp.pk)
            asigna_imp.save()
            impactos_pc.add(asigna_imp)
            proceso.save()
    #else:
         #print('NO entra')


    # Calculo de Puntaje de Impacto.
    total_imp=00.00
    puntaje=00.00
    for imp2 in impactos_pc.all():
        pond=imp2.impacto.ponderacion
        #print('imp2.nivel=', imp2.nivel)
        if imp2.nivel:
            puntaje=imp2.nivel.valor*pond/100   # calcula la ponderacion del valor del nivel
            total_imp=total_imp+float(puntaje)
        #print('riesgo=', imp2.impacto.nombre, 'pond=', pond/100, 'puntaje pond=', puntaje)
              
    #print('total=', total_imp)


    if nro_indicador_pc == 0:

        indicadores = Tipo_Indicador.objects.all()
        for ind in indicadores:
            asigna_ind=Indicadores_Asig()
            asigna_ind.pk_proc=pk
            asigna_ind.indicador = get_object_or_404(Tipo_Indicador, pk=ind.pk)
            asigna_ind.save()
            indicador_pc.add(asigna_ind)
            proceso.save()

    # Calculo de Puntaje de Indicadores.
    total_ind=00.00
    puntaje=00.00
    for ind2 in indicador_pc.all():
        if ind2.nivel:
            puntaje=float(ind2.nivel.valor)
            total_ind=total_ind+puntaje
        #print('indicador =', ind2.indicador.nombre,  'puntaje =', puntaje)
              
    #print('total=', total_ind)

    total_pro=total_imp+total_ind
    if total_pro != total_pro_ant:
        proceso.subproceso.ranking = total_pro
        proceso.subproceso.save()


    # Rescata los Comentarios 
    comentarios_proceso=Log_Revision.objects.filter(proceso=proceso)
    comentarios_m=[]
    for com in comentarios_proceso:
        if com.seccion == "V":
            comentarios_m.append(com)

    impactos=proceso.subproceso.impact_subp
    indicadores=proceso.subproceso.indicador_subp

    #pon_impacto = get_object_or_404(Parametros_G, pk = 3)
    #pon_indicad = get_object_or_404(Parametros_G, pk = 4)    
    

    if request.method=='POST':

        form = Revisa_Asig_BIA_Form(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro

            notifica=form.cleaned_data['notifica']
           

            #Cambia status del Proceso a x Aprobar

            # Si el Gestor Autorizador es igual al Gestor Consultor
            if proceso.subproceso.gestor_C == proceso.subproceso.gestor_A:
                print('Si Gestor Consultor = Gestor Autorizador')
                
                if proceso.subproceso.gestor_C == proceso.subproceso.gestor_R:
                    #Aprobada por Responsable area 
                    proceso.subproceso.status='R'
                    

                    #Notificar a Gestor I por email
                    if notifica:
                        email = proceso.subproceso.gestor_I.user_gestor.email
                        cc_email= proceso.subproceso.gestor_C.user_gestor.email
                        nombre=proceso.subproceso.gestor_C.user_gestor.last_name
                        proceso=proceso.path
                        accion='tomar conocimiento de la puesta en vigencia del '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
                else:
                    #Por Vigentear
                    proceso.subproceso.status='r'

                    #Notificar a Gestor R por email           
                    if notifica:
                        email = proceso.subproceso.gestor_R.user_gestor.email
                        cc_email= proceso.subproceso.gestor_C.user_gestor.email
                        nombre=proceso.subproceso.gestor_C.user_gestor.last_name
                        proceso=proceso.path
                        accion='dar visto bueno o requerir cambios para el '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                        
            else:
            # Si el Gestor Consultor y Gestor Autorizador son distintos
                print('Si Gestor Consultor = Gestor Autorizador')

                #Por Aprobar
                proceso.subproceso.status='A'



                #Notifica por correo a Gestor A            
                if notifica:
                    email = proceso.subproceso.gestor_A.email
                    cc_email= proceso.subproceso.gestor_C.email
                    nombre=proceso.subproceso.gestor_C.last_name
                    proceso=proceso.path
                    accion='revisar definicion y aprobar o requerir cambios al '
                
                    Manda_Correo(email, cc_email, nombre, proceso, accion)
                
                   
            proceso.subproceso.save()
            proceso.save()
         
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Evaluaciones') )

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:

        form = Revisa_Asig_BIA_Form(initial= {'proceso':proceso,
                                              'impactos':impactos,
                                              'indicadores':indicadores,
                                              #'observaciones':obs_asig_bia,
                                              'notifica':False} )

                                               
        return render(request, 'bcp/map_eval/asigna_eval_rev.html', {'form': form,
                                                                     'proceso':proceso,
                                                                     'impactos':impactos_pc,
                                                                     'indicadores':indicador_pc,
                                                                     'total_imp':total_imp,
                                                                     'total_ind':total_ind,
                                                                     'total_pro':total_pro,
                                                                     'comentarios':comentarios_m
                                                                     })


#**************************************
#  Registra un Comentario de Revision *
#**************************************

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Log_Revision
import json

@csrf_exempt
@login_required
def Crea_Rev_OC(request):
    """ Crea un Comentario de Revision durante la Revision
    de cada Proceso o PC segun su etapa. """

    print('>>>>> Crea Observacion  ------')
    print('----- metodo=', request.method)

    #Asigna al usuario de sesion como Autorizador
    print('----- asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    usuario_sesion=Gestor.objects.get(user_pk=pk_usr_sesion)
    print('----- usuario de sesion',usuario_sesion)

    fecha_hoy=datetime.date.today()

    if request.method == "POST":
        # rescata datos del json
        data = json.loads(request.body)
        print('----- data=', data)
        obj_id = data.get("obj_id") # id del SubProceso asociado
        campo = data.get("field")
        seccion = data.get("seccion")
        comentario = data.get("comment")

        if seccion == "P":
        #El Comentario proviene de la Fase de definicion de PC
            try:
                    procedimiento = Procedimientos.objects.get(id=obj_id)
                    print('** procedimiento =', procedimiento)
                    log_revision = Log_Revision(fecha=fecha_hoy,
                                                procedimiento=procedimiento,
                                                gestor_aut=usuario_sesion,
                                                seccion=seccion, 
                                                campo=campo,
                                                comentario=comentario)
                    log_revision.save()
                    return JsonResponse({"success": True})
            except Proceso.DoesNotExist:
                return JsonResponse({"success": False, "error": "Proceso no encontrado"})
            

        elif seccion[0] == "D":

        # El Comentario proviene de la Fase de definicion del DRP
            try:
                    drp = Drp.objects.get(id=obj_id)
                    print('** DRP =', drp)
                    log_revision = Log_Revision(fecha=fecha_hoy,
                                                drp=drp,
                                                gestor_aut=usuario_sesion,
                                                seccion=seccion, 
                                                campo=campo,
                                                comentario=comentario)
                    log_revision.save()
                    return JsonResponse({"success": True})
            except Proceso.DoesNotExist:
                return JsonResponse({"success": False, "error": "Proceso no encontrado"})

        elif seccion == "C":
                
                print('----- Entra a Seccion C Bitacora de Ejecucion')

                try:
                        procedimiento = Procedimientos_V.objects.get(id=obj_id)
                        print('----- procedimiento =', procedimiento)
                        log_revision = Log_Revision(fecha=fecha_hoy,
                                                    procedimiento_v=procedimiento,
                                                    gestor_aut=usuario_sesion,
                                                    seccion=seccion, 
                                                    campo=campo,
                                                    comentario=comentario)
                        log_revision.save()
                        return JsonResponse({"success": True})
                except Proceso.DoesNotExist:
                    return JsonResponse({"success": False, "error": "Proceso no encontrado"})

#------------------------------------------------


        else:
        # El Comentario proviene de la Fase de Mapeo de Procesos
            try:
                    proceso = Proceso.objects.get(id=obj_id)
                    print('** proceso =', proceso)
                    log_revision = Log_Revision(fecha=fecha_hoy,
                                                proceso=proceso,
                                                gestor_aut=usuario_sesion,
                                                seccion=seccion, 
                                                campo=campo,
                                                comentario=comentario)
                    log_revision.save()
                    return JsonResponse({"success": True})
            except Proceso.DoesNotExist:
                return JsonResponse({"success": False, "error": "Proceso no encontrado"})

  
    return JsonResponse({"success": False, "error": "Invalid request"})


#********************************
#  Borra Comentario de Revision *
#********************************
@login_required
def Borra_Rev_OC(request, pk):
    """
    Borra un Comentario de Revision """
    print('*** Entra a Borra Comentario ****')

    url_ant = request.META['HTTP_REFERER']

    com_rev=get_object_or_404(Log_Revision, pk=pk)
    com_rev.delete()

    return HttpResponseRedirect(url_ant)

#********************************
#  Marca Comentario de Revision *
#********************************
@login_required
def OK_Rev_OC(request, pk):
    """
    Marca el Comentario de Revision como resuelto.
    pk: Pk del Comentario en Log """
    print('*** Entra a OK Comentario ****')


    url_ant = request.META['HTTP_REFERER']

    com_rev=get_object_or_404(Log_Revision, pk=pk)
    if not com_rev.resuelto:
        com_rev.resuelto=True
    else:
        com_rev.resuelto=False


    com_rev.save()

    return HttpResponseRedirect(url_ant)


#*********************************************************************************************************************************************
#*********************************************** 4. Asignacion de Relaciones a Procesos ******************************************************
#*********************************************************************************************************************************************

#***********************************
#4.1 Asigna Escenarios a un Proceso*
#***********************************
from .forms import Asig_Esc_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def Asigna_Escenarios(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))
    

    model = Proceso
    proceso = get_object_or_404(Proceso, pk = pk)
    escenarios = proceso.subproceso.escenarios
    
    form = Asig_Esc_Form()

    if request.method=='POST':
        print('entra a POST ESCENARIOS')
        form = Asig_Esc_Form(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            p1= form.cleaned_data['escenarios']
            proceso.subproceso.escenarios.set(p1)

            #Cambia el estado para inicio de las autorizaciones
            proceso.subproceso.status='C'
            proceso.subproceso.fase_status='E'
                                           
            proceso.subproceso.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Escenarios') )

        else:

            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 

            
        
    else:
        print('Entra a GET Escenarios')
        p2 = proceso.subproceso.escenarios.all()
        form = Asig_Esc_Form(initial= {'escenarios':set(p2)})
                                        
        return render(request, 'bcp/map_esc/asigna_escenarios.html', {'form': form, 'proceso':proceso, 'escenarios':escenarios})




#********************************
#4.2 Asigna Activos a un Proceso*
#********************************
from .forms import Act_x_Proc_Form

# CODIGO OBSOLETO - BORRAR

#@permission_required('Catalogo.can_mark_returned')
@login_required
def Asigna_Activos(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))
    

    model = Proceso
    proceso = get_object_or_404(Proceso, pk = pk)
    #p2 = proceso.subproceso.recursos.all()
    
    form = Act_x_Proc_Form()

    if request.method=='POST':
        print('entra a POST ACTIVOS')
        form = Act_x_Proc_Form(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            #p1 = form.data.get('activos')
            p1 = form.cleaned_data['activos']
            proceso.subproceso.recursos.set(p1)

            #Cambia el estado para inicio de las autorizaciones
            proceso.subproceso.status='C'
            proceso.subproceso.fase_status='B'
                                           
            proceso.subproceso.save()


            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Recursos') )
            
        else:

                    
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        #p2 = proceso.subproceso.recursos.all()
        #form = Act_x_Proc_Form(initial= {'activos':set(p2)})
        form = Act_x_Proc_Form()
                                        
        return render(request, 'bcp/map_act/asigna_activos.html', {'form': form, 'proceso':proceso})



from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Proceso, SubProceso, Recursos
from .forms import ServicioForm

@login_required
def asigna_servicio(request, pk):
    """
    Asigna Servicios Criticos al Proceso
    Utiliza Box de Seleccion con JavaScript
    """

    proceso = get_object_or_404(Proceso, pk=pk)
    subproceso = proceso.subproceso

    if request.method == "POST":
        recursos_ids_str = request.POST.get("recursos", "")
        recursos_ids = [int(r) for r in recursos_ids_str.split(",") if r.isdigit()]

        if recursos_ids:
            subproceso.recursos.set(Recursos.objects.filter(id__in=recursos_ids))
        #else:
            #subproceso.recursos.clear()

        # Cambia Status
        #subproceso.status = 'C'
        #subproceso.fase_status = 'B'
        #subproceso.save()

        #return redirect(reverse('Lista-Recursos'))
        return HttpResponseRedirect(reverse('Asigna-Escenarios', args=[pk])) 


    recursos_asignados = subproceso.recursos.all()
    recursos_disponibles = Recursos.objects.exclude(id__in=recursos_asignados.values_list('id', flat=True))

    origen=1

    return render(request, 'bcp/map_act/asigna_activos_v2.html', {
        'proceso': proceso,
        'subproceso': subproceso,
        'recursos_disponibles': recursos_disponibles,
        'recursos_asignados': recursos_asignados,
        'origen':origen,
    })

from .forms import EscenarioForm

@login_required
def asigna_escenarios(request, pk):
    """
    Asigna los Escenarios de Riesgo asociados al Proceso 
    Utiliza Box Script. 
    """
    proceso = get_object_or_404(Proceso, pk=pk)
    subproceso = proceso.subproceso

    if request.method == "POST":

        # Rescata los Datos seleccionados desde el Script
        escenarios_ids = request.POST.get("escenarios", "").split(",")
        escenarios_ids = [int(e) for e in escenarios_ids if e.isdigit()]

        if escenarios_ids:
            subproceso.escenarios.set(Escenarios.objects.filter(id__in=escenarios_ids))
        #else:
            #subproceso.escenarios.clear()


        #Cambia el estado para inicio de las autorizaciones
        subproceso.status='C'
        subproceso.fase_status='B'
        subproceso.save()

        #return HttpResponseRedirect(reverse('Asigna-Escenarios', args=[pk]))
        return HttpResponseRedirect(reverse('Lista-Recursos') )


    escenarios_disponibles = Escenarios.objects.exclude(id__in=subproceso.escenarios.values_list('id', flat=True))
    escenarios_asignados = subproceso.escenarios.all()

    return render(request, 'bcp/map_esc/asigna_escenarios_v2.html', {
        'form': EscenarioForm(),
        'proceso': proceso,
        'subproceso': subproceso,
        'escenarios_disponibles': escenarios_disponibles,
        'escenarios_asignados': escenarios_asignados,
    })


#***********************************************
#4.3 Asigna Impactos e Indicadores a un Proceso*
#***********************************************

#@permission_required('Catalogo.can_mark_returned')
@login_required
def Asigna_Imp_Ind(request, pk):
    """
    Lista los (Riesgos) Impactos e Indicadores asignados al subproceso pk
    Si no tiene riesgos o indicadores crea la instancia en tablas de 
    asignacion """

    print('---- Entra a Lista de Impactos e Indicadores x Proceso ---- ')

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))
    

    proceso = get_object_or_404(Proceso, pk = pk)
    total_pro_ant=proceso.subproceso.ranking

    impactos_pc = proceso.subproceso.impact_subp
    nro_impactos_pc=impactos_pc.count()

    indicador_pc=proceso.subproceso.indicador_subp
    nro_indicador_pc=indicador_pc.count()

    print('impactos_pc=', impactos_pc)
    print(not impactos_pc)


    if  nro_impactos_pc == 0:
        print('entra')
        impactos = Tipo_Impacto.objects.all()
        print('Tipo de Impacto Maestro =', impactos)

        for imp in impactos:
            asigna_imp=Impactos_Asig()
            asigna_imp.pk_proc=pk
            asigna_imp.impacto = get_object_or_404(Tipo_Impacto, pk=imp.pk)
            asigna_imp.save()
            impactos_pc.add(asigna_imp)
            proceso.save()
    else:
         print('NO entra')

    # Calculo de Puntaje de Impacto.
    total_imp=00.00
    puntaje=00.00
    for imp2 in impactos_pc.all():
        pond=imp2.impacto.ponderacion
        print('imp2.nivel=', imp2.nivel)
        if imp2.nivel:
            puntaje=imp2.nivel.valor*pond/100   # calcula la ponderacion del valor del nivel
            total_imp=total_imp+float(puntaje)
        print('riesgo=', imp2.impacto.nombre, 'pond=', pond/100, 'puntaje pond=', puntaje)
              
    print('total=', total_imp)


    if nro_indicador_pc == 0:

        indicadores = Tipo_Indicador.objects.all()
        for ind in indicadores:
            asigna_ind=Indicadores_Asig()
            asigna_ind.pk_proc=pk
            asigna_ind.indicador = get_object_or_404(Tipo_Indicador, pk=ind.pk)
            asigna_ind.save()
            indicador_pc.add(asigna_ind)
            proceso.save()

    # Calculo de Puntaje de Indicadores.
    total_ind=00.00
    puntaje=00.00
    for ind2 in indicador_pc.all():
        if ind2.nivel:
            puntaje=float(ind2.nivel.valor)
            total_ind=total_ind+puntaje
        print('indicador =', ind2.indicador.nombre,  'puntaje =', puntaje)
              
    print('total=', total_ind)

    total_pro=total_imp+total_ind
    if total_pro != total_pro_ant:
        proceso.subproceso.ranking = total_pro
        proceso.subproceso.save()

                                        
    return render(request, 'bcp/map_eval/asigna_eval.html', {'proceso':proceso,
                                                             'impactos':impactos_pc,
                                                             'indicadores':indicador_pc,
                                                             'total_imp':total_imp,
                                                             'total_ind':total_ind,
                                                             'total_pro':total_pro})

from .forms import Asig_Imp_Form 
@login_required
def Asig_Imp(request, pk, status):
    """
    Asigna un nivel al nub (proceso/Impacto) pk
    """
    print('-------- Entra a Asigna nivel de impacto ---------')

    nub_impacto=get_object_or_404(Impactos_Asig, pk=pk)
    riesgo=nub_impacto.impacto
    proceso=get_object_or_404(Proceso, pk=nub_impacto.pk_proc)
    opciones=Nivel_Impacto.objects.filter(tipo=riesgo)
    print('riesgo =', riesgo.nombre)
    print('opciones=', opciones)


    if request.method=='POST':

        form = Asig_Imp_Form(request.POST  or None, param=riesgo)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            nub_impacto.nivel=form.cleaned_data['nivel']
            nub_impacto.save()

            # redirect to a new URL:
            if status=="V":
                return HttpResponseRedirect(reverse('Asigna-Evaluacion', args=[str(proceso.id)] ) )
            else:
                return HttpResponseRedirect(reverse('Rev-Asig-BIA', args=[str(proceso.id)] ) )

        else:

                    
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        #p2 = proceso.subproceso.recursos.all()
        #form = Act_x_Proc_Form(initial= {'activos':set(p2)})
        form = Asig_Imp_Form(request.POST  or None, param=riesgo,
                             initial= {'nivel':nub_impacto.nivel} )
                                        
        return render(request, 'bcp/map_eval/asigna_nivel_imp.html', {'nub_impacto':nub_impacto,
                                                                      'proceso':proceso,
                                                                      'opciones':opciones,
                                                                      'riesgo':riesgo,
                                                                      'form':form})

from .forms import Asig_Ind_Form
@login_required
def Asig_Ind(request, pk, status):
    """
    Asigna un nivel al nub (proceso/Impacto) pk
    """
    print('-------- Entra a Asigna nivel de Indicador de Recuperacion ---------')

    nub_indicador=get_object_or_404(Indicadores_Asig, pk=pk)
    indicador= nub_indicador.indicador
    proceso=get_object_or_404(Proceso, pk=nub_indicador.pk_proc)
    opciones=Indicadores_BIA.objects.filter(tipo=indicador)
    print('indicador =', indicador.nombre)
    print('opciones=', opciones)


    if request.method=='POST':

        form = Asig_Ind_Form(request.POST  or None, param=indicador)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            nub_indicador.nivel=form.cleaned_data['nivel']
            nub_indicador.save()

            # redirect to a new URL:
            if status=="V":
                return HttpResponseRedirect(reverse('Asigna-Evaluacion', args=[str(proceso.id)] ) )
            else:
                return HttpResponseRedirect(reverse('Rev-Asig-BIA', args=[str(proceso.id)] ) )
            
        else:

                    
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        #p2 = proceso.subproceso.recursos.all()
        #form = Act_x_Proc_Form(initial= {'activos':set(p2)})
        form = Asig_Ind_Form(request.POST  or None, param=indicador,
                             initial= {'nivel':nub_indicador.nivel} )
                                        
        return render(request, 'bcp/map_eval/asigna_nivel_ind.html', {'nub_indicador':nub_indicador,
                                                                      'proceso':proceso,
                                                                      'opciones':opciones,
                                                                      'indicador':indicador,
                                                                      'form':form})

@login_required
def Envia_Ev_RACI(request, pk, etapa):
    """
    Envia al Proceso a la definicion del esquema RACI.
    Cambia el Estado del Proceso a C (x Aprobar) para la asignacion RACI 
    pk: pk del Proceso
    etapa: Etapa del Proceso.
    """
    proceso=get_object_or_404(Proceso, pk=pk)
    
    proceso.subproceso.status="C"

    if etapa=="V":
        if proceso.subproceso.ranking == 0:
            return HttpResponseRedirect(reverse('error-sesion-mgm', args=[3001] ))
        else:
            proceso.subproceso.fase_status="V"
            proceso.subproceso.save()
            return HttpResponseRedirect(reverse('Lista-Evaluaciones'))

            
    
    elif etapa == "B":
        proceso.subproceso.fase_status="B"
        proceso.subproceso.save()
        return HttpResponseRedirect(reverse('Lista-Recursos'))
    
    elif etapa == "E":
        proceso.subproceso.fase_status="E"
        proceso.subproceso.save()
        return HttpResponseRedirect(reverse('Lista-Escenarios'))


@login_required
def Envia_Auth(request, pk, etapa):
    """
    Envia a proceso de Autorizacion luego de correccion de los Comentarios.
    Cambia el Estado del Proceso a A (x Aprobar)  para la asignacion RACI
    pk: pk del Proceso
    etapa: Etapa del Proceso.
     """
    
    print('------ Entra a Envia Autorizacion (cambia status= "A") ---- ')
    proceso=get_object_or_404(Proceso, pk=pk)

    proceso.subproceso.status="A"

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)


    if etapa=="V":
        # Crea Log de aprobacion de Autorizador
        log=Log_Revision()
        log.fecha = datetime.date.today()
        log.proceso= proceso
        log.gestor_aut=usr_aut
        log.seccion="V"
        log.campo="Corregido por:"+aut
        log.comentario="BIA corregida por Gestor Consultor. Se envia a Gestor Autorizador."
        log.resuelto=True
        log.save()

        proceso.subproceso.fase_status="V"
        proceso.subproceso.save()
        return HttpResponseRedirect(reverse('Lista-Evaluaciones'))
    
    elif etapa == "B":

        # Crea Log de aprobacion de Autorizador
        log=Log_Revision()
        log.fecha = datetime.date.today()
        log.proceso= proceso
        log.gestor_aut=usr_aut
        log.seccion="B"
        log.campo="Corregido por:"+aut
        log.comentario="Asignacion de Servicios Criticos corregida por Gestor Consultor. Se envia a Gestor Autorizador."
        log.resuelto=True
        log.save()

        proceso.subproceso.fase_status="B"
        proceso.subproceso.save()
        return HttpResponseRedirect(reverse('Lista-Recursos'))
    
    elif etapa == "E":

        # Crea Log de aprobacion de Autorizador
        log=Log_Revision()
        log.fecha = datetime.date.today()
        log.proceso= proceso
        log.gestor_aut=usr_aut
        log.seccion="E"
        log.campo="Corregido por:"+aut
        log.comentario="Asignacion de Escenarios de Riesgo corregida por Gestor Consultor. Se envia a Gestor Autorizador."
        log.resuelto=True
        log.save()

        proceso.subproceso.fase_status="E"
        proceso.subproceso.save()
        return HttpResponseRedirect(reverse('Lista-Escenarios'))


#***********************************************  Fin de Asignacion de Relaciones a Procesos  *********************************************



#*********************************************************************************************************************************************
#***********************************************  5. Procedimientos de Contingencia (PC)  ****************************************************
#*********************************************************************************************************************************************


#************************************
#5.0 Lista de Procedimientos (PC)   *
#************************************
class ProcedimientosListView(generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model =  Proceso
    template_name='bcp/proced_cont/proced_list.html'

@login_required
def Lista_Procedimientos(request, vigente):
    """
    Lista Procedimientos 
    """
    if vigente == 0:
        procedimientos_vigentes = True
    else:
        procedimientos_vigentes = False

    print('>>>> Entra a Lista de Procedimientos ----------')
    #Determina tramos de criticidad del Proceso
        #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, nombre = 'BIA_BAJO')
    bia_medio = get_object_or_404(Parametros_G, nombre = 'BIA_MEDIO')
    bia_max   = get_object_or_404(Parametros_G, nombre = 'BIA_MAX')

    tramo_1 = float(bia_bajo.valor_2)/100
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100
    valor_max=float(bia_max.valor_2)
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2)
    print('valor_max:', valor_max) 



    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    lista_procesos = Proceso.objects.all() # Solo los Procesos Vigentes (Aprobados)

    # Selecciona procesos vigentes
    lista_procesos_v=[]
    for prc in lista_procesos:
        if prc.subproceso_v !=None or not prc.es_subproceso:
            lista_procesos_v.append(prc)

    print('Procesos seleccionados', lista_procesos_v)

    return render(request, 'bcp/proced_cont/proced_list.html',
                  context={'lista_procesos':lista_procesos_v, 'tramo_1':tramo_1,
                           'tramo_2':tramo_2, 'valor_max':valor_max,
                           'procedimientos_vigentes':procedimientos_vigentes})
    
#*****************************************************
# 5.1  Creacion de Procedimiento de Recuperacion (PC) *
#*****************************************************

#***********************************************************
# 5.1.1  Creacion Inicial de Procedimiento de Recuperacion *
#***********************************************************
from .forms import CreaProc_A_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_prcd_a(request, pk):
    """
    Realiza la creacion inicial al hacer click en +
    """

    #model = Proceso

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[200] ))

    proceso = get_object_or_404(Proceso, pk = pk)
    proced = Procedimientos()

    # Determinacion de Codigo a asignar.
    cod = proceso.proceso
    codigo = cod.strip()+"-" 
    hijos_i = proceso.subproceso_v.nro_prdto+1
    if hijos_i<10:
        codigo=codigo+"0"+str(hijos_i)
    else:
        codigo=codigo+str(hijos_i)


    #Asigna el formulario creado en Forrms
    form=CreaProc_A_Form()


    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_A_Form(request.POST)
        
        # Check if the form is valid:
        
        if form.is_valid():
            
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso

            proceso.subproceso_v.nro_prdto = hijos_i
            
            proced.codigo = codigo
            proced.pk_padre=pk
            
            proced.nombre = form.cleaned_data['nombre']
            #proced.tipo = form.cleaned_data['tipo'] Dato en revision


            #Asigna al usuario de sesion como gestor consultor
            usuario_sesion = request.user.pk
            print('usr_ses=',usuario_sesion)
            usuario_ges=get_object_or_404(Gestor, user_pk=usuario_sesion)
            print('usuario_gestor', usuario_ges)
            proced.gestor_consultor = usuario_ges
            

            #Asigna estatus C : En definicion 
            proced.status = 'C'
            
            #Graba Procedimiento
            proced.save()
            proceso.subproceso_v.procedimientos_contingencia.add(proced)
            proceso.subproceso_v.save()
            proceso.save()            

            print('Grabo Procedimiento')

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Proced', args=[1]))
        
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})             
            
        
        

    # If this is a GET (or any other method) create the default form.
    else:

        form = CreaProc_A_Form(initial= {
                                'nombre':proced.nombre,
                                'tipo':proced.tipo,
                                
                                }
                        )

    
        return render(request, 'bcp/proced_cont/prcd_crea_A.html', {'form': form, 'proceso':proceso})

#*************************************************************
# 5.1.2  Creacion parte (B) de Procedimiento de Recuperacion *
#*************************************************************
from .forms import CreaProc_B_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_prcd_b(request, pk):

    print('>>>> Crea Procedimiento B')
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso= get_object_or_404(Proceso, pk = proced.pk_padre)
    escenarios=proceso.subproceso.escenarios
    
    ruta=resta_string(proceso.path, proceso.nombre)
    print('---- ruta: ', ruta)

    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos


        
    print('---- nombre proceso=', proceso.nombre)
    print('---- nombre procedimiento=', proced.nombre)

    print('Crea parte B')
    
  
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        #form = CreaProc_B_Form(request.POST)
        form = CreaProc_B_Form(request.POST  or None, param=escenarios.all()) # Envia Escenarios del Proceso

        
        # Check if the form is valid:
        
        if form.is_valid():
            
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso

            proced.nombre = form.cleaned_data['nombre']
            #proced.tipo = form.cleaned_data['tipo'] 
            
            proced.escenarios = form.cleaned_data['escenarios']

            proced.estrategia = form.cleaned_data['estrategia']
            


            responsable = form.cleaned_data['resp_proceso']
            print('responsable :',  responsable.user_gestor.email)
            proced.resp_proceso = responsable

            respaldo_resp = form.cleaned_data['bck_resp']
            proced.bck_resp = respaldo_resp

            ejecutor = form.cleaned_data['gestor_ejecutor']
            proced.gestor_ejecutor = ejecutor

            respaldo_ejec = form.cleaned_data['bck_ejecutor']
            proced.bck_ejecutor = respaldo_ejec

            enlace = form.cleaned_data['enlace_c_crisis']
            proced.enlace_c_crisis = enlace

            respaldo_enl = form.cleaned_data['bck_enlace'] 
            proced.bck_enlace = respaldo_enl

            nro_cont=contactos.count()
            print('contactos=', nro_cont)
            if  nro_cont == 0:
                print ('sin contactos =', proced.contactos_pc)
                #Hace prellenado de la lista de Contactos

                #responsable y respaldo
                cont_pc=Contactos_PC()
                cont_pc.pk_padre = proced.pk
                cont_pc.nombre=responsable.user_gestor.first_name+' '+responsable.apellido
                cont_pc.correo=responsable.user_gestor.email
                cont_pc.tel_lab=responsable.fono_t
                cont_pc.cel_lab=responsable.cod_area.codigo+responsable.fono_c
                cont_pc.save()
                proced.contactos_pc.add(cont_pc)

                if respaldo_resp:
                    cont_pc=Contactos_PC()
                    cont_pc.pk_padre = proced.pk
                    cont_pc.nombre=respaldo_resp.user_gestor.first_name+' '+respaldo_resp.apellido
                    cont_pc.correo=respaldo_resp.user_gestor.email
                    cont_pc.tel_lab=respaldo_resp.fono_t
                    cont_pc.cel_lab=respaldo_resp.cod_area.codigo+respaldo_resp.fono_c
                    cont_pc.save()
                    proced.contactos_pc.add(cont_pc)

                #ejecutor y respaldo
                cont_pc=Contactos_PC()
                cont_pc.pk_padre = proced.pk
                cont_pc.nombre=ejecutor.user_gestor.first_name+' '+ejecutor.apellido
                cont_pc.correo=ejecutor.user_gestor.email
                cont_pc.tel_lab=ejecutor.fono_t
                cont_pc.cel_lab=ejecutor.cod_area.codigo+ejecutor.fono_c
                cont_pc.save()
                proced.contactos_pc.add(cont_pc)  

                if respaldo_ejec:
                    cont_pc=Contactos_PC()
                    cont_pc.pk_padre = proced.pk
                    cont_pc.nombre=respaldo_ejec.user_gestor.first_name+' '+respaldo_ejec.apellido
                    cont_pc.correo=respaldo_ejec.user_gestor.email
                    cont_pc.tel_lab=respaldo_ejec.fono_t
                    cont_pc.cel_lab=respaldo_ejec.cod_area.codigo+respaldo_ejec.fono_c
                    cont_pc.save()
                    proced.contactos_pc.add(cont_pc)

                #enlace y respaldo
                cont_pc=Contactos_PC()
                cont_pc.pk_padre = proced.pk
                cont_pc.nombre=enlace.user_gestor.first_name+' '+enlace.apellido
                cont_pc.correo=enlace.user_gestor.email
                cont_pc.tel_lab=enlace.fono_t
                cont_pc.cel_lab=enlace.cod_area.codigo+enlace.fono_c
                cont_pc.save()
                proced.contactos_pc.add(cont_pc)

                if respaldo_enl:
                    cont_pc=Contactos_PC()
                    cont_pc.pk_padre = proced.pk
                    cont_pc.nombre=respaldo_enl.user_gestor.first_name+' '+respaldo_enl.apellido
                    cont_pc.correo=respaldo_enl.user_gestor.email
                    cont_pc.tel_lab=respaldo_enl.fono_t
                    cont_pc.cel_lab=respaldo_enl.cod_area.codigo+respaldo_enl.fono_c
                    cont_pc.save()
                    proced.contactos_pc.add(cont_pc)                     
            else:
                print('tiene contactos')
                     
            
            # Marca seccion como completa
            proced.sec_1_completa = True
            
            #Graba Procedimiento
            proced.save()
            proceso.subproceso.save()
            proceso.save()            

            print('Grabo Procedimiento')

            
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            
            
        # redirect to a new URL:
        
        #return HttpResponseRedirect(reverse('Lista-Proced'))
        return HttpResponseRedirect(reverse('crea-proced-C', args=[str(proced.id)]))
        #return render(request, 'bcp/proced_cont/proced_crea_C.html', {'proced':proced, 'proceso':proceso, 'escenarios':escenarios, 'servicios':servicios,
        #                                                          'contactos':contactos, 'pasos':pasos})
        
                      

    # If this is a GET (or any other method) create the default form.
    else:
        print('nombre procedimiento=', proced.nombre)
        form = CreaProc_B_Form(request.POST  or None, param=escenarios.all(),
                               initial= {
                                'nombre':proced.nombre,
                                'tipo':proced.tipo,
                                'escenarios':proced.escenarios,
                                'estrategia':proced.estrategia,
                                'resp_proceso':proced.resp_proceso,
                                'bck_resp':proced.bck_resp,
                                'gestor_ejecutor':proced.gestor_ejecutor,
                                'bck_ejecutor':proced.bck_ejecutor,
                                'enlace_c_crisis':proced.enlace_c_crisis,
                                'bck_enlace':proced.bck_enlace,
                                'servicios':proced.servicios_pc,
                                'contactos':proced.contactos_pc,
                                'pasos':proced.pasos}
                                )

    
        return render(request, 'bcp/proced_cont/proced_crea_B.html', {'form': form,
                                                                      'proced':proced,
                                                                      'proceso':proceso,
                                                                      'escenarios':escenarios,
                                                                      'servicios':servicios,
                                                                      'contactos':contactos,
                                                                      'pasos':pasos,
                                                                      'ruta':ruta})


#*************************************************************
# 2.2.3  Creacion parte (C) de Procedimiento de Recuperacion *
#*************************************************************
from .forms import CreaProc_P5_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_prcd_P5(request, pk):
    """
    Ingresa Servicios Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision 
    """
    print('-- CREA Servicios en Formulario de Definicion de Procedimiento (cr_prcd_P6)')

    #fase_i=int(fase)


    global url_ant

    proced = get_object_or_404(Procedimientos, pk = pk)

    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P5_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            servicio = Servicios_PC()

            servicio.pk_padre = pk
            servicio.nombre = form.cleaned_data['nombre']
            servicio.objetivo = form.cleaned_data['objetivo']
            servicio.contacto = form.cleaned_data['contacto']
            servicio.contacto_bck = form.cleaned_data['contacto_bck']
            
            #Adiciona el Servicio al Procedimiento
            servicio.save()
            proced.servicios_pc.add(servicio)

            #Marca la seccion como completa
            #num = proced.sec_servicios
            #num = num+1
            #proced.sec_servicios = num
            proced.save()
            
                     
            # Redirecciona a la lista 
            #return HttpResponseRedirect(url_ant)
            #if fase == 0:
            #    return HttpResponseRedirect(reverse('rev-proced-c', args=[str(proced.id)]))
            #else:
            #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))
            
            # Dirige la Salida 
            next_url = request.GET.get('next', '/')
            return redirect(next_url)

        
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        print(url_ant)
        form = CreaProc_P5_Form()
        return render(request, 'bcp/proced_cont/prcd_crea_serP5.html', {'form': form,
                                                                        'servicios':proced.servicios_pc})    


#@permission_required('Catalogo.can_mark_returned')
@login_required
def br_prcd_P5(request, pk):
    """
    Borra Servicios Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision 

    """
    print('-- BORRA Servicios en Formulario de Definicion de Procedimiento (cr_prcd_P6)')

    servicio_pc = get_object_or_404(Servicios_PC, pk = pk)
    proced = get_object_or_404(Procedimientos, pk = servicio_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_servicios
    #num = num-1
    #proced.sec_servicios = num
    proced.save()

    #Borra Servicio                
    servicio_pc.delete()
    
    #if fase == 0:
    #    return HttpResponseRedirect(reverse('rev-proced-c', args=[str(proced.id)]))
    #else:
    #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


from .forms import CreaProc_P6_Form


@login_required
def cr_prcd_P6(request, pk):
    """
    Ingresa Contactos Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision 

    """

    print('-- CREA Contacto en Formulario de Definicion de Procedimiento (cr_prcd_P6)')

    proced = get_object_or_404(Procedimientos, pk = pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P6_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            contacto = Contactos_PC()
            
            contacto.pk_padre = pk
            contacto.nombre = form.cleaned_data['nombre']
            contacto.correo = form.cleaned_data['correo']
            contacto.tel_lab = form.cleaned_data['tel_lab']
            contacto.cel_lab = form.cleaned_data['cel_lab']
            
            #Agrega Contacto al Procedimiento
            contacto.save()
            proced.contactos_pc.add(contacto)

            #Marca la seccion como completa
            #num = proced.sec_contactos
            #num = num+1
            #proced.sec_contactos = num
            proced.save()

            
            #if fase == 0:
            #    return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
            #else:
            #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))
            
            # Dirige la Salida 
            next_url = request.GET.get('next', '/')
            return redirect(next_url)

            #proced.servicios_pc.save()
        
        else:
            
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})            
                     
        

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        form = CreaProc_P6_Form()
        return render(request, 'bcp/proced_cont/prcd_crea_conP6.html', {'form': form, 'contactos':proced.contactos_pc})
    


#@permission_required('Catalogo.can_mark_returned')
@login_required
def br_prcd_P6(request, pk):
    """
    Borra Servicios Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision
    """
    print('-- BORRA  Contacto en Formulario de Definicion de Procedimiento (cr_prcd_P6)')

    contacto_pc = get_object_or_404(Contactos_PC, pk = pk)
    proced = get_object_or_404(Procedimientos, pk = contacto_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_contactos
    #num = num-1
    #proced.sec_contactos = num
    proced.save()
   
    contacto_pc.delete()

   
    #if fase == 0:
    #    return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
    #else:
    #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

    
    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)



from .forms import CreaProc_P7_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_prcd_P7(request, pk, fase):
    """
    Ingresa Pasos del PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision
    """
    global url_ant

    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso=get_object_or_404(Proceso, pk=proced.pk_padre)

    # rescata el valor del rto para controlar el tiempo total de los pasos del PC
    indicadores=proceso.subproceso.indicador_subp
    for ind in indicadores.all():
        print('ind nombre', ind.indicador.nombre)
        print('ind nivel ', ind.nivel.valor)

        if ind.indicador.nombre=="RTO":
            rto=ind.nivel.definicion
    print('rto',rto)
   
    # Calcula tiempo disponible en relacion al RTO
    pasos_ac=proced.pasos
    acum=0
    acum_h=00.00
    for pas in pasos_ac.all():
        acum=acum+pas.tiempo_esp
    acum_h=float(acum/60)
    print('Tiempo acumulado de pasos', acum,'-',acum_h)

   
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P7_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            paso = Pasos_PC()
            
            paso.pk_padre = pk
            paso.nro_paso = form.cleaned_data['nro_paso']
            paso.descripcion = form.cleaned_data['descripcion']
            paso.ejecutor = form.cleaned_data['ejecutor']
            paso.tiempo_esp = form.cleaned_data['tiempo_esp']
            

            paso.save()
            proced.pasos.add(paso)

            #Marca la seccion como completa
            #num = proced.sec_pasos
            #num = num+1
            #proced.sec_pasos = num
            #proced.save()
            
            # redirect to a new URL:
            if fase == 0:
                return HttpResponseRedirect(reverse('crea-P7', args=[str(proced.id), 0]))
            else:
                return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

            
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            

    # If this is a GET (or any other method) create the default form.
    else:

        form = CreaProc_P7_Form(initial={'ejecutor':proced.gestor_ejecutor})

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'bcp/proced_cont/prcd_crea_pasP7.html', {'form': form, 'pasos':proced.pasos,
                                                                        'rto':rto,
                                                                        'proc':proced,
                                                                        'proceso':proceso,
                                                                        'acum':acum,
                                                                        'acum_h':acum_h})
    

#@permission_required('Catalogo.can_mark_returned')
@login_required
def br_prcd_P7(request, pk):
    """
    Borra Pasos del PC
    """
       
    
    paso_pc = get_object_or_404(Pasos_PC, pk = pk)
    proced = get_object_or_404(Procedimientos, pk = paso_pc.pk_padre)

 
    paso_pc.delete()

    #if fase == 0:
    #    return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
    #else:
    #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))


    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


from .forms import CreaProc_P8_Form
#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_prcd_P8(request, pk):
    """
    Ingresa Pruebas al Procedimiento Parte A (datos generales)
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision
    """
    global url_ant

    print('>>>>>> Crea Prueba ')
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso=get_object_or_404(Proceso, pk=proced.pk_padre)

   
   
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P8_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            # Determina Codigo de la Prueba (Idem al nombre del Procedimiento + correlativo)

            # Rescata correlativo de Incidente. 
            n=proced.corr_prbas

            # Compone la parte numerica del codigo a un largo fijo 
            if n<9:
                nro='00' 
                nro=nro+str(n)
            elif n > 9 and n <= 99:
                nro='0' 
                nro=nro+str(n)
            elif n > 99 and n <= 999:
                nro=str(n)
            else:
                proced.corr_prbas=1

            proced.corr_prbas=n+1
            proced.save()

            #Crea el Registro del Proceso
            test = PruebaContingencia()
            print('----- nro=', nro)
            test.codigo=nro
            test.procedimiento=proced
            test.objetivo = form.cleaned_data['objetivo']
            test.alcance  = form.cleaned_data['alcance']
            test.criterios_exito = form.cleaned_data['criterios_exito']
            test.responsable = form.cleaned_data['responsable']

            test.save()

            
            # redirect to a new URL:
            #if fase == 0:
                # Dirige a la lista de casos.
            #    return HttpResponseRedirect(reverse('Lista-Casos-P8', args=[str(test.id)]))
            #else:
            #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

            # Dirige la Salida 
            next_url = request.GET.get('next', '/')
            return redirect(next_url)


            
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            

    # If this is a GET (or any other method) create the default form.
    else:

        form = CreaProc_P8_Form(initial={'responsable':proced.gestor_ejecutor})

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'bcp/proced_cont/prcd_crea_prbaP8.html', {'form': form, 'pasos':proced.pasos,
                                                                        'proc':proced,
                                                                        'proceso':proceso
                                                                        })


@login_required
def br_prcd_P8(request, pk):
    """
    Borra la Prueba de Procedimiento C.
    """
    print('>>>>> Borra Prueba')
    print('pk=', pk)
    test=get_object_or_404(PruebaContingencia, pk=pk)
    test.delete()

    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


    #if fase == 0:
    #    print('vuelva a lista-c')
    #    return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
    #else:
    #    print('vuelve a rev-proced-v')
    #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

    # Dirige la Salida 



from .forms import CreaProc_P8_Form
#@permission_required('Catalogo.can_mark_returned')
@login_required
def md_prcd_P8(request, pk):
    """
    Modifica la Prueba asociada al  Procedimiento -  Parte A (datos generales)
    pk: pk de la prueba
    """
    global url_ant

    print('>>>>>> Crea Prueba ')
    test = get_object_or_404(PruebaContingencia, pk = pk)
    proced=test.procedimiento

    proceso=get_object_or_404(Proceso, pk=proced.pk_padre)

   
   
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P8_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            #Modifica el Registro de la prueba
            test.objetivo = form.cleaned_data['objetivo']
            test.alcance  = form.cleaned_data['alcance']
            test.criterios_exito = form.cleaned_data['criterios_exito']
            test.responsable = form.cleaned_data['responsable']

            test.save()

            
            # redirect to a new URL:
            #if fase == 0:
            #    # Dirige a la lista de casos.
            #    return HttpResponseRedirect(reverse('Lista-Casos-P8', args=[str(test.id)]))
            #else:
            #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

            # Dirige la Salida 
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            
    
    # If this is a GET (or any other method) create the default form.
    else:

        form = CreaProc_P8_Form(initial={'objetivo':test.objetivo,
                                         'alcance':test.alcance,
                                         'criterios_exito':test.criterios_exito,
                                         'responsable':test.responsable})

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'bcp/proced_cont/prcd_crea_prbaP8.html', {'form': form, 'pasos':proced.pasos,
                                                                        'proc':proced,
                                                                        'proceso':proceso
                                                                        })

@login_required
def lta_casos_P8_B(request, pk):
    """
    Lista los Casos de Prueba durante ingreso/modificacion de Prueba
    pk: pk de la Prueba
    """
    
    prueba=get_object_or_404(PruebaContingencia, pk=pk)
    proced=prueba.procedimiento
    proceso=get_object_or_404(Proceso, pk=proced.pk_padre)
    lista_casos=CasoPrueba.objects.filter(prueba=prueba)


    return render(request, 'bcp/proced_cont/lta_casos_P8.html', {'lista_casos':lista_casos,
                                                                 'prueba':prueba,
                                                                 'proceso':proceso,
                                                                 'proced':proced
                                                                        })

from .forms import Caso_P8_Form
#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_caso_P8(request, pk, origen):
    """
    Crea Caso de Prueba asociado a una Prueba de Procedimiento
    pk: pk del la Prueba
    origen: Origen de la llamada
            0: Desde la Creacion del Procedimiento
            1: Desde la Revision del Procedimiento
    """
    global url_ant

    prueba = get_object_or_404(PruebaContingencia, pk = pk)
    proced=prueba.procedimiento
    proceso=get_object_or_404(Proceso, pk=proced.pk_padre)
    lista_casos=CasoPrueba.objects.filter(prueba=prueba)
   
   
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = Caso_P8_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            # Determina Codigo de la Prueba (Idem al nombre del Procedimiento + correlativo)

            # Rescata correlativo de Incidente. 
            n=prueba.corr_casos
            n=n+1
            prueba.corr_casos=n
            prueba.save()

            # Compone la parte numerica del codigo a un largo fijo 
            if n <= 9:
                nro='00' 
                nro=nro+str(n)
            elif n > 9 and n <= 99:
                nro='0' 
                nro=nro+str(n)
            elif n > 99 and n <= 999:
                nro=str(n)
            else:
                prueba.corr_casos=1
                nro='001'

            #Crea el Registro del Proceso
            caso = CasoPrueba()
            
            caso.codigo=nro
            caso.prueba=prueba
            caso.descripcion = form.cleaned_data['descripcion']
            caso.resultado_esperado = form.cleaned_data['resultado_esperado']
            caso.precondiciones = form.cleaned_data['precondiciones']
            caso.prioridad = form.cleaned_data['prioridad']

            caso.save()

            
            # redirect to a new URL:
            #if fase == 0:
            #    return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
            #else:
            #    return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))
                  
            return HttpResponseRedirect(reverse('Crea-Caso-P8', args=[str(prueba.id), origen ]))
            
            # Dirige la Salida 
            #next_url = request.GET.get('next', '/')
            #return redirect(next_url)

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            

    # If this is a GET (or any other method) create the default form.
    else:

        form = Caso_P8_Form()

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'bcp/proced_cont/crea_caso_P8.html', {'form': form,
                                                                     'origen':origen,
                                                                     'prueba':prueba,
                                                                        'proc':proced,
                                                                        'proceso':proceso,
                                                                        'lista_casos':lista_casos
                                                                        })
@login_required
def br_caso_P8(request, pk):
    """
    Borra un Caso de Prueba"""

    caso = get_object_or_404(CasoPrueba, pk=pk)
    prueba=caso.prueba
    caso.delete()
 
    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

    #return HttpResponseRedirect(reverse('Crea-Caso-P8', args=[str(prueba.id), fase]))


#**************************************************************
# Ejecucion de Pruebas 





#*************************************************************
# 2.2.4  Borra el Procedimiento de Contingencia              *
#*************************************************************
@login_required
def borra_procedimiento(request, pk):
    "Borra el Procedimiento de Contingencia (PC)"

    proced=get_object_or_404(Procedimientos, pk=pk)

    if proced.es_borrable:
        proced.delete()

    return HttpResponseRedirect(reverse('Lista-Proced', args=[1]) )


    
#*******************************************************
# 3.10 Autorizacion del  Procedimiento de Contingencia *
#*******************************************************

@login_required
def Env_Aut_Proced(request, pk):
    """
    Envia el Procedimiento a Autorizacion 
    (Cambia el status del Procedimientoa "a": En autorizacion A)
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    proced = get_object_or_404(Procedimientos, pk = pk)

    proced.status = 'a'

    proced.save()
    
    print('status=',proced.status)

    # redirect to a new URL:
    return HttpResponseRedirect(reverse('Lista-Proced', args=[1]) )








    
from .forms import Autoriza_Proced_C_Form
import datetime
@login_required
def Aut_Proced_C(request, pk):
    """
    Autorizacion del Procedimiento
    Crea o Actualiza el Procedimiento Vigente 
    """
    print('>>>>> Entra Autoriza Procedimiento')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso= get_object_or_404(Proceso, pk = proced.pk_padre)

    sproceso_v = proceso.subproceso_v  # Para establecer relacion del PC con su Proceso asociado
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos

    # Selecciona las Pruebas y Casos por cada una
    tests = PruebaContingencia.objects.filter(procedimiento=proced)
    lista_prbas=[]
    for prba in tests:
        casos=CasoPrueba.objects.filter(prueba=prba)

        lista_prbas.append({'test':prba,
                 'casos':casos})
        
    print('---- Lista de Pruebas :', lista_prbas)

    # Selecciona observaciones del PC ("P")
    comentarios_pc=Log_Revision.objects.filter(procedimiento=proced)
    #comentarios_pc=[]
    #for com in comentarios_proced:
    #   if com.seccion == "P":
    #        comentarios_pc.append(com)

    print('comentarios_v=', comentarios_pc)

     
    form = Autoriza_Proced_C_Form()
    #aut=LogAut()

    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    #aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    #print('usuario de sesion',aut.gestor_aprobador)

     
    #aut.cod_proceso=proced.codigo 

    if request.method=='POST':

        form = Autoriza_Proced_C_Form(request.POST)
        
        print('> POST ')
        
        if form.is_valid():
            
            #Registra autorizacion en log
                                
            #aut.fecha=datetime.date.today()
            #aut.p_status=proced.status+'P'
            #aut.observacion=form.cleaned_data['comentario']
            aprobado=form.cleaned_data['aprobacion']
            #aut.Aprobado=aprobado           
            notifica=form.cleaned_data['notifica']
            
                            
            if aprobado:

                # Cambia de estado 
                # ================
                print('Estado Inicial=', proced.status)
                if proced.status == 'a':   
                    print('> aprobo a->A')
                    proced.status='A'      # Aprobado por Gestor Ejecutor
                    print('status final=',proced.status)

                elif proced.status == 'A':
                    print('> aprobo A->R')
                    proced.status='R'      # Aprobado por Gestor Responsable de Procedimiento
                    print('status final=',proced.status)


                    # Crea o Modifica Procedimiento  (SubProceso) Vigente
                    # Crea una entrada al log de Control de Cambios
                    # =============================================

                    # Determina si el PC existe para ese Proceso Vigente.
                    #pc_en_proceso_v=proceso.subproceso_v.procedimientos_contingencia_v

                    codigo_prcd=proced.codigo

                    existe=Procedimientos_V.objects.filter(codigo=codigo_prcd).exists()
                    hay_cambios=False

                    if not existe:    # Verifica si el PC Vigente existe
                            print('> Procedimiento NO Existe pc=', existe)

                            #==========================================
                            # **** Crea Nuevo Procedimiento Vigente ***
                            #==========================================

                            proced_v = Procedimientos_V()
                            print('>  PC vigente  no existe. Crea version inicial del PC vigente.')
                            detalle_log="Version Inicial."
                            proced_v.version = 1  
                            

                            proced_v.fecha_c = datetime.date.today()
                            proced_v.pk_padre = proced.pk_padre
                            proced_v.codigo   = proced.codigo
                            proced_v.subproceso = sproceso_v

                            #Asigna Identificacion del Procedimiento
                            proced_v.nombre = proced.nombre
                            proced_v.tipo = proced.tipo

                            #Asigna Contexto
                            proced_v.escenarios = proced.escenarios
                            proced_v.estrategia = proced.estrategia

                            #Asigna Responsables
                            proced_v.resp_proceso = proced.resp_proceso
                            proced_v.bck_resp = proced.bck_resp
                            proced_v.gestor_ejecutor = proced.gestor_ejecutor 
                            proced_v.bck_ejecutor  = proced.bck_ejecutor

                            proced_v.enlace_c_crisis = proced.enlace_c_crisis
                            proced_v.bck_enlace = proced.bck_enlace
                            proced_v.gestor_consultor = proced.gestor_consultor
                            proced_v.save()

                            #Asigna Servicios  
                            for spc in proced.servicios_pc.all():
                                # Crea entrada a Servicios
                                servicios_pc_v=Servicios_PC_V()

                                servicios_pc_v.pk_padre = spc.pk_padre 
                                servicios_pc_v.nombre = spc.nombre
                                servicios_pc_v.objetivo = spc.objetivo
                                servicios_pc_v.contacto = spc.contacto
                                servicios_pc_v.contacto_bck = spc.contacto_bck

                                servicios_pc_v.save()
                                proced_v.servicios_pc.add(servicios_pc_v)

                            
                            # Asigna Contactos
                            for con in proced.contactos_pc.all():
                                # Crea entrada de Contactos Vigentes
                                contactos_pc_v=Contactos_PC_V()

                                contactos_pc_v.pk_padre = con.pk_padre
                                contactos_pc_v.cont_int = con.cont_int
                                contactos_pc_v.nombre = con.nombre
                                contactos_pc_v.correo = con.correo
                                contactos_pc_v.tel_lab = con.tel_lab
                                contactos_pc_v.cel_lab = con.cel_lab

                                contactos_pc_v.save()
                                proced_v.contactos_pc.add(contactos_pc_v)

                            #Asigna Pasos del Procedimiento
                            for pas in proced.pasos.all():
                                # Crea entrada de Pasos Vigentes
                                pasos_v=Pasos_PC_V()

                                pasos_v.pk_padre = pas.pk_padre
                                pasos_v.nro_paso = pas.nro_paso
                                pasos_v.descripcion = pas.descripcion
                                pasos_v.ejecutor = pas.ejecutor
                                pasos_v.tiempo_esp = pas.tiempo_esp

                                pasos_v.save()
                                proced_v.pasos.add(pasos_v)

                            #Asigna Pruebas del Procedimiento
                            pruebas_prcd=PruebaContingencia.objects.filter(procedimiento=proced)
                            for prba in pruebas_prcd:
                                test_v=PruebaContingencia_V()

                                test_v.procedimiento=proced_v
                                test_v.codigo=prba.codigo
                                test_v.objetivo=prba.objetivo
                                test_v.alcance=prba.alcance
                                test_v.criterios_exito=prba.criterios_exito
                                test_v.fecha_programada=prba.fecha_programada
                                test_v.responsable=prba.responsable
                                test_v.estado=prba.estado

                                test_v.save()

                                # Asigna Casos de Prueba
                                casos_prba=CasoPrueba.objects.filter(prueba=prba)
                                for caso in casos_prba:
                                    caso_v=CasoPrueba_V()

                                    caso_v.prueba=test_v
                                    caso_v.codigo=caso.codigo
                                    caso_v.descripcion=caso.descripcion
                                    caso_v.resultado_esperado=caso.resultado_esperado
                                    caso_v.precondiciones=caso.precondiciones
                                    caso_v.prioridad=caso.prioridad

                                    caso_v.save()
                            

                            proced.existe_p_vigente=True  # Marca que el Procedimiento Vigente existe
                            
                            proced_v.save()

                            proced.save()

                            # asigna el Procedimiento Vigente creado al Proceso (vigente)
                            #proceso.subproceso_v.save()
                            proceso.subproceso_v.procedimientos_contingencia_v.add(proced_v)
                            proceso.subproceso_v.save()


                    else:
                            #=================================================
                            # Cambios en Procedimiento vigente (PC) existente /
                            #=================================================

                            print('-- > Existe PC vigente. Lo modifica! ')

                            proced_v=get_object_or_404(Procedimientos_V, codigo=codigo_prcd)

                            proced_v.fecha_c = datetime.date.today()        # Fecha de la autorizacion
                            version=int(proced_v.version)+1 # Incrementa version
                            proced_v.version = version      # asigna version 
                            detalle_log="Cambios autorizados a version "+str(version)+" : "

                            proced_v.subproceso = sproceso_v

                            hay_cambios=False

                            #=============================================================
                            # Deteccion de Cambios y actualizacion de Control de Cambios /
                            #=============================================================

                            # Cambio de Nombre   
                            if proced_v.nombre != proced.nombre:
                                print('--- Cambio Nombre')
                                detalle_log=detalle_log+'Cambio al Nombre "'+proced_v.nombre+'", por "'+proced.nombre+'". // '
                                proced_v.nombre = proced.nombre
                                hay_cambios=True
                            else:
                                print('--- Sin Cambio en en nombre')

                            # Cambio Tipo
                            if proced_v.tipo != proced.tipo:
                                print('--- Cambio Tipo')
                                detalle_log=detalle_log+'Cambio al Tipo de PC ['+proced_v.tipo.nombre+'], por ['+proced.tipo.nombre+']. //'
                                proced_v.tipo = proced.tipo
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Tipo')


                            # Cambio a Escenario
                            if proced_v.escenarios != proced.escenarios:
                                print('--- Cambio en Escenarios')
                                detalle_log=detalle_log+'Cambio al Escenario ['+proced_v.escenarios.titulo+'], por ['+proced.escenarios.titulo+']. //'
                                proced_v.escenarios = proced.escenarios
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Escenario')


                            # Cambio en Estrategia
                            if proced_v.estrategia != proced.estrategia:
                                print('--- Cambio en Estrategia')
                                detalle_log=detalle_log+'Cambio a la Estrategia ['+proced_v.estrategia+'], por ['+proced.estrategia+']. // '
                                proced_v.estrategia = proced.estrategia
                                hay_cambios=True 
                            else:
                                print('--- Sin cambio en Estrategia')



                            # Cambios en Roles
                            if proced_v.resp_proceso != proced.resp_proceso:
                                print('--- Cambio en el Responsable')
                                detalle_log=detalle_log+'Cambio al Responsable -'+proced_v.resp_proceso.user_gestor.last_name+'-, por -'+proced.resp_proceso.user_gestor.last_name+'-. '
                                proced_v.resp_proceso = proced.resp_proceso
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Responsable')


                            if proced_v.bck_resp != proced.bck_resp:
                                print('--- Cambio en el Respaldo del Responsable')
                                if proced_v.bck_resp != None and  proced.bck_resp != None:
                                    detalle_log=detalle_log+'Cambio al Respaldo del Responsable -'+proced_v.bck_resp.user_gestor.last_name+'-,'+proced_v.bck_resp.user_gestor.first_name+', por '+proced.bck_resp.user_gestor.last_name+','+proced_v.bck_resp.user_gestor.first_name+'.'
                                elif  proced.bck_resp == None:
                                    detalle_log=detalle_log+'Se elimino al Respaldo del Responsable sin Asignacion definida. '
                                else:
                                    detalle_log=detalle_log+'Se asigna a '+proced.bck_resp.user_gestor.last_name+' Como Respaldo al Responsable.'
                                proced_v.bck_resp = proced.bck_resp
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Respaldo Responsable')


                            if proced_v.gestor_ejecutor != proced.gestor_ejecutor:
                                print('--- Cambio en el Ejecutor')
                                detalle_log=detalle_log+'Cambio al Ejecutor '+proced_v.gestor_ejecutor.user_gestor.last_name+' '+proced_v.gestor_ejecutor.user_gestor.first_name+', por '+proced.gestor_ejecutor.user_gestor.last_name+' '+proced.gestor_ejecutor.user_gestor.first_name+'.'
                                proced_v.gestor_ejecutor = proced.gestor_ejecutor
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Ejecutor')


                            if proced_v.bck_ejecutor != proced.bck_ejecutor:
                                print('--- Cambio en el Respaldo Ejecutor')
                                if proced_v.bck_ejecutor != None : 
                                    detalle_log=detalle_log+'Cambio al Respaldo del Ejecutor '+proced_v.bck_ejecutor.user_gestor.last_name+','+proced_v.bck_ejecutor.user_gestor.first_name+', por '+proced.bck_ejecutor.user_gestor.last_name+','+proced_v.bck_ejecutor.user_gestor.first_name+'.'
                                elif  proced.bck_ejecutor == None:
                                    detalle_log=detalle_log+'Se elimino al Respaldo del Ejecutor sin Asignacion definida. '
                                else:
                                    detalle_log=detalle_log+'Se asigna a '+proced.bck_ejecutor.user_gestor.last_name+' '+proced.bck_ejecutor.user_gestor.first_name+' Como Respaldo al Ejecutor.'

                                proced_v.bck_ejecutor = proced.bck_ejecutor
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Respaldo Ejecutor')

                            if proced_v.enlace_c_crisis != proced.enlace_c_crisis:
                                print('--- Cambio en el Enlace CC')
                                detalle_log=detalle_log+'Cambio al Enlace del Comite de Crisis '+proced.enlace_c_crisis.user_gestor.last_name+' '+proced.enlace_c_crisis.user_gestor.first_name+', por '+proced_v.enlace_c_crisis.user_gestor.last_name+' '+proced_v.enlace_c_crisis.user_gestor.first_name +'.'
                                proced_v.enlace_c_crisis = proced.enlace_c_crisis
                                hay_cambios=True
                            else:
                                print('--- Sin cambio en Enlace')


                            if proced_v.bck_enlace != proced.bck_enlace:
                                print('--- Cambio en el Respaldo Enlace CC')
                                if proced_v.bck_enlace != None and proced.bck_enlace != None:
                                    detalle_log += 'Cambio del  Respaldo del Enlace del Comite de Crisis sr(a) '+proced_v.bck_enlace.user_gestor.last_name+','+proced_v.bck_enlace.user_gestor.first_name+', por el sr(a) '+proced.bck_enlace.user_gestor.last_name+','+proced_v.bck_enlace.user_gestor.first_name+'.'
                                elif  proced.bck_enlace == None:
                                    detalle_log=detalle_log+'Se elimino al Respaldo del Enlace del Comite de Crisis sin Asignacion definida. '
                                else:
                                    detalle_log += 'Se asigna a '+ proced.bck_enlace.user_gestor.last_name+' '+proced.bck_enlace.user_gestor.first_name+' Como Respaldo del Enlace del Comite de Crisis.'

                                proced_v.bck_enlace = proced.bck_enlace
                                hay_cambios=True
                            else:
                                print('--- Sin cambios en Respaldo Enlace')


                            detalle_log += './/'

                            # Actualiza Servicios
                            # ===================

                                #impactos_p = list(proc.subproceso.impact_subp.all())
                                #impactos_v = list(sub_proceso_v.impact_subp.all())

                                # Diccionarios por nombre de impacto

                                #dict_p = {imp.impacto.nombre: imp for imp in impactos_p}
                                #dict_v = {imp.impacto.nombre: imp for imp in impactos_v}

                                #nombres_p = set(dict_p.keys())
                                #nombres_v = set(dict_v.keys())

                                #impactos_agregados = nombres_p - nombres_v
                                #impactos_eliminados = nombres_v - nombres_p
                                #impactos_comunes = nombres_p & nombres_v


                            # Obtener Servicios como conjuntos
                            servicios_p = list(proced.servicios_pc.all())
                            servicios_v = list(proced_v.servicios_pc.all())

                            # Diccionarios por nombre de servicio
                            dict_p = {ser.nombre: ser for ser in servicios_p}
                            dict_v = {ser.nombre: ser for ser in servicios_v}

                            servicios_p = set(dict_p.keys())
                            servicios_v = set(dict_v.keys())

                            # Detectar diferencias
                            servicios_agregados = servicios_p - servicios_v
                            servicios_eliminados = servicios_v - servicios_p
                            print('-- servicios_agregados :', servicios_agregados)
                            print('-- servicios eliminados :', servicios_eliminados)

                            # Si hay cambios
                            if servicios_agregados or servicios_eliminados:
                                hay_cambios = True

                                # Actualiza los servicios vigentes a partir de los servicios
                                servicios_p2 = []
                                for s in proced.servicios_pc.all():  # s es de Servicios_PC
                                    print('s=', s.nombre)
                                    # Buscar el equivalente en Servicios_PC_V (por nombre en comun)
                                    s_v = Servicios_PC_V.objects.filter(nombre=s.nombre).first()
                                    print('s_v=', s_v)
                                    if s_v:
                                        servicios_p2.append(s_v)
                                    else:
                                        # Crea entrada a Servicios
                                        s_v=Servicios_PC_V()
                                        s_v.pk_padre = s.pk_padre 
                                        s_v.nombre = s.nombre
                                        s_v.objetivo = s.objetivo
                                        s_v.contacto = s.contacto
                                        s_v.contacto_bck = s.contacto_bck
                                        s_v.save()

                                        servicios_p2.append(s_v)

                                print("proced_v PK:", proced_v.pk)
                                print("Servicios actuales en proced_v:", list(proced_v.servicios_pc.all()))
                                print("Servicios en lista a asignar:", servicios_p2)
                                proced_v.save()
                                proced_v.servicios_pc.set(servicios_p2)

                                detalle_log += "Cambios en Servicios:\n"

                                if servicios_agregados:
                                    detalle_log += 'Servicios Agregados :'
                                    for servicio in servicios_agregados:
                                        detalle_log += servicio+', '

                                for servicio in servicios_eliminados:
                                    detalle_log += f"- Servicio eliminado: {servicio}\n"

                                detalle_log += './/'
                                print("CAMBIOS EN SERVICIOS:\n", detalle_log)
                            else:
                                print("Sin cambios en servicios.")
                        

                            # Actualiza Contactos
                            # ====================

                            # Obtener Contactos como conjuntos
                            contactos_p = list(proced.contactos_pc.all())
                            contactos_v = list(proced_v.contactos_pc.all())

                            # Diccionarios por nombre de servicio
                            dict_p = {ser.nombre: ser for ser in contactos_p}
                            dict_v = {ser.nombre: ser for ser in contactos_v}

                            contactos_p = set(dict_p.keys())
                            contactos_v = set(dict_v.keys())

                            # Detectar diferencias
                            contactos_agregados = contactos_p - contactos_v
                            contactos_eliminados = contactos_v - contactos_p
                            print('-- Contactos agregados :', contactos_agregados)
                            print('-- Contactos eliminados :', contactos_eliminados)


                            # Si hay cambios
                            if contactos_agregados or contactos_eliminados:
                                hay_cambios = True

                                # Crea Contactos vigentes 
                                contactos_p2 = []
                                for s in proced.contactos_pc.all():  # s es de Contactos_PC
                                    # Buscar el equivalente en Contactos_PC_V (por nombre en comun)
                                    s_v = Contactos_PC_V.objects.filter(nombre=s.nombre).first()
                                    if s_v:
                                        contactos_p2.append(s_v)
                                    else:
                                        # Crea entrada de Contactos Vigentes
                                        s_v = Contactos_PC_V()
                                        s_v.pk_padre = s.pk_padre
                                        s_v.cont_int = s.cont_int
                                        s_v.nombre = s.nombre
                                        s_v.correo = s.correo
                                        s_v.tel_lab = s.tel_lab
                                        s_v.cel_lab = s.cel_lab
                                        s_v.save()
                                        contactos_p2.append(s_v)

                                proced_v.contactos_pc.set(contactos_p2)
                                proced_v.save()

                                detalle_log += "Cambios en Contactos:\n"

                                for contacto in contactos_agregados:
                                    detalle_log += f"+ Contacto agregado: {contacto}\n"

                                for contacto in contactos_eliminados:
                                        detalle_log += f"- Contacto eliminado: {contacto}\n"

                                detalle_log +='.//'
                                print("CAMBIOS EN CONTACTOS:\n", detalle_log)

                            else:
                                    print("Sin cambios en contactos.")


                            # Deteccion de Cambios y Actualizacion Pasos del PC
                            # =================================================
                            
                            # Obtener Pasos como conjuntos
                            pasos_p = list(proced.pasos.all())
                            pasos_v = list(proced_v.pasos.all())

                            # Diccionarios por nombre de servicio
                            dict_p = {ser.descripcion: ser for ser in pasos_p}
                            dict_v = {ser.descripcion: ser for ser in pasos_v}

                            pasos_p = set(dict_p.keys())
                            pasos_v = set(dict_v.keys())

                            # Detectar diferencias
                            pasos_agregados = pasos_p - pasos_v
                            pasos_eliminados = pasos_v - pasos_p
                            print('-- Pasos agregados :', pasos_agregados)
                            print('-- Pasos eliminados :', pasos_eliminados)

                            # Si hay cambios
                            if pasos_agregados or pasos_eliminados:
                                hay_cambios = True

                                # Actualiza Pasos vigentes 
                                pasos_p2 = []
                                for s in proced.pasos.all():  # s es de Pasos_PC
                                    # Buscar el equivalente en Contactos_PC_V (por descripcion)
                                    s_v = Pasos_PC_V.objects.filter(descripcion=s.descripcion).first()
                                    if s_v:
                                        pasos_p2.append(s_v)
                                    else:
                                        # Crea  Pasos Vigentes
                                        s_v=Pasos_PC_V()
                                        s_v.pk_padre = s.pk_padre
                                        s_v.nro_paso = s.nro_paso
                                        s_v.descripcion = s.descripcion
                                        s_v.ejecutor = s.ejecutor
                                        s_v.tiempo_esp = s.tiempo_esp
                                        s_v.save()
                                        pasos_p2.append(s_v)

                                proced_v.pasos.set(pasos_p2)
                                proced_v.save()

                                detalle_log += "Cambios en pasos del PC:\n"

                                for paso in pasos_agregados:
                                    detalle_log += f"+ Paso agregado: {paso}\n"

                                for paso in pasos_eliminados:
                                        detalle_log += f"- Paso eliminado: {paso}\n"

                                detalle_log +='.//'
                                print("CAMBIOS EN PASOS:\n", detalle_log)

                            else:
                                    print("Sin cambios en pasos.")


                            # Deteccion de Cambios y Actualizacion de Pruebas
                            # ===============================================

                            # --- OBTENER LAS PRUEBAS PARA EL PROCEDIMIENTO (NO M2M, filtrado por FK) ---
                            pruebas_p_qs = PruebaContingencia.objects.filter(procedimiento=proced)
                            pruebas_v_qs = PruebaContingencia_V.objects.filter(procedimiento=proced_v)

                            # Diccionarios por codigo (clave lógica)
                            dict_p = {p.codigo: p for p in pruebas_p_qs}
                            dict_v = {p.codigo: p for p in pruebas_v_qs}

                            set_p = set(dict_p.keys())
                            set_v = set(dict_v.keys())

                            pruebas_agregadas = set_p - set_v
                            pruebas_eliminadas = set_v - set_p
                            pruebas_comunes = set_p & set_v

                            detalle_log += f"-- Pruebas agregadas: {pruebas_agregadas}\n"
                            detalle_log += f"-- Pruebas eliminadas: {pruebas_eliminadas}\n"

                            # Campos de cabecera a comparar/actualizar en PruebaContingencia_V
                            campos_prueba = ['codigo', 'objetivo', 'alcance', 'criterios_exito', 'fecha_programada', 'responsable', 'estado', 'corr_casos']

                            with transaction.atomic():
                                cambios_globales = False

                                # ----------------------------
                                # 1) Crear PruebaContingencia_V faltantes (agregadas en diseño)
                                # ----------------------------
                                for codigo in pruebas_agregadas:
                                    p = dict_p[codigo]  # PruebaContingencia origen
                                    p_v = PruebaContingencia_V.objects.create(
                                        procedimiento=proced_v,
                                        codigo=p.codigo,
                                        objetivo=p.objetivo,
                                        alcance=p.alcance,
                                        criterios_exito=p.criterios_exito,
                                        fecha_programada=p.fecha_programada,
                                        responsable=p.responsable,
                                        estado=p.estado,
                                        corr_casos=p.corr_casos,
                                    )
                                    cambios_globales = True
                                    hay_cambios = True
                                    detalle_log += f"+ Prueba agregada: {p.codigo}\n"

                                    # Crear también todos los casos asociados a la prueba nueva
                                    casos_origen = CasoPrueba.objects.filter(prueba=p)
                                    for c in casos_origen:
                                        CasoPrueba_V.objects.create(
                                            prueba=p_v,
                                            codigo=c.codigo,
                                            descripcion=c.descripcion,
                                            resultado_esperado=c.resultado_esperado,
                                            precondiciones=c.precondiciones,
                                            prioridad=c.prioridad,
                                        )
                                        detalle_log += f"    + Caso agregado (al crear prueba): {c.codigo}\n"

                                # ----------------------------
                                # 2) Eliminar PruebaContingencia_V que ya no existen en diseño
                                # ----------------------------
                                for codigo in pruebas_eliminadas:
                                    p_v = dict_v[codigo]
                                    # opcional: loguear cuantos casos tenía antes de borrar
                                    num_casos = CasoPrueba_V.objects.filter(prueba=p_v).count()
                                    detalle_log += f"- Prueba eliminada: {p_v.codigo} (casos vigentes borrados: {num_casos})\n"
                                    p_v.delete()
                                    cambios_globales = True
                                    hay_cambios = True

                                # ----------------------------
                                # 3) Para pruebas existentes en ambos lados, comparar cabecera y sincronizar
                                # ----------------------------
                                for codigo in pruebas_comunes:
                                    p = dict_p[codigo]   # PruebaContingencia origen
                                    p_v = dict_v[codigo] # PruebaContingencia_V vigente
                                    cambios_cabecera = []

                                    for campo in campos_prueba:
                                        # Normalizaciones simples si las necesitas, por ejemplo:
                                        val_p = getattr(p, campo)
                                        val_v = getattr(p_v, campo)
                                        # Si trabajas con DateTimeField y zonas horarias, normalizar antes de comparar
                                        if val_p != val_v:
                                            cambios_cabecera.append((campo, val_v, val_p))
                                            setattr(p_v, campo, val_p)

                                    if cambios_cabecera:
                                        p_v.save()
                                        cambios_globales = True
                                        hay_cambios = True
                                        detalle_log += f"* Prueba actualizada: {codigo}\n"
                                        for campo, old, new in cambios_cabecera:
                                            detalle_log += f"    - {campo}: '{old}' -> '{new}'\n"

                                    # --- Ahora sincronizar los CASOS de esta prueba ---
                                    casos_p_qs = CasoPrueba.objects.filter(prueba=p)
                                    casos_v_qs = CasoPrueba_V.objects.filter(prueba=p_v)

                                    dict_c_p = {c.codigo: c for c in casos_p_qs}
                                    dict_c_v = {c.codigo: c for c in casos_v_qs}

                                    set_c_p = set(dict_c_p.keys())
                                    set_c_v = set(dict_c_v.keys())

                                    casos_agregados = set_c_p - set_c_v
                                    casos_eliminados = set_c_v - set_c_p
                                    casos_comunes = set_c_p & set_c_v

                                    # Crear casos agregados
                                    for cc in casos_agregados:
                                        c = dict_c_p[cc]
                                        CasoPrueba_V.objects.create(
                                            prueba=p_v,
                                            codigo=c.codigo,
                                            descripcion=c.descripcion,
                                            resultado_esperado=c.resultado_esperado,
                                            precondiciones=c.precondiciones,
                                            prioridad=c.prioridad,
                                        )
                                        cambios_globales = True
                                        hay_cambios = True
                                        detalle_log += f"    + Caso agregado: {c.codigo}\n"

                                    # Eliminar casos que ya no existen
                                    for cc in casos_eliminados:
                                        c_v = dict_c_v[cc]
                                        detalle_log += f"    - Caso eliminado: {c_v.codigo}\n"
                                        c_v.delete()
                                        cambios_globales = True
                                        hay_cambios = True

                                    # Actualizar campos en casos comunes
                                    campos_caso = ['descripcion', 'resultado_esperado', 'precondiciones', 'prioridad']
                                    for cc in casos_comunes:
                                        c = dict_c_p[cc]
                                        c_v = dict_c_v[cc]
                                        cambios_campos_caso = []
                                        for campo in campos_caso:
                                            val_p = getattr(c, campo)
                                            val_v = getattr(c_v, campo)
                                            if val_p != val_v:
                                                cambios_campos_caso.append((campo, val_v, val_p))
                                                setattr(c_v, campo, val_p)
                                        if cambios_campos_caso:
                                            c_v.save()
                                            cambios_globales = True
                                            hay_cambios = True
                                            detalle_log += f"    * Caso actualizado: {cc}\n"
                                            for campo, old, new in cambios_campos_caso:
                                                detalle_log += f"        - {campo}: '{old}' -> '{new}'\n"

                                    # Mantener corr_casos en p_v sincronizado con la cantidad real (si cambió)
                                    nueva_corr = CasoPrueba_V.objects.filter(prueba=p_v).count()
                                    if p_v.corr_casos != nueva_corr:
                                        detalle_log += f"    # corr_casos: {p_v.corr_casos} -> {nueva_corr}\n"
                                        p_v.corr_casos = nueva_corr
                                        p_v.save()
                                        cambios_globales = True
                                        hay_cambios = True

                                if cambios_globales:
                                    detalle_log += ".//\n"

                            # Al final puedes imprimir o persistir el log
                            if hay_cambios:
                                print("CAMBIOS DETECTADOS:\n", detalle_log)
                            else:
                                print("Sin cambios en Pruebas ni Casos.")

                            #=================================================================
                            # FIN Deteccion de Cambios y actualizacion de Control de Cambios /
                            #=================================================================


                            if not hay_cambios:
                                detalle_log='Vigenteo version '+str(version)+' sin cambios en version anterior.'

                            print('Detalle log final', detalle_log)

                            proced_v.save()
                            #proceso.subproceso_v.procedimientos_contingencia_v.set([proced_v])
                            proceso.subproceso_v.save()
                            proceso.save()

                            # FIN PC existe. Se modifica 
                    
                    # Crea registro del Control de Cambios
                    # =======================================

                    print('> Crea entrada al log de Control de Cambios')
                    log=Control_Cambios()

                    # Crea entrada
                    log.procedimiento=proced_v
                    log.gestor_aut=proced_v.resp_proceso
                    log.descripcion=detalle_log
                    log.save()


                    # Prepara email para Gestor Consultor
                    # ===================================
                    #  
                    # nombre=proc.subproceso.gestor_C.user_gestor.last_name
                    # email = proc.subproceso.gestor_C.user_gestor.email
                    # accion='tomar conocimiento de la puesta en vigencia del '


                    # Prepara mensaje x correo
                    #nombre=proced.resp_proceso.user_gestor.last_name
                    #email = proc_rev.subproceso.gestor_R.user_gestor.email
                    #accion='dar visto bueno o requerir cambios para el '
                    
            else:

                print('> No aprobo C->A')

                proced.status='x'
                proced.sec_1_completa = False
                proced.sec_2_completa = False
                #aut.p_status=proced.status+'P'
                #aut.item='Enviado a Gestor Consultor para revision de Observaciones'
                    
                #email = proc_rev.subproceso.gestor_C.user_gestor.email
                #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
           
            #Graba en Base de Datos                
            #aut.save()
            #proced.log_auth.add(aut)      
            proced.save()
            proceso.save()
            
                
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Proced', args=[1]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'bcp/proced_cont/proced_auth.html', {'form': form,
                                                                    'proceso':proceso,
                                                                    'proced':proced,
                                                                    'servicios':servicios,
                                                                    'contactos':contactos,
                                                                    'lista_prbas':lista_prbas,
                                                                    'comentarios':comentarios_pc,
                                                                    'pasos':pasos})




#****************************************************************************
#3.11 Revision Autorizacion RACI de Procedimiento de Contingencia Rechazada *
#****************************************************************************

from .forms import Revisa_Proced_B_Form
@login_required
def Revisa_Proced_B(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))


    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso= get_object_or_404(Proceso, pk = proced.pk_padre)
    escenarios=proceso.subproceso.escenarios
    ruta=resta_string(proceso.path, proceso.nombre)
    
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos

    # rescata las Pruebas asociadas al procedimiento
    pruebas=PruebaContingencia.objects.filter(procedimiento=proced)

    comentarios_pc=Log_Revision.objects.filter(procedimiento=proced)

    print('nombre proceso=', proceso.nombre)
    print('nombre procedimiento=', proced.nombre)

    print('Revisa parte B')
    

    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        #form = Revisa_Proced_B_Form(request.POST)
        #form = CreaProc_B_Form(request.POST)
        form = CreaProc_B_Form(request.POST  or None, param=escenarios.all()) # Envia Escenarios del Proceso

        
        # Check if the form is valid:
        
        if form.is_valid():
            
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Actualiza el Registro del Proceso
                        
            proced.nombre = form.cleaned_data['nombre']
            #proced.tipo = form.cleaned_data['tipo']
            
            proced.escenarios = form.cleaned_data['escenarios']

            proced.estrategia = form.cleaned_data['estrategia']
            
            proced.resp_proceso = form.cleaned_data['resp_proceso']
            proced.bck_resp = form.cleaned_data['bck_resp']

            proced.gestor_ejecutor = form.cleaned_data['gestor_ejecutor']
            proced.bck_ejecutor = form.cleaned_data['bck_ejecutor']

            proced.enlace_c_crisis = form.cleaned_data['enlace_c_crisis']
            proced.bck_enlace = form.cleaned_data['bck_enlace']
            
            
            # Cambia Status a "a" (Por Autorizar)
            
            #proced.status = 'a'
            

            #if notifica: (manda correo de notificacion)
            
            #Graba Procedimiento
            proced.save()
            proceso.subproceso.save()
            proceso.save()            

            print('Grabo Procedimiento')
            
            # redirect to a new URL:
        
            #return HttpResponseRedirect(reverse('Lista-Proced', args=[1]))
            return HttpResponseRedirect(reverse('rev-proced-c', args=[str(proced.id)]))
            
        else:
            
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    # If this is a GET (or any other method) create the default form.
    else:
        print('nombre procedimiento=', proced.nombre)
        form = CreaProc_B_Form(request.POST  or None, param=escenarios.all(),
                               initial= {
                                'nombre':proced.nombre,
                                'tipo':proced.tipo,
                                'escenarios':proced.escenarios,
                                'estrategia':proced.estrategia,
                                'resp_proceso':proced.resp_proceso,
                                'bck_resp':proced.bck_resp,
                                'gestor_ejecutor':proced.gestor_ejecutor,
                                'bck_ejecutor':proced.bck_ejecutor,
                                'enlace_c_crisis':proced.enlace_c_crisis,
                                'bck_enlace':proced.bck_enlace,
                                }
                        )

    
        return render(request, 'bcp/proced_cont/proced_rev_B.html', {'form': form,
                                                                     'proced':proced,
                                                                     'proceso':proceso,
                                                                     'escenarios':escenarios,
                                                                     'servicios':servicios,
                                                                     'contactos':contactos,
                                                                     'pasos':pasos,
                                                                     'pruebas':pruebas,
                                                                     'comentarios':comentarios_pc,
                                                                     'ruta':ruta
                                                                     })




    
#*******************************************************************************
#1.10 Lista de Servicios, Contactos, Pasos y Pruebas en Creacion de Procedimiento(PC)   *
#*******************************************************************************

@login_required
def cr_prcd_list(request, pk):
    """
    Lista de Servicios, Contactos, Pasos y Pruebas en Creacion de Procedimiento(PC)
    pk: pk del procedimiento
    """
    print('lista Servicios/Contactos/Pasos')
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso = get_object_or_404(Proceso, pk=proced.pk_padre)
    escenarios = proceso.subproceso.escenarios
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos
    ruta=resta_string(proceso.path, proceso.nombre)

    # rescata las Pruebas asociadas al procedimiento
    pruebas=PruebaContingencia.objects.filter(procedimiento=proced)

    # rescata el valor del rto para controlar el tiempo total de los pasos del PC
    indicadores=proceso.subproceso.indicador_subp
    for ind in indicadores.all():
        print('ind nombre', ind.indicador.nombre)
        print('ind nivel ', ind.nivel.valor)

        if ind.indicador.nombre=="RTO":
            rto=ind.nivel.definicion
    print('rto',rto)

    
    return render(request, 'bcp/proced_cont/proced_crea_C.html', {'proced':proced,
                                                                  'proceso':proceso,
                                                                  'escenarios':escenarios,
                                                                  'servicios':servicios,
                                                                  'contactos':contactos,
                                                                  'pasos':pasos,
                                                                  'pruebas':pruebas,
                                                                  'rto':rto,
                                                                  'ruta':ruta
                                                                  })

@login_required
def rev_prcd_list(request, pk):
    """
    Lista de Servicios, Contactos, Pasos y Pruebas en Revision de la Creacion de 
    Procedimiento(PC)
    pk: pk del procedimiento
    origen: 0: Desde Creacion del Procedimiento
            1: Desde Revision del PC. 
    """
    print('lista Servicios/Contactos/Pasos')
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso = get_object_or_404(Proceso, pk=proced.pk_padre)
    escenarios = proceso.subproceso.escenarios
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos
    ruta=resta_string(proceso.path, proceso.nombre)

    # rescata las Pruebas asociadas al procedimiento
    pruebas=PruebaContingencia.objects.filter(procedimiento=proced)

    comentarios_pc=Log_Revision.objects.filter(procedimiento=proced)

    # rescata el valor del rto para controlar el tiempo total de los pasos del PC
    indicadores=proceso.subproceso.indicador_subp
    for ind in indicadores.all():
        print('ind nombre', ind.indicador.nombre)
        print('ind nivel ', ind.nivel.valor)

        if ind.indicador.nombre=="RTO":
            rto=ind.nivel.definicion
    print('rto',rto)

    
    return render(request, 'bcp/proced_cont/proced_rev_C.html', {'proced':proced,
                                                                  'proceso':proceso,
                                                                  'escenarios':escenarios,
                                                                  'servicios':servicios,
                                                                  'contactos':contactos,
                                                                  'pasos':pasos,
                                                                  'pruebas':pruebas,
                                                                  'comentarios':comentarios_pc,
                                                                  'rto':rto,
                                                                  'ruta':ruta
                                                                  })

#******************************************************
# 1.10 Muestra datos (detalle) del Procedimiento(PC)  *
#******************************************************
@login_required
def detalle_procedimiento(request, pk ):
    """ Detalle del Procedimiento
    pk: Identificacion del Procedimiento
    """

    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso = get_object_or_404(Proceso, pk=proced.pk_padre)

        # Selecciona las Pruebas y Casos por cada una
    tests = PruebaContingencia.objects.filter(procedimiento=proced)
    lista_prbas=[]
    for prba in tests:
        casos=CasoPrueba.objects.filter(prueba=prba)

        lista_prbas.append({'test':prba,
                 'casos':casos})
        
    print('---- Lista de Pruebas :', lista_prbas)

    return render(request, 'bcp/proced_cont/proced_detalle.html', {'proced':proced,
                                                                   'lista_prbas':lista_prbas, 
                                                                   'proceso':proceso})

@login_required   
def detalle_procedimiento_v(request, pk): 
    """ Muestra detalle del Procedimiento Vigente
    pk: Identificacion del Procedimiento Vigente
    """

    #proced = get_object_or_404(Procedimientos, pk = pk)
    proced_v=get_object_or_404(Procedimientos_V, pk=pk)
    proceso = get_object_or_404(Proceso, pk=proced_v.pk_padre)

    c_cambio=Control_Cambios.objects.filter(procedimiento=proced_v)
    n_proc=proceso.nombre
    ruta=resta_string(proceso.path,n_proc)
    consultor=proced_v.gestor_consultor
    print('---- Ruta: ', ruta)


    # Selecciona las Pruebas y Casos por cada una
    tests = PruebaContingencia_V.objects.filter(procedimiento=proced_v)
    lista_prbas=[]
    for prba in tests:
        casos=CasoPrueba_V.objects.filter(prueba=prba)

        lista_prbas.append({'test':prba,
                 'casos':casos})
        
    print('---- Lista de Pruebas :', lista_prbas)


    return render(request, 'bcp/proced_cont/proced_detalle_v.html', {'proced':proced_v,
                                                                     'proceso':proceso,
                                                                     'ruta':ruta,
                                                                     'lista_prbas':lista_prbas,
                                                                     'consultor':consultor,
                                                                     'c_cambio':c_cambio})


#******************************************************
# 1.11 Muestra datos (detalle) del Procedimiento(PC)  *
#******************************************************
@login_required
def ActualizaPC(request, pk):
    """
    Cambia el estado del PC de A (Autorizado) a C (En definicion) 
    para Actualizacion
    pk: pk del Procedimiento"""

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    proced=get_object_or_404(Procedimientos, pk=pk)

    proced.status="C"
    proced.save()

    return HttpResponseRedirect(reverse('Lista-Proced', args=[1]))


#*******************************
# 1.12 Activa / Desactiva PC   *
#*******************************
@login_required
def ConfirmaActivacionPC(request, pk):
    """
    Flag de Confirmacion por parte del Gestor Ejecutor de la Activacion del PC
    pk: pk del PC"""

    proced = get_object_or_404(Procedimientos, pk = pk)

    if proced.esta_confirmado:
        proced.esta_confirmado=False
    else:
        proced.esta_confirmado=True

        # Notificacion a Stackeholders

    proced.save()

    return HttpResponseRedirect(reverse('Lista-Proced', args=[1]))


#*********************************************************************************************************************************************
#***********************************************  6. DRP  ************************************************************************************
#*********************************************************************************************************************************************

#********************************
# 6.1 Lista los DRPs definidos  *
#********************************
@login_required
def Lista_DRP(request):
    """Lista los DRPs"""

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user,'TI']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[500] ))

    lista_drp = Drp.objects.all()
    
    return render(request, 'bcp/drp/lista_drp.html', context={'lista_drp':lista_drp})

#******************************************************
# 6.2 Muestra el Indice con las Secciones del DRP     *
#******************************************************
@login_required
def Indice_DRP(request, pk):
    """
    Indice de DRP 
    """
    print('------ Indice_DRP --------')
    #lista_procesos = Proceso.objects.all()
    drp =  get_object_or_404(Drp, pk = pk)
    
    return render(request, 'bcp/drp/indice_drp.html', context={'drp':drp})


#**********************
# 6.3 Crea un DRP     *
#**********************
from .forms import Crea_DRP_Enc_Form
@login_required
def Crea_Drp(request):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    
    # Determinacion de Codigo a asignar.

    cod = get_object_or_404(Parametros_G, nombre='CORRELATIVO_DRP')
    codigo = 'DRP-'+str(cod.valor_2) 
    cod.valor_2=cod.valor_2+1
    cod.save()

    if request.method == 'POST':

        form = Crea_DRP_Enc_Form(request.POST)

        if form.is_valid():

            # Crea en registro
            drp=Drp()

            drp.nombre=form.cleaned_data['nombre']
            drp.codigo=codigo

            #Asigna al usuario de sesion como gestor consultor
            usuario_sesion = request.user.pk
            usuario_ges=get_object_or_404(Gestor, user_pk=usuario_sesion)
            print('usuario_gestor', usuario_ges)
            drp.gestor_consultor_drp = usuario_ges

            drp.save()

            return HttpResponseRedirect(reverse('Lista-DRP'))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        form = Crea_DRP_Enc_Form()
        return render(request, 'bcp/drp/crea_drp.html', {'form':form})

#**********************
# 6.4 Borra un DRP    *
#**********************
@login_required
def Borra_Drp(request, pk):
    """ 
    Borra el DRP. Debe estar en estado de Creacion
    """    
    # Borra el DRP     
    drp = get_object_or_404(Drp, pk = pk)

    if not drp.status_t:
        # Borra el DRP 
        drp.delete()

    return HttpResponseRedirect(reverse('Lista-DRP'))

#*************************************
# 6.5 registra Objetivo del  DRP     *
#*************************************
from .forms import Drp_Sec_1_Form
@login_required
def Drp_Sec_1(request, pk):
    """
    Registra Objetivo del DRP
    """
    print('---- Registra Objetivo ----')
    print('pk=',pk)
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))


    drp=get_object_or_404(Drp, pk=pk)
 

    if request.method == 'POST':

        form = Drp_Sec_1_Form(request.POST)

        if form.is_valid():

            # Crea en registro
           
            drp.introduccion=form.cleaned_data['objetivo']
            drp.status_t='C'
            drp.save()

            #return HttpResponseRedirect(reverse('Lista-DRP'))
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        form = Drp_Sec_1_Form(initial={'objetivo':drp.introduccion})
        return render(request, 'bcp/drp/objetivo_drp.html', {'drp':drp, 'form':form})

 

#*************************************
# 6.6 registra Equipo Gestores  DRP  *
#*************************************
from .forms import Drp_Sec_2_Form
@login_required
def Drp_Sec_2(request, pk):
    """
    Registra el equipo de Gestores del DRP
    """
    print('*** Registra equipo DRP ***')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    global selec_Autorizadores, selec_Ejecutores, selec_Gestion_de_Crisis, selec_TI


    drp=get_object_or_404(Drp, pk=pk)

    if request.method == 'POST':

        form = Drp_Sec_2_Form(request.POST or None)

        print (form.is_valid())
        print(form.non_field_errors)
        print(form.errors)
        #print(form)

        if  form.is_valid():

            # Crea en registro
           
            responsable = form.cleaned_data['resp_drp']
            drp.resp_drp = responsable
            respaldo_resp =form.cleaned_data['bck_resp']
            drp.bck_resp_drp = respaldo_resp

            ejecutor=form.cleaned_data['gestor_ejecutor']
            drp.gestor_ejecutor_drp=ejecutor
            respaldo_ejec= form.cleaned_data['bck_ejecutor']
            drp.bck_ejecutor_drp=respaldo_ejec 


            enlace = form.cleaned_data['enlace_c_crisis']
            drp.enlace_c_crisis_drp=enlace 
            respaldo_enl= form.cleaned_data['bck_enlace']
            drp.bck_enlace_drp=respaldo_enl 

            #Actualiza lista de Contactos
            #============================
            print('--- Actualiza lista de contactos ---')
            

            #responsable y respaldo

            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0101')

            if contacto:
                if responsable:
                    contacto0101 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0101')
                    contacto0101.nombre=responsable.user_gestor.first_name+' '+responsable.apellido
                    contacto0101.correo=responsable.user_gestor.email
                    contacto0101.tel_lab=responsable.fono_t
                    contacto0101.cel_lab=responsable.cod_area.codigo+responsable.fono_c
                    contacto0101.save()
                    print('Actualiza contacto responsable=', contacto0101.nombre)
                else:
                    contacto.delete()
                    
            else:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0101'
                    contacto.nombre=responsable.user_gestor.first_name+' '+responsable.apellido
                    contacto.correo=responsable.user_gestor.email
                    contacto.tel_lab=responsable.fono_t
                    contacto.cel_lab=responsable.cod_area.codigo+responsable.fono_c
                    contacto.save()                    
                    drp.contactos_drp.add(contacto)
                    print('Crea contacto responsable=', contacto.nombre)
                    
                    
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0102')

            if contacto:
                if respaldo_resp:
                    contacto0102 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0102')
                    contacto0102.nombre=respaldo_resp.user_gestor.first_name+' '+respaldo_resp.apellido
                    contacto0102.correo=respaldo_resp.user_gestor.email
                    contacto0102.tel_lab=respaldo_resp.fono_t
                    contacto0102.cel_lab=respaldo_resp.cod_area.codigo+respaldo_resp.fono_c
                    contacto0102.save()
                    print('Actualiza resp. responsable=', contacto0102.nombre)

                else:
                    contacto.delete()

            else:
                if respaldo_resp:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0102'
                    contacto.nombre=respaldo_resp.user_gestor.first_name+' '+respaldo_resp.apellido
                    contacto.correo=respaldo_resp.user_gestor.email
                    contacto.tel_lab=respaldo_resp.fono_t
                    contacto.cel_lab=respaldo_resp.cod_area.codigo+respaldo_resp.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea resp. responsable=', contacto.nombre)
                   
            #ejecutor y respaldo
            
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0201')
                
            if contacto:
                if ejecutor:
                    contacto0201 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0201')
                    contacto0201.nombre=ejecutor.user_gestor.first_name+' '+ejecutor.apellido
                    contacto0201.correo=ejecutor.user_gestor.email
                    contacto0201.tel_lab=ejecutor.fono_t
                    contacto0201.cel_lab=ejecutor.cod_area.codigo+ejecutor.fono_c
                    contacto0201.save()
                    #drp.contactos_drp.set(contacto0201)
                    print('Actualiza contacto ejecutor=', contacto0201.nombre)
                else:
                    contacto.delete()

            else:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0201'
                    contacto.nombre=ejecutor.user_gestor.first_name+' '+ejecutor.apellido
                    contacto.correo=ejecutor.user_gestor.email
                    contacto.tel_lab=ejecutor.fono_t
                    contacto.cel_lab=ejecutor.cod_area.codigo+ejecutor.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea contacto ejecutor=', contacto.nombre)
           
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0202')

            if contacto:
                if respaldo_ejec:
                    contacto0202 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0202')
                    contacto0202.nombre=respaldo_ejec.user_gestor.first_name+' '+respaldo_ejec.apellido
                    contacto0202.correo=respaldo_ejec.user_gestor.email
                    contacto0202.tel_lab=respaldo_ejec.fono_t
                    contacto0202.cel_lab=respaldo_ejec.cod_area.codigo+respaldo_ejec.fono_c
                    contacto0202.save()
                    #drp.contactos_drp.set(contacto0202)
                    print('Actualiza respaldo ejecutor=', contacto0202.nombre)
                else:
                    contacto.delete()

            else:
                if respaldo_ejec:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0202'
                    contacto.nombre=respaldo_ejec.user_gestor.first_name+' '+respaldo_ejec.apellido
                    contacto.correo=respaldo_ejec.user_gestor.email
                    contacto.tel_lab=respaldo_ejec.fono_t
                    contacto.cel_lab=respaldo_ejec.cod_area.codigo+respaldo_ejec.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea respaldo ejecutor=', contacto.nombre)
            
            #enlace y respaldo
           
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0301')
                
            if contacto:
                if enlace:
                    contacto0301 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0301')
                    contacto0301.nombre=enlace.user_gestor.first_name+' '+enlace.apellido
                    contacto0301.correo=enlace.user_gestor.email
                    contacto0301.tel_lab=enlace.fono_t
                    contacto0301.cel_lab=enlace.cod_area.codigo+enlace.fono_c
                    contacto0301.save()
                    #drp.contactos_drp.set(contacto0301)
                    print('Actualiza contacto enlace=', contacto0301.nombre)
                else:
                    contacto.delete()

            else:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0301'
                    contacto.nombre=enlace.user_gestor.first_name+' '+enlace.apellido
                    contacto.correo=enlace.user_gestor.email
                    contacto.tel_lab=enlace.fono_t
                    contacto.cel_lab=enlace.cod_area.codigo+enlace.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea contacto enlace=', contacto.nombre)
                        
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0302')

            if contacto:
                if respaldo_enl:
                    contacto0302 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0302')                
                    contacto0302.nombre=respaldo_enl.user_gestor.first_name+' '+respaldo_enl.apellido
                    contacto0302.correo=respaldo_enl.user_gestor.email
                    contacto0302.tel_lab=respaldo_enl.fono_t
                    contacto0302.cel_lab=respaldo_enl.cod_area.codigo+respaldo_enl.fono_c
                    contacto0302.save()
                    print('Actualiza respaldo enlace=', contacto0302.nombre)
                else:
                    contacto.delete()
                    
            else:
                if respaldo_enl:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0302'
                    contacto.nombre=respaldo_enl.user_gestor.first_name+' '+respaldo_enl.apellido
                    contacto.correo=respaldo_enl.user_gestor.email
                    contacto.tel_lab=respaldo_enl.fono_t
                    contacto.cel_lab=respaldo_enl.cod_area.codigo+respaldo_enl.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea respaldo enlace=', contacto.nombre)

            # Cambia status y graba al equipo de Gestores
            drp.status_t='C'
            
            drp.save()

            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print('*** ERROR DE INGRESO ***', form.errors)
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form.errors':form.errors})

    else:

        form = Drp_Sec_2_Form(initial={'resp_drp':drp.resp_drp,
                                       'bck_resp':drp.bck_resp_drp,
                                       'gestor_ejecutor':drp.gestor_ejecutor_drp,
                                       'bck_ejecutor':drp.bck_ejecutor_drp,
                                       'enlace_c_crisis':drp.enlace_c_crisis_drp,
                                       'bck_enlace':drp.bck_enlace_drp})

        return render(request, 'bcp/drp/responsable_drp.html', {'drp':drp, 'form':form})


#*************************************
# 6.7 Definicion Alcance del   DRP   *
#*************************************
from .forms import Drp_Sec_3_Form
# Codigo obsoleto (Borrar)
def Drp_Sec_3(request, pk):
    """
    Define al Alcance del DRP. Este se define por la seleccion de Procesos con 
    Procedimientos de tipo "Automatico".
    """
    global Drp_Sec_3_url_ant

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))


    drp=get_object_or_404(Drp, pk=pk)
    
    p=SubProceso.objects.all().update()
    pp=Procedimientos.objects.all().update()

    if request.method == 'POST':

        form = Drp_Sec_3_Form(request.POST)

        if form.is_valid():

            # Crea en registro
           
            p1=form.cleaned_data['procesos']
            drp.procesos_drp.set(p1)
            drp.status_t='C'
            drp.save()

            return HttpResponseRedirect(Drp_Sec_3_url_ant)

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Drp_Sec_3_url_ant = request.META['HTTP_REFERER']
        print('Drp_Sec_3_url_ant  =', Drp_Sec_3_url_ant)
        p2=drp.procesos_drp.all()

        form = Drp_Sec_3_Form(initial={ 'procesos':set(p2)})
        return render(request, 'bcp/drp/alcance_drp.html', {'drp':drp, 'form':form})


#****************************************************
# 6.7.v2 Definicion del Alcance del DRP (version 2) *
#****************************************************

from django.shortcuts import render, get_object_or_404, redirect
from .models import Drp, SubProceso_V
@login_required
def asigna_procesos_drp(request, pk):
    """ Asigna al DRP los Procesos que seran cubiertos por el DRP (Alcance) 
        Filtra por aquellos que tienen activa_drp=True en su Estrategia Asociada. 
        """
    
    drp = get_object_or_404(Drp, pk=pk)

    if request.method == "POST":
        ids = request.POST.get("procesos_ids", "")
        drp.procesos_drp.clear()
        if ids.strip():
            procesos_seleccionados = SubProceso_V.objects.filter(id__in=ids.split(","))
            drp.procesos_drp.set(procesos_seleccionados)


        return redirect(drp.get_absolute_url())

    procesos_disponibles = SubProceso_V.objects.filter(
        escenarios__estrategias__activa_drp=True
    ).exclude(id__in=drp.procesos_drp.all()).distinct()

    procesos_asignados = drp.procesos_drp.all()

    return render(request, "bcp/drp/alcance_drp.html", {
        "drp": drp,
        "procesos_disponibles": procesos_disponibles,
        "procesos_asignados": procesos_asignados,
    })


#*******************************************
# 6.8 Definicion la Estrategia del   DRP   *
#*******************************************
from .forms import Drp_Sec_4_Form
@login_required
def Drp_Sec_4(request, pk):
    """
    Registra la Estrategia de Recuperacion del del  DRP """

    global Drp_Sec_4_url_ant

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))


    drp=get_object_or_404(Drp, pk=pk)
    
    form=Drp_Sec_4_Form()

    if request.method == 'POST':

        form = Drp_Sec_4_Form(request.POST)

        if form.is_valid():

            # Crea en registro
            drp.tipo_Site=form.cleaned_data['tipo_site']
            drp.disposicion_componentes=form.cleaned_data['tipo_disp']
            drp.desc_estrategia=form.cleaned_data['desc_estrategia']

            drp.status_t='C'
            
            drp.save()

            return HttpResponseRedirect(Drp_Sec_4_url_ant)

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Drp_Sec_4_url_ant = request.META['HTTP_REFERER']

        form = Drp_Sec_4_Form(initial={ 'tipo_site':drp.tipo_Site,
                                       'tipo_disp':drp.disposicion_componentes,
                                       'desc_estrategia':drp.desc_estrategia
                                       
                                       })
        return render(request, 'bcp/drp/estrategia_drp.html', {'drp':drp, 'form':form})


#**************************************
# 6.9 Especificacion Tecnica  del DRP *
#**************************************
@login_required
def asigna_componentes(request, pk):
    """
    Asigna al DRP los Componentes de Hw y Sw. Base del Site. 
    Utiliza Box Script.
    pk: pk del DRP 
    """
    drp = get_object_or_404(Drp, pk=pk)
    #subproceso = proceso.subproceso

    if request.method == "POST":
        print('>>> Entra a POST')
        # Rescata los Datos seleccionados desde el Script
        componentes_ids = request.POST.get("componentes", "").split(",")
        componentes_ids = [int(e) for e in componentes_ids if e.isdigit()]

        #for comp in componentes_ids:
        #    print('>>>> componentes seleccionados a grabar:', comp.nombre)

        if componentes_ids:
            drp.componentes.set(Componentes.objects.filter(id__in=componentes_ids))
        #else:
            #subproceso.escenarios.clear()


        return redirect(drp.get_absolute_url())


    componentes_disponibles = Componentes.objects.exclude(id__in=drp.componentes.values_list('id', flat=True))
    componentes_asignados = drp.componentes.all()
    # url_retorno = request.build_absolute_uri()
    origen=1 # Indica que le origen es la asignacion de Componentes (No la Revision x Comentarios)

    return render(request, 'bcp/drp/asigna_cmp_v2.html', {
        #'form': EscenarioForm(),
        'drp': drp,
        'componentes_disponibles': componentes_disponibles,
        'componentes_asignados': componentes_asignados,
        #'url_retorno':url_retorno
        'origen':origen,
        'drp':drp
    })

#**********************************
# 6.9.1 Lista Componentes del DRP *
#**********************************
@login_required
def Lista_CMP(request, pk_drp, origen):
    """Lista los Componentes de Hw y Sw del DRPs
    
        pk_drp: 
            Si <> 0 Trae el pk del Drp 
            0 si viene de la Configuracion
        origen: 
            0: si viene de la configuracion 
            1: si viene de Asignar el Componente
            2: si viene de Corregir las observaciones
    """

    print('----- Lista CMP----')

    if pk_drp != 0:
        drp=get_object_or_404(Drp, pk=pk_drp)
    else:
        drp=0

    lista_cmp=Componentes.objects.all() 

    #url_comp=Componentes.get_absolute_url
    print('url ant=', url_ant)

    return render(request, 'bcp/drp/lista_cmp.html', context={'lista_cmp':lista_cmp,
                                                              'drp':drp,
                                                              'origen':origen
                                                              })

#************************************
# 6.9.3.1 Crea Componentes en la BD *
#************************************
from .forms import Crea_CMP_Form
@login_required
def Crea_CMP(request):
    """
    Crea un Componente de Infraestructura de Hw o Sw en la Base de Datos.
    """
    print("=== Entra a Crea_CMP ===")
    print("Método:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)
    print('--- CREA CMP ----')

    # Determina el URL al que volver
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    print(">>> next_url:", next_url)

    if request.method == 'POST':
        form = Crea_CMP_Form(request.POST)

        if form.is_valid():

            # Genera el código solo al grabar
            cod = get_object_or_404(Parametros_G, nombre='CORRELATIVO COMPONENTES')
            codigo = f"CMP-{cod.valor_2}"
            cod.valor_2 += 1
            cod.save()

            # Crea en BD
            cmp = Componentes(
                codigo=codigo,
                tipo_act=form.cleaned_data['tipo_act'],
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                identificacion=form.cleaned_data['identificacion'],
                fabricante=form.cleaned_data['fabricante'],
                codigo_inv=form.cleaned_data['codigo_inv']

            )
            cmp.save()

            print('>>> Componente creado, redirigiendo a:', next_url)
            return redirect(next_url)

        else:
            print('>>> Error de formulario:', form.errors)
            return render(
                request,
                'bcp/mensajes/mensajes_error_Form.html',
                {'form': form.errors}
            )

    else:
        form = Crea_CMP_Form()

    return render(request, 'bcp/drp/crea_cmp.html', {
        'form': form,
        'next': next_url
    })

#************************************
# 6.9.3.1 Crea Componentes en la BD *
#************************************
from .forms import Crea_CMP_Form
@login_required
def Modifica_CMP(request, pk):
    """
    Modifica Componente de Infraestructura de Hw o Sw en la Base de Datos.
    pk: pk del Componente
    """
    print("=== Entra a Modifica_CMP ===")
    print("Método:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)

    # Determina el URL al que volver
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    print(">>> next_url:", next_url)

    comp=get_object_or_404(Componentes, pk=pk)

    if request.method == 'POST':
        form = Crea_CMP_Form(request.POST)

        if form.is_valid():

            # Modifica en BD
            comp.tipo_act=form.cleaned_data['tipo_act']
            comp.nombre=form.cleaned_data['nombre']
            comp.descripcion=form.cleaned_data['descripcion']
            comp.identificacion=form.cleaned_data['identificacion']
            comp.fabricante=form.cleaned_data['fabricante']
            comp.codigo_inv=form.cleaned_data['codigo_inv']

            comp.save()

            print('>>> Componente creado, redirigiendo a:', next_url)
            return redirect(next_url)

        else:
            print('>>> Error de formulario:', form.errors)
            return render(
                request,
                'bcp/mensajes/mensajes_error_Form.html',
                {'form': form.errors}
            )

    else:
        form = Crea_CMP_Form(initial={'tipo_act':comp.tipo_act,
                                      'nombre':comp.nombre,
                                      'descripcion':comp.descripcion,
                                      'identificacion':comp.identificacion,
                                      'fabricante':comp.fabricante,
                                      'codigo_inv':comp.codigo_inv})

    return render(request, 'bcp/drp/crea_cmp.html', {
        'form': form,
        'next': next_url
    })


#*************************************
# 6.9.3.2 Borra Componentes de la BD *
#*************************************
@login_required
def Borra_CMP(request, cmp_pk):
     
    # Borra el Componente 
    comp=get_object_or_404(Componentes, pk=cmp_pk)
    comp.delete()

    # Borra la LBC (incluir)
 
    # Dirige la Salida 
    #return HttpResponseRedirect(url_retorno)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)



#****************************
# 6.9.3.3  Lista la LBC DRP *
#****************************

#def Lista_LBC(request, pk, ulr_comp):
@login_required
def Lista_LBC(request, url_retorno):
    """Lista la Linea Base de Configuracion de un Componente
    pk      : Pk del Componente
    pk_drp  : pk del DRP """

    print('----- Lista LBC----')
    comp=get_object_or_404(Componentes, pk=pk)
    drp=get_object_or_404(Drp, pk=pk_drp)
    lista_lbc=comp.lbc
    print('comp=',comp)
    print('Lista_lbc=', lista_lbc)


    return render(request, 'bcp/drp/lista_lbc.html', context={'comp':comp,
                                                              'lista_lbc':lista_lbc,
                                                              'drp':drp,
                                                              'url_retorno':url_retorno})


#***************************
# 6.9.3.4 Crea  la LBC     *
#***************************
from .forms import Crea_LBC_Form
@login_required
def Crea_LBC(request, pk):
    """Crea una Parametro de Linea Base de Configuracion para un
    Componente de Infraestructura de Hw o Sw.
    pk        :pk del Componente
    """
    print("=== Entra a Crea PARAMETRO de LBC ===")
    print("Método:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)
    print('--- CREA CMP ----')

    # Determina el URL al que volver
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    print(">>> next_url:", next_url)
      
    cmp = get_object_or_404(Componentes, pk=pk)
     
    if request.method == 'POST':

        form = Crea_LBC_Form(request.POST)

        if form.is_valid():

            # Determinacion de Codigo a asignar.
            cod = get_object_or_404(Parametros_G, nombre = 'CORRELATIVO LBC')
            codigo = cmp.codigo+'-'+str(cod.valor_2) 
            cod.valor_2=cod.valor_2+1
            cod.save()

            # Crea en BD 
            #cmp.lbc=LBC()
            p=LBC()
            
            p.codigo=codigo
            p.nombre = form.cleaned_data['nombre']
            p.descripcion = form.cleaned_data['descripcion']
            p.metodo_acceso = form.cleaned_data['metodo_acceso']
            p.valor = form.cleaned_data['valor']
            p.save()

            print('p=',p)

            # Actualiza el Componente
            cmp.lbc.add(p)
            cmp.save()
           
            # Retorna a la Lista de Componentes
            #return HttpResponseRedirect(Crea_LBC_url_ant)
            #return HttpResponseRedirect(reverse(cmp.get_absolute_url))
            #return HttpResponseRedirect(reverse('Lista-CMP', args=[pk, 1]))
            print('>>> Paramero creado, redirigiendo a:', next_url)
            return redirect(next_url)


        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Crea_LBC_url_ant=request.META['HTTP_REFERER']

        form = Crea_LBC_Form()
        return render(request, 'bcp/drp/crea_lbc.html', {'form':form, 'cmp':cmp})  


@login_required
def Modifica_LBC(request, pk, pk_cmp):
    """
    Modifica un Parametro de LBC del Componente de Infraestructura de Hw o Sw en la Base de Datos.
    pk          : pk del Parametro del LBC
    pk_cmp      : pk del Componente asociado.
    """
    print("=== Entra a Modifica_LBC ===")
    print("Método:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)

    # Determina el URL al que volver
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    print(">>> next_url:", next_url)

    lbc=get_object_or_404(LBC, pk=pk)
    cmp=get_object_or_404(Componentes, pk=pk_cmp)

    if request.method == 'POST':
        form = Crea_LBC_Form(request.POST)

        if form.is_valid():

            # Modifica en BD
            lbc.nombre=form.cleaned_data['nombre']
            lbc.descripcion=form.cleaned_data['descripcion']
            lbc.metodo_acceso=form.cleaned_data['metodo_acceso']
            lbc.valor=form.cleaned_data['valor']

            lbc.save()

            print('>>> Parametro de LBC modificado, redirigiendo a:', next_url)
            return redirect(next_url)

        else:
            print('>>> Error de formulario:', form.errors)
            return render(
                request,
                'bcp/mensajes/mensajes_error_Form.html',
                {'form': form.errors}
            )

    else:
        form = Crea_LBC_Form(initial={'nombre':lbc.nombre,
                                      'descripcion':lbc.descripcion,
                                      'metodo_acceso':lbc.metodo_acceso,
                                      'valor':lbc.valor})

    return render(request, 'bcp/drp/crea_lbc.html', {'form': form, 'cmp':cmp, 'next': next_url })

#***************************
# 6.9.3.5 Borra la LBC     *
#***************************
@login_required
def Borra_LBC(request, pk):
    """ 
    Borra un registro de Linea Base de Configuracion asociado a un Componente
    
    pk: Pk del Parametro de Configuracion """

    url_ant=request.META['HTTP_REFERER']
    lbc=get_object_or_404(LBC, pk=pk)
    lbc.delete()

    # Dirige la Salida 
    #return HttpResponseRedirect(url_retorno)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

    #return HttpResponseRedirect(url_ant)


#*******************************
# 6.10 Servicios Criticos DRP  *
#*******************************

#****************************************
# 6.10.1 Lista  Servicios Criticos DRP  *
#****************************************
@login_required
def Lista_Serv_Crtc(request, pk):
    
    """Lista los Servicios Criticos asociados al DRPs"""

    print('----- Lista Servicios Criticos DRP ----')

    drp=get_object_or_404(Drp, pk=pk)
    lista_sc=drp.servicios_drp 

   
    return render(request, 'bcp/drp/lista_sc.html',
                  context={'lista_sc':lista_sc, 'drp':drp})


#**************************************
# 6.10.2 Crea Servicios Criticos DRP  *
#**************************************

#@permission_required('Catalogo.can_mark_returned')
@login_required
#def cr_drp_P5(request, pk, acc):
def cr_drp_P5(request, pk):
    """
    Ingresa Servicios Criticos para el DRP
    """
    print('------ Crea Servicio Critico DRP -------')
    #print('Accion=',acc)
    global cr_drp_P5_url_ant

    drp = get_object_or_404(Drp, pk = pk)
  
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P5_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            servicio = Servicios_PC()

            servicio.pk_padre = pk
            nombre = form.cleaned_data['nombre']
            servicio.nombre = nombre
            servicio.objetivo = form.cleaned_data['objetivo']
            contacto_drp= form.cleaned_data['contacto']
            servicio.contacto = contacto_drp
            contacto_bck_drp = form.cleaned_data['contacto_bck']
            servicio.contacto_bck = contacto_bck_drp

            #Crea contactos en Nomina de Contactos
            if contacto_drp:
                contacto=Contactos_PC()
                contacto.nombre=contacto_drp + ' (' + nombre + ')'
                contacto.save()
                drp.contactos_drp.add(contacto)

            if contacto_bck_drp:
                contacto2=Contactos_PC()
                contacto2.nombre=contacto_bck_drp + ' (' + nombre + ')'
                contacto2.save()
                drp.contactos_drp.add(contacto2)  
            
            # en caso de ser una revision cambia el status a autorizar.
            #if acc == 'revisa':
            #    drp.status_6 = 'a'

            #Adiciona el Servicio al Procedimiento
            servicio.save()
            drp.servicios_drp.add(servicio)
            drp.save()

            

            #Marca la seccion como completa
            #num = proced.sec_servicios
            #num = num+1
            #drp.sec_servicios = num
            #proced.save()
            
                     
            # Dirige la Salida 
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
            #return HttpResponseRedirect(cr_drp_P5_url_ant)
            #return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))
            #return HttpResponseRedirect(drp.get_absolute_url)

        
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            

    # If this is a GET (or any other method) create the default form.
    else:

        form=CreaProc_P5_Form()

        cr_drp_P5_url_ant=request.META['HTTP_REFERER']
        print(url_ant)
        return render(request, 'bcp/proced_cont/prcd_crea_serP5.html', {'form': form, 
                                                                        'servicios':drp.servicios_drp})    



#@permission_required('Catalogo.can_mark_returned')
@login_required
#def cr_drp_P5(request, pk, acc):
def md_drp_P5(request, pk):
    """
    Modifica  Servicio Criticos para el DRP
    pk:pk del Servicio
    """
    print('>>>>> Modifica Servicio Critico DRP -------')
    #print('Accion=',acc)
    global cr_drp_P5_url_ant

    servicio = get_object_or_404(Servicios_PC, pk = pk)
    contacto_actual=servicio.contacto
    bck_actual=servicio.contacto_bck
    nombre_actual=servicio.nombre

    print('---- Servicio : ', nombre_actual)
    print('---- contacto_actual :', contacto_actual)
    print('---- bck actual', bck_actual)

    #drp = get_object_or_404(Drp, pk = servicio.pk_padre)
    #print("DRP : ", drp)


    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P5_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso

            servicio.pk_padre = pk
            nombre = form.cleaned_data['nombre']
            servicio.nombre = nombre
            servicio.objetivo = form.cleaned_data['objetivo']
            new_contacto = form.cleaned_data['contacto']
            servicio.contacto = new_contacto
            new_bck = form.cleaned_data['contacto_bck']
            servicio.contacto_bck = new_bck

            #Modifica contactos en Nomina de Contactos
            if contacto_actual != new_contacto:  # Cambio contacto

                # Se crea nuevo contacto
                contacto_new=Contactos_PC()
                contacto_new.nombre=new_contacto + ' (' + nombre + ')'
                contacto_new.save()
                print('---- Se crea nuevo contacto :', contacto_new.nombre)

                # Se elimina contacto actual
                #llave=contacto_actual+' ('+nombre_actual+')'
                #print('---- Se elimina contacto antiguo ', llave)
                #contacto_old=Contactos_PC.objects.filter(nombre==llave).all()
                #if contacto_old:
                #    contacto_old.delete()
                #    print('---- Se elimino contacto antiguo ')


            #Modifica respaldo contactos en Nomina de Contactos
            if bck_actual  != new_bck :  # Cambio respaldo contacto

                # Se crea nuevo bck contacto
                contacto_new=Contactos_PC()
                contacto_new.nombre=new_bck + ' (' + nombre + ')'
                contacto_new.save()
                print('---- Se crea nuevo bck contacto :', new_bck.nombre)

                # Se elimina contacto actual
                #contacto_old=get_object_or_404(Contactos_PC, nombre=bck_actual)
                #contacto_old.delete()
                #print('---- Se elimino bck contacto antiguo ')

            
            # en caso de ser una revision cambia el status a autorizar.
            #if acc == 'revisa':
            #    drp.status_6 = 'a'

            #Adiciona el Servicio al Procedimiento
            servicio.save()
            #drp.save()

            

            #Marca la seccion como completa
            #num = proced.sec_servicios
            #num = num+1
            #drp.sec_servicios = num
            #proced.save()
            
                     
            # Dirige la Salida 
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
            #return HttpResponseRedirect(cr_drp_P5_url_ant)
            #return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))
            #return HttpResponseRedirect(drp.get_absolute_url)

        
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            

    # If this is a GET (or any other method) create the default form.
    else:

        form=CreaProc_P5_Form(initial={'nombre':servicio.nombre,
                                       'objetivo':servicio.objetivo,
                                       'contacto':servicio.contacto,
                                       'contacto_bck':servicio.contacto_bck
                                       })

        #cr_drp_P5_url_ant=request.META['HTTP_REFERER']
        #print(url_ant)
        return render(request, 'bcp/proced_cont/prcd_crea_serP5.html', {'form': form,
                                                                        'servicios':servicio})    


#***************************************
# 6.10.2 Borra Servicios Criticos DRP  *
#***************************************
    
#@permission_required('Catalogo.can_mark_returned')
@login_required
#def br_drp_P5(request, pk, acc):
def br_drp_P5(request, pk):

    """
    Borra Servicios Criticos para el DRP
    """
    print('>>>>> Borra Servicio Critico DRP --------')
    
    servicio_drp = get_object_or_404(Servicios_PC, pk = pk)
    drp = get_object_or_404(Drp, pk = servicio_drp.pk_padre)

    print(servicio_drp)
    #drp = get_object_or_404(Procedimientos, pk = servicio_drp.pk_padre) 

    #Actualiza cantidad de SSCC    
    #num = proced.sec_servicios
    #num = num-1
    #proced.sec_servicios = num
    #proced.save()
    #if acc == 'revisa':
    #    drp.status_6 = 'a'
    #

    #Borra Servicio                
    servicio_drp.delete()
    drp.save()

    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


from .forms import CreaProc_P6_Form

#*******************************
# 6.11 Procedimiento del  DRP  *
#*******************************
#**************************************************
# 6.11.1 Lista Pasos del  Procedimiento del  DRP  *
#**************************************************
@login_required
def Lista_Pasos_Drp(request, pk):
    """Lista los Componentes de Hw y Sw del DRPs"""

    print('----- Lista Pasos del Procedimiento del  DRP ----')
    drp=get_object_or_404(Drp, pk=pk)
    lista_pasos=drp.pasos_drp 

   
    return render(request, 'bcp/drp/lista_pasos.html', context={'lista_pasos':lista_pasos, 'drp':drp})

#*******************************
# 6.11 Procedimiento del  DRP  *
#*******************************
#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_drp_P7(request, pk):
    """
    Ingresa Pasos del DRP
    """
    global url_ant

    drp = get_object_or_404(Drp, pk = pk)

   
    #Asigna el formulario creado en Forrms
    form=CreaProc_P7_Form()

    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P7_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            paso = Pasos_PC()
            
            paso.pk_padre = pk
            paso.nro_paso = form.cleaned_data['nro_paso']
            paso.descripcion = form.cleaned_data['descripcion']
            paso.ejecutor = form.cleaned_data['ejecutor']
            paso.tiempo_esp = form.cleaned_data['tiempo_esp']
            

            paso.save()
            drp.pasos_drp.add(paso)

            #Marca la seccion como completa
            #num = proced.sec_pasos
            #num = num+1
            #proced.sec_pasos = num
            #proced.save()
            
            # redirect to a new URL:
            #return HttpResponseRedirect(url_ant)
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))            
            
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            

    # If this is a GET (or any other method) create the default form.
    else:

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'bcp/proced_cont/prcd_crea_pasP7.html', {'form': form, 'pasos':drp.pasos_drp})
    

#@permission_required('Catalogo.can_mark_returned')
@login_required
def br_drp_P7(request, pk):
    """
    Borra Pasos del DRP
    """
        
    url_ant=request.META['HTTP_REFERER']
    print('url ant en borra P7:', url_ant)
    
    paso_pc = get_object_or_404(Pasos_PC, pk = pk)
    #proced = get_object_or_404(Procedimientos, pk = paso_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_pasos
    #num = num-1
    #proced.sec_pasos = num
    #proced.save()
   
    paso_pc.delete()

    return HttpResponseRedirect(url_ant)



#************************************
# 6.12 Datos de Contacto  del  DRP  *
#************************************
#******************************************************
# 6.12.1 Lista Contactos del  Procedimiento del  DRP  *
#******************************************************
@login_required
def Lista_Contactos_DRP(request, pk):
    """Lista de Contactos del DRPs"""

    print('----- Lista de Contactos del  DRP ----')
    drp=get_object_or_404(Drp, pk=pk)
    lista_contactos=drp.contactos_drp 

   
    return render(request, 'bcp/drp/lista_contactos.html', context={'lista_contactos':lista_contactos, 'drp':drp})


#@permission_required('Catalogo.can_mark_returned')
@login_required
def cr_drp_P6(request, pk):
    """
    Crea Contactos Criticos para el DRP
    """
    global url_ant

    drp = get_object_or_404(Drp, pk = pk)

   
    #Asigna el formulario creado en Forrms
    form=CreaProc_P6_Form()

    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P6_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            contacto = Contactos_PC()
            
            contacto.pk_padre = pk
            contacto.nombre = form.cleaned_data['nombre']
            contacto.correo = form.cleaned_data['correo']
            contacto.tel_lab = form.cleaned_data['tel_lab']
            contacto.cel_lab = form.cleaned_data['cel_lab']
            
            #Agrega Contacto al Procedimiento
            contacto.save()
            drp.contactos_drp.add(contacto)

            #Marca la seccion como completa
            #num = proced.sec_contactos
            #num = num+1
            #proced.sec_contactos = num
            #proced.save()

            return HttpResponseRedirect(url_ant)
            
            #proced.servicios_pc.save()
        
        else:
            
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})            
                     
        

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        return render(request, 'bcp/proced_cont/prcd_crea_conP6.html', {'form': form, 'contactos':drp.contactos_drp})
    

#@permission_required('Catalogo.can_mark_returned')
@login_required
def md_drp_P6(request, pk):
    """
    Modifica Contactos Criticos para el PC
    """
    global url_ant

    contacto = get_object_or_404(Contactos_PC, pk = pk)
    #drp=get_object_or_404(Drp, pk=contacto.pk_padre)

   
    #Asigna el formulario creado en Forrms
    form=CreaProc_P6_Form()
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_P6_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            
            contacto.nombre = form.cleaned_data['nombre']
            contacto.correo = form.cleaned_data['correo']
            contacto.tel_lab = form.cleaned_data['tel_lab']
            contacto.cel_lab = form.cleaned_data['cel_lab']
            
            #Actualiza 
            contacto.save()
            
            #Marca la seccion como completa
            #num = proced.sec_contactos
            #num = num+1
            #proced.sec_contactos = num
            #proced.save()

            return HttpResponseRedirect(url_ant)
            
            #proced.servicios_pc.save()
        
        else:
            
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})            
                     
        

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        form=CreaProc_P6_Form(initial={'nombre':contacto.nombre,
                                       'correo':contacto.correo,
                                       'tel_lab':contacto.tel_lab,
                                       'cel_lab':contacto.cel_lab})
        
        return render(request, 'bcp/drp/drp_mod_conP6.html', {'form': form })
    


#@permission_required('Catalogo.can_mark_returned')
@login_required
def br_drp_P6(request, pk):
    """
    Borra Contactos para el DRP
    """
    
    url_ant=request.META['HTTP_REFERER']
    
    contacto_pc = get_object_or_404(Contactos_PC, pk = pk)
    #proced = get_object_or_404(Procedimientos, pk = contacto_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_contactos
    #num = num-1
    #proced.sec_contactos = num
    #proced.save()
   
    contacto_pc.delete()

    return HttpResponseRedirect(url_ant)
    
from .forms import CreaProc_P7_Form


#*********************************************************
# 6.13  Autorizaciones  del DRP                          *
#*********************************************************

from django.views.decorators.cache import never_cache

@never_cache
@login_required
def Env_Aut_DRP(request, pk, sec):
    """
    Envia la Seccion 'sec' del DRP  a Autorizacion 
    (Cambia el status del Procedimientoa a "a": En autorizacion A)
    """
    print('------- Envia Autorizacion DRP ----------')
    print('Pk=', pk, '-', 'sec=', sec)

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    drp = get_object_or_404(Drp, pk = pk)

    if sec == 1:
        drp.status_1 = 'a'
    elif sec == 2:
        drp.status_2 = 'a'
    elif sec == 3:
        drp.status_3 = 'a'
    elif sec == 4:
        drp.status_4 = 'a'
    elif sec == 5:
        drp.status_5 = 'a'
    elif sec == 6:
        drp.status_6 = 'a'
    elif sec == 7:
        drp.status_7 = 'a'
    elif sec == 8:
        drp.status_A = 'a'

    drp.status_t='a'
    drp.save()
    
    # redirect to a new URL:
    return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)])) 

from .forms import AutorizaRaciForm
import datetime

# ************************************************
# *******  Autorizaciones del DRP ****************
# ************************************************

# inhibe el boton de vuelta atras desde el indice 
from django.views.decorators.cache import never_cache, cache_control
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Aut_Drp(request, pk, sec):
    """
    Autorizacion/Observacion  del Jefe de Operacion a la seccion (sec) del DRP 
    """
    print('------- Autoriza Seccion: ', sec )
    print('Pk=', pk )

    # Evita reingreso al formulario desde sesión
    #if request.session.get('form_enviado'):
    #    print('---> El formulario YA fue enviado' )
    #    del request.session['form_enviado']
    #    #return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))
    #    return HttpResponseRedirect(reverse('error-sesion-mgm', args=[4000] ))
    #else:
    #    print('---> El Formulario NO ha sido enviado')


    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
        
    #proceso= get_object_or_404(Proceso, pk = proced.pk_padre)

    if sec == 3:
        procesos_asig = drp.procesos_drp
        procesos_disp = SubProceso.objects.all()

        for p in procesos_asig.all():
            print(p.path)

    if sec == 5:
        compo_asig = drp.componentes
        compo_disp = Componentes.objects.all()

    if sec == 6:
        servicios_asig = drp.servicios_drp
        servicios_disp = Servicios_PC.objects.all()

    elif sec == 8:
        contactos = drp.contactos_drp
    elif sec == 7:
        pasos = drp.pasos_drp


    form = AutorizaRaciForm() #Utiliza el Formulario para la autorizacion de Procesos
    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)

  
    if request.method=='POST':

        form = AutorizaRaciForm(request.POST)
        
        if form.is_valid():
                     
            #Actualiza los status
            #====================

            aprobado=form.cleaned_data['aprobacion']
            # notifica=form.cleaned_data['notifica']

                            
            if aprobado:
                # Si es Aprobado cambia a status "r"

                if sec == 1:
                    drp.status_1='r'
                    comentario="Definicion de Objetivo DRP aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable "
                    seccion="D1"


                if sec == 2:
                    drp.status_2='r'
                    comentario="Asignacion de Roles aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D2"
                    
                if sec == 3:
                    drp.status_3='r'
                    comentario="Especificacion de Alcance aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D3"

                if sec == 4:
                    drp.status_4='r'
                    comentario="Especificacion de Estrategia aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D4"

                if sec == 5:
                    drp.status_5='r'
                    comentario="Especificacion Tecnica aprobada por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D5"

                if sec == 6:
                    drp.status_6='r'
                    comentario="Especificacion de Servicios Criticos aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D6"

                if sec == 7:
                    drp.status_7='r'
                    comentario="Especificacion del Procedimiento aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D7"

                if sec == 8:
                    drp.status_A='r'
                    comentario="Especificacion de Contactos aprobado por Jefe Operativo del DRP. En Autorizacion por Gestor Responsable"
                    seccion="D8"

                # Crea Log de aprobacion de Autorizador
                log=Log_Revision()
                log.fecha = datetime.date.today()
                log.drp= drp
                log.gestor_aut=usr_aut
                log.seccion=seccion
                log.campo="Autorizado por:"+aut
                log.comentario=comentario
                log.resuelto=True
                log.save()

                #Prepara mensaje x correo
                #========================
                #nombre=proced.resp_proceso.user_gestor.last_name
                #email = proc_rev.subproceso.gestor_R.user_gestor.email
                #accion='dar visto bueno o requerir cambios para el '
                    
            else:
                #Si es Rechazado cambia a status "x"
                #=========


                if sec == 1:
                    drp.status_1='x'
                    seccion="D1"

                if sec == 2:
                    drp.status_2='x'
                    seccion="D2"

                if sec == 3:
                    drp.status_3='x'
                    seccion="D3"
                    
                if sec == 4:
                    drp.status_4='x'
                    seccion="D4"
                    
                if sec == 5:
                    drp.status_5='x'
                    seccion="D5"
                    
                if sec == 6:
                    drp.status_6='x'
                    seccion="D6"
                    
                if sec == 7:
                    drp.status_7='x'
                    seccion="D7"
                    
                if sec == 8:
                    drp.status_A='x'
                    seccion="D7"

                # Crea Log de aprobacion de Autorizador
                log=Log_Revision()
                log.fecha = datetime.date.today()
                log.drp= drp
                log.gestor_aut=usr_aut
                log.seccion=seccion
                log.campo="Observado por:"+aut
                log.comentario="Favor considerar observaciones adjuntas (abajo)"
                log.resuelto=True
                   
                #email = proc_rev.subproceso.gestor_C.user_gestor.email
                #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
           
            #Graba en Base de Datos
            log.save()                
            drp.save()

            # Marca la sesión para prevenir reingreso
            #request.session['form_enviado'] = True

                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )

        if sec == 1:    # 2. Objetivo 

            # Selecciona Comentarios sobre Objetivo
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D1":
                    comentarios.append(com)


            return render(request, 'bcp/drp/drp_s1_auth.html', {'form': form,
                                                                'drp':drp,
                                                                'comentarios':comentarios})
        
        if sec == 2:    # 1. Organizacion

            # Selecciona Comentarios sobre Organizacion
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D2":
                    comentarios.append(com)
                            
            return render(request, 'bcp/drp/drp_s2_auth.html', {'form': form, 
                                                                'drp':drp,
                                                                'comentarios':comentarios})
        
        if sec == 3:    # 3. Alcance 

            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D3":
                    comentarios.append(com)

            # Determina los Procesos Asignados y Disponibles
            procesos_disp = SubProceso_V.objects.filter(
            escenarios__estrategias__activa_drp=True
            ).exclude(id__in=drp.procesos_drp.all()).distinct()

            procesos_asig = drp.procesos_drp.all()


            return render(request, 'bcp/drp/drp_s3_auth.html', {'form': form,
                                                                'drp':drp,
                                                                'procesos_disp':procesos_disp,
                                                                'procesos_asig':procesos_asig,
                                                                'comentarios':comentarios})
        
        if sec == 4:    # 4. Estrategia de Recuperacion 

            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D4":
                    comentarios.append(com)


            return render(request, 'bcp/drp/drp_s4_auth.html', {'form': form,'drp':drp,
                                                                'comentarios':comentarios})
        
        if sec == 5:    # 5. Especificacion Tecnica del Site de Contingencias 

            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D5":
                    comentarios.append(com)

            # Determina los Componentes Disponibles y Asignados
            componentes_disp = Componentes.objects.all( ).exclude(id__in=drp.componentes.all()).distinct()
            componentes_asig = drp.componentes.all()

            return render(request, 'bcp/drp/drp_s5_auth.html',  {'form': form, 'drp':drp,
                                                                 'componentes_asig':componentes_asig,
                                                                 'componentes_disp':componentes_disp,
                                                                 'comentarios':comentarios})
        
        if sec == 6:   # 6. Servicios Criticos 
            print('>>>>> Autorizacion Servicios Criticos')
            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D6":
                    comentarios.append(com)
            print('---- Comentarios :', comentarios)

            # Determina Servicios Criticos declarados
            servicios=drp.servicios_drp

            return render(request, 'bcp/drp/drp_s6_auth.html',   {'form': form, 'drp':drp,
                                                                  'servicios':servicios,
                                                                  'comentarios':comentarios
                                                                  })
        
        if sec == 7:  


            return render(request, 'bcp/proced_cont/proced_auth.html',
                        {'form': form, 'proceso':proceso, 'proced':proced, 'servicios':servicios,
                        'contactos':contactos, 'pasos':pasos})
        if sec == 8:                            
            return render(request, 'bcp/proced_cont/proced_auth.html',
                        {'form': form, 'proceso':proceso, 'proced':proced, 'servicios':servicios,
                        'contactos':contactos, 'pasos':pasos})
        

# -------------------------------------------------------------------------

from django.views.decorators.cache import never_cache

@never_cache
@login_required
def Aut_Drp_V(request, pk, sec):
    """
    Autorizacion/Observacion  del Responsable DRP a la seccion (sec) del DRP 
    """
    print('------- Autoriza Seccion: ', sec )
    print('Pk=', pk )

    # Evita reingreso al formulario desde sesión
    if request.session.get('form_enviado'):
        print('---> El formulario YA fue enviado' )
        del request.session['form_enviado']
        #return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[4000] ))
    else:
        print('---> El Formulario NO ha sido enviado')


    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
        
    #proceso= get_object_or_404(Proceso, pk = proced.pk_padre)

    if sec == 3:
        procesos_asig = drp.procesos_drp
        procesos_disp = SubProceso.objects.all()
        for p in procesos_asig.all():
            print(p.path)

    if sec == 5:
        compo_asig = drp.componentes
        compo_disp = Componentes.objects.all()

    if sec == 6:
        servicios_asig = drp.servicios_drp
        servicios_disp = Servicios_PC.objects.all()

    elif sec == 8:
        contactos = drp.contactos_drp
    elif sec == 7:
        pasos = drp.pasos_drp


    form = AutorizaRaciForm() #Utiliza el Formulario para la autorizacion de Procesos
    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name
    print('usuario aprobador = usuario sesion =', usr_aut)

  
    if request.method=='POST':

        form = AutorizaRaciForm(request.POST)
        
        if form.is_valid():
                     
            #Actualiza los status
            #====================

            aprobado=form.cleaned_data['aprobacion']
            # notifica=form.cleaned_data['notifica']

            # Marca la sesión para prevenir reingreso
            request.session['form_enviado'] = True


            if aprobado:
                # Aprobado

                if sec == 1:
                    drp.status_1='R'
                    comentario="Especificacion del Objetivo del DRP aprobado por Responsable del DRP."
                    seccion="D1"


                if sec == 2:
                    drp.status_2='R'
                    comentario="Asignacion de Roles aprobado por Responsable del DRP."
                    seccion="D2"
                    
                if sec == 3:
                    drp.status_3='R'
                    comentario="Especificacion del Alcance del DRP aprobado por Responsable del DRP."
                    seccion="D3"

                if sec == 4:
                    drp.status_4='R'
                    comentario="Estrategia del DRP aprobada por Responsable del DRP."
                    seccion="D4"

                if sec == 5:
                    drp.status_5='R'
                    comentario="Especificacion Tecnica aprobada por Responsable del DRP."
                    seccion="D5"

                if sec == 6:
                    drp.status_6='R'
                    comentario="Especificacion del Servicios Criticos aprobado por Responsable del DRP."
                    seccion="D6"

                if sec == 7:
                    drp.status_7='R'
                    comentario="Procedimiento de Recuperacion aprobado por Responsable del DRP."
                    seccion="D7"

                if sec == 8:
                    drp.status_A='R'
                    comentario="Especificacion del Contactos aprobado por Responsable del DRP."
                    seccion="D1"

                # Crea Log de aprobacion de Autorizador
                log=Log_Revision()
                log.fecha = datetime.date.today()
                log.drp= drp
                log.gestor_aut=usr_aut
                log.seccion=seccion
                log.campo="Autorizado por:"+aut
                log.comentario=comentario
                log.resuelto=True
                log.save()

                #Prepara mensaje x correo
                #========================
                #nombre=proced.resp_proceso.user_gestor.last_name
                #email = proc_rev.subproceso.gestor_R.user_gestor.email
                #accion='dar visto bueno o requerir cambios para el '
                    
            else:
                #Rechazado
                #=========


                if sec == 1:
                    drp.status_1='x'
                    seccion="D1"

                if sec == 2:
                    drp.status_2='x'
                    seccion="D2"

                if sec == 3:
                    drp.status_3='x'
                    seccion="D3"

                if sec == 4:
                    drp.status_4='x'
                    seccion="D4"

                if sec == 5:
                    drp.status_5='x'
                    seccion="D5"

                if sec == 6:
                    drp.status_6='x'
                    seccion="D6"

                if sec == 7:
                    drp.status_7='x'
                    seccion="D7"

                if sec == 8:
                    drp.status_A='x'
                    seccion="DA"


                # Crea Log de aprobacion de Autorizador
                log=Log_Revision()
                log.fecha = datetime.date.today()
                log.drp= drp
                log.gestor_aut=usr_aut
                log.seccion=seccion
                log.campo="Observado por:"+aut
                log.comentario="Observado por Gestor Responsable del DRP"
                log.resuelto=True
                   
                #email = proc_rev.subproceso.gestor_C.user_gestor.email
                #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
           
            #Graba en Base de Datos
            log.save()                
            drp.save()
            
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )

        if sec == 1:    # 2. Objetivo  

            # Selecciona Comentarios sobre Escenarios
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D1":
                    comentarios.append(com)
                         
            return render(request, 'bcp/drp/drp_s1_auth.html', {'form': form, 
                                                                'drp':drp,
                                                                'comentarios':comentarios})
        
        if sec == 2:    # 1. Organizacion

            # Selecciona Comentarios sobre Organizacion
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D2":
                    comentarios.append(com)
                            
            return render(request, 'bcp/drp/drp_s2_auth.html', {'form': form, 
                                                                'drp':drp,
                                                                'comentarios':comentarios})
        
        if sec == 3:    # 3. Alcance 

            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D3":
                    comentarios.append(com)

            # Determina los Procesos Asignados y Disponibles
            procesos_disp = SubProceso_V.objects.filter(
            escenarios__estrategias__activa_drp=True
            ).exclude(id__in=drp.procesos_drp.all()).distinct()

            procesos_asig = drp.procesos_drp.all()
                          
            return render(request, 'bcp/drp/drp_s3_auth.html', {'form': form,
                                                                'drp':drp,
                                                                'procesos_disp':procesos_disp,
                                                                'procesos_asig':procesos_asig,
                                                                'comentarios':comentarios})
        
        if sec == 4:    # 4. Estrategia de Recuperacion

            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D4":
                    comentarios.append(com)

            return render(request, 'bcp/drp/drp_s4_auth.html', {'form': form, 'drp':drp,
                                                                'comentarios':comentarios})
        
        if sec == 5:    # 5. Especificacion Tecnica del Site de Contingencias 

            # Selecciona Comentarios 
            comentarios_drp=Log_Revision.objects.filter(drp=drp)
            comentarios=[]
            for com in comentarios_drp:
                if com.seccion == "D5":
                    comentarios.append(com)

            # Determina los Componentes Disponibles y Asignados
            componentes_disp = Componentes.objects.all( ).exclude(id__in=drp.componentes.all()).distinct()
            componentes_asig = drp.componentes.all()
                          
            return render(request, 'bcp/drp/drp_s5_auth.html',  {'form': form, 'drp':drp,
                                                                 'componentes_asig':componentes_asig,
                                                                 'componentes_disp':componentes_disp,
                                                                 'comentarios':comentarios})
        
        if sec == 6:   # 6. Servicios Criticos                         
            return render(request, 'bcp/drp/drp_s6_auth.html',   {'form': form, 'drp':drp,
                                                                  'servicios_asig':servicios_asig,
                                                                  'servicios_disp':servicios_disp
                                                                  })
        
        if sec == 7:                            
            return render(request, 'bcp/proced_cont/proced_auth.html',
                        {'form': form, 'proceso':proceso, 'proced':proced, 'servicios':servicios,
                        'contactos':contactos, 'pasos':pasos})
        if sec == 8:                            
            return render(request, 'bcp/proced_cont/proced_auth.html',
                        {'form': form, 'proceso':proceso, 'proced':proced, 'servicios':servicios,
                        'contactos':contactos, 'pasos':pasos})
        

# -------------------------------------------------------------------------

# ************************* Codigo obsoleto **********************************
from .forms import Autoriza_obs_Proced_C_Form
def aut_obs_proced(request, item, pk, valor):
    """
    Registra observaciones por item a la
    Autorizacion de Procedimientos
    """

    global  url_ant_obs_aut

    print('item pk :', pk)
    print('item nro:', item)
    print('item nro 2:', valor)
    
    proced = get_object_or_404(Procedimientos, pk = pk)
        
    aut=LogAut()
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    print('usuario de sesion',aut.gestor_aprobador)

     
    aut.cod_proceso=proced.codigo
    aut.item=item
    

    if request.method=='POST':

        form = Autoriza_obs_Proced_C_Form(request.POST)
        
        print('FORMATO VALID0?',form.is_valid())
        
        if form.is_valid():
            
            #Registra autorizacion en log
                                
            aut.fecha=datetime.date.today()
            aut.p_status=proced.status+'P'
            aut.observacion=form.cleaned_data['comentario']
            #aut.Aprobado=form.cleaned_data['aprobacion']
            
            #notifica=form.cleaned_data['notifica']
            #aprobado=form.cleaned_data['aprobacion']
            
            #---
                            
           
            #Graba en Base de Datos                
            aut.save()
            proced.log_auth.add(aut)      
            proced.save()
            
                
            # redirect to a new URL:
            return HttpResponseRedirect(url_ant_obs_aut)
        
        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
    
        url_ant_obs_aut =request.META['HTTP_REFERER']
        form= Autoriza_obs_Proced_C_Form()
        
        return render(request, 'bcp/proced_cont/proced_obs_auth.html', {'form': form, 'proced':proced, 'item':item, 'valor':valor})



#*********************************************************
# 6.14  Revision de Observaciones  del DRP               *
#*********************************************************

#*********************************************************
# 6.14.1   Revision de Responsables del DRP              *
#*********************************************************

from django.views.decorators.cache import never_cache
@never_cache # inhibe el boton de vuelta atras desde el indice 
@login_required
def Rev_S2_Drp(request, pk):
    """
    Revisa la denegacion de autorizacion  para cada  la seccion 2 : Responsbles DRP 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
    print('asigna drp', drp)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name

    # Selecciona Comentarios 
    comentarios_drp=Log_Revision.objects.filter(drp=drp)
    comentarios=[]
    for com in comentarios_drp:
        if com.seccion == "D2": # Comentarios sobre las Asignaiones de Roles del DRP
            comentarios.append(com)

 
    if request.method=='POST':

        form=Drp_Sec_2_Form(request.POST)

                    
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            responsable = form.cleaned_data['resp_drp']
            drp.resp_drp = responsable

            respaldo_resp =form.cleaned_data['bck_resp']
            drp.bck_resp_drp = respaldo_resp


            ejecutor=form.cleaned_data['gestor_ejecutor']
            drp.gestor_ejecutor_drp=ejecutor

            respaldo_ejec= form.cleaned_data['bck_ejecutor']
            drp.bck_ejecutor_drp=respaldo_ejec 


            enlace = form.cleaned_data['enlace_c_crisis']
            drp.enlace_c_crisis_drp=enlace 

            respaldo_enl= form.cleaned_data['bck_enlace']
            drp.bck_enlace_drp=respaldo_enl 

            drp.status_2 ='a'

            #Actualiza lista de Contactos
            #============================
            print('--- Actualiza lista de contactos ---')
            
            #responsable y respaldo
            
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0101')

            if contacto:
                if responsable:
                    contacto0101 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0101')
                    contacto0101.nombre=responsable.user_gestor.first_name+' '+responsable.apellido
                    contacto0101.correo=responsable.user_gestor.email
                    contacto0101.tel_lab=responsable.fono_t
                    contacto0101.cel_lab=responsable.cod_area.codigo+responsable.fono_c
                    contacto0101.save()
                    print('Actualiza contacto responsable=', contacto0101.nombre)
                else:
                    contacto.delete()
                    
            else:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0101'
                    contacto.nombre=responsable.user_gestor.first_name+' '+responsable.apellido
                    contacto.correo=responsable.user_gestor.email
                    contacto.tel_lab=responsable.fono_t
                    contacto.cel_lab=responsable.cod_area.codigo+responsable.fono_c
                    contacto.save()                    
                    drp.contactos_drp.add(contacto)
                    print('Crea contacto responsable=', contacto.nombre)
                    
                    
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0102')

            if contacto:
                if respaldo_resp:
                    contacto0102 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0102')
                    contacto0102.nombre=respaldo_resp.user_gestor.first_name+' '+respaldo_resp.apellido
                    contacto0102.correo=respaldo_resp.user_gestor.email
                    contacto0102.tel_lab=respaldo_resp.fono_t
                    contacto0102.cel_lab=respaldo_resp.cod_area.codigo+respaldo_resp.fono_c
                    contacto0102.save()
                    print('Actualiza resp. responsable=', contacto0102.nombre)

                else:
                    contacto.delete()

            else:
                if respaldo_resp:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0102'
                    contacto.nombre=respaldo_resp.user_gestor.first_name+' '+respaldo_resp.apellido
                    contacto.correo=respaldo_resp.user_gestor.email
                    contacto.tel_lab=respaldo_resp.fono_t
                    contacto.cel_lab=respaldo_resp.cod_area.codigo+respaldo_resp.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea resp. responsable=', contacto.nombre)
                   
            #ejecutor y respaldo
            
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0201')
                
            if contacto:
                if ejecutor:
                    contacto0201 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0201')
                    contacto0201.nombre=ejecutor.user_gestor.first_name+' '+ejecutor.apellido
                    contacto0201.correo=ejecutor.user_gestor.email
                    contacto0201.tel_lab=ejecutor.fono_t
                    contacto0201.cel_lab=ejecutor.cod_area.codigo+ejecutor.fono_c
                    contacto0201.save()
                    #drp.contactos_drp.set(contacto0201)
                    print('Actualiza contacto ejecutor=', contacto0201.nombre)
                else:
                    contacto.delete()

            else:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0201'
                    contacto.nombre=ejecutor.user_gestor.first_name+' '+ejecutor.apellido
                    contacto.correo=ejecutor.user_gestor.email
                    contacto.tel_lab=ejecutor.fono_t
                    contacto.cel_lab=ejecutor.cod_area.codigo+ejecutor.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea contacto ejecutor=', contacto.nombre)
           
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0202')

            if contacto:
                if respaldo_ejec:
                    contacto0202 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0202')
                    contacto0202.nombre=respaldo_ejec.user_gestor.first_name+' '+respaldo_ejec.apellido
                    contacto0202.correo=respaldo_ejec.user_gestor.email
                    contacto0202.tel_lab=respaldo_ejec.fono_t
                    contacto0202.cel_lab=respaldo_ejec.cod_area.codigo+respaldo_ejec.fono_c
                    contacto0202.save()
                    #drp.contactos_drp.set(contacto0202)
                    print('Actualiza respaldo ejecutor=', contacto0202.nombre)
                else:
                    contacto.delete()

            else:
                if respaldo_ejec:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0202'
                    contacto.nombre=respaldo_ejec.user_gestor.first_name+' '+respaldo_ejec.apellido
                    contacto.correo=respaldo_ejec.user_gestor.email
                    contacto.tel_lab=respaldo_ejec.fono_t
                    contacto.cel_lab=respaldo_ejec.cod_area.codigo+respaldo_ejec.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea respaldo ejecutor=', contacto.nombre)
            
            #enlace y respaldo
           
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0301')
                
            if contacto:
                if enlace:
                    contacto0301 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0301')
                    contacto0301.nombre=enlace.user_gestor.first_name+' '+enlace.apellido
                    contacto0301.correo=enlace.user_gestor.email
                    contacto0301.tel_lab=enlace.fono_t
                    contacto0301.cel_lab=enlace.cod_area.codigo+enlace.fono_c
                    contacto0301.save()
                    #drp.contactos_drp.set(contacto0301)
                    print('Actualiza contacto enlace=', contacto0301.nombre)
                else:
                    contacto.delete()

            else:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0301'
                    contacto.nombre=enlace.user_gestor.first_name+' '+enlace.apellido
                    contacto.correo=enlace.user_gestor.email
                    contacto.tel_lab=enlace.fono_t
                    contacto.cel_lab=enlace.cod_area.codigo+enlace.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea contacto enlace=', contacto.nombre)
                        
            contacto=Contactos_PC.objects.filter(cont_int = str(pk)+'0302')

            if contacto:
                if respaldo_enl:
                    contacto0302 = get_object_or_404(Contactos_PC, cont_int = str(pk)+'0302')                
                    contacto0302.nombre=respaldo_enl.user_gestor.first_name+' '+respaldo_enl.apellido
                    contacto0302.correo=respaldo_enl.user_gestor.email
                    contacto0302.tel_lab=respaldo_enl.fono_t
                    contacto0302.cel_lab=respaldo_enl.cod_area.codigo+respaldo_enl.fono_c
                    contacto0302.save()
                    print('Actualiza respaldo enlace=', contacto0302.nombre)
                else:
                    contacto.delete()

            else:
                if respaldo_enl:
                    contacto=Contactos_PC()
                    contacto.cont_int=str(pk)+'0302'
                    contacto.nombre=respaldo_enl.user_gestor.first_name+' '+respaldo_enl.apellido
                    contacto.correo=respaldo_enl.user_gestor.email
                    contacto.tel_lab=respaldo_enl.fono_t
                    contacto.cel_lab=respaldo_enl.cod_area.codigo+respaldo_enl.fono_c
                    contacto.save()
                    drp.contactos_drp.add(contacto)
                    print('Crea respaldo enlace=', contacto.nombre)

            #Graba en Base de Datos                
            drp.save()

            # Crea Log de Revision
            log=Log_Revision()
            log.fecha = datetime.date.today()
            log.drp= drp
            log.gestor_aut=usr_aut
            log.seccion="D3"
            log.campo="Revisado por:"+aut
            log.comentario="Se revisaron los comentarios e implementan las modificaciones."
            log.resuelto=True

            # Graba en Base de Datos                
            log.save()

                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = Drp_Sec_2_Form(initial= {
                                        'resp_drp':drp.resp_drp,
                                        'bck_resp':drp.bck_resp_drp,
                                        'gestor_ejecutor':drp.gestor_ejecutor_drp,
                                        'bck_ejecutor':drp.bck_ejecutor_drp,
                                        'enlace_c_crisis':drp.enlace_c_crisis_drp,
                                        'bck_enlace':drp.bck_enlace_drp
                                        }
                             )

                                 
        return render(request, 'bcp/drp/drp_s2_rev.html', {'form': form,
                                                           'drp':drp,
                                                           'comentarios':comentarios})
        

#******************************************************
# 6.14.2   Revision de Objetivo  del DRP              *
#******************************************************

from django.views.decorators.cache import never_cache
@never_cache # inhibe el boton de vuelta atras desde el indice 
@login_required
def Rev_S1_Drp(request, pk):
    """
    Revisa la denegacion de autorizacion  para cada  la seccion 2 : Objetivo del  DRP 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
       
    # Selecciona Comentarios 
    comentarios_drp=Log_Revision.objects.filter(drp=drp)
    comentarios=[]
    for com in comentarios_drp:
        if com.seccion == "D1": # Comentarios sobre las declaracion de Objetivo del DRP
            comentarios.append(com)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name


    if request.method=='POST':

        form=Drp_Sec_1_Form(request.POST)

                      
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            drp.introduccion = form.cleaned_data['objetivo']
            
            drp.status_1 ='a'

            # Crea Log de Revision
            log=Log_Revision()
            log.fecha = datetime.date.today()
            log.drp= drp
            log.gestor_aut=usr_aut
            log.seccion="D3"
            log.campo="Revisado por:"+aut
            log.comentario="Se revisaron los comentarios e implementan las modificaciones."
            log.resuelto=True

            # Graba en Base de Datos                
            drp.save()
            log.save()
                
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = Drp_Sec_1_Form(initial= {
                                        'objetivo':drp.introduccion
                                        }
                             )

                                 
        return render(request, 'bcp/drp/drp_s1_rev.html', {'form': form,
                                                           'drp':drp,
                                                           'comentarios':comentarios})
    

#*****************************************************
# 6.14.3   Revision de Alcance  del DRP              *
#*****************************************************

#******************************* Codigo obsoleto ****************************************** 
def Rev_S3_Drp(request, pk): 
    """
    Revisa las observaciones realizadas 
    para  la seccion 3 : Alcance del  DRP 
    (Version descontinuada. Ver : rev_asigna_procesos_drp)
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
       
    # Selecciona Comentarios 
    comentarios_drp=Log_Revision.objects.filter(drp=drp)
    comentarios=[]
    for com in comentarios_drp:
        if com.seccion == "D3": # Comentarios 
            comentarios.append(com)


    if request.method=='POST':

        form=Drp_Sec_3_Form(request.POST)

                      
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            p1 = form.cleaned_data['procesos']
            drp.procesos_drp.set(p1)
            
            drp.status_3 ='a'


            #Graba en Base de Datos                
            drp.save()
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        Drp_Sec_3_url_ant = request.META['HTTP_REFERER']
        print('Drp_Sec_3_url_ant  =', Drp_Sec_3_url_ant)
        p2=drp.procesos_drp.all()

        form = Drp_Sec_3_Form(initial={ 'procesos':set(p2)})

                                 
        return render(request, 'bcp/drp/drp_s3_rev.html', {'form': form,
                                                           'drp':drp,
                                                           'comentarios':comentarios})

from django.views.decorators.cache import never_cache
@never_cache # inhibe el boton de vuelta atras desde el indice
@login_required 
def rev_asigna_procesos_drp(request, pk):
    """ Modifica la Asignacion de los Procesos que seran cubiertos por el DRP (Alcance) en 
        base a los comentarios de revision.

        Esta version utiliza Javascript para el manejo de Box de Asignacion/Desasignacion.

        Filtra por aquellos que tienen activa_drp=True en su Estrategia Asociada.
        
        """
    
    drp = get_object_or_404(Drp, pk=pk)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name


    if request.method == "POST":
        ids = request.POST.get("procesos_ids", "")
        drp.procesos_drp.clear()
        if ids.strip():
            procesos_seleccionados = SubProceso_V.objects.filter(id__in=ids.split(","))
            drp.procesos_drp.set(procesos_seleccionados)

        drp.status_3="a"

        # Crea Log de Revision
        log=Log_Revision()
        log.fecha = datetime.date.today()
        log.drp= drp
        log.gestor_aut=usr_aut
        log.seccion="D3"
        log.campo="Revisado por:"+aut
        log.comentario="Formulario revisado conforme a los comentarios del autorizador."
        log.resuelto=True

        # Graba en Base de Datos                
        drp.save()
        log.save()


        return redirect(drp.get_absolute_url())



    # Selecciona Comentarios 
    comentarios_drp=Log_Revision.objects.filter(drp=drp)
    comentarios=[]
    for com in comentarios_drp:
        if com.seccion == "D3": # Comentarios sobre Asignacion de Procesos p/Alcance
            comentarios.append(com)


    procesos_disponibles = SubProceso_V.objects.filter(
        escenarios__estrategias__activa_drp=True
    ).exclude(id__in=drp.procesos_drp.all()).distinct()

    procesos_asignados = drp.procesos_drp.all()

    return render(request, "bcp/drp/drp_s3_rev.html", {
        "drp": drp,
        "comentarios":comentarios,
        "procesos_disponibles": procesos_disponibles,
        "procesos_asignados": procesos_asignados,
    })



#*****************************************************
# 6.14.4   Revision de Estrategia de Recuperacin     *
#*****************************************************

# inhibe el boton de vuelta atras desde el indice 
from django.views.decorators.cache import never_cache, cache_control
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Rev_S4_Drp(request, pk):
    """
    Revisa las observaciones realizadas 
    para  la seccion 4 : Estrategia de Recuperacion 
    """
    print('--- Revision de Estrategia de Recuperacion ')

    # Evita reingreso al formulario desde sesión
    if request.session.get('form_enviado'):
        print('---> El formulario YA fue enviado' )
        del request.session['form_enviado']
        #return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[4000] ))
    else:
        print('---> El Formulario NO ha sido enviado')


    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
       
    # Selecciona Comentarios 
    comentarios_drp=Log_Revision.objects.filter(drp=drp)
    comentarios=[]
    for com in comentarios_drp:
        if com.seccion == "D4": # Comentarios 
            comentarios.append(com)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name


    if request.method=='POST':

        form=Drp_Sec_4_Form(request.POST)

                      
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            drp.tipo_Site = form.cleaned_data['tipo_site']
            drp.desc_estrategia = form.cleaned_data['desc_estrategia']
            drp.disposicion_componentes = form.cleaned_data['tipo_disp']
            
            drp.status_4 ='a'

            # Crea Log de Revision
            log=Log_Revision()
            log.fecha = datetime.date.today()
            log.drp= drp
            log.gestor_aut=usr_aut
            log.seccion="D4"
            log.campo="Revisado por:"+aut
            log.comentario="Formulario revisado conforme a los comentarios del autorizador."
            log.resuelto=True

            # Graba en Base de Datos                
            drp.save()
            log.save()
                
            # Marca la sesión para prevenir reingreso
            request.session['form_enviado'] = True

            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        #Drp_Sec_3_url_ant = request.META['HTTP_REFERER']
        #print('Drp_Sec_3_url_ant  =', Drp_Sec_3_url_ant)
        #p2=drp.procesos_drp.all()

        form = Drp_Sec_4_Form(initial={'tipo_site':drp.tipo_Site,
                                       'desc_estrategia': drp.desc_estrategia,
                                       'tipo_disp':drp.disposicion_componentes
                                       })

                                 
        return render(request, 'bcp/drp/drp_s4_rev.html', {'form': form,
                                                           'drp':drp,
                                                           'comentarios':comentarios})


#***************************************************************
# 6.14.5 Revision Especificacion Tecnica Site de Contingencias *
#***************************************************************
from django.views.decorators.cache import never_cache
@never_cache # inhibe el boton de vuelta atras desde el indice 
@login_required
def Rev_S5_Drp(request, pk):
    """
    Revisa las observaciones realizadas 
    para  la seccion 5 : Especificacion Tecnica del Site de Contingencias 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    
    drp = get_object_or_404(Drp, pk = pk)
    lista_cmp = drp.componentes

    if request.method=='POST':

        form=Drp_Sec_5_Form(request.POST)

                      
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            p1 = form.cleaned_data['componentes']
            drp.procesos_drp.set(p1)
            
            drp.status_5 ='a'

            #Graba en Base de Datos                
            drp.save()
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        p2=drp.componentes.all()

        form = Drp_Sec_5_Form(initial={'componentes':set(p2)})

                                 
        return render(request, 'bcp/drp/drp_s5_rev.html', {'form': form, 'drp':drp,
                                                           'lista_cmp':lista_cmp})

@never_cache # inhibe el boton de vuelta atras desde el indice
@login_required 
def rev_esp_tec_drp(request, pk):
    """ Modifica la Especificacion Tecnica (Asignacion de Componentes) del DRP en 
        base a los comentarios de revision.

        Esta version utiliza Javascript para el manejo de Box de Asignacion/Desasignacion.
     
       
        """
    
    drp = get_object_or_404(Drp, pk=pk)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    usr =  request.user
    usr_aut=Gestor.objects.get(user_pk=usr.pk)
    aut=usr_aut.user_gestor.first_name+' '+usr_aut.user_gestor.last_name

    # POST
    if request.method == "POST":
        ids = request.POST.get("procesos_ids", "")
        #drp.componentes.clear()
        if ids.strip():
            componentes_seleccionados = Componentes.objects.filter(id__in=ids.split(","))
            drp.componentes.set(componentes_seleccionados)

        drp.status_5="a"

        # Crea Log de Revision
        log=Log_Revision()
        log.fecha = datetime.date.today()
        log.drp= drp
        log.gestor_aut=usr_aut
        log.seccion="D5"
        log.campo="Revisado por:"+aut
        log.comentario="Formulario revisado conforme a los comentarios del autorizador."
        log.resuelto=True

        # Graba en Base de Datos                
        drp.save()
        log.save()


        return redirect(drp.get_absolute_url())

    # GET

    # Selecciona Comentarios 
    comentarios_drp=Log_Revision.objects.filter(drp=drp)
    comentarios=[]
    for com in comentarios_drp:
        if com.seccion == "D5": # Comentarios sobre Asignacion de Procesos p/Alcance
            comentarios.append(com)


    componentes_disponibles = Componentes.objects.all().exclude(id__in=drp.componentes.all()).distinct()

    componentes_asignados = drp.componentes.all()

    origen=2

    return render(request, "bcp/drp/drp_s5_rev.html", {
        "drp": drp,
        "comentarios":comentarios,
        "componentes_disponibles": componentes_disponibles,
        "componentes_asignados": componentes_asignados,
        "origen":origen
    })

#***************************************************************
# 6.14.6  Revision Especificacion de Servicios Criticos del DRP*
#***************************************************************
from django.views.decorators.cache import never_cache
@never_cache # inhibe el boton de vuelta atras desde el indice 
@login_required
def Rev_S6_Drp(request, pk):
    """
    Revisa las observaciones realizadas 
    para  la seccion 6 : Servicios Criticos 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    
    drp = get_object_or_404(Drp, pk = pk)
    lista_sc = drp.servicios_drp

    return render(request, 'bcp/drp/drp_s6_rev.html', {'drp':drp,'lista_sc':lista_sc})


#****************************************************
# 6.15  Detalle del DRP en Desarrollo/Actualizacion *
#****************************************************
@login_required
def detalle_drp(request, pk):

    drp = get_object_or_404(Drp, pk = pk)

    # Seleccion de Recursos/Servicios criticos asociados a los Procesos alcanzados
    servicios_criticos = set() # set evita automaticamente el duplicado
    for pr in drp.procesos_drp.all():
        for sc in pr.recursos.all():
            servicios_criticos.add(sc)

    # servicios_criticos = {sc for pr in drp.procesos_drp for sc in pr.recursos}  /Alternativa mas "pythonizada"

    
    print('>>> Servicios Criticos:', servicios_criticos)

    # Selecciona los Coponentes asignados al DRP
    componentes_asig=drp.componentes


    return render(request, 'bcp/drp/drp_detalle.html', {'drp':drp,
                                                        'componentes_asig':componentes_asig,
                                                        'servicios_criticos':servicios_criticos})
                  
#*********************************************** Fin DRP ************************************************************************************


#*********************************************************************************************************************************************
#***********************************************  7. Administracion de Incidentes  ************************************************************
#*********************************************************************************************************************************************



#***************************
#7.1.1  Declara Incidente  *
#***************************
from .forms import Declara_Incidente_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def Declara_Inc(request):
    """
    Registra el Incidente y Selecciona los Procesos relacionados con las amenazas 
    declaradas en el mismo. """
    print('>>>>>  Entra a Registro de Incidente ------')

    model = Incidentes
    
    #procesos=get_object_or_404(Proceso)

  
    if request.method=='POST':
        print('---- metodo POST')
        form = Declara_Incidente_Form(request.POST)
        
        if form.is_valid():
            print('----- Formato valido')
            
            incidente=Incidentes()

            # Define codigo del incidente
            #==============================
            # Rescata correlativo de Incidente. 
            parametro = get_object_or_404(Parametros_G, nombre = 'FOLIO INCIDENTES')

            #f_i = incidente.fecha.strftime('%Y%m')
            f_i = timezone.now().strftime('%Y%m')

            n=parametro.valor_2

            # Compone la parte numerica del codigo a un largo fijo 
            nro=''
            if n<9:
                nro='00' 
                nro=nro+str(n)
            elif n > 9 and n <= 99:
                nro='0' 
                nro=nro+str(n)
            elif n > 99 and n <= 999:
                nro=str(n)
            else:
                parametro.valor_2=1

            incidente.codigo = f_i+'/'+nro  # codigo = YYYYMM/999 (largo= 10)
            parametro.valor_2=n+1
            parametro.save()
            
            # Graba intancias en Registro (Base de Incidentes)
            incidente.nombre_r = form.cleaned_data['nombre']
            incidente.area_r = form.cleaned_data['area']
            incidente.descripcion = form.cleaned_data['descripcion']
            #incidente.correo = form.cleaned_data['correo']

            #amenazas_declaradas = form.cleaned_data['amenazas_i']
            #incidente.amenazas_i.set(amenazas_declaradas)
            incidente.save()

            # Rescata los Datos seleccionados desde el Script
            amenazas_ids = request.POST.get("amenazas_i", "").split(",")
            amenazas_ids = [int(e) for e in amenazas_ids if e.isdigit()]
            print('---- Amenazas rescatadas:', amenazas_ids)

            if amenazas_ids:
                
                incidente.amenazas_i.set(Amenazas.objects.filter(id__in=amenazas_ids))
            #else:
                #subproceso.escenarios.clear()

            
            # Selecciona los Procesos asociados al incidente en base a las amenazas declaradas
            # =================================================================================

            amenazas_declaradas=incidente.amenazas_i
            # Identifica los escenarios alcanzados
            # ------------------------------------

            # Recorre amenazas declaradas
            for amenaza in amenazas_declaradas.all():

                # Recorre los Escenarios de cada "amenaza" declarada
                escenarios_en_amenaza=amenaza.landscape
                for escenario in escenarios_en_amenaza.all():

                    # Identifica a los Procesos Vigentes asociados al "escenario".
                    sprocesos=SubProceso_V.objects.all()
                    sprocesos_selec=[]
                    for sproc in sprocesos:
                        
                        # Selecciona los Escenarios que estan Asociados al Sproceso
                        esc_en_sproc=sproc.escenarios # Escenarios asociados al Proceso
                        escenarios_selec=[]
                        for esc in esc_en_sproc.all():

                            # Si el Escenario en la "amenaza" es igual al Escenario en el Sproceso
                            if escenario == esc:
                                # Asigna el Escenario a los Escenarios del Incidente
                                if not esc in escenarios_selec:
                                    escenarios_selec.append(esc)
                                    incidente.escenarios_i.add(esc)

                                    # Asigna el Proceso a los Procesos del Incidente
                                    #pk_padre=sproc.pk_padre
                                    #proceso=get_object_or_404(Proceso, pk=pk_padre)
                                if not sproc in sprocesos_selec:
                                    sprocesos_selec.append(sproc)
                                    incidente.procesos_i.add(sproc)

            #print('-- Procesos   Sel.=', sprocesos_selec)
            #print('-- Escenarios Sel.=', escenarios_selec)                
                
            #Graba en BD
            print('Grabo incidente')
            
            incidente.save()
            parametro.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))
            

        else:

            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        form = Declara_Incidente_Form()

        #amenazas_disponibles = Amenazas.objects.exclude(id__in=incidente.amenazas_i.values_list('id', flat=True))
        #amenazas_asignadas = incidente.amenazas_i.all()
        amenazas_disponibles = Amenazas.objects.all()

        return render(request, 'bcp/inc_mgm/crea_inc.html',{'form':form,
                                                            'amenazas_disponibles':amenazas_disponibles })


# ==================================
# Plan de Pruebas
# =================================
from .forms import Plan_Pruebas_A_Form
#@permission_required('Catalogo.can_mark_returned')
@login_required
def Define_Plan_Pruebas_A(request):
    """
    Define el Plan de Pruebas 
    """
    print('>>>>>  Entra a Registro del PLAN DE PRUEBAS A ------')

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Gestion de Crisis']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[400] ))

  
    #procesos=get_object_or_404(Proceso)

  
    if request.method=='POST':
        print('---- metodo POST')
        form = Plan_Pruebas_A_Form(request.POST)
        
        if form.is_valid():
            print('----- Formato valido')

            # Graba intancias en Registro (Base de Incidentes)
            # ================================================

            incidente=Incidentes()
            fecha=form.cleaned_data['fecha_hora']
            incidente.fecha_creacion = fecha
            incidente.fecha = fecha
            incidente.nombre_r = 'COMITE DE CRISIS'
            incidente.area_r = 'Preparado por Gestion de Riesgos'
            incidente.descripcion = 'Prueba integral de Procedimientos de Contingencias del BCP/DRP'
            incidente.test= True
            incidente.estado=False

             # Define codigo del incidente
            #==============================
            # Rescata correlativo de Incidente. 
            parametro = get_object_or_404(Parametros_G, nombre = 'FOLIO INCIDENTES')

            f_i = fecha.strftime('%Y%m')
            n=parametro.valor_2

            # Compone la parte numerica del codigo a un largo fijo 
            nro=''
            if n<9:
                nro='00' 
                nro=nro+str(n)
            elif n > 9 and n <= 99:
                nro=str(n)
            else:
                parametro.valor_2=1

            incidente.codigo = f_i+'P/'+nro  # codigo = YYYYMMP/99 (largo= 10)
            parametro.valor_2=n+1
            parametro.save()

              
            #Graba en BD
            print('Grabo incidente')
            
            incidente.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Define-Plan-Pruebas-B',  args=[str(incidente.id)]))
            

        else:

            print('Form invalido', form.errors)
            #return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})


            return render(request, 'bcp/inc_mgm/crea_plan_prba_A.html',{'form':form })


    else:

        form = Plan_Pruebas_A_Form()

        return render(request, 'bcp/inc_mgm/crea_plan_prba_A.html',{'form':form })


from .forms import Plan_Pruebas_B_Form
#@permission_required('Catalogo.can_mark_returned')
@login_required
def Define_Plan_Pruebas_B(request, pk):
    """
    Define el Plan de Pruebas 
    """
    print('>>>>>  Entra a Registro del PLAN DE PRUEBAS B ------')

      
    incidente=get_object_or_404(Incidentes, pk=pk)

  
    if request.method=='POST':
        print('---- metodo POST')
        form = Plan_Pruebas_B_Form(request.POST)
        
        if form.is_valid():
            print('----- Formato valido')
     

            # Rescata los Datos seleccionados desde el Script
            escenarios_ids = request.POST.get("escenarios_i", "").split(",")
            escenarios_ids = [int(e) for e in escenarios_ids if e.isdigit()]
            print('---- Escenarios rescatados:', escenarios_ids)

            if escenarios_ids:
                
                incidente.escenarios_i.set(Escenarios.objects.filter(id__in=escenarios_ids))
            #else:
                #subproceso.escenarios.clear()

            
            # Selecciona las Amenazas y Procesos asociados al incidente
            # en base a los Escenarios declarados 
            # =========================================================

            alcance_prba=incidente.escenarios_i

            # Identificacion de Amenazas
            # --------------------------
            amenazas=Amenazas.objects.all()

            for amn in amenazas:
                escenarios=amn.landscape
                for esc in escenarios.all():
                    if esc in alcance_prba.all():
                        incidente.amenazas_i.add(amn)


            # Identificacion de Procesos
            # --------------------------
            sprocesos=SubProceso_V.objects.all()

            for proc in sprocesos.all():
                escenarios=proc.escenarios
                for esc in escenarios.all():
                    if esc in alcance_prba.all():
                        incidente.procesos_i.add(proc)



            #print('-- Procesos   Sel.=', sprocesos_selec)
            #print('-- Escenarios Sel.=', escenarios_selec)                
                
            #Graba en BD
            print('Grabo incidente')
            
            incidente.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Incidentes'))
            

    else:

        form = Plan_Pruebas_B_Form()

        escenarios_disponibles = Escenarios.objects.exclude(id__in=incidente.escenarios_i.values_list('id', flat=True))
        escenarios_asignados   = incidente.escenarios_i.all()
        #escenarios_disponibles = Escenarios.objects.all()

        return render(request, 'bcp/inc_mgm/crea_plan_prba_B.html',{'form':form,
                                                            'escenarios_disponibles':escenarios_disponibles,
                                                            'escenarios_asignados':escenarios_asignados })



from .forms import Plan_Pruebas_A_Form
#@permission_required('Catalogo.can_mark_returned')
@login_required
def Modif_Plan_Pruebas(request, pk):
    """
    Modifica el Plan de Pruebas 
    pk:pk del Plan de Pruebas
    """
    print('>>>>>  Entra a Modificacion del PLAN DE PRUEBAS A ------')
  
    incidente=get_object_or_404(Incidentes, pk=pk)
  
    if request.method=='POST':
        print('---- metodo POST')
        form = Plan_Pruebas_A_Form(request.POST)
        
        if form.is_valid():
            print('----- Formato valido')
         
          
            
            # Graba intancias en Registro (Base de Incidentes)
            incidente.fecha_creacion = form.cleaned_data['fecha_hora']
            incidente.fecha = form.cleaned_data['fecha_hora']
            incidente.nombre_r = 'COMITE DE CRISIS'
            incidente.area_r = 'Preparado por Gestion de Riesgos'
            incidente.descripcion = 'Prueba integral de Procedimientos de Contingencias del BCP/DRP'
            incidente.test= True
            incidente.estado=False

              
            #Graba en BD
            print('Grabo incidente')
            
            incidente.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Define-Plan-Pruebas-B',  args=[str(incidente.id)]))
            

        else:

            print('Form invalido', form.errors) 
            #return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})


            return render(request, 'bcp/inc_mgm/crea_plan_prba_A.html',{'form':form })


    else:

        form = Plan_Pruebas_A_Form(initial={'fecha': incidente.fecha_creacion.date(),
                                            'hora':  incidente.fecha_creacion.strftime("%H:%M"),
                                            })

        return render(request, 'bcp/inc_mgm/crea_plan_prba_A.html',{'form':form })




@login_required
def Borra_Incidente(request, pk):
    """
    Borra el Incidente"""

    print('>>>>> Borra el Incidente')

    incidente=get_object_or_404(Incidentes, pk=pk)
    incidente.delete()

    print('----- Borra el Incidente y retorna')
    # Dirige la Salida 
    next_url = request.GET.get('next', '/')
    return redirect(next_url)
 

#************************************
#6.2 Lista de Incidentes reportados *
#************************************
@login_required
def Lista_Incidentes(request):
    """
    Generic class-based view listing books on loan to current user.
    """
    print('>>>>> Lista Incidentes')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Gestion de Crisis']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[400] ))

    incidentes=Incidentes.objects.all()

    lista_incidentes=[]
    for inc in incidentes:
        print('-- Incidente :',inc.codigo)


        # Determina si algun Procedimiento del incidente asociado se encuentra Activado.
        # ------------------------------------------------------------------------------
        proced_act=False
        procesos=inc.procesos_i
        amenazas=inc.amenazas_i
      
        for amn in amenazas.all():
        # Para cada amenaza del Incidente
            print('----  Amenaza :', amn.titulo)
            escenarios_amn=amn.landscape

            for esc_amn in escenarios_amn.all():
            # Para cada escenario de la Amenaza del Incidente
                print('---- Escenario x Amenaza:', esc_amn.titulo)

                escenario_amenaza=esc_amn.titulo #(1)
                                                
                for prc in procesos.all():
                # Para cada Proceso asociado al  Incidente
                    escenarios_proceso=prc.escenarios
                    procedimientos_proceso=prc.procedimientos_contingencia_v
                
                    print('------ Proceso Asociado al Incidente :', prc.nombre)

                    for esc_prc in escenarios_proceso.all():
                    # Para cada Escenario asociado al Proceso en Incidente 
                        print('---- Escenario del Proceso', esc_prc.titulo)
                        
                        escenario_prc=esc_prc.titulo #(2)

                        if escenario_prc == escenario_amenaza:
                            print('> ESCENARIO AMENAZA = ESCENARIO PROCESO')

                            for prcd in procedimientos_proceso.all():
                            # Para cada Procedimiento de cada Proceso del Incidente
                                print('---------- Procedimientos Asociado al Proceso', prcd.nombre)
                                
                                escenario_procedimiento=prcd.escenarios.titulo #(3)

                                if escenario_prc  == escenario_procedimiento:
                                    print('> ESCENARIO PROCESO = ESCENARIO PROCEDIMIENTO')

                                    # Condiciones para Borrado
                                    # ------------------------

                                    if prcd.esta_activo:
                                        print('---------- Procedimiento Activo !!. Canbia a True')
                                        proced_act=True
                                    else:
                                        print('---------- Procedimiento NO Activo !!. Se mantiene False ')
                        
                                else:
                                    print('> ESCENARIO PROCESO DISTINTO A ESCENARIO PROCEDIMIENTO')

                        else:
                            print('> ESCENARIO AMENAZA DISTINTO A ESCENARIO PROCESO')

   
        inc_2={'inc':inc, 'activo':proced_act}
        print('---- incidente', inc.codigo, 'inc_2=', inc_2)
        lista_incidentes.append(inc_2)
        


    return render(request, 'bcp/inc_mgm/incidentes__list.html', {'lista_incidentes':lista_incidentes})

#****************************
#6.2.1  Modifica Incidente  *
#****************************
from .forms import Modifica_Incidente_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def Modifica_Inc(request, pk):
    """
    Permite modificar la declaracion inicial del incidente
    Elimina los Procesos asociados seleccionados y los selecciona nuevamente
    """
    
    print('Entra Modifica Incidente')


    incidente = get_object_or_404(Incidentes, pk = pk)
   
    
    if request.method=='POST':
        print('metodo POST')
          
        # Rescata los Datos seleccionados desde el Script
        amenazas_ids = request.POST.get("amenazas_i", "").split(",")
        amenazas_ids = [int(e) for e in amenazas_ids if e.isdigit()]
        print('---- Amenazas rescatadas:', amenazas_ids)

        if amenazas_ids:
            
            incidente.amenazas_i.set(Amenazas.objects.filter(id__in=amenazas_ids))
        #else:
            #subproceso.escenarios.clear()


        # Selecciona los nuevos Procesos y Escenarios asociados al incidente en base a las nuevas amenazas declaradas
        # ===========================================================================================================

        # Identifica los escenarios alcanzados
        # ------------------------------------


        #incidente.escenarios_i.clear() # Borra todos los escenarios del incidente
        #incidente.procesos_i.clear() # Borra todos los procesos antiguos del incidente

        sprocesos=SubProceso_V.objects.all() # rescata todos los subprocesos vigentes
        sprocesos_selec=[]
        escenarios_selec=[]

        # Recorre las nuevas amenazas declaradas

        nuevas_amenazas_declaradas=incidente.amenazas_i
        print('---- Recorre nuevas amenazas :.', nuevas_amenazas_declaradas)


        for amenaza in nuevas_amenazas_declaradas.all():
            print('--- Amenaza: ', amenaza)

            # Recorre los Escenarios de cada "amenaza" declarada
            escenarios_en_amenaza=amenaza.landscape
            #incidente.save()

            for escenario in escenarios_en_amenaza.all():

                # Identifica a los Procesos Vigentes asociados al nuevo escenario.
                for sproc in sprocesos:
                    
                    # Selecciona los Escenarios que estan Asociados al Sproceso
                    esc_en_sproc=sproc.escenarios # Escenarios asociados al Proceso
                    
                    for esc in esc_en_sproc.all():

                        # Si el Escenario en la "amenaza" es igual al Escenario en el Sproceso
                        if escenario == esc:

                            # Asigna el Escenario a los Escenarios del Incidente
                            if not esc in escenarios_selec:
                                escenarios_selec.append(esc)
                                #incidente.escenarios_i.add(esc)
                                #incidente.save()
                                print('--- Nuevo escenario :', esc.titulo)

                                # Asigna el Proceso a los Procesos del Incidente
                                #pk_padre=sproc.pk_padre
                                #proceso=get_object_or_404(Proceso, pk=pk_padre)
                            if not sproc in sprocesos_selec:
                                sprocesos_selec.append(sproc)
                                #incidente.procesos_i.add(sproc)
                                #incidente.save()
                                print('--- Nuevo Proceso :', sproc.nombre)


            print('----- escenarios selecc:', escenarios_selec)
            print('----- sprocesos_selecc: ', sprocesos_selec)
            incidente.escenarios_i.set(escenarios_selec)
            incidente.procesos_i.set(sprocesos_selec)
            incidente.save()

            #print('-- Procesos   Sel.=', sprocesos_selec)
            #print('-- Escenarios Sel.=', escenarios_selec)                
                
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Incidentes'))                          

                      

    amenazas_disponibles = Amenazas.objects.exclude(id__in=incidente.amenazas_i.values_list('id', flat=True))
    amenazas_asignadas = incidente.amenazas_i.all()


    print('GET')
    
    return render(request, 'bcp/inc_mgm/modi_inc.html',{'form':Modifica_Incidente_Form(),
                                                        'amenazas_disponibles':amenazas_disponibles,
                                                        'amenazas_asignadas':amenazas_asignadas,
                                                        'incidente':incidente })

      

#*************************************
# 6.3 Reporte de Perfil de Incidente *
#*************************************
@login_required
def Perfil_Inc(request, pk):

    print('>>>>> Perfil del Incidente (Dashboard)')

    incidente = get_object_or_404(Incidentes, pk = pk)
    print('---- Informa incidente : ', incidente.nombre_r)


    procesos_inc = incidente.procesos_i
    #escenarios_inc=incidente.escenarios_i

    # Escenarios asociados al incidente
    # =================================
    escenarios_inc = [] 
    print('---- Escenarios:')
    for esc in incidente.escenarios_i.all():
        print('-------  Escenarios:', esc.titulo)
        escenarios_inc.append(esc.titulo)

    # PC asociados al incidente
    # =========================

    procedimientos_inc=[]
    cont_procedimientos=0
    cont_proced_act=0
    cont_proced_ina=0
    cont_proced_con=0
    cont_proced_no_con=0
    for proc in procesos_inc.all():
        for proced in proc.procedimientos_contingencia_v.all():
            if proced.escenarios.titulo in escenarios_inc:
                procedimientos_inc.append(proced)
                cont_procedimientos += 1
                if proced.esta_activo:
                    cont_proced_act += 1
                    if proced.esta_confirmado:
                        cont_proced_con += 1
                    else:
                        cont_proced_no_con += 1
                else:
                    cont_proced_ina += 1

                


    P100_activos_vs_totales = (cont_proced_act / cont_procedimientos * 100) if cont_procedimientos else 0
    P100_inactivos_vs_totales = 100 - P100_activos_vs_totales

    P100_confirm_vs_activos = (cont_proced_con / cont_proced_act * 100) if cont_proced_act else 0
    P100_no_confirm_vs_activos = 100 - P100_confirm_vs_activos


    print('----- Total procedimientos : ', cont_procedimientos)
    print('----- Total proced. Activos : ', cont_proced_act)
    print('----- Total proced. Confirmados : ', cont_proced_con)

    data_1 = {
        "Activos": float(P100_activos_vs_totales or 0),
        "Inactivos": float(P100_inactivos_vs_totales or 0),
    }

    colors_1 = {
        "Activos": "#2ecc71",
        "Inactivos": "#e74c3c",
    }

    data_2 = {
        "Confirmados": float(P100_confirm_vs_activos or 0),
        "No Confirmados": float(P100_no_confirm_vs_activos or 0),
    }

    colors_2 = {
        "Confirmados": "#2ecc71",
        "No Confirmados": "#e74c3c",
    }

    #context.update({
    #    "chart_data_1": data_1,
    #    "chart_colors_1": colors_1,
    #    "chart_data_1": data_2,
    #    "chart_colors_1": colors_2,
    #})


    # Escenarios asociados al incidente
    # =================================
    escenarios_inc = [] 
    for esc in incidente.escenarios_i.all():
        print('-- Escenarios:', esc.titulo)
        escenarios_inc.append(esc.titulo)

    amenazas_inc = incidente.amenazas_i

    # Identifica al Comite de Crisis.
    comite=[]
    gestores=Gestor.objects.all()
    for integrante in gestores:
        for grp in integrante.user_gestor.groups.all():
            if grp.name=='Gestion de Crisis':
                comite.append(integrante)
    print('integrantes del comite =', comite)


    # Estadisticas de Proceso
    # -----------------------

    # Numero de Procesos 
    n_procesos=incidente.procesos_i.count()
    print('- Numero de Procesos en Incidente=', n_procesos)

    # Puntaje Promedio
    puntaje_x=00.00
    if n_procesos > 0:
            total_puntaje=00.00
            for prc in incidente.procesos_i.all():
                total_puntaje=total_puntaje+float(prc.ranking)
            puntaje_x=total_puntaje/n_procesos

    print('-- Puntaje Promedio =', puntaje_x)


    # Estadistica de Procesos x Riesgo/Impacto y Nivel

    estadistica_impactos = contar_procesos_por_tipo_nivel_impacto(incidente)
    estadistica_impactos = {tipo: dict(niveles) for tipo, niveles in estadistica_impactos.items()}

    # Imprimir el resultado
    for tipo, niveles in estadistica_impactos.items():
            for nivel, cantidad in niveles.items():
                print(f"Tipo: {tipo} | Nivel: {nivel} | Procesos: {cantidad}")

 
    # Estadistica de Procesos x Indicadores de Recuperacion

    estadistica_indicadores = contar_procesos_por_tipo_nivel_indicadores(incidente)
    estadistica_indicadores = {tipo: dict(niveles) for tipo, niveles in estadistica_indicadores.items()}

    # Imprimir el resultado
    for tipo, niveles in estadistica_indicadores.items():
            for nivel, cantidad in niveles.items():
                print(f"Tipo: {tipo} | Nivel: {nivel} | Procesos: {cantidad}")


    # Estadistica de Procesos x Escenarios

    estadistica_escenarios = contar_procesos_por_escenario(incidente)

    # Imprimir el resultado
    for escenario, cantidad in estadistica_escenarios.items():
                print(f"Escenario: {escenario} | Procesos: {cantidad}")

    estadistica_recursos = contar_procesos_por_servicio(incidente)

    # Imprimir el resultado
    for recurso, cantidad in estadistica_recursos.items():
                print(f"Escenario: {recurso} | Procesos: {cantidad}")


    # Fin Estadisticas de Proceso
    # ---------------------------

    

    return render(request,'bcp/inc_mgm/perfil_inc.html', {'incidente':incidente,
                                                          'escenarios_inc':escenarios_inc,
                                                          'comite':comite,
                                                          'amenazas':amenazas_inc,
                                                          'n_procesos':n_procesos,
                                                          'procesos':procesos_inc,
                                                          'puntaje_x':puntaje_x,
                                                          'estadistica_impactos':estadistica_impactos,
                                                          'estadistica_indicadores':estadistica_indicadores,
                                                          'estadistica_escenarios':estadistica_escenarios,
                                                          'estadistica_recursos':estadistica_recursos,
                                                          'cont_procedimientos':cont_procedimientos,
                                                          'cont_proced_act':cont_proced_act,
                                                          'cont_proced_ina':cont_proced_ina,
                                                          'cont_proced_con':cont_proced_con,
                                                          'cont_proced_no_con':cont_proced_no_con,
                                                          'P100_activos_vs_totales':P100_activos_vs_totales,
                                                          'P100_inactivos_vs_totales':P100_inactivos_vs_totales,
                                                          'P100_confirm_vs_activos':P100_confirm_vs_activos,
                                                          'P100_no_confirm_vs_activos':P100_no_confirm_vs_activos,
                                                          "chart_data_1": data_1,
                                                          "chart_colors_1":colors_1,
                                                          "chart_data_2": data_2,
                                                          "chart_colors_2": colors_2
                                                          })




from collections import defaultdict

#===============================================
# Contadores de Procesos x variable estadistica 
#===============================================
def contar_procesos_por_tipo_nivel_impacto(incidente):
    """
    Contabilizacion estadistica de Procesos x Impacto y Nivel
    Usado en el Perfil del Incidente.
    """
    print('-----Entra a Contar Procesos por tipo y nivel -----')
    # Estructura del contador como diccionario anidado
    contador = defaultdict(lambda: defaultdict(int))

    # Obtener todos los procesos asociados al incidente
    procesos = incidente.procesos_i.all()

    for proceso in procesos:
        # Obtener los impactos asignados al proceso
        impactos = proceso.impact_subp.all()

        for impacto_asig in impactos:
            if impacto_asig.impacto and impacto_asig.nivel:
                tipo_impacto = impacto_asig.impacto.nombre  # Nombre del Tipo_Impacto
                nivel_impacto = impacto_asig.nivel.nombre  # Nombre del Nivel_Impacto

                # Incrementar el contador en la matriz
                contador[tipo_impacto][nivel_impacto] += 1

    return contador

def contar_procesos_por_tipo_nivel_indicadores(incidente):
    """
    Contabilizacion estadistica de Procesos x Indicadores de Recuperacion
    Usado en el Perfil del Incidente.
    """
    print('-----Entra a Contar Procesos por tipo y nivel -----')
    # Estructura del contador como diccionario anidado
    contador = defaultdict(lambda: defaultdict(int))

    # Obtener todos los procesos asociados al incidente
    procesos = incidente.procesos_i.all()

    for proceso in procesos:
        # Obtener los impactos asignados al proceso
        indicadores = proceso.indicador_subp.all()

        for indicador_asig in indicadores:
            if indicador_asig.indicador and indicador_asig.nivel:
                tipo_indicador = indicador_asig.indicador.nombre  # Nombre del Tipo_Impacto
                nivel_indicador = indicador_asig.nivel.nivel  # Nombre del Nivel_Impacto

                # Incrementar el contador en la matriz
                contador[tipo_indicador][nivel_indicador] += 1

    return contador


from collections import defaultdict
def contar_procesos_por_escenario(incidente):
    """
    Contabilización estadística de Procesos por Escenarios
    asociados al Perfil del Incidente.
    """
    print('-----Entra a Contar Procesos por Escenario -----')

    contador = defaultdict(int)  # Almacena un número entero por escenario

    # Obtener todos los procesos asociados al incidente
    procesos = incidente.procesos_i.all()

    for proceso in procesos:
        # Obtener los escenarios asociados al proceso
        for escenario in proceso.escenarios.all():
            if escenario:
                contador[escenario.titulo] += 1  # Usar el nombre del escenario como clave

    return dict(contador)  # Convertir defaultdict en un diccionario normal


def contar_procesos_por_servicio(incidente):
    """
    Contabilización estadística de Procesos por Servicios/Recursos
    asociados al Perfil del Incidente.
    """
    print('-----Entra a Contar Procesos por Servicio/REcursos -----')

    contador = defaultdict(int)  # Almacena un número entero por escenario

    # Obtener todos los procesos asociados al incidente
    procesos = incidente.procesos_i.all()

    for proceso in procesos:
        # Obtener los escenarios asociados al proceso
        for recurso in proceso.recursos.all():
            if recurso:
                contador[recurso.nombre] += 1  # Usar el nombre del escenario como clave

    return dict(contador)  # Convertir defaultdict en un diccionario normal

# ---- Fin Contadores ---------------------------------------------------


# =====================================
# Switchs de Activacion / Desactivacion
# =====================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def toggle_procedimiento(request, procedimiento_id=None):
    """
    Switch de Activacion/Desactivacion del Procedimiento desde DashBoard del 
    Comite de Crisis
    """
    print('>>>>> Entra a Switch ')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("---- Datos recibidos en POST:", data)
            procedimiento = Procedimientos_V.objects.get(id=procedimiento_id)
            nuevo_estado = data.get("esta_activo", False)
            incidente_id = data.get("incidente_id")

            print(f"---- nuevo estado: {nuevo_estado}")
            print(f"---- Procedimiento: {procedimiento.nombre}")
            print(f"---- Incidente recibido: {incidente_id}")

            procedimiento.esta_activo = nuevo_estado
            procedimiento.save()

            if nuevo_estado:
                print('----  Estado es Activado')
                print('----  Crea CheckList de Ejecucion')

                # ✅ Validamos que incidente_id sea válido antes de usarlo
                if not incidente_id:
                    print("⚠️  No se recibió incidente_id válido, se omite creación de checklist")
                else:
                    try:
                        # 🧩 Bloque de diagnóstico insertado aquí
                        print("CheckList importado desde:", CheckList.__module__)
                        print("CheckList clase real:", CheckList)

                        print("---- Intentando obtener incidente con ID:", incidente_id)
                        incidente = Incidentes.objects.get(pk=int(incidente_id))
                        print("---- Incidente encontrado:", incidente.codigo)

                        # Crea Checklist
                        # ==============

                        # Determina el nro. del Checklist
                        n=procedimiento.correlativo_chk
                        if n<9:
                            nro='0000' 
                            nro=nro+str(n)
                        elif n > 9 and n <= 99:
                            nro='000' 
                            nro=nro+str(n)
                        elif n > 99 and n <= 999:
                            nro='00'
                            nro=nro+str(n)
                        elif n > 999 and n <= 9999:
                            nro='0'
                            nro=nro+str(n)
                        elif n > 9999:
                            nro=str(n)

                        procedimiento.correlativo_chk=n+1
                        procedimiento.save()

                        print("---- Creando instancia de CheckList vacía...")
                        chk = CheckList()
                        chk.nro_chk=nro
                        chk.procedimiento = procedimiento
                        chk.incidente = incidente
                        chk.save()
                        print(f"---- CheckList asociado al incidente: {incidente.codigo}")

                        # Crear items del checklist
                        for item in procedimiento.pasos.all():
                            chk_p = Check_Pasos(checklist=chk, paso=item)
                            chk_p.save()


                        # Crea  Check de Pruebas (en caso de ser un Incidente de Prueba)
                        # ============================================================
                        if incidente.test:
                            print('---- Crea Check de Ejecuciones de Prueba. test =', incidente.test)
                            print('---- Procedimiento : ', procedimiento.id,':',procedimiento.nombre)
                            # Crea Ejecucion de Prueba
                            # ------------------------
                            pruebas_proced=PruebaContingencia_V.objects.filter(procedimiento=procedimiento)
                            
                            for prba in pruebas_proced.all():
                                
                                ejec_prba=EjecucionPrueba()
                                ejec_prba.incidente=incidente
                                ejec_prba.prueba=prba
                                ejec_prba.checklist=chk
                                ejec_prba.nro_ejecucion=prba.codigo
                                ejec_prba.save()
                                print('----- Crea Ejecucion de Prueba. Prueba: ', prba.codigo)
                                print("----- ID ejec_prba:", ejec_prba.id)

                                # Crea Ejecucion de Caso de Prueba
                                casos=CasoPrueba_V.objects.filter(prueba=prba)
                                for cas in casos.all():

                                    ejec_caso=EjecucionCasoPrueba()
                                    ejec_caso.caso=cas
                                    ejec_caso.ejecucion=ejec_prba
                                    ejec_caso.nro_ejecucion=cas.codigo
                                    print("CASO ID:", cas.id)
                                    print("CASO EXISTS DB:", CasoPrueba_V.objects.filter(id=cas.id).exists())
                                    print("TABLA:", CasoPrueba_V._meta.db_table)
                                    print("MANAGED:", CasoPrueba_V._meta.managed)
                                    ejec_caso.save()
                                    print('----- Crea Caso de Prueba. Caso=', cas.codigo)



                                

                    except (Incidentes.DoesNotExist, ValueError) as e:
                        print(f"⚠️  Error al obtener incidente ({incidente_id}): {e}")

                    except Exception as e:
                        import traceback
                        print("❌ Error al crear Checklist:", e)
                        traceback.print_exc()

            else:
                print('>>>>> Estado Desactivado')
                procedimiento.esta_confirmado = False
                procedimiento.save()

            # --------------------------------------------
            # 🚀 Envío de correo (simulado)
            # --------------------------------------------
            try:
                accion = "Activado PC: " + procedimiento.nombre if nuevo_estado else "Desactivado PC: " + procedimiento.nombre
                print('Se envía correo de', accion)
            except Exception as e:
                print(f"⚠️ Error enviando correo: {e}")

            return JsonResponse({"success": True, "nuevo_estado": procedimiento.esta_activo})

        except Procedimientos_V.DoesNotExist:
            print("❌ Procedimiento no encontrado")
            return JsonResponse({"success": False, "error": "Procedimiento no encontrado"}, status=404)

        except json.JSONDecodeError:
            print("❌ Error en JSON recibido")
            return JsonResponse({"success": False, "error": "Error en JSON"}, status=400)

        except Exception as e:
            print(f"❌ Error general en toggle_procedimiento: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    elif request.method == "GET":
        procedimientos = Procedimientos_V.objects.values("id", "esta_activo")
        print('--- PC Activo ---')
        return JsonResponse(list(procedimientos), safe=False)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
import json

@csrf_exempt
def toggle_field(request, app_label, model_name, object_id):
    """
    Endpoint genérico para cambiar el valor de cualquier campo booleano
    (ACTIVA/DESACTIVA)  en cualquier modelo Django.
    """
    print('>>>>> Toggle de Switch general desde:', model_name)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        if field is None:
            return JsonResponse({"success": False, "error": "Falta 'field' en el JSON"}, status=400)

        # Obtener el modelo dinámicamente
        Model = apps.get_model(app_label, model_name)
        print('>>>>> Modelo=', Model)
        if not Model:
            print('>>>>> Modelo no encontrado')
            return JsonResponse({"success": False, "error": f"Modelo {app_label}.{model_name} no encontrado"}, status=404)

        # Obtener la instancia
        instance = Model.objects.get(id=object_id)

        # Validar que el campo exista y sea booleano
        field_obj = Model._meta.get_field(field)
        if field_obj.get_internal_type() != "BooleanField":
            return JsonResponse({"success": False, "error": f"El campo '{field}' no es booleano"}, status=400)

        # Actualizar y guardar
        setattr(instance, field, bool(value))
        instance.save()

        # Funciones segun Modelo
        #========================
        # Esta seccion se usa para incorporar funcionalidades dentro del toggle
        # segun Modelo de origen.

        if model_name == "check_pasos":
            print('---- Entra a funciones s/ Modelo:', Model)
        
            # Determina si todos los Items(pasos) han sido completados
            completado=True
            checkl=instance.checklist # Identifica el CheckList asociado al paso
            items_check=Check_Pasos.objects.filter(checklist=checkl) # Selecciona los items asociado al CheckList
            for chk in items_check:
                if not chk.terminado:
                    completado=False
            if completado:
                checkl.completado=True
            else:
                checkl.completado=False

            checkl.save()
                




        print(f"✔️ {Model.__name__}({object_id}) → {field} = {value}")

        return JsonResponse({
            "success": True,
            "model": f"{app_label}.{model_name}",
            "id": object_id,
            "field": field,
            "nuevo_estado": bool(value)
        })

    except Model.DoesNotExist:
        return JsonResponse({"success": False, "error": "Objeto no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)




#***************************************************
# 6.4 Lista PC asociados a Proceso para Activacion *
#***************************************************
@login_required
def Lista_PC_Px(request, pk, pk_padre):


    proceso_det = get_object_or_404(SubProceso, pk = pk)
    proceso_enc = get_object_or_404(Proceso, proceso = proceso_det.codigo)
    proced = proceso_det.procedimientos_contingencia

    url_ant = request.META['HTTP_REFERER']

    return render(request,'bcp/inc_mgm/pcxp_inc_list.html',
                  context={'proceso_det':proceso_det, 'proceso_enc':proceso_enc, 'proced':proced,
                           'url_ant':url_ant,'pk_padre':pk_padre}) 


#********************************************************
# 6.5 Activa/Desactiva un Procedimiento de Contingencia *
#********************************************************
@login_required
def ActivaDesactivaPc(request, pk ):
    """
    Activacion/Desactivacion del PC por el Comite de Crisis
    """

    print('pk proced', pk)
        

    proced = get_object_or_404(Procedimientos, pk = pk)

    print('activo?',proced.esta_activo)

    activo = proced.esta_activo
    
    if activo :
        print('verdadero')
        
        activo = False
                
    else:
        print('falso')
     
        activo = True
        
    proced.esta_activo = activo
    proced.save()

    
    print('Status PC=', activo)           
              
    # redirect to a new URL:
    url_ant=request.META['HTTP_REFERER']
    return HttpResponseRedirect(url_ant)


# ********************************************
# Lista de Procesos de Contingencia x Gestor *
# ********************************************
@login_required
def Lista_ProcedimientosxGestor(request):
    """
    Lista los Procedimientos asociados al Gestor en Sesion
    """

    print('>>>>> Lista de Procesos x Gestor en sesion')

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Ejecutores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[302] ))

    # Identifica a username del Gestor en Sesion
    usr=request.user
    username=usr.username
    print('username=', username)
    
    # Selecciona los Procedimientos de BCP asociados al Gestor en sesion
    # ===================================================================
    procedimientos=Procedimientos_V.objects.all()
    Lista_Procedimientos=[]
    for prc in procedimientos.all():

        # Identifica usernames
        # -------------------- 
        user_resp=prc.resp_proceso.user_gestor.username
        if prc.bck_resp:
            user_bck_r =prc.bck_resp.user_gestor.username
        else:
            user_bck_r="no definido"

        user_ejecutor =prc.gestor_ejecutor.user_gestor.username
        if prc.gestor_ejecutor:
            user_bck_e =prc.gestor_ejecutor.user_gestor.username
        else:
            user_bck_e="no definido"

        print('responsable:', user_resp, 'respaldo:', user_bck_r)
        print('ejecutor :', user_ejecutor, 'respaldo', user_bck_e)


        # Determina el rol del usuario en sesion
        # -------------------------------------- 

        if username == user_resp:
            rol='Responsable'
          
        elif username == user_bck_r:
            rol='Respaldo Responsable'

        elif username == user_ejecutor:
            rol='Ejecutor'

        elif username == user_bck_e:
            rol='Respaldo Ejecutor'
        else:
            rol='no identificado'

        # Determina el RTO asociado al Procedimiento
        # ------------------------------------------
        if rol != 'no identificado':
            proceso=get_object_or_404(Proceso, pk=prc.pk_padre) # Identifica el Proceso padre

            indicadores=proceso.subproceso_v.indicador_subp # Rescata tabla de indicadores

            for ind in indicadores.all():
                indicador_asig=ind.indicador.nombre
                indicador_nivel=ind.nivel.nivel
                if indicador_asig == "RTO":
                    rto=indicador_nivel+':'+ind.nivel.definicion
                elif indicador_asig=="RPO":
                    rpo=indicador_nivel+':'+ind.nivel.definicion

            print('---- RTO:', rto)
            print('---- RPO:', rpo)

            # Carga flags de estados
            #-----------------------
            activado  =prc.esta_activo
            confirmado=prc.esta_confirmado

            # Arma lista de Diccionario
            proced={'pc':prc,
                    'rol':rol,
                    'rto':rto,
                    'rpo':rpo,
                    'tipo':'BCP',
                    'activado':activado,
                    'confirmado':confirmado}

            Lista_Procedimientos.append(proced)

     # Selecciona los Procedimientos de DRP asociados al Gestor en sesion (Completar)
           


    return render(request,'bcp/inc_mgm/proced_list.html',
                  context={'lista_procedimientos':Lista_Procedimientos}) 



# Lista CheckList por Procediiento e Incidente *
#***********************************************
@login_required
def Lista_CheckList(request, pk):
    """
    pk: Pk del Procedimiento
    """

    print('>>>>> Entra a Listado Checklist')
    proc=get_object_or_404(Procedimientos_V, pk=pk)
    proceso=get_object_or_404(Proceso, pk=proc.pk_padre) # Identifica el Proceso padre
    lista_chk=CheckList.objects.filter(procedimiento=proc)

    # Determina el RTO asociado al Procedimiento
    # ------------------------------------------
    indicadores=proceso.subproceso_v.indicador_subp # Rescata tabla de indicadores

    for ind in indicadores.all():
        indicador_asig=ind.indicador.nombre
        indicador_nivel=ind.nivel.nivel
        if indicador_asig == "RTO":
            rto=indicador_nivel+':'+ind.nivel.definicion
        elif indicador_asig=="RPO":
            rpo=indicador_nivel+':'+ind.nivel.definicion

    print('---- RTO:', rto)
    print('---- RPO:', rpo)


    return render(request,'bcp/inc_mgm/checklist_list.html',
                  context={'lista_chk':lista_chk,
                           'proc':proc,
                           'rto':rto,
                           'rpo':rpo}) 

@login_required
def Ejecucion_CheckList(request, pk):
    """
    Registra en un  checklist la ejecucion de los pasos del Procedimiento.
    pk: Pk del Checklist
    """

    print('>>>>> Ejecucion Checklist')

    check=get_object_or_404(CheckList,pk=pk)
    proced=check.procedimiento
    items=Check_Pasos.objects.filter(checklist=check)

    # Identifica al Comite de Crisis.
    comite=[]
    gestores=Gestor.objects.all()
    for integrante in gestores:
        for grp in integrante.user_gestor.groups.all():
            if grp.name=='Gestion de Crisis':
                comite.append(integrante)
    print('---- integrantes del comite =', comite)

    # Rescata los Comentarios 
    comentarios_proceso=Log_Revision.objects.filter(procedimiento_v=proced)
    comentarios_m=[]
    for com in comentarios_proceso:
        cod=com.campo
        codigo_inc=substring(cod,0,10)
        print('---- codigo incidente=', codigo_inc)

        if com.seccion == "C":
            #Selecciona los asociados al Incidente 
            comentarios_m.append(com)




    return render(request,'bcp/inc_mgm/checklist.html',
                    context={'check':check,
                             'proced':proced,
                             'comite':comite,
                             'comentarios':comentarios_m,
                            'items':items}) 

#============================================
# Lista de Checklist de Ejecucion de Pruebas 
#============================================
@login_required
def Lista_Ejec_Prbas(request, pk):
    """
    Lista los Checklist de Ejecucion de Pruebas asociados a un incidente
    pk: pk del checklist 
    """
    checklist=get_object_or_404(CheckList, pk=pk)
    proc=checklist.procedimiento
    lista_ejec_prbas=EjecucionPrueba.objects.filter(checklist=checklist)
    print('Lista de Ejecucion de Pruebas =', lista_ejec_prbas)
 
    return render(request,'bcp/inc_mgm/ejec_prbas_list.html',
                    context={'lista_ejec_prbas':lista_ejec_prbas,
                    'checklist':checklist,
                    'proc':proc})

@login_required
def Lista_Prbas_x_Eval(request, pk, eval):
    """
    Lista las Ejecuciones de Pruebas de un incidente segun Evaluacion
    pk: pk del incidente
    eval:   Existosas
            Parciales
            Fallidas
            En Ejecucion 
    """

    incidente =get_object_or_404(Incidentes, pk=pk)
    # Selecciona las Ejecuciones de Prueba del Incidente
    lista_ejec_prbas_incidente=EjecucionPrueba.objects.filter(incidente=incidente)
    lista_ejec_prbas_eval=lista_ejec_prbas_incidente.filter(evaluacion_final=eval)


    lista_ejec_prbas=[]
    for ejec_p in lista_ejec_prbas_eval:
        ejec_casos=EjecucionCasoPrueba.objects.filter(ejecucion=ejec_p)
        ejec={'prueba':ejec_p,'casos':ejec_casos}
        lista_ejec_prbas.append(ejec)

    # Selecciona las Ejecuciones de Prueba del Incidente de acuerdo a Evaluacion
    
    print('Lista de Ejecucion de Pruebas =', lista_ejec_prbas)
 
    return render(request,'bcp/inc_mgm/prbasxeval_list.html',
                    context={'lista_ejec_prbas':lista_ejec_prbas,
                             'incidente':incidente
                             })


from .forms import EjecucionPruebasForm
@login_required
def Lista_Ejec_Casos(request, pk):
    """
    Lista los casos asociados a una Prueba de Procedimiento y registra Conclusion
    pk: pk de Ejecucion de Pruebas
    """
    print('>>>>> Entra a Evaluacion de la Prueba (lista casos)')
    ejec_prueba=get_object_or_404(EjecucionPrueba, pk=pk)
    incidente=ejec_prueba.incidente     # Incidente asociado
    prueba=ejec_prueba.prueba           # Prueba asociada
    checklist=ejec_prueba.checklist     # Checklist de PC  asociado
    proc=checklist.procedimiento        # Procedimiento asociado

    lista_ejec_casos=EjecucionCasoPrueba.objects.filter(ejecucion=ejec_prueba)

    # Registro de Conclusion

    if request.method=='POST':
        print('---- metodo POST')
        form = EjecucionPruebasForm(request.POST)
        
        if form.is_valid():
            print('----- Formato valido')
         
        
            # Rescata datos del formulario
            # ============================
            descripcion_ejecucion=form.cleaned_data['descripcion_ejecucion']
            incidentes=form.cleaned_data['incidentes']
            resultados_obtenidos=form.cleaned_data['resultados_obtenidos']
            evaluacion_final=form.cleaned_data['evaluacion_final']
            lecciones_aprendidas=form.cleaned_data['lecciones_aprendidas']
            archivo=form.cleaned_data['evidencia_general']

            # Validaciones de contexto
            # ========================

            # ----------------------------------------------------------------------
            # Valida si la conclusion de la Prueba Exitosa o Fallida es coherente
            # con la evaluacion de casos de Alta prioridad. No se puede concluir
            # si hay casos de prioridad Alta no concluidos como Exitosa o Fallida.
            # ---------------------------------------------------------------------- 
            evaluacion_final_ok=True
            if evaluacion_final !='En Ejecucion':
                print('---- Entra a validacion con Evaluacion =', evaluacion_final)
                
                for caso in lista_ejec_casos:
                    prioridad=caso.caso.prioridad #Identifica prioridad del caso de prueba
                    print('---- prioridad caso =', prioridad)
                    if prioridad=='Alta':
                        if  caso.resultado == 'No Aplica' or caso.resultado == 'En Proceso' :
                            evaluacion_final_ok=False
            

            # Graba Registro en la BD
            # ------------------------
            print('---- Graba Registro ')
            ejec_prueba.descripcion_ejecucion = descripcion_ejecucion
            ejec_prueba.incidentes = incidentes
            ejec_prueba.resultados_obtenidos = resultados_obtenidos
            ejec_prueba.lecciones_aprendidas = lecciones_aprendidas

            # Graba Archivo Adjunto. 
            # -----------------------
            print('---- ARCHIVO =', archivo)
            if archivo is False:
                # Usuario marcó "clear"
                ejec_prueba.evidencia_general.delete(save=False)
                ejec_prueba.evidencia_general = None

            elif archivo:
                # Usuario subió archivo nuevo
                ejec_prueba.evidencia_general = archivo

            # Valida  Evaluacion Final
            # ----------------------------
            if evaluacion_final_ok:
                ejec_prueba.evaluacion_final = evaluacion_final

            else:
                ejec_prueba.save() # Mantiene datos preliminares (excepto la evaluacion)
                return HttpResponseRedirect(reverse('error-sesion-mgm', args=[5000] ))

            ejec_prueba.save()
          
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Ejec-Prbas',  args=[str(checklist.id)]))
            

        else:

            print('Form invalido', form.errors)
            #return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            return render(request, 'bcp/inc_mgm/ejec_casos_list.html',{'form':form })

    else:

        form=EjecucionPruebasForm( initial= { 'descripcion_ejecucion':ejec_prueba.descripcion_ejecucion,
                                             'incidentes':ejec_prueba.incidentes,
                                            'resultados_obtenidos':ejec_prueba.resultados_obtenidos,
                                           'evaluacion_final':ejec_prueba.evaluacion_final,
                                           'lecciones_aprendidas':ejec_prueba.lecciones_aprendidas,
                                           'evidencia_general':ejec_prueba.evidencia_general})
        

        return render(request,'bcp/inc_mgm/ejec_casos_list.html',   
                            context={'lista_ejec_casos':lista_ejec_casos,
                                    'incidente':incidente,
                                    'prueba':prueba,
                                    'ejec':ejec_prueba,
                                    'checklist':checklist,
                                    'proc':proc,
                                    'form':form})



#============================================
# Checklist de Ejecucion de Pruebas 
#============================================
@login_required
def Ejec_Prba(request, pk):
    """
    Lista los Checklist de Ejecucion de Pruebas asociados a un incidente
    pk: pk del checklist de ejecucion 
    """
    checklist_ejec=get_object_or_404(EjecucionPrueba, pk=pk)
    proc=checklist_ejec.checklist.procedimiento
    lista_ejec_casos=EjecucionCasoPrueba.objects.filter(ejecucion=checklist_ejec)
    print('Lista de Ejecucion de Pruebas =', lista_ejec_casos)


    if request.method=='POST':
        print('---- metodo POST')
        form = Plan_Pruebas_A_Form(request.POST)
        
        if form.is_valid():
            print('----- Formato valido')
         
           
            
            # Graba intancias en Registro (Base de Incidentes)

              
            #Graba en BD
            print('Grabo incidente')
            

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Define-Plan-Pruebas-B',  args=[str(incidente.id)]))
            

        else:

            print('Form invalido', form.errors)
            #return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            return render(request, 'bcp/inc_mgm/ejec_prba.html',{'form':form })

    else:

        return render(request,'bcp/inc_mgm/ejec_prba.html',
                        context={'checklist_ejec':checklist_ejec,
                                'lista_ejec_casos':lista_ejec_casos,
                                'proc':proc})


from .forms import EjecucionCasoPruebaForm
@login_required
def Ejec_Caso(request, pk):
    """
    Ejecuta Caso de Prueba de Procedimiento asociados a un incidente
    pk: pk de la Ejecucion de Caso  
    """

    # Aplicar solo una vez (Borrar) --------------------------------------------
    from bcp.models import EjecucionCasoPrueba
    EjecucionCasoPrueba.objects.filter(evidencia='False').update(evidencia=None)
    # Borrar -----------------------------------------

    print('>>>>> Registra Ejecucion del Caso')
    caso_ejec=get_object_or_404(EjecucionCasoPrueba, pk=pk)
    prba_ejec=caso_ejec.ejecucion
    checklist=prba_ejec.checklist           # Prueba asociada al Caso
    proc=prba_ejec.checklist.procedimiento  # Procedimiento asociado al Caso

    if request.method=='POST':
        print('---- metodo POST')
        form = EjecucionCasoPruebaForm(request.POST, request.FILES)
        
        if form.is_valid():
            print('----- Formato valido')
            #form.save()

            # Rescata datos del Fromulario
            # ---------------------------- 
            resultado = form.cleaned_data['resultado']
            observaciones = form.cleaned_data['observaciones']
            archivo = form.cleaned_data['evidencia']

            # Graba Registros en BD
            # ---------------------

            # Graba Archivo Adjunto. 
            print('---- ARCHIVO =', archivo)
            if archivo is False:
                print('---- archivo es Falso')
                # Usuario marcó "clear"
                caso_ejec.evidencia.delete(save=False)
                caso_ejec.evidencia = None

            elif archivo:
                # Usuario subió archivo nuevo
                caso_ejec.evidencia = archivo

            caso_ejec.observaciones = observaciones

            # Valida  Evaluacion Final
            # ----------------------------
            esta_ok = True
            print('---- Valida resultado=', resultado)
            if  resultado == 'No Aplica':
                print('------- valida con resultado=', resultado)

                # El caso no debe ser de Prioridad Alta
                if caso_ejec.caso.prioridad == 'Alta':
                    esta_ok=False
                    caso_ejec.save() # Mantiene datos preliminares (excepto la evaluacion)
                    return HttpResponseRedirect(reverse('error-sesion-mgm', args=[5001] ))
            
            elif resultado == 'Exitosa':
                print('------- valida con resultado=', resultado)

                # Debe tener archivo adjunto
                print('------- archivo : ', archivo, 'en BD : ', caso_ejec.evidencia )
                if not archivo and not caso_ejec.evidencia :
                    esta_ok=False
                    print('----- No hay archivo adjunto')    
                    caso_ejec.save() # Mantiene datos preliminares (excepto la evaluacion)
                    return HttpResponseRedirect(reverse('error-sesion-mgm', args=[5002] ))
            

            elif resultado == 'Fallida':
                print('------- valida con resultado=', resultado)
                
                # Debe tener Observaciones. 
                if  len(observaciones)<=3:
                # Valida que si que se redacte un minimo de observaciones.
                    esta_ok=False 
                    caso_ejec.save() # Mantiene datos preliminares (excepto la evaluacion)
                    return HttpResponseRedirect(reverse('error-sesion-mgm', args=[5003] ))


            if esta_ok:
                caso_ejec.resultado=resultado


            # else: no tocar
            caso_ejec.save()

            print('---- Graba instancia caso_ejec :', caso_ejec)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Ejec-Casos',  args=[str(prba_ejec.id)]))
            

        else:

            print('Form invalido', form.errors)
            #return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
            return render(request, 'bcp/inc_mgm/ejec_caso.html',{'form':form })

    else:

        form=EjecucionCasoPruebaForm(initial={'resultado':caso_ejec.resultado,
                                              'observaciones':caso_ejec.observaciones,
                                              'evidencia':caso_ejec.evidencia})

        return render(request,'bcp/inc_mgm/ejec_caso.html',
                        context={'caso_ejec':caso_ejec,
                                 'checklist':checklist,
                                'ejec':prba_ejec, # Se adapto al Template (ejec)
                                'proc':proc,
                                'form':form})


# ===================================
# Dashboard y Reportes de Pruebas
# ===================================

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum

from .models import (
    Incidentes, EjecucionPrueba, Indicadores_Asig_v, 
    EjecucionCasoPrueba, Impactos_Asig_v  # Recuperado explícitamente
)
#import json
from django.shortcuts import render


# Versión 35 | Lógica de recuperación de datos por jerarquía de modelos
def reporte_prueba(request, pk):

    print('>>>>> DASHBOARD Y REPORTE DE PRUEBAS')

    # Obtenemos el incidente (que es el disparador del reporte)
    incidente = get_object_or_404(Incidentes, pk=pk)
    print('---- incidente :', incidente.codigo, 'descripcion :', incidente.descripcion)
    

    # Procesos asociados
    # ==================
    procesos=incidente.procesos_i.all()
    n_procesos=procesos.count()
    print('---- Nro.de Procesos : ', n_procesos)

    context=({'incidente':incidente,
              'procesos':procesos,
              'n_procesos':n_procesos})
    

    # Escenarios asociados
    # ====================
    escenarios_del_incidente=incidente.escenarios_i.all()
    n_escenarios=escenarios_del_incidente.count()
    context.update({'escenarios':escenarios_del_incidente,
             'n_escenarios':n_escenarios})
    print('---- Nro. de Escenarios : ', n_escenarios)

    # PC asociados
    # ============
    lista_proced = []
    cont_pc=0
    cont_pc_activos=0
    cont_pc_confirm=0

    # Obtiene los PCs asociados a cada proceso
    for proc in procesos.all():
        
        PC = Procedimientos_V.objects.filter(subproceso=proc)

        print('------ Proceso :', proc.nombre)
        # Selecciona los PC asociados a los Escenarios del Incidente
        for proced in PC:

            if proced.escenarios in escenarios_del_incidente:
            # Si el PC esta asociado a algun escenario del Incidente
                cont_pc += 1
                if proced.esta_activo == True:
                    cont_pc_activos += 1
                if proced.esta_confirmado == True:
                    cont_pc_confirm  += 1

                lista_proced.append(PC)
                print('------- PC : ', proced.nombre,'-', proced.escenarios.titulo)


    print('---- Totales:')
    print('---- Nro. PCs :', cont_pc)
    print('---- Nro. PC Activos : ', cont_pc_activos)
    print('---- Nro. PC confirmados : ', cont_pc_confirm)
    print('---- Lista de PC : ', lista_proced)

    context.update({
            'lista_proced': lista_proced,
            'cont_pc': cont_pc,
            'cont_pc_activos':cont_pc_activos,
            'cont_pc_confirm':cont_pc_confirm,
        })


    # Pruebas 
    # =================================================
    print('---- PRUEBAS')
    ejecucion_prbas = EjecucionPrueba.objects.filter(incidente=incidente)
    cont_pruebas=ejecucion_prbas.count()
    
    prbas_exitosas = ejecucion_prbas.filter(evaluacion_final='Exitosa')
    cont_prbas_exitosas = prbas_exitosas.count()

    prbas_parciales = ejecucion_prbas.filter(evaluacion_final='Parcial')
    cont_prbas_parciales = prbas_parciales.count()

    prbas_fallidas = ejecucion_prbas.filter(evaluacion_final='Fallidas')
    cont_prbas_fallidas = prbas_fallidas.count()

    prbas_en_ejecucion = ejecucion_prbas.filter(evaluacion_final='En Ejecucion')
    cont_prbas_en_ejecucion = prbas_en_ejecucion.count()

    print('---- Nro. Pruebas', cont_pruebas)
    print('---- Nro. P. exitosas', cont_prbas_exitosas)
    print('---- Nro. P. parciales', cont_prbas_parciales)
    print('---- Nro. P. fallidas', cont_prbas_fallidas)
    print('---- Nro. P. en ejecucion', cont_prbas_en_ejecucion)

    #P100_prbas_exitosas  = cont_prbas_exitosas/cont_pruebas*100
    P100_prbas_exitosas  = 0.35*100
    #P100_prbas_parciales = cont_prbas_parciales/cont_pruebas*100
    P100_prbas_parciales = 0.15*100
    #P100_prbas_fallidas   = cont_prbas_fallidas/cont_pruebas*100
    P100_prbas_fallidas   = 0.10*100
    #P100_prbas_en_ejecucion = cont_prbas_en_ejecucion/cont_pruebas*100
    P100_prbas_en_ejecucion = 0.40*100

    print('% Pruebas Exitosas : ', P100_prbas_exitosas)
    print('% Pruebas Parciales : ', P100_prbas_parciales)
    print('% Pruebas Fallidas  : ', P100_prbas_fallidas)
    print('% Pruebas En Ejecucion : ', P100_prbas_en_ejecucion)


    context.update({
            'ejecucion_prbas':ejecucion_prbas,
            'cont_pruebas': cont_pruebas,
            'prbas_exitosas':prbas_exitosas,
            'cont_prbas_exitosas':cont_prbas_exitosas,
            'prbas_parciales':prbas_parciales,
            'cont_prbas_parciales':cont_prbas_parciales,
            'prbas_fallidas':prbas_fallidas,
            'cont_prbas_fallidas':cont_prbas_fallidas,
            'prbas_en_ejecucion':prbas_en_ejecucion,
            'cont_prbas_en_ejecucion':cont_prbas_en_ejecucion,

            'P100_prbas_exitosas':P100_prbas_exitosas,
            'P100_prbas_parciales':P100_prbas_parciales,
            'P100_prbas_fallidas':P100_prbas_fallidas,
            'P100_prbas_en_ejecucion':P100_prbas_en_ejecucion

        })
    
    # Prepara grafico
    # ===============

    # Ejemplo de datos obtenidos por tus Queries
    import json

    data = {
        "Exitosas": float(P100_prbas_exitosas or 0),
        "Parciales": float(P100_prbas_parciales or 0),
        "Fallidas": float(P100_prbas_fallidas or 0),
        "En Ejecucion": float(P100_prbas_en_ejecucion or 0),
    }

    colors = {
        "Exitosas": "#2ecc71",
        "Parciales": "#f1c40f",
        "Fallidas": "#e74c3c",
        "En Ejecucion": "#3498db",
    }

    context.update({
        "chart_data": data,
        "chart_colors": colors,
    })


    print('---- Pruebas')
    #.select_related(
    #    'prueba__procedimiento__subproceso', 'prueba__responsable'
    #).order_by('-fecha_real').first()
    for prba in ejecucion_prbas:
        print('----- Prueba :', prba.prueba.codigo, 'objetivo :', prba.prueba.objetivo)

        

    template = 'bcp/reportes/reporte_formal.html' if 'formal' in request.GET else 'bcp/reportes/dashboard_ejecucion.html'
    return render(request, template, context)


    
#*********************************************** Fin Administracion del Incidente *********************************************************
   
#*********************************************************************************************************************************************
#***********************************************  6. Maestros ********************************************************************************
#*********************************************************************************************************************************************
@login_required
def Menu_Conf(request):
    """
    Menu para la definicion de Datos Fijos
    """
    print('menu conf')
   
    if not es_del_grupo([request.user, 'Administradores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[100] ))
        
    return render(request,'bcp/conf/menu_conf.html')


#******************************************
#       Mantencion Gestores/Usuarios      *
#******************************************

from .forms import Crea_Gestor_Form, Crea_Gestor2_Form
@login_required
def Crea_G(request):
    """
    Creacion de un usuario o gestor
    """

    print('crea gestor')

    # Codigo para borrar Base de Gestores
    #gest= Gestor.objects.all()
    #for i in gest.all():
    #    i.delete()
    #return HttpResponseRedirect(reverse('menu-conf') )
    
   
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = Crea_Gestor_Form(request.POST)
        form2= Crea_Gestor2_Form(request.POST)

        # Check if the form is valid:
        if form.is_valid() and form2.is_valid():
            
            
            #Crea el Registro del Proceso

            # Registro en Tabla User
            user = User()
           
            username = form.cleaned_data['username']
            user.username=username
            
            # Crea Hash para passord y asigna a user
            pwd=make_password(form.cleaned_data['password1'])
            print('PWD=', pwd)
            user.password = pwd

            
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.is_staff = True


            # Registro en Tabla Gestor
            gestor = Gestor()
                     
            gestor.cargo = form2.cleaned_data['cargo']
            gestor.area  = form2.cleaned_data['area']
            gestor.fono_t = form2.cleaned_data['fono_t']
            gestor.cod_area = form2.cleaned_data['cod_area']
            gestor.fono_c = form2.cleaned_data['fono_c']
            gestor.apellido = form.cleaned_data['last_name']

            user.save()
            gestor.save()

            gestor.user_pk = user.pk
            gestor.user_gestor=user
            gestor.save()
            
          
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('menu-conf') )
        
        else:
            
            print (dict(form.errors))
            for error  in form.errors:
                
                print ('campo error:', error)
                print ('mensaje :', form.errors[error])
                                    
                #return HttpResponseRedirect(reverse('error-mgm', args=[mensaje]))
                return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors, 'form2':form2.errors} )
                #form = Crea_Gestor_Form(request.POST, data=form.errors)
                #return render(request, 'bcp/conf/crea_gestor.html', {'form':form} )

    # If this is a GET (or any other method) create the default form.
    else:

        form = Crea_Gestor_Form()
        form2= Crea_Gestor2_Form()
        
        return render(request, 'bcp/conf/crea_gestor.html', {'form':form, 'form2':form2} )


from .forms import Borra_Gestor_Form

@login_required
def Borra_Gestor(request):

    """
    Borra al usuario Gestor de la Base
    """
    

    if request.method == 'POST':

        form=Borra_Gestor_Form(request.POST)

        if form.is_valid():

            usuario = form.cleaned_data['usuario']
            confirma_borra = form.cleaned_data['confirma_borra']
            confirma_desactiva = form.cleaned_data['confirma_desactiva']

            usr = get_object_or_404(User, username = usuario.user_gestor.username )
            print('usr.pk=', usr.pk)
             
            if confirma_desactiva:

                usr.is_active = False
                usr.save()
                
            if confirma_borra:
                
                ges = get_object_or_404(Gestor, user_pk = usr.pk)

                ges.delete()
                usr.delete()
                
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('menu-conf') )

        else:

            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})   


    else:
        
        form = Borra_Gestor_Form()
        
    return render(request,'bcp/conf/borra_gestor.html', {'form':form})
    


class GestorListView(generic.ListView):
    """
    Generic class-based view listing - Listado de Gestores para asignacion de Grupos.
    """
    model = Gestor
    template_name='bcp/conf/gestor_list.html'


    #def get_queryset(self):
    #    return Proceso.objects.filter(Proceso.es_subproceso=True).filter(Proceso.subproceso.fase_status=='M')|Proceso.objects.filter(proceso.subproceso.fase_status=='B') 


#********************************
#4.2 Asigna Grupos a Usuario    *
#********************************
from .forms import Asigna_Grupo_Form

#@permission_required('Catalogo.can_mark_returned')
@login_required
def Asigna_Grupo(request, pk):
    
    model = User
    usuario = get_object_or_404(User, pk = pk)
    gestor =  get_object_or_404(Gestor, user_pk = pk)

    print (usuario.last_name, '=', gestor.user_gestor.last_name)
    
    print('usuario=', usuario)

    
    if request.method=='POST':
        print('entra a POST ASIGNA GRUPO')
        form = Asigna_Grupo_Form(request.POST)
        
        if form.is_valid():
            
            #Graba intancias en Registro
            gr= form.cleaned_data['grupos']
            print('grupos=',gr)
            
            usuario.groups.set(gr)
            #usuario.groups.set(p1)

            usuario.save()
           


            # redirect to a new URL:
            return HttpResponseRedirect(reverse('lista-gestores') )
            
        else:

                    
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        p2 = usuario.groups.all()
        form = Asigna_Grupo_Form(initial= {'grupos':set(p2)})
                                        
        return render(request, 'bcp/conf/asigna_grupos.html', {'form': form, 'usuario':usuario})



# **********************************
# Administracion de Riesgo/Impacto *
# **********************************
@login_required
def Lista_riesgos(request):

    print('Entra a Lista Impactos')

    riesgos=Tipo_Impacto_P.objects.all()

    total=00.00
    resto=00.00
    for imp in riesgos:
        total=float(imp.ponderacion)+float(total)
    
    print('total=', total)

    menor_a_100 = False
    if total < 100.00:
        menor_a_100 = True
        resto=100-total

    print('menor_a_100', menor_a_100)

    return render(request, 'bcp/ria/lista_riesgos.html', {'riesgos':riesgos,
                                                           'menor_a_100':menor_a_100,
                                                           'resto':resto})


from .forms import Crea_Impacto_Form
@login_required
def Crea_Impacto(request):
    """
    Crea un Registro de Riesgo/Impacto propuesto
    """

    impactos=Tipo_Impacto_P.objects.all()
    total=00.00
    for imp in impactos:
        total=float(imp.ponderacion)+float(total)
    resto=100-total

    if request.method=='POST':

        form = Crea_Impacto_Form(request.POST)
        
        if form.is_valid():
            
            # Crea Registro 

            ponderacion=form.cleaned_data['ponderacion']

            total=float(ponderacion)+total

            if total > 100.00:
                return HttpResponseRedirect(reverse('error-sesion-mgm', args=[3000] ))
            else:
                # Crea Registro 

                impacto=Tipo_Impacto_P()
                impacto.nombre=form.cleaned_data['nombre']
                impacto.descripcion=form.cleaned_data['descripcion']
                impacto.ponderacion=ponderacion           
                
                impacto.save()

                return HttpResponseRedirect(reverse('Lista-Impactos') )
         
        else:
                  
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
        
        form = Crea_Impacto_Form(initial={'ponderacion':resto})
                                        
        return render(request, 'bcp/ria/crea_impacto.html', {'form':form })


from .forms import Crea_Impacto_Form
@login_required
def Mod_Impacto(request, pk):
    """
    Crea un Registro de Riesgo/Impacto
    pk: pk del Impacto
    """
    print('---- Entra a Modifica Impacto ------')
    impacto=get_object_or_404(Tipo_Impacto_P, pk=pk)
    impactos=Tipo_Impacto_P.objects.all()
    total=00.00
    for imp in impactos:
        if imp.pk != impacto.pk:
            print('ponderacion =', imp.ponderacion)
            total=float(imp.ponderacion)+float(total)

    print('precalculo total=', total)


    if request.method=='POST':

        form = Crea_Impacto_Form(request.POST)
        
        if form.is_valid():
            
            # Modifica Registro 

            ponderacion=form.cleaned_data['ponderacion']

            total=float(ponderacion)+total
            print('total=',total)

            if total > 100.00:
                return HttpResponseRedirect(reverse('error-sesion-mgm', args=[3000] ))
            else:
                # Modifica Registro 

                impacto.nombre=form.cleaned_data['nombre']
                impacto.descripcion=form.cleaned_data['descripcion']
                impacto.ponderacion=ponderacion           
                
                impacto.save()

                return HttpResponseRedirect(reverse('Lista-Impactos') )
            
        else:
                  
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
        
        form = Crea_Impacto_Form(initial={'nombre':impacto.nombre,
                                          'descripcion':impacto.descripcion,
                                          'ponderacion':impacto.ponderacion})
                                        
        return render(request, 'bcp/ria/mod_impacto.html', {'form':form })

@login_required
def Borra_Impacto(request, pk):
    """
    Borra el Registro de Riesgo/Impacto
    """

    impacto=get_object_or_404(Tipo_Impacto_P, pk=pk)
    impacto.delete()

    return HttpResponseRedirect(reverse('Lista-Impactos') )

@login_required
def Lista_Nivel_Impactos(request, pk):
    """
    Lista los niveles de impacto del riesgo pk (propuestos)
    """
    print('Entra a Lista Nivel Impactos')

    riesgo=get_object_or_404(Tipo_Impacto_P, pk=pk)
    niveles = Nivel_Impacto_P.objects.filter(tipo=riesgo)



    return render(request, 'bcp/ria/lista_nivel_imp.html', {'niveles':niveles,
                                                            'riesgo':riesgo})


from .forms import Crea_Nivel_Imp_Form
@login_required
def Crea_Nivel_Impacto(request, pk):
    """
    Crea un nivel asociada al riesgo pk
    """

    riesgo=get_object_or_404(Tipo_Impacto_P, pk=pk)

    if request.method=='POST':

        form = Crea_Nivel_Imp_Form(request.POST)
        
        if form.is_valid():
            
            # Crea Registro 

            nivel=Nivel_Impacto_P()
            nivel.nombre=form.cleaned_data['nombre']
            nivel.descripcion=form.cleaned_data['descripcion']
            nivel.valor=form.cleaned_data['valor']
            nivel.tipo=riesgo
            nivel.save()

            return HttpResponseRedirect(reverse('Lista-Impactos') )
         
        else:
                  
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
        
        form = Crea_Nivel_Imp_Form()
    

    return render(request, 'bcp/ria/crea_nivel_impacto.html', {'riesgo':riesgo, 'form':form})


#*********************************************************************************************************************************************
#***********************************************  8. Proposito General ***********************************************************************
#*********************************************************************************************************************************************

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings

from bcp.models import Gestor
from bcp.services.seguridad import generar_clave_temporal
def olvido_clave(request):
    """
    Flujo 'Olvidó su clave':
    - Usuario NO autenticado
    - Genera clave temporal
    - Envía correo
    - Fuerza cambio de clave en el próximo login
    """

    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username, is_active=True)
            Gestor.objects.get(user_gestor=user)
        except (User.DoesNotExist, Gestor.DoesNotExist):
            return render(
                request,
                'auth/olvido_clave.html',
                {'error': 'Usuario no válido o no registrado'}
            )

        # 1️⃣ Generar clave temporal
        clave_temporal = generar_clave_temporal()
        print('CLAVE TEMPORAL : ', clave_temporal)

        # 2️⃣ Asignar nueva clave
        user.set_password(clave_temporal)
        user.save()

        # 3️⃣ Forzar cambio de clave en el próximo login
        gestor = Gestor.objects.get(user_gestor=user)
        gestor.must_change_password = True
        gestor.save()

        # 4️⃣ Enviar correo
        print('Envia Correo')
        #send_mail(
        #    subject='DEFCON – Restablecimiento de clave',
        #    message=(
        #        f'Estimado/a {user.first_name},\n\n'
        #        f'Su nueva clave temporal es:\n\n'
        #        f'   {clave_temporal}\n\n'
        #        f'Deberá cambiarla obligatoriamente al iniciar sesión.\n\n'
        #        f'Saludos,\n'
        #        f'Equipo DEFCON'
        #    ),
        #    from_email=settings.DEFAULT_FROM_EMAIL,
        #    recipient_list=[user.email],
        #    fail_silently=False
        #)

        return render(request, 'auth/olvido_clave_ok.html')

    # GET
    return render(request, 'auth/olvido_clave.html')

#******************
#Reseteo de Clave *
#******************

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from bcp.models import Gestor
from bcp.services.seguridad import resetear_clave_gestor

@login_required
@permission_required('auth.change_user')
def reset_clave_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    resetear_clave_gestor(gestor)
    return redirect('lista_gestores')


#******************
#Cambio de Clave  *
#******************

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def cambiar_clave(request):
    """
    Cambia la Clave del Usuario
    """
    
    gestor = get_object_or_404(Gestor, user_gestor=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            gestor.must_change_password = False
            gestor.save()

            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
        form = PasswordChangeForm(
                                        request.user,
                                        label_suffix='',
                                    )
        form.fields['old_password'].label = 'Clave actual'
        form.fields['new_password1'].label = 'Nueva clave'
        form.fields['new_password2'].label = 'Confirmar nueva clave'


    return render(request, 'auth/cambiar_clave.html', {'form': form})


# ***********************************
# Despliegue de cuadro informativo
# ***********************************

import json
from django.apps import apps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

@csrf_exempt
def api_detalle_modelo(request):

    try:
        data = json.loads(request.body)

        modelo_nombre = data['modelo']
        obj_id = data['id']
        lista_campos = data['listaCampos']

        Modelo = apps.get_model('bcp', modelo_nombre) if modelo_nombre != 'User' else User
        obj = Modelo.objects.get(pk=obj_id)

        if modelo_nombre == 'User' and request.user.id != obj.id:
            raise PermissionDenied

        resultado = []

        for label, path in lista_campos.items():

            partes = path.split('.')
            actual = obj

            # Resolver path completo
            for parte in partes:
                actual = getattr(actual, parte, None)
                if actual is None:
                    break

            if actual is None:
                resultado.append({'label': label, 'valor': ''})
                continue

            # MANY TO MANY (groups)
            if hasattr(actual, 'all'):
                resultado.append({
                    'label': label,
                    'lista': [str(x) for x in actual.all()]
                })
            else:
                resultado.append({
                    'label': label,
                    'valor': str(actual)
                })

        return JsonResponse({'campos': resultado})

    except PermissionDenied:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    except Exception as e:
        return JsonResponse(
            {'error': f'Excepción interna: {str(e)}'},
            status=500
        )


#*****************************
#Manda correo de Notificacion*
#*****************************

from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
@login_required
def Manda_Correo(email,cc_email,nombre,proceso, accion):

    context = {'email':email, 'nombre':nombre,'proceso':proceso, 'accion':accion}
    plantilla = get_template('bcp/mensajes/mensaje1.html')
    contenido = plantilla.render(context)

    correo= EmailMultiAlternatives(
        'DEFCON 5 / bcp - Autorizacion de Proceso',
        'Aprobacion de Proceso ',
        settings.EMAIL_HOST_USER,
        [email],
        cc=[cc_email]
    )

    correo.attach_alternative(contenido,'text/html')
    correo.send()


#*******************
#Manejo de Errores *
#*******************

def Err_Sesion_Mgm(request, ce):
#def err_mgm(request, mensaje):

    print('---- Manejo de Error de Sesion -----')
    print('codigo error:',ce)

    #user=user.request
    
    #if user.is_authenticated:
        #mensaje='Debe iniciar sesion con su nombre de usuario y clave'
        
    #if not request.user.is_authenticated:
    #    mensaje='El Usuario no esta en una sesion autenticada. Inicie sesion con su username y clave '
    #   ce='NA'

    if ce == '100':
        mensaje='100: Usuario debe pertenecer al grupo de Administracion'
        
    elif ce == '200':
        mensaje='200: Usuario debe pertenecer al grupo de Consultores'

    elif ce == '300':
        mensaje='300: Usuario debe pertenecer al grupo de Autorizadores'

    elif ce== '301':
            mensaje='301: Usuario debe pertenecer al grupo de Consultores o  Autorizadores'

    elif ce== '302':
            mensaje='301: Usuario debe pertenecer al grupo de Autorizadores o Ejecutores'
            
    elif ce == '400':
         mensaje='400: Usuario debe pertenecer al grupo de Gestion de Crisis'

    elif ce == '500':
         mensaje='500: Usuario debe pertenecer al grupo TI'
         
    elif ce == '600':
        mensaje='Debe abrir una sesion mediante su nombre de usuario y clave'

    elif ce == '3000':
        mensaje='3000: La Poderacion no puede superar el 100 %'

    elif ce == '3001':
        mensaje='3001 : Puntaje no puede ser 0'

    elif ce == '4000':
        mensaje='El Formulario ya fue enviado y ha sido bloquedo para edicion '

    elif ce == '5000':   # Errores en Evaluacion de la Prueba
        mensaje='Todos los Casos de prioridad "Alta" deben se evaluados como "Exitosos" o "Fallidos" '

    elif ce == '5001':   # Errores en Evaluacion del Caso
        mensaje='No se puede asignar "No Aplica" a Casos de prioridad "Alta".'
    elif ce == '5002':   # Errores en Evaluacion del Caso
        mensaje='Debe adjuntar Evidencia.'
    elif ce == '5003':   # Errores en Evaluacion del Caso
        mensaje='Debe indicar en "Observaciones", las causas  de la falla del Caso de Prueba.'


    else:
        mensaje='Error de Sesion no identificado.'
        
 
    return render(request, 'bcp/mensajes/mensajes_error_sesion.html', context={'mensaje':mensaje,
                                                                               'error':ce}) 

#*******************************
#Valida el acceso de la sesion *
#*******************************

def es_del_grupo(self, **grupos):
   
    print('----- Verifica si es del grupo ----')
    usr_s=self[0]
    grp=self[1:]
    print('usr_s=',usr_s)
    print('grp=',grp)

    es_del_grupo = usr_s.groups.filter(name__in=grp).exists()
    print(es_del_grupo)
 
    
    #return usr_s.groups.filter(name__in=grp).exists()
    return es_del_grupo


#*******************************
#      Manejo de Graficos      *
#*******************************
from django.http.response import JsonResponse

def get_chart(request):
    print('---- Get Chart ---')
   
    serie=[5,4,3,2]

    chart={ 
        'xAxis':[
            {
                'type':'category',
                'data':['RTO','RPO','MDT']
            }
        ],
        'yAxis':[
            {
                'type':'value'
            }
        ],
        'series':[
            {
                'data':serie,
                'type':'line'
            } 
        ]
    }
    
    return JsonResponse(chart)


def selec_usr(grupos):
    """
    funcion que devuelve una lista con los usuarios asociados al grupo.
    
    :param grupos: grupos de usuarios
    """

    seleccion=[]
    gestores=Gestor.objects.all()
    for ges in gestores:
        grp=ges.user_gestor.groups
        for g in grp.all():
            if g.name in grupos:
                seleccion.append(ges.user_pk)
    
    return seleccion 


#**************
# Reinicia BD *
#**************

from django.http import HttpResponse
from django.db import connection
from django.conf import settings

from .forms import Reset
@login_required
def reset(request):
    """ Reinicia toda la Base de Datos"""
    print('**** REINICIA BASE DE DATOS *****')
    print('--- Método HTTP recibido:', request.method) 

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Administradores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[100] ))

    # Modelos a Reiniciar
    modelos = [
        Proceso, SubProceso, SubProceso_V, Incidentes,
        Procedimientos, Contactos_PC, Servicios_PC, Pasos_PC,
        Procedimientos_V, Contactos_PC_V, Servicios_PC_V, Pasos_PC_V,
        Impactos_Asig, Indicadores_Asig, Impactos_Asig_v, Indicadores_Asig_v 
    ]

    print('prepost')
    if request.method=='POST':

        print('post-post')
        form=Reset(request.POST)

        engine = settings.DATABASES['default']['ENGINE']
        print('Metodo=Post,  BD=', engine)
        resultados = []

                    
        if form.is_valid():


            with connection.cursor() as cursor:  # Permite usar comandos del DBMS

                #Borra Registros
                print('--- Borra registros')
                for modelo in modelos:
                    table_name = modelo._meta.db_table
                    modelo.objects.all().delete()

                    # Reinicia el id=1
                    print('--- Reinicia Id.')
                    try:
                        if 'postgresql' in engine:
                            seq_name = f"{table_name}_id_seq"
                            cursor.execute(f"ALTER SEQUENCE {seq_name} RESTART WITH 1;")
                            resultados.append(f"{table_name}: Registros eliminados, ID reiniciado (PostgreSQL).")
                        elif 'sqlite' in engine:
                            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
                            resultados.append(f"{table_name}: Registros eliminados, ID reiniciado (SQLite).")
                        elif 'mysql' in engine:
                            cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
                            resultados.append(f"{table_name}: Registros eliminados, ID reiniciado (MySQL).")
                        else:
                            resultados.append(f"{table_name}: Motor de BD no compatible.")
                    except Exception as e:
                        resultados.append(f"{table_name}: Error al reiniciar ID -> {str(e)}")
                           

            # Crea Proceso Raiz
            print('--- Crea Proceso Raiz')
            raiz= form.cleaned_data['raiz']
            proceso=Proceso()
            proceso.proceso='0'
            proceso.nombre=raiz
            proceso.nro_hijos=0
            proceso.save()

            # Vuelve a la pagina Principal 
            return HttpResponseRedirect(reverse('index'))

        else:
            print(form.errors)
            return render(request, 'bcp/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = Reset()
                                 
        return render(request, 'bcp/conf/reset.html', {'form': form})


### Codigo temporal para cargar usuarios y grupos a produccion
from django.core.management import call_command
from django.http import HttpResponse
import os
@login_required
def importa_usuarios(request):
    try:
        ruta_fixture = os.path.join('bcp', 'fixtures', 'usuarios.json')
        call_command('loaddata', ruta_fixture, verbosity=0)
        return HttpResponse("✅ Usuarios y grupos importados correctamente.")
    except Exception as e:
        return HttpResponse(f"❌ Error al importar usuarios: {e}")
    

import os
from django.core.management import call_command
from django.http import HttpResponse

# Puedes agregar @staff_member_required si deseas restringir
# el acceso solo a usuarios con acceso al admin.
# from django.contrib.admin.views.decorators import staff_member_required

# @staff_member_required
@login_required
def importa_backup(request):
    try:
        nombres_archivos = [
            'tipo_indicador.json',
            'parametros_g.json',
            'tipo_impacto.json',
            'nivel_impacto.json',
            'indicadores_bia.json',
            'escenarios.json',
            'estrategias.json',
            'tipo_rr.json',
            'recursos.json',
        ]

        errores = []
        exitos = []

        for nombre in nombres_archivos:
            ruta_fixture = os.path.join('bcp', 'fixtures', nombre)

            if os.path.exists(ruta_fixture):
                try:
                    call_command('loaddata', ruta_fixture, verbosity=1)
                    exitos.append(nombre)
                except Exception as carga_error:
                    errores.append(f"{nombre} → {carga_error}")
            else:
                errores.append(f"{nombre} → No encontrado")

        # Construye el mensaje final
        mensaje = ""
        if exitos:
            mensaje += f"✅ Cargados correctamente: {', '.join(exitos)}.<br>"
        if errores:
            mensaje += f"❌ Errores:<br>" + "<br>".join(errores)

        return HttpResponse(mensaje)

    except Exception as e:
        return HttpResponse(f"❌ Error inesperado: {e}")
    
#************************************
#* Respaldo / Recuperacion de la BD *
#************************************

import io
import zipfile
import datetime
import json
from django.core import serializers
from django.http import HttpResponse
from django.apps import apps
@login_required
def respaldo_json_zip(request):
    """
    Genera un ZIP con un archivo JSON por cada modelo de la app 'bcp'
    y agrega además User y Group.
    Incluye relaciones ManyToMany explícitas en la clave 'm2m'.
    """
    from django.contrib.auth.models import User, Group

    # Modelos de la app bcp + User y Group
    MODELOS = list(apps.get_app_config("bcp").get_models()) + [User, Group]

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for modelo in MODELOS:
            nombre = modelo.__name__
            try:
                registros = []
                for obj in modelo.objects.all():
                    base = serializers.serialize("json", [obj])
                    base_data = json.loads(base)[0]

                    # Capturar M2M explícitamente
                    m2m_data = {}
                    for field in obj._meta.many_to_many:
                        rel_ids = list(getattr(obj, field.name).values_list("id", flat=True))
                        m2m_data[field.name] = rel_ids

                    base_data["m2m"] = m2m_data
                    registros.append(base_data)

                # Guardar archivo JSON en ZIP
                json_data = json.dumps(registros, indent=2, ensure_ascii=False)
                zipf.writestr(f"{nombre}.json", json_data)

                print(f"[OK] Respaldo generado para el modelo: {nombre}")

            except Exception as e:
                print(f"[ERROR] No se pudo respaldar el modelo {nombre}: {e}")

    buffer.seek(0)
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"respaldo_{fecha}.zip"

    response = HttpResponse(buffer, content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

# ==================================================================

from django.db import transaction

import os
import io
import json
import zipfile
import tempfile
import datetime
from collections import defaultdict

from django.shortcuts import render
from django.apps import apps
from django.db import connection
from django.db.models import AutoField
from django.core import serializers
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.models import User, Group
from django.db import connection # Importante para desactivar checks

from collections import defaultdict
import os, json, zipfile, tempfile



from django.db import connection
from django.apps import apps
from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldDoesNotExist
from django.db.models import AutoField
from collections import defaultdict
import os, json, zipfile, tempfile

def recuperar_json_zip(request):
    """
    Version: 6
    Vista para restaurar datos desde un archivo ZIP de respaldo.
    - Maneja UNIQUE constraint failed mediante lógica de Update-if-exists.
    - Mantiene desactivación de FK checks para evitar fallos de jerarquía.
    - Preserva comentarios originales en FK_MAP.
    """
    
    def obtener_modelo(nombre_modelo):
        if nombre_modelo == "User": return User
        if nombre_modelo == "Group": return Group
        return apps.get_model("bcp", nombre_modelo)

    # --- FK_MAP: adapta/añade según tu modelo ---
    FK_MAP = {
        # =============================
        # Usuarios y Grupos
        # =============================
        "Grupos.grupo": Group,
        "Gestor.user_gestor": User,
        "Gestor.area": "Area",
        "Gestor.cod_area": "Cod_Area",

        # =============================
        # Recursos y Tipos
        # =============================
        "Recursos.tipo": "Tipo_RR",
        "Nivel_Impacto.tipo": "Tipo_Impacto",
        "Indicadores_BIA.tipo": "Tipo_Indicador",

        "Impactos_Asig.impacto": "Tipo_Impacto",
        "Impactos_Asig_v.impacto": "Tipo_Impacto",
        "Impactos_Asig.nivel": "Nivel_Impacto",
        "Impactos_Asig_v.nivel": "Nivel_Impacto",

        "Indicadores_Asig.indicador": "Tipo_Indicador",
        "Indicadores_Asig_v.indicador": "Tipo_Indicador",
        "Indicadores_Asig.nivel": "Indicadores_BIA",
        "Indicadores_Asig_v.nivel": "Indicadores_BIA",

        # =============================
        # Procedimientos
        # =============================
        "Procedimientos.tipo": "Tipo_Proc",
        "Procedimientos_V.tipo": "Tipo_Proc",

        "Procedimientos.escenarios": "Escenarios",
        "Procedimientos_V.escenarios": "Escenarios",

        "Procedimientos.resp_proceso": "Gestor",
        "Procedimientos_V.resp_proceso": "Gestor",
        "Procedimientos.bck_resp": "Gestor",
        "Procedimientos_V.bck_resp": "Gestor",
        "Procedimientos.gestor_ejecutor": "Gestor",
        "Procedimientos_V.gestor_ejecutor": "Gestor",
        "Procedimientos.bck_ejecutor": "Gestor",
        "Procedimientos_V.bck_ejecutor": "Gestor",
        "Procedimientos.enlace_c_crisis": "Gestor",
        "Procedimientos_V.enlace_c_crisis": "Gestor",
        "Procedimientos.bck_enlace": "Gestor",
        "Procedimientos_V.bck_enlace": "Gestor",
        "Procedimientos.gestor_consultor": "Gestor",
        "Procedimientos_V.gestor_consultor": "Gestor",

        # =============================
        # Componentes
        # =============================
        "Componentes.tipo_act": "Tipo_Componente",

        # =============================
        # Logs
        # =============================
        "LogAut.gestor_aprobador": "Gestor",
        "Log_Revision.proceso": "Proceso",
        "Log_Revision.procedimiento": "Procedimientos",
        "Log_Revision.drp": "Drp",
        "Log_Revision.gestor_aut": "Gestor",

        "Control_Cambios.proceso": "SubProceso_V",
        "Control_Cambios.procedimiento": "Procedimientos_V",
        "Control_Cambios.gestor_aut": "Gestor",

        # =============================
        # Pasos PC
        # =============================
        "Pasos_PC.ejecutor": "Gestor",
        "Pasos_PC_V.ejecutor": "Gestor",

        # =============================
        # DRP
        # =============================
        "Drp.resp_drp": "Gestor",
        "Drp.bck_resp_drp": "Gestor",
        "Drp.gestor_ejecutor_drp": "Gestor",
        "Drp.bck_ejecutor_drp": "Gestor",
        "Drp.enlace_c_crisis_drp": "Gestor",
        "Drp.bck_enlace_drp": "Gestor",
        "Drp.gestor_consultor_drp": "Gestor",
        "Drp.tipo_Site": "Tipo_Site",
        "Drp.disposicion_componentes": "Tipo_Disp",

        # =============================
        # SubProcesos / Procesos
        # =============================
        "SubProceso.gestor_R": "Gestor",
        "SubProceso_V.gestor_R": "Gestor",
        "SubProceso.gestor_A": "Gestor",
        "SubProceso_V.gestor_A": "Gestor",
        "SubProceso.gestor_C": "Gestor",
        "SubProceso_V.gestor_C": "Gestor",
        "SubProceso.gestor_I": "Gestor",
        "SubProceso_V.gestor_I": "Gestor",

        "Proceso.subproceso": "SubProceso",
        "Proceso.subproceso_v": "SubProceso_V",

        # =============================
        # PRUEBAS DE CONTINGENCIA 
        # =============================
        # PruebaContingencia
        "PruebaContingencia.procedimiento": "Procedimientos",
        "PruebaContingencia.responsable": "Gestor",

        # PruebaContingencia_V
        "PruebaContingencia_V.procedimiento": "Procedimientos_V",
        "PruebaContingencia_V.responsable": "Gestor",

        # CasoPrueba
        "CasoPrueba.prueba": "PruebaContingencia",

        # CasoPrueba_V
        "CasoPrueba_V.prueba": "PruebaContingencia_V",

        # EjecucionPrueba
        "EjecucionPrueba.incidente": "Incidentes",
        "EjecucionPrueba.prueba": "PruebaContingencia_V",
        "EjecucionPrueba.checklist": "CheckList",

        # EjecucionCasoPrueba
        "EjecucionCasoPrueba.ejecucion": "EjecucionPrueba",
        "EjecucionCasoPrueba.caso": "CasoPrueba_V",

        # =============================
        # CHECKLIST / PASOS
        # =============================

        # Checklist
        "Checklist.incidente": "Incidentes",
        "Checklist.procedimiento": "Procedimientos_V",

        # Check_Pasos
        "Check_Pasos.checklist": "CheckList",
        "Check_Pasos.paso": "Pasos_PC_V",
    }

    ORDEN_MODELOS = [
        "Group", "User", "Area", "Cod_Area", "Grupos", "Tipo_RR", "Tipo_Indicador", "Tipo_Impacto",
        "Tipo_Impacto_P", "Nivel_Impacto", "Nivel_Impacto_P", "Tipo_Proc", "Tipo_Site", "Tipo_Disp",
        "Tipo_Componente", "Gestor", "Recursos", "Escenarios", "Amenazas", "Estrategias", "Parametros_G",
        "Indicadores_BIA", "Drp", "Proceso", "SubProceso", "SubProceso_V", "Impactos_Asig", "Impactos_Asig_v",
        "Indicadores_Asig", "Indicadores_Asig_v", "Procedimientos", "Procedimientos_V", "Servicios_PC",
        "Servicios_PC_V", "Pasos_PC", "Pasos_PC_V", "Contactos_PC", "Contactos_PC_V", "Componentes", "LBC",
        "LogAut", "Log_Revision", "Control_Cambios", "Incidentes", "CheckList", 'Check_Pasos',
        "PruebaContingencia", "PruebaContingencia_V", "CasoPrueba", "CasoPrueba_V", "EjecucionPrueba",
        "EjecucionCasoPrueba",
    ]

    log, id_map, data_map = [], {}, {}

    if request.method == "POST" and request.FILES.get("zipfile"):
        zip_file = request.FILES["zipfile"]
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "upload.zip")
            with open(zip_path, "wb") as f:
                for chunk in zip_file.chunks(): f.write(chunk)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdirname)

            for model_name in ORDEN_MODELOS:
                file_path = os.path.join(tmpdirname, f"{model_name}.json")
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_map[model_name] = json.load(f)

            # --- Borrado ---
            for model_name in reversed(ORDEN_MODELOS): # Borramos en orden inverso para respetar FKs
                try:
                    model = obtener_modelo(model_name)
                    model.objects.all().delete()
                except Exception as e:
                    log.append(f"[AVISO] No se pudo limpiar tabla {model_name}: {e}")

            # --- PRIMERA PASADA: Creación / Actualización ---
            create_errors = defaultdict(int)
            
            with connection.constraint_checks_disabled():
                for model_name in ORDEN_MODELOS:
                    data = data_map.get(model_name, [])
                    try: model = obtener_modelo(model_name)
                    except Exception: continue

                    for record in data:
                        pk, fields = record.get("pk"), record.get("fields", {})
                        try:
                            # Cambio clave: Intentamos recuperar el objeto si ya existe (evita UNIQUE constraint failed)
                            obj = model.objects.filter(pk=pk).first() or model(pk=pk)
                            
                            for field, value in fields.items():
                                if value is None: continue
                                try:
                                    fmeta = model._meta.get_field(field)
                                    if getattr(fmeta, 'many_to_many', False): continue
                                    if getattr(fmeta, 'is_relation', False):
                                        setattr(obj, f"{fmeta.name}_id", value)
                                    else:
                                        # No sobrescribir password si es User y ya existe (opcional)
                                        setattr(obj, field, value)
                                except Exception: pass
                            
                            # Usamos save() normal. Django detectará si es UPDATE o INSERT según el PK
                            obj.save()
                            
                            # Forzar actualización de fechas (save() suele sobrescribir auto_now_add)
                            date_fields = [f.name for f in model._meta.get_fields() if f.get_internal_type() in ("DateTimeField", "DateField")]
                            update_dates = {f: fields[f] for f in date_fields if f in fields}
                            if update_dates: model.objects.filter(pk=obj.pk).update(**update_dates)

                            id_map[f"{model_name}.{pk}"] = obj
                        except Exception as e:
                            log.append(f"[ERROR] {model_name}: pk={pk} :: {e}")

            # --- SEGUNDA PASADA: Relaciones formales ---
            for model_name in ORDEN_MODELOS:
                data = data_map.get(model_name, [])
                try: model = obtener_modelo(model_name)
                except Exception: continue

                for record in data:
                    pk, fields, m2m_fields = record.get("pk"), record.get("fields", {}), record.get("m2m", {})
                    obj = id_map.get(f"{model_name}.{pk}")
                    if not obj: continue

                    for field, value in fields.items():
                        if value is None: continue
                        key = f"{model_name}.{field}"
                        try:
                            fmeta = model._meta.get_field(field)
                            if not getattr(fmeta, 'is_relation', False) or getattr(fmeta, 'many_to_many', False): continue
                            
                            target = FK_MAP.get(key) or fmeta.remote_field.model.__name__
                            target_name = target if isinstance(target, str) else getattr(target, '__name__', None)
                            
                            res = id_map.get(f"{target_name}.{value}") or obtener_modelo(target_name).objects.filter(pk=value).first()
                            if res:
                                setattr(obj, field, res)
                                obj.save()
                        except Exception: pass

                    for field, ids in m2m_fields.items():
                        try:
                            fmeta = model._meta.get_field(field)
                            rel_mod = fmeta.related_model
                            objs = [id_map.get(f"{rel_mod.__name__}.{r_pk}") or rel_mod.objects.filter(pk=r_pk).first() for r_pk in ids]
                            getattr(obj, field).set([o for o in objs if o])
                        except Exception: pass

            log.append("[INFO] Restauración completada.")

        # Reajuste de secuencias (Postgres)
        if connection.vendor == "postgresql":
            with connection.cursor() as cursor:
                for m_name in ORDEN_MODELOS:
                    try:
                        m = obtener_modelo(m_name)
                        if isinstance(m._meta.pk, AutoField):
                            cursor.execute(f"SELECT setval(pg_get_serial_sequence('{m._meta.db_table}', '{m._meta.pk.name}'), COALESCE(MAX({m._meta.pk.name}), 1)) FROM {m._meta.db_table};")
                    except Exception: pass

        return render(request, "bcp/conf/recuperar_form.html", {"log": log})
    return render(request, "bcp/conf/recuperar_form.html", {"log": None})


# ===============================================================================================

import io
import json
import zipfile
import tempfile
import datetime
from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction, models as dj_models
from django.contrib import messages

@staff_member_required
def auditoria_integridad(request):
    """
    Auditoría de integridad para la app 'bcp'.
    GET -> muestra el informe (HTML).
    GET ?format=json -> devuelve JSON con el informe.
    (Solo usuarios staff pueden ejecutarla.)
    """
    app_label = "bcp"
    models_list = list(apps.get_app_config(app_label).get_models())

    report = []
    total_issues = 0

    for model in models_list:
        model_name = model.__name__
        model_issues = []

        # 1) ForeignKey / OneToOne checks
        for field in model._meta.get_fields():
            if isinstance(field, (dj_models.ForeignKey, dj_models.OneToOneField)):
                # resolver modelo destino
                target = field.remote_field.model
                if isinstance(target, str):
                    if "." in target:
                        app_name, model_short = target.split(".", 1)
                        target = apps.get_model(app_name, model_short)
                    else:
                        target = apps.get_model(app_label, target)

                # 1.a) registros con NULL cuando field.null == False
                if not field.null:
                    null_qs = model.objects.filter(**{f"{field.name}__isnull": True})
                    null_count = null_qs.count()
                    if null_count:
                        sample = list(null_qs.values_list("pk", flat=True)[:10])
                        model_issues.append({
                            "type": "missing_required_fk",
                            "field": field.name,
                            "target": target.__name__,
                            "count": null_count,
                            "sample_pks": sample,
                        })
                        total_issues += null_count

                # 1.b) FK huérfanas: ids presentes en fk_id pero no existen en target
                ids_qs = model.objects.exclude(**{f"{field.name}__isnull": True}).values_list(f"{field.name}_id", flat=True).distinct()
                ids = [i for i in ids_qs if i is not None]
                if ids:
                    existing_ids = set(target.objects.filter(pk__in=ids).values_list("pk", flat=True))
                    missing_ids = set(ids) - existing_ids
                    if missing_ids:
                        sample_records = list(model.objects.filter(**{f"{field.name}_id__in": list(missing_ids)}).values("pk")[:10])
                        model_issues.append({
                            "type": "orphaned_fk",
                            "field": field.name,
                            "target": target.__name__,
                            "missing_ids": list(missing_ids)[:200],
                            "sample_records": sample_records,
                        })
                        total_issues += len(missing_ids)

        # 2) ManyToMany checks (solo relaciones M2M reales, no auto_created)
        for field in model._meta.get_fields():
            if field.many_to_many and not getattr(field, "auto_created", False):
                related_model = field.remote_field.model
                if isinstance(related_model, str):
                    if "." in related_model:
                        app_name, model_short = related_model.split(".", 1)
                        related_model = apps.get_model(app_name, model_short)
                    else:
                        related_model = apps.get_model(app_label, related_model)

                m2m_orphans = []
                # iteramos; en tablas grandes puede tardar: optimizable
                for obj in model.objects.all():
                    ids = list(getattr(obj, field.name).values_list("pk", flat=True))
                    if not ids:
                        continue
                    existing = set(related_model.objects.filter(pk__in=ids).values_list("pk", flat=True))
                    missing = set(ids) - existing
                    if missing:
                        m2m_orphans.append({"obj_pk": obj.pk, "missing_ids": list(missing)})
                if m2m_orphans:
                    model_issues.append({
                        "type": "m2m_orphaned",
                        "field": field.name,
                        "related_model": related_model.__name__,
                        "details_count": len(m2m_orphans),
                        "details_sample": m2m_orphans[:10],
                    })
                    total_issues += sum(len(d["missing_ids"]) for d in m2m_orphans)

        if model_issues:
            report.append({"model": model_name, "issues": model_issues})

    if request.GET.get("format") == "json":
        return JsonResponse({"report": report, "total_issues": total_issues}, safe=False)

    return render(request, "bcp/conf/auditoria_integridad.html", {"report": report, "total_issues": total_issues})


@staff_member_required
def reparar_integridad(request):
    """
    Vista para reparar problemas detectados por auditoria_integridad.
    - GET: muestra la misma auditoria con un formulario para elegir la acción.
    - POST: ejecuta la reparación solicitada (confirmar 'confirm' = 'yes').
    Parámetros POST esperados:
        action: 'clean_orphans' | 'delete_orphans' | 'apply_defaults'
        default_map (opcional): JSON string mapping "Model.field" -> default_pk (o list for M2M)
        confirm: must be "yes"
    """
    # recalcular informe (reusamos la lógica de auditoria, simplificada)
    app_label = "bcp"
    models_list = list(apps.get_app_config(app_label).get_models())

    # recomputar reporte (igual que auditoria_integridad)
    report = []
    for model in models_list:
        model_name = model.__name__
        model_issues = []

        for field in model._meta.get_fields():
            if isinstance(field, (dj_models.ForeignKey, dj_models.OneToOneField)):
                target = field.remote_field.model
                if isinstance(target, str):
                    if "." in target:
                        app_name, model_short = target.split(".", 1)
                        target = apps.get_model(app_name, model_short)
                    else:
                        target = apps.get_model(app_label, target)

                if not field.null:
                    null_qs = model.objects.filter(**{f"{field.name}__isnull": True})
                    null_count = null_qs.count()
                    if null_count:
                        sample = list(null_qs.values_list("pk", flat=True)[:10])
                        model_issues.append({
                            "type": "missing_required_fk",
                            "field": field.name,
                            "target": target.__name__,
                            "count": null_count,
                            "sample_pks": sample,
                        })

                ids_qs = model.objects.exclude(**{f"{field.name}__isnull": True}).values_list(f"{field.name}_id", flat=True).distinct()
                ids = [i for i in ids_qs if i is not None]
                if ids:
                    existing_ids = set(target.objects.filter(pk__in=ids).values_list("pk", flat=True))
                    missing_ids = set(ids) - existing_ids
                    if missing_ids:
                        sample_records = list(model.objects.filter(**{f"{field.name}_id__in": list(missing_ids)}).values("pk")[:10])
                        model_issues.append({
                            "type": "orphaned_fk",
                            "field": field.name,
                            "target": target.__name__,
                            "missing_ids": list(missing_ids)[:200],
                            "sample_records": sample_records,
                        })

            if field.many_to_many and not getattr(field, "auto_created", False):
                related_model = field.remote_field.model
                if isinstance(related_model, str):
                    if "." in related_model:
                        app_name, model_short = related_model.split(".", 1)
                        related_model = apps.get_model(app_name, model_short)
                    else:
                        related_model = apps.get_model(app_label, related_model)

                m2m_orphans = []
                for obj in model.objects.all():
                    ids = list(getattr(obj, field.name).values_list("pk", flat=True))
                    if not ids:
                        continue
                    existing = set(related_model.objects.filter(pk__in=ids).values_list("pk", flat=True))
                    missing = set(ids) - existing
                    if missing:
                        m2m_orphans.append({"obj_pk": obj.pk, "missing_ids": list(missing)})
                if m2m_orphans:
                    model_issues.append({
                        "type": "m2m_orphaned",
                        "field": field.name,
                        "related_model": related_model.__name__,
                        "details_count": len(m2m_orphans),
                        "details_sample": m2m_orphans[:10],
                    })

        if model_issues:
            report.append({"model": model_name, "issues": model_issues})

    if request.method == "GET":
        return render(request, "bcp/conf/auditoria_integridad_reparar.html", {"report": report})

    # POST -> ejecutar reparación
    action = request.POST.get("action")
    confirm = request.POST.get("confirm")
    default_map_raw = request.POST.get("default_map", "{}")

    if confirm != "yes":
        return HttpResponseBadRequest("Debe confirmar la operación (confirm=yes).")

    try:
        default_map = json.loads(default_map_raw) if default_map_raw else {}
    except Exception:
        return HttpResponseBadRequest("default_map debe ser JSON válido.")

    # Ejecución de la reparación
    results = []
    with transaction.atomic():
        for item in report:
            model_name = item["model"]
            model = apps.get_model(app_label, model_name)
            for issue in item["issues"]:
                if issue["type"] == "orphaned_fk":
                    field_name = issue["field"]
                    missing_ids = issue["missing_ids"]
                    # Acción: clean_orphans => set NULL si permite; delete_orphans => delete; apply_defaults => set default if provided
                    if action == "clean_orphans":
                        field_obj = model._meta.get_field(field_name)
                        if field_obj.null:
                            q = model.objects.filter(**{f"{field_name}_id__in": missing_ids})
                            updated = q.update(**{f"{field_name}": None})
                            results.append({"model": model_name, "field": field_name, "action": "set_null", "count": updated})
                        else:
                            results.append({"model": model_name, "field": field_name, "action": "skip_set_null_not_nullable", "count": 0})
                    elif action == "delete_orphans":
                        q = model.objects.filter(**{f"{field_name}_id__in": missing_ids})
                        deleted_count, _ = q.delete()
                        results.append({"model": model_name, "field": field_name, "action": "delete_records", "count": deleted_count})
                    elif action == "apply_defaults":
                        key = f"{model_name}.{field_name}"
                        if key in default_map:
                            default_pk = default_map[key]
                            target_model = model._meta.get_field(field_name).remote_field.model
                            try:
                                default_obj = target_model.objects.get(pk=default_pk)
                                q = model.objects.filter(**{f"{field_name}_id__in": missing_ids})
                                updated = q.update(**{f"{field_name}": default_obj})
                                results.append({"model": model_name, "field": field_name, "action": f"set_default:{default_pk}", "count": updated})
                            except Exception as e:
                                results.append({"model": model_name, "field": field_name, "action": "set_default_failed", "error": str(e)})
                        else:
                            results.append({"model": model_name, "field": field_name, "action": "no_default_provided", "count": 0})
                elif issue["type"] == "missing_required_fk":
                    field_name = issue["field"]
                    if action == "apply_defaults":
                        key = f"{model_name}.{field_name}"
                        if key in default_map:
                            default_pk = default_map[key]
                            target_field = model._meta.get_field(field_name).remote_field.model
                            try:
                                default_obj = target_field.objects.get(pk=default_pk)
                                q = model.objects.filter(**{f"{field_name}__isnull": True})
                                updated = q.update(**{f"{field_name}": default_obj})
                                results.append({"model": model_name, "field": field_name, "action": f"set_default_missing:{default_pk}", "count": updated})
                            except Exception as e:
                                results.append({"model": model_name, "field": field_name, "action": "set_default_failed", "error": str(e)})
                        else:
                            results.append({"model": model_name, "field": field_name, "action": "no_default_provided", "count": 0})
                    elif action == "delete_orphans":
                        q = model.objects.filter(**{f"{field_name}__isnull": True})
                        deleted_count, _ = q.delete()
                        results.append({"model": model_name, "field": field_name, "action": "delete_records_missing_required", "count": deleted_count})
                    else:
                        results.append({"model": model_name, "field": field_name, "action": "skip_missing_required", "count": 0})
                elif issue["type"] == "m2m_orphaned":
                    field_name = issue["field"]
                    # remove missing ids from M2M (safe)
                    if action in ("clean_orphans", "delete_orphans", "apply_defaults"):
                        related_model = None
                        for f in model._meta.get_fields():
                            if f.many_to_many and f.name == field_name:
                                related_model = f.remote_field.model
                                break
                        if related_model is None:
                            results.append({"model": model_name, "field": field_name, "action": "related_model_not_found"})
                            continue

                        # recorrer sample o todos (aquí recorremos todos)
                        removed_total = 0
                        for obj in model.objects.all():
                            ids = list(getattr(obj, field_name).values_list("pk", flat=True))
                            if not ids:
                                continue
                            existing = set(related_model.objects.filter(pk__in=ids).values_list("pk", flat=True))
                            missing = set(ids) - existing
                            if not missing:
                                continue
                            # quitar los missing
                            kept = [i for i in ids if i in existing]
                            getattr(obj, field_name).set(kept)
                            removed_total += len(missing)
                        results.append({"model": model_name, "field": field_name, "action": "remove_missing_from_m2m", "count": removed_total})

    # Al final mostrar resultados
    return render(request, "bcp/conf/auditoria_reparacion_result.html", {"results": results})




# *********************************************
# Vista para Grabar en cada Seleccion de Item *
#**********************************************
# views.py
import json
import logging
from django.http import JsonResponse
from django.apps import apps
from django.db import transaction
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

# WHITELIST: mantener control sobre qué modelos pueden usar este endpoint.
# Formato: "app_label.ModelName"
ALLOWED_MODELS = {
    "bcp.Drp",
    "bcp.Proceso",
    "bcp.SubProceso",
    "bcp.Incidentes"
    # Añade aquí solo los modelos que explícitamente quieras exponer.
}

@login_required
@require_POST
def ajax_toggle_generic(request):
    """
    Endpoint AJAX para añadir/remover elementos de una relación ManyToMany
    de forma inmediata al clic del usuario.
    Usado en los Box de Seleccion de Items

    Se espera recibir en el body un JSON con las claves:
      - model   : "app_label.ModelName"   (debe estar en ALLOWED_MODELS)
      - obj_id  : id del objeto base (ej: drp.id)
      - field   : nombre del campo ManyToMany en el objeto base (ej: "componentes")
      - item_id : id del elemento relacionado (ej: componente.id)
      - action  : "add" o "remove"

    Responde JSON con status "ok" o "error" y mensaje explicativo.
    """
    # 1) Validación método (decoradores arriba ya manejan POST y login)
    # 2) Parseo JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON inválido"}, status=400)

    # 3) Validación de parámetros requeridos
    required = ("model", "obj_id", "field", "item_id", "action")
    for k in required:
        if k not in payload:
            return JsonResponse({"status": "error", "message": f"Falta parámetro '{k}'"}, status=400)

    model_path = payload["model"]
    obj_id = payload["obj_id"]
    field_name = payload["field"]
    item_id = payload["item_id"]
    action = payload["action"]

    # 4) Seguridad: verificar whitelist
    if model_path not in ALLOWED_MODELS:
        logger.warning("Intento de acceso a modelo no permitido: %s por usuario %s", model_path, request.user)
        return JsonResponse({"status": "error", "message": "Modelo no autorizado"}, status=403)

    # 5) Cargar modelo de forma dinámica
    try:
        app_label, model_name = model_path.split(".")
        Model = apps.get_model(app_label, model_name)
        if Model is None:
            raise LookupError("Modelo no encontrado")
    except Exception as e:
        logger.exception("Error cargando modelo %s: %s", model_path, e)
        return JsonResponse({"status": "error", "message": "Modelo inválido"}, status=400)

    # 6) Obtener objeto base
    obj = Model.objects.filter(pk=obj_id).first()
    if not obj:
        return JsonResponse({"status": "error", "message": f"Objeto {obj_id} no encontrado"}, status=404)

    # 7) Verificar que el campo exista en el objeto
    if not hasattr(obj, field_name):
        return JsonResponse({"status": "error", "message": f"Campo '{field_name}' inexistente en modelo."}, status=400)

    rel = getattr(obj, field_name)

    # 8) Verificar que el atributo sea manejable como relación M2M (tiene add/remove)
    if not (hasattr(rel, "add") and hasattr(rel, "remove")):
        return JsonResponse({"status": "error", "message": f"Campo '{field_name}' no es ManyToMany."}, status=400)

    # 9) Obtener modelo relacionado y elemento
    RelatedModel = rel.model
    item = RelatedModel.objects.filter(pk=item_id).first()
    if not item:
        return JsonResponse({"status": "error", "message": f"Elemento {item_id} no encontrado"}, status=404)

    # 10) Ejecutar acción dentro de transacción para consistencia
    try:
        with transaction.atomic():
            if action == "add":
                rel.add(item)       # añade relación M2M
                msg = f"Elemento {item_id} agregado a {model_path}.{field_name}"
            elif action == "remove":
                rel.remove(item)    # remueve relación M2M
                msg = f"Elemento {item_id} removido de {model_path}.{field_name}"
            else:
                return JsonResponse({"status": "error", "message": "Acción inválida"}, status=400)

            # Opcional: logger info (útil para auditoría)
            logger.info("User %s: %s %s.%s <- %s", request.user, action, model_path, field_name, item_id)

    except Exception as exc:
        logger.exception("Error aplicando cambio en %s.%s: %s", model_path, field_name, exc)
        return JsonResponse({"status": "error", "message": "Error interno al guardar"}, status=500)

    # 11) Responder OK con datos útiles para el frontend
    return JsonResponse({
        "status": "ok",
        "message": msg,
        "model": model_path,
        "field": field_name,
        "action": action,
        "obj_id": obj_id,
        "item_id": item_id
    })


