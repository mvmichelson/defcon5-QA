#Programa PYTHON
#Definicion de Vistas para el Sistema BCP del Proyecto DEFCON5
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


# 6. Maestros
# Administracion de Riesgo/Impacto 


# 7. Proposito General
#=======================




# ============================================================================================
# ============================================================================================


from queue import Full
from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from .models import Proceso, SubProceso, LogAut, Recursos, Tipo_RR, Gestor, Escenarios, Amenazas, Estrategias, Tipo_Impacto, Nivel_Impacto, Tipo_Impacto_P, Nivel_Impacto_P
from .models import Drp, Indicadores_BIA, Tipo_Indicador, Parametros_G, Incidentes, Procedimientos, Tipo_Proc, Servicios_PC, Contactos_PC, Pasos_PC 
from .models import Componentes, Tipo_Componente, LBC, Tipo_Disp, Tipo_Site, Impactos_Asig, Contactos_PC_V, Pasos_PC_V
from .models import Indicadores_Asig, Log_Revision, SubProceso_V, Control_Cambios, Procedimientos_V, Servicios_PC_V

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

class Base_GenericPageView(TemplateView):
    
    model = Parametros_G
    template_name = '/BCP/base_generic.html'

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

    usr=request.user
    #if not usr.is_authenticated:
        #return HttpResponseRedirect(reverse('error-sesion-mgm', args=[500] ))

    # Genera contadores de algunos de los objetos principales
    num_proc=Proceso.objects.all().count()
    num_sproc=SubProceso.objects.all().count()
    num_proced=Procedimientos.objects.all().count()
   
    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    defcon = get_object_or_404(Parametros_G , pk=1)

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_proc':num_proc,'num_sproc':num_sproc, 'num_proced':num_proced,'num_visits':num_visits,
                 'defcon':defcon})

def En_Construccion(request):
    return render(request, 'BCP/Mensajes/en_construccion.html')


def Mapeo(request):
    """
    Despliega Grafico con la Metodologia de Mapeo 
    """

    return render(request, 'BCP/mapeo.html')

def Mapa_RIA(request):
    """
    Despliega Grafico con la Metodologia de Evaluacion RIA 
    """

    return render(request, 'BCP/ria/diagrama_ria.html')



#******************************************************************************************************************************************
#************************************************************* 1. Listas y Detalles *******************************************************
#******************************************************************************************************************************************


#***********************
# 1.1 Lista de Procesos *
#***********************

def Lista_Procesos(request):
    """
    Lista Procesos 
    """
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, pk = 5)
    bia_medio = get_object_or_404(Parametros_G, pk = 6)
    bia_alto  = get_object_or_404(Parametros_G, pk = 7)

    tramo_1 = float(bia_bajo.valor_2)/100*5
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100*5
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2) 

    lista_procesos = Proceso.objects.all()
    
    return render(request, 'BCP/proceso_list.html',
                  context={'lista_procesos':lista_procesos, 'tramo_1':tramo_1, 'tramo_2':tramo_2})
 

#********************************************
# 1.2 Lista de Procesos para asociar Activos*
#********************************************
def Lista_Recursos(request):
    """
    Lista Procesos para asociar Servicios Criticos
    """
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, pk = 5)
    bia_medio = get_object_or_404(Parametros_G, pk = 6)
    bia_alto  = get_object_or_404(Parametros_G, pk = 7)

    tramo_1 = float(bia_bajo.valor_2)/100*5
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100*5

    lista_procesos = Proceso.objects.all()
    return render(request, 'BCP/map_act/map_activos__list.html',
                  context={'lista_procesos':lista_procesos, 'tramo_1':tramo_1, 'tramo_2':tramo_2})
    


#***********************************************
# 1.3 Lista de Procesos para asociar Escenarios*
#***********************************************
def Lista_Escenarios(request):
    """
    Lista Procesos para asignar Escenarios.
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, pk = 5)
    bia_medio = get_object_or_404(Parametros_G, pk = 6)
    bia_alto  = get_object_or_404(Parametros_G, pk = 7)

    tramo_1 = float(bia_bajo.valor_2)/100*5
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100*5

    lista_procesos = Proceso.objects.all()
    
    return render(request, 'BCP/map_esc/map_esc_list.html',
                  context={'lista_procesos':lista_procesos, 'tramo_1':tramo_1, 'tramo_2':tramo_2})
    


#***********************************************
# 1.4 Lista de Procesos para asociar Evaluacion*
#***********************************************

def Lista_Evaluaciones(request):
    """
    Lista Procesos para Evaluacion BIA.
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores', 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, pk = 5)
    bia_medio = get_object_or_404(Parametros_G, pk = 6)
    bia_alto  = get_object_or_404(Parametros_G, pk = 7)

    tramo_1 = float(bia_bajo.valor_2)/100*5
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100*5

    lista_procesos = Proceso.objects.all()
    
    return render(request, 'BCP/map_eval/map_eval__list.html',
                  context={'lista_procesos':lista_procesos, 'tramo_1':tramo_1, 'tramo_2':tramo_2})


    
#***********************
#1.5 Detalle de Proceso*
#***********************
class ProcesoDetailView(generic.DetailView):
    model = Proceso


def Detalle_Proceso(request, pk):
    """
    muestra todos los datos asociados al proceso pk
    """
    print('------- Detalle del Proceso -----------------')
    proceso=get_object_or_404(Proceso, pk=pk)
    print('proceso=', proceso.proceso)
    comentarios=Log_Revision.objects.filter(proceso=proceso)
    print('comentarios=', comentarios)

    return render(request, 'BCP/proceso_detail.html',
                  context={'proceso':proceso, 'comentarios':comentarios})

def Detalle_Proceso_V(request, pk):
    """
    muestra todos los datos asociados al proceso vigente
    pk
    """
    print('------- Detalle del Proceso Vigente -----------------')

    proceso=get_object_or_404(Proceso, pk=pk)
    print('proceso=', proceso.proceso)

    control_cambios=Control_Cambios.objects.filter(proceso=proceso.subproceso_v)
    print('comentarios=', control_cambios)

    return render(request, 'BCP/proceso_detail_v.html',
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

#@permission_required('Catalogo.can_mark_returned')
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
            


    # If this is a GET (or any other method) create the default form.
    else:
    
        return render(request, 'BCP/proceso_crea.html', {'form': form, 'proceso':proc_padre})

#***********************
# 2.1.2 Borra  Proceso *
#***********************

#@permission_required('Catalogo.can_mark_returned')
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
    
from .forms import CreaActivoForm
#@permission_required('Catalogo.can_mark_returned')
def Crea_Activo(request):
    """
    Crea en Activo o Recurso
    """

    model=Recursos

   
    #Asigna el formulario creado en Forrms
    form=CreaActivoForm()

    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaActivoForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso
            activo=Recursos()

            activo.nombre = form.cleaned_data['nombre']
            activo.descripcion = form.cleaned_data['descripcion']
            activo.tipo = form.cleaned_data['clase']
            
            activo.save()
               
           
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Recursos') )
        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    # If this is a GET (or any other method) create the default form.
    else:

        
        return render(request, 'BCP/map_act/crea_activo.html', {'form': form})



#************************************************** Fin Creacion/Borrado de Entidades *****************************************************    

#*********************************************************************************************************************************************
#*********************************************** 3. Gestion de Autorizaciones *** ************************************************************
#*********************************************************************************************************************************************

#**********************
# 3.1 Asignacion  RACI*
#**********************
from .forms import AsignaRaciForm

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
            
            #Cambia status del Proceso a x Aprobar
            if proc_raci.subproceso.gestor_C == form.cleaned_data['gestor_A']:
                
                if proc_raci.subproceso.gestor_C == form.cleaned_data['gestor_R']:
                    # En caso que el Gestor Consultor sea el Gestor Responsable
                    #Aprobada por Responsable area 
                    proc_raci.subproceso.status='R'

                    # Crea Log de aprobacion de [R]utorizador
                    log=Log_Revision()
                    log.fecha = datetime.date.today()
                    log.proceso= proc_raci
                    log.gestor_aut=proc_raci.subproceso.gestor_C
                    log.seccion=proc_raci.subproceso.fase_status
                    log.campo="Autorizacion Express"
                    log.comentario="Aprobado por Nivel [R]esponsable"
                    log.resuelto=True
                    log.save()
                   

                    #Notificar a Gestor I por email
                    if notifica:
                        email = proc_raci.subproceso.gestor_I.email
                        cc_email= proc_raci.subproceso.gestor_C.email
                        nombre=proc_raci.subproceso.gestor_C.last_name
                        proceso=proc_raci.path
                        accion='tomar conocimiento de la puesta en vigencia del '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                    
                else:
                    #Por Vigentear
                    proc_raci.subproceso.status='r'

                    #Notificar a Gestor R por email           
                    if notifica:
                        email = proc_raci.subproceso.gestor_R.email
                        cc_email= proc_raci.subproceso.gestor_C.email
                        nombre=proc_raci.subproceso.gestor_C.last_name
                        proceso=proc_raci.path
                        accion='dar visto bueno o requerir cambios para el '
                
                        Manda_Correo(email, cc_email, nombre, proceso, accion)
                        
            else:
                #Por Aprobar
                proc_raci.subproceso.status='A'

                #Notifica por correo a Gestor A            
                if notifica:
                    email = proc_raci.subproceso.gestor_A.email
                    cc_email= proc_raci.subproceso.gestor_C.email
                    nombre=proc_raci.subproceso.gestor_C.last_name
                    proceso=proc_raci.path
                    accion='revisar definicion y aprobar o requerir cambios al '
                
                    Manda_Correo(email, cc_email, nombre, proceso, accion)
                
                   
            proc_raci.subproceso.save()
     
            
            # redirect to a new URL:

            print ('url anterior 0 POST =', url_ant)
                         
            return HttpResponseRedirect(url_ant)

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
        
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
                                        
        return render(request, 'BCP/raci_asigna.html', {'form': form, 'proc_raci':proc_raci, 'etapa':etapa})


#*********************************
#3.2 Autorizacion RACI de Proceso*
#*********************************
from .forms import AutorizaRaciForm
import datetime

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
                    log.comentario="Aprobado por Nivel [A]utorizador"
                    log.resuelto=True
                    log.save()
                    
                    # Prepara datos del correo 
                    nombre=proc.subproceso.gestor_R.user_gestor.last_name
                    email = proc.subproceso.gestor_R.user_gestor.email
                    accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    proc.subproceso.status='x' # (Devuelve a [C]onsultor)
                    print ('rechazo A->x')
                    email = proc.subproceso.gestor_C.user_gestor.email
                    accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proc.subproceso.status=='r': # (Si es una revision ... )

                    if aprobado:
                        """ Pasa a estado Vigenteado"""
                        print('aprobo A->R')
                        proc.subproceso.status='R'

                        # Crea Log de aprobacion de [A]utorizador
                        log=Log_Revision()
                        log.fecha = datetime.date.today()
                        log.proceso= proc
                        log.gestor_aut=usr_aut
                        log.seccion="M"
                        log.campo="Autorizado por:"+aut
                        log.comentario="Aprobado por Nivel [R]esponsable"
                        log.resuelto=True
                        log.save()
                    
                        if proc.subproceso.gestor_I:
                            nombre=proc.subproceso.gestor_I.user_gestor.last_name
                            email = proc.subproceso.gestor_C.user_gestor.email
                            accion='tomar conocimiento de la puesta en vigencia del '
                            
                    else:
                        """ Pasa a revision por C """
                        proc.subproceso.status='x'

                
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'BCP/proceso_auth.html', {'form': form, 
                                                         'proceso':proc,
                                                         'comentarios':comentarios_m})
    

#********************************************************
#3.3  Autorizacion RACI de Asignacion   BIA  a Proceso **
#********************************************************
from .forms import Autoriza_BIA_Form
#import datetime

def Aut_Asig_BIA(request, pk):
    """ Los comentarios se registran mediante un script (main.js) en el Template y se cargan a la 
    base con la vista "Crea_Rev_OC" """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    proceso=get_object_or_404(Proceso, pk = pk)

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
                
                if aprobado:
                    print('aprobo A->r')
                    proceso.subproceso.status='r'
                    
                    nombre=proceso.subproceso.gestor_R.user_gestor.last_name
                    email = proceso.subproceso.gestor_R.user_gestor.email
                    accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    proceso.subproceso.status='x'
                    
                    email = proceso.subproceso.gestor_C.user_gestor.email
                    accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proceso.subproceso.status=='r':

                    if aprobado:
                        print('aprobo A->R')
                        proceso.subproceso.status='R'
                    
                        if  proceso.subproceso.gestor_I:
                            nombre=proceso.subproceso.gestor_I.user_gestor.last_name
                            email = proceso.subproceso.gestor_C.user_gestor.email
                            accion='tomar conocimiento de la puesta en vigencia del '
                    else:
                        proceso.subproceso.status='x'

                
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

        
    else:
    
        form = AutorizaRaciForm(initial= {'aprobacion':False, 'notifica':False }
                             )
                                        
        return render(request, 'BCP/map_eval/asig_eval_auth.html', {'form': form,
                                                                    'proceso':proceso,
                                                                    'comentarios':comentarios_v})
    

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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        url_ant_obs_aut =request.META['HTTP_REFERER']
        form= Autoriza_obs_Proced_C_Form()
        
        return render(request, 'BCP/proceso_obs_auth.html', {'form': form, 'proc':proc, 'item':item, 'valor':valor})


def borra_obs_proceso(request, pk):
    """
    Borra observacion a nivel de item
    """

    url_ant= request.META['HTTP_REFERER']
    
    item_auth=get_object_or_404(LogAut, pk = pk)
    item_auth.delete()
    
    return HttpResponseRedirect(url_ant)



#*********************************************************
#3.4 Autorizacion RACI de Asignacion de Activos a Proceso*
#*********************************************************
from .forms import Autoriza_Act_x_Proc_Form
import datetime

def Aut_Asig_Act(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[300] ))
    
    model = Proceso
    proc = get_object_or_404(Proceso, pk = pk)
    activos=proc.subproceso.recursos
    activos_disp=Recursos.objects.all().order_by('tipo')
    
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
                    
                    # Prepara correo al Gestor Responsable
                    #nombre=proc.subproceso.gestor_R.user_gestor.last_name
                    #email = proc.subproceso.gestor_R.user_gestor.email
                    #accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    proc.subproceso.status='x'
                    # Prepara correo para Gestor Consultor
                    #email = proc.subproceso.gestor_C.user_gestor.email
                    #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proc.subproceso.status=='r':

                    if aprobado:
                        print('aprobo A->R')
                        proc.subproceso.status='R'
                    
                        # Prepara correo a Gestor Interesado
                        #if proc.subproceso.gestor_I:
                        #    nombre=proc.subproceso.gestor_I.user_gestor.last_name
                        #    email = proc.subproceso.gestor_C.user_gestor.email
                        #    accion='tomar conocimiento de la puesta en vigencia del '
                    else:
                        proc.subproceso.status='x'

                
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'BCP/map_act/asig_act_auth.html', {'form': form,
                                                                  'proceso':proc,
                                                                  'activos':activos,
                                                                  'activos_disp':activos_disp,
                                                                  'comentarios':comentarios_a})


#***********************************************************
#3.5 Autorizacion RACI de Asignacion de Escenario a Proceso*
#***********************************************************
from .forms import Autoriza_Asig_Escenarios_Form
import datetime

def Aut_Asig_Esc(request, pk):

    print('----Entra a View  Autorizacion Asignacion Escenario (Aut_Asig_Esc) ----')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[300] ))
    
    model = Proceso
    proc = get_object_or_404(Proceso, pk = pk)
    escenarios=proc.subproceso.escenarios
    esc_disp=Escenarios.objects.all()
    
    form = Autoriza_Asig_Escenarios_Form()
    aut=LogAut()

    # Selecciona Comentarios sobre Escenarios
    comentarios_proceso=Log_Revision.objects.filter(proceso=proc)
    comentarios_e=[]
    for com in comentarios_proceso:
        if com.seccion == "E":
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
                    proc.subproceso.status='r'  # Por vigentear
                    
                    # Prepara email para Gestor Responsable 
                    #nombre=proc.subproceso.gestor_R.user_gestor.last_name
                    #email = proc.subproceso.gestor_R.user_gestor.email
                    #accion='dar visto bueno o requerir cambios para el '
                    
                else:
                    proc.subproceso.status='x'
                    
                    #Prepara email para Gestor Consultor
                    #email = proc.subproceso.gestor_C.user_gestor.email
                    #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
            else:
                if proc.subproceso.status=='r':

                    if aprobado:
                        print('aprobo A->R')
                        proc.subproceso.status='R'

                        # Crea o Modifica Proceso (SubProceso) Vigente
                        # Crea una entrada al log de Control de Cambios
                        # =============================================

                        
                        hay_cambios=False
                        if proc.subproceso_v == None:
                            sub_proceso_v=SubProceso_V()
                            print('Crea version inicial del Subproceso vigente.')
                            detalle_log="Version Inicial"

                            sub_proceso_v.fecha_ult_aut=datetime.date.today()
                            sub_proceso_v.pk_padre = proc.subproceso.pk_padre
                            sub_proceso_v.codigo   = proc.subproceso.codigo
                            sub_proceso_v.path = proc.subproceso.path

                            sub_proceso_v.gestor_R = proc.subproceso.gestor_R
                            sub_proceso_v.gestor_A = proc.subproceso.gestor_A
                            sub_proceso_v.gestor_C = proc.subproceso.gestor_C
                            sub_proceso_v.gestor_I = proc.subproceso.gestor_I

                            sub_proceso_v.save()
                            sub_proceso_v.impact_subp.set(proc.subproceso.impact_subp.all())
                            sub_proceso_v.indicador_subp.set(proc.subproceso.indicador_subp.all())

                            sub_proceso_v.ranking =  proc.subproceso.ranking

                            sub_proceso_v.recursos.set(proc.subproceso.recursos.all())
                            sub_proceso_v.escenarios.set(proc.subproceso.escenarios.all())

                            sub_proceso_v.save()


                        else:
                            print('Modifica el Proceso vigente existente')
                            sub_proceso_v.fecha_ult_aut=datetime.date.today()
                            detalle_log="Cambios implementados :"
                            
                            if proc.subproceso.gestor_R != proc.subproceso.gestor_R:
                                print('Cambio al Gestor Responsable')
                                detalle_log=detalle_log+'Cambio al Gestor Responsable '+proc.subproceso.gestor_R+', por'+proc.subproceso.gestor_R+'.'
                                sub_proceso_v.gestor_R != proc.subproceso.gestor_R+'. '
                                hay_cambios=True

                            if sub_proceso_v.gestor_A != proc.subproceso.gestor_A:
                                print('Cambio al Gestor Autorizador')
                                detalle_log=detalle_log+'Cambio al Gestor Autorizador '+proc.subproceso.gestor_A+', por'
                                +proc.subproceso.gestor_A+'. '
                                sub_proceso_v.gestor_A = proc.subproceso.gestor_A
                                hay_cambios=True

                            if sub_proceso_v.gestor_C != proc.subproceso.gestor_C:
                                print('Cambio al Gestor Consultor')
                                detalle_log=detalle_log+'Cambio al Gestor Consultor '+proc.subproceso.gestor_C+', por'
                                +proc.subproceso.gestor_C+'. '
                                sub_proceso_v.gestor_C = proc.subproceso.gestor_C
                                hay_cambios=True

                            if sub_proceso_v.gestor_I != proc.subproceso.gestor_I:
                                print('Cambio Persona Interesada')
                                detalle_log=detalle_log+'Cambio a la persona Interesada '+proc.subproceso.gestor_I+', por'
                                +proc.subproceso.gestor_I+'. '
                                sub_proceso_v.gestor_I = proc.subproceso.gestor_I
                                hay_cambios=True

                            #Impactos e Indicadores de recuperacion
                        
                            if sub_proceso_v.impact_subp != proc.subproceso.impact_subp:
                                print('Cambio en impactos')
                                sub_proceso_v.impact_subp.set(proc.subproceso.impact_subp)
                                hay_cambios=True

                            if sub_proceso_v.indicador_subp != proc.subproceso.indicador_subp:
                                print('CAmbio en Indicadores')
                                sub_proceso_v.indicador_subp.set(proc.subproceso.indicador_subp)
                                hay_cambios=True 

                            if sub_proceso_v.ranking !=  proc.subproceso.ranking:
                                print('Cambio en el puntaje')
                                detalle_log=detalle_log+'Cambio al Puntaje '+proc.subproceso.gestor_A+', por'
                                +proc.subproceso.gestor_A+'.'
                                sub_proceso_v.ranking =  proc.subproceso.ranking
                                hay_cambios=True
                            
                            if sub_proceso_v.recursos != proc.subproceso.recursos:
                                print('Cambios en Servicios/Recursos asignados')
                                sub_proceso_v.recursos.set(proc.subproceso.recursos)
                                hay_cambios=True

                            if sub_proceso_v.escenarios != proc.subproceso.escenarios:
                                print('Cambios en escenarios de Riesgo')
                                sub_proceso_v.escenarios.set(proc.subproceso.escenarios)
                                hay_cambios=True

                            if not hay_cambios:
                                detalle_log=detalle_log+'Vigenteo sin cambios'

                            sub_proceso_v.save()

                        # Actualiza Base 
                        proc.subproceso_v=sub_proceso_v
                        proc.save()

                        # Crea entrada para el Control de Cambios
                        # =======================================

                        log=Control_Cambios()

                        # Crea entrada
                        log.proceso=proc.subproceso_v
                        log.gestor_aut=proc.subproceso_v.gestor_R
                        log.descripcion=detalle_log
                        log.save()


                        # Prepara email para Gestor Consultor
                        # ===================================
                        #  
                        # nombre=proc.subproceso.gestor_C.user_gestor.last_name
                        # email = proc.subproceso.gestor_C.user_gestor.email
                        # accion='tomar conocimiento de la puesta en vigencia del '

                    else:
                        proc.subproceso.status='x'

                
            #Notificar a Gestor I por email
            if notifica:
                if aprobado:
                    print('***** Envio de Correo Deshabilitado ******')
                    # Envia Correo
                    # cc_email= proc.subproceso.gestor_C.user_gestor.email
                    # proceso=proc.path
                    # Manda_Correo(email, cc_email, nombre, proceso, accion)

            #Registra autorizacion en log
                                
            aut.fecha=datetime.date.today()
            aut.p_status=proc.subproceso.status+proc.subproceso.fase_status
            aut.item = 'Conclusion etapa Autorizacion.:'
            #aut.observacion=form.cleaned_data['comentario']
            aut.Aprobado=form.cleaned_data['aprobacion']                    
            
            #Graba en Base de Datos                
            aut.save()
            proc.log_auth.add(aut)      
            proc.subproceso.save()
            
             
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Escenarios') )

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'BCP/map_esc/asig_esc_auth.html', {'form': form, 'proc':proc,
                                                                  'escenarios':escenarios,
                                                                  'comentarios':comentarios_e,
                                                                  'esc_disp':esc_disp})




#*********************************************************
#3.6  Revision de Proceso con autorizazion RACI rechazada*
#*********************************************************
from .forms import RevisaProcesoForm

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
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Procesos') )

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
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
                                        
        return render(request, 'BCP/proceso_revisa.html', {'form': form,
                                                           'proceso':proc_rev,
                                                           'comentarios':comentarios_m})



#*********************************************************************************
#3.7  Revision de Asignacion de Activos a Proceso con autorizazion RACI rechazada*
#*********************************************************************************
from .forms import Revisa_AsigAct_x_Proc_Form

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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:

        p2=proc_rev.subproceso.recursos.all()
        form = Revisa_AsigAct_x_Proc_Form(initial= {'activos':set(p2),
                                                    'notifica':False}
                                          )

                                               
        return render(request, 'BCP/map_act/asigna_act_revisa.html', {'form': form, 'proceso':proc_rev})


def rev_asigna_servicio(request, pk):
    """ ----------------------------------------------------------------
    Revisa e implementa los Comentarios realizados por los Supervisores 
    pk: Pk del Proceso.
    --------------------------------------------------------------------
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
        else:
            subproceso.recursos.clear()  # Si no hay recursos, limpiar asignaciones

        subproceso.save()  # Guardar los cambios

        return HttpResponseRedirect(reverse('Lista-Recursos'))

    # Cargar recursos disponibles y asignados
    recursos_disponibles = Recursos.objects.exclude(id__in=subproceso.recursos.values_list('id', flat=True))
    recursos_asignados = subproceso.recursos.all()

    return render(request, 'BCP/map_act/rev_asigna_activos_v2.html', {
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

            
        
    else:

        p2=proc_rev.subproceso.escenarios.all()
        form = Revisa_Asig_Esc_Form(initial= {'escenarios':set(p2),
                                              'notifica':False} )

                                               
        return render(request, 'BCP/map_esc/asigna_esc_revisa.html', {'form': form,
                                                                      'proceso':proc_rev,
                                                                      'comentarios':comentarios_m})
    
    

#****************************************************************************
# 3.9 Revision de Asignacion BIA  a Proceso con autorizazion RACI rechazada *
#****************************************************************************
from .forms import Revisa_Asig_BIA_Form

def Revisa_Asig_BIA(request, pk):

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
            if proceso.subproceso.gestor_C == proceso.subproceso.gestor_A:
                
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:

        form = Revisa_Asig_BIA_Form(initial= {'proceso':proceso,
                                              'impactos':impactos,
                                              'indicadores':indicadores,
                                              #'observaciones':obs_asig_bia,
                                              'notifica':False} )

                                               
        return render(request, 'BCP/map_eval/asigna_eval_rev.html', {'form': form,
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
def Crea_Rev_OC(request):
    """ Crea un Comentario de Revision durante la Revision
    de cada Proceso o PC segun su etapa. """

    print('---- Crea Observacion  ------')
    print('metodo=', request.method)

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    usuario_sesion=Gestor.objects.get(user_pk=pk_usr_sesion)
    print('usuario de sesion',usuario_sesion)

    fecha_hoy=datetime.date.today()

    if request.method == "POST":
        # rescata datos del json
        data = json.loads(request.body)
        print('data=', data)
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

        else:
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 

            
        
    else:
        print('Entra a GET Escenarios')
        p2 = proceso.subproceso.escenarios.all()
        form = Asig_Esc_Form(initial= {'escenarios':set(p2)})
                                        
        return render(request, 'BCP/map_esc/asigna_escenarios.html', {'form': form, 'proceso':proceso, 'escenarios':escenarios})




#********************************
#4.2 Asigna Activos a un Proceso*
#********************************
from .forms import Act_x_Proc_Form

#@permission_required('Catalogo.can_mark_returned')
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        #p2 = proceso.subproceso.recursos.all()
        #form = Act_x_Proc_Form(initial= {'activos':set(p2)})
        form = Act_x_Proc_Form()
                                        
        return render(request, 'BCP/map_act/asigna_activos.html', {'form': form, 'proceso':proceso})





from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Proceso, SubProceso, Recursos
from .forms import ServicioForm

def asigna_servicio(request, pk):
    proceso = get_object_or_404(Proceso, pk=pk)
    subproceso = proceso.subproceso

    if request.method == "POST":
        recursos_ids = request.POST.get("recursos", "").split(",")  # Obtener los recursos seleccionados
        recursos_ids = [int(r) for r in recursos_ids if r.isdigit()]  # Filtrar solo los números válidos

        if recursos_ids:
            subproceso.recursos.set(Recursos.objects.filter(id__in=recursos_ids))  # Asignar recursos
        else:
            subproceso.recursos.clear()  # Si no hay recursos, limpiar asignaciones

        subproceso.save()  # Guardar los cambios

        return HttpResponseRedirect(reverse('Lista-Recursos'))

    # Cargar recursos disponibles y asignados
    recursos_disponibles = Recursos.objects.exclude(id__in=subproceso.recursos.values_list('id', flat=True))
    recursos_asignados = subproceso.recursos.all()

    return render(request, 'BCP/map_act/asigna_activos_v2.html', {
        'form': ServicioForm(),
        'proceso': proceso,
        'subproceso': subproceso,
        'recursos_disponibles': recursos_disponibles,
        'recursos_asignados': recursos_asignados,
    })

#***********************************************
#4.3 Asigna Impactos e Indicadores a un Proceso*
#***********************************************

#@permission_required('Catalogo.can_mark_returned')
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

                                        
    return render(request, 'BCP/map_eval/asigna_eval.html', {'proceso':proceso,
                                                             'impactos':impactos_pc,
                                                             'indicadores':indicador_pc,
                                                             'total_imp':total_imp,
                                                             'total_ind':total_ind,
                                                             'total_pro':total_pro})

from .forms import Asig_Imp_Form 
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        #p2 = proceso.subproceso.recursos.all()
        #form = Act_x_Proc_Form(initial= {'activos':set(p2)})
        form = Asig_Imp_Form(request.POST  or None, param=riesgo,
                             initial= {'nivel':nub_impacto.nivel} )
                                        
        return render(request, 'BCP/map_eval/asigna_nivel_imp.html', {'nub_impacto':nub_impacto,
                                                                      'proceso':proceso,
                                                                      'opciones':opciones,
                                                                      'riesgo':riesgo,
                                                                      'form':form})

from .forms import Asig_Ind_Form
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        #p2 = proceso.subproceso.recursos.all()
        #form = Act_x_Proc_Form(initial= {'activos':set(p2)})
        form = Asig_Ind_Form(request.POST  or None, param=indicador,
                             initial= {'nivel':nub_indicador.nivel} )
                                        
        return render(request, 'BCP/map_eval/asigna_nivel_ind.html', {'nub_indicador':nub_indicador,
                                                                      'proceso':proceso,
                                                                      'opciones':opciones,
                                                                      'indicador':indicador,
                                                                      'form':form})

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


    if etapa=="V":
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
    template_name='BCP/proced_cont/proced_list.html'


def Lista_Procedimientos(request):
    """
    Lista Procedimientos 
    """
    print('-------- Entra a Lista de Procedimientos ----------')
    #Determina tramos de criticidad del Proceso
    bia_bajo  = get_object_or_404(Parametros_G, pk = 5)
    bia_medio = get_object_or_404(Parametros_G, pk = 6)
    bia_alto  = get_object_or_404(Parametros_G, pk = 7)

    tramo_1 = float(bia_bajo.valor_2)/100*5
    tramo_2 = tramo_1 + float(bia_medio.valor_2)/100*5
    print('tramo_1:', tramo_1)
    print('tramo_2:', tramo_2) 


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

    return render(request, 'BCP/proced_cont/proced_list.html',
                  context={'lista_procesos':lista_procesos_v, 'tramo_1':tramo_1, 'tramo_2':tramo_2})
    
#*****************************************************
# 5.1  Creacion de Procedimiento de Recuperacion (PC) *
#*****************************************************

#***********************************************************
# 5.1.1  Creacion Inicial de Procedimiento de Recuperacion *
#***********************************************************
from .forms import CreaProc_A_Form

#@permission_required('Catalogo.can_mark_returned')
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
            proced.tipo = form.cleaned_data['tipo']


            #Asigna al usuario de sesion como gestor consultor
            usuario_sesion = request.user.pk
            print('usr_ses=',usuario_sesion)
            usuario_ges=get_object_or_404(Gestor, user_pk=usuario_sesion)
            print('usuario_gestor', usuario_ges)
            proced.gestor_consultor = usuario_ges
            

            #Asigna estarus C : En definicion 
            proced.status = 'C'
            
            #Graba Procedimiento
            proced.save()
            proceso.subproceso_v.procedimientos_contingencia.add(proced)
            proceso.subproceso_v.save()
            proceso.save()            

            print('Grabo Procedimiento')

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Proced'))
        
        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})             
            
        
        

    # If this is a GET (or any other method) create the default form.
    else:

        form = CreaProc_A_Form(initial= {
                                'nombre':proced.nombre,
                                'tipo':proced.tipo,
                                
                                }
                        )

    
        return render(request, 'BCP/proced_cont/prcd_crea_A.html', {'form': form, 'proceso':proceso})

#*************************************************************
# 5.1.2  Creacion parte (B) de Procedimiento de Recuperacion *
#*************************************************************
from .forms import CreaProc_B_Form

#@permission_required('Catalogo.can_mark_returned')
def cr_prcd_b(request, pk):

    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso= get_object_or_404(Proceso, pk = proced.pk_padre)
    escenarios=proceso.subproceso.escenarios
   
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos


        
    print('nombre proceso=', proceso.nombre)
    print('nombre procedimiento=', proced.nombre)

    print('Crea parte B')
    
  
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreaProc_B_Form(request.POST)
        form = CreaProc_B_Form(request.POST  or None, param=escenarios.all()) # Envia Escenarios del Proceso

        
        # Check if the form is valid:
        
        if form.is_valid():
            
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Crea el Registro del Proceso

                        
            proced.nombre = form.cleaned_data['nombre']
            proced.tipo = form.cleaned_data['tipo']
            
            proced.escenarios = form.cleaned_data['escenarios']

            proced.estrategia = form.cleaned_data['estrategia']
            


            responsable = form.cleaned_data['resp_proceso']
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            
            
        # redirect to a new URL:
        
        #return HttpResponseRedirect(reverse('Lista-Proced'))
        return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
        #return render(request, 'BCP/proced_cont/proced_crea_C.html', {'proced':proced, 'proceso':proceso, 'escenarios':escenarios, 'servicios':servicios,
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

    
        return render(request, 'BCP/proced_cont/proced_crea_B.html', {'form': form, 'proced':proced, 'proceso':proceso, 'escenarios':escenarios,
                                                                      'servicios':servicios, 'contactos':contactos,'pasos':pasos})


#*************************************************************
# 2.2.3  Creacion parte (C) de Procedimiento de Recuperacion *
#*************************************************************
from .forms import CreaProc_P5_Form

#@permission_required('Catalogo.can_mark_returned')
def cr_prcd_P5(request, pk, fase):
    """
    Ingresa Servicios Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision 
    """
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
            if fase == '0':
                return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
            else:
                return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))
        
        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        print(url_ant)
        form = CreaProc_P5_Form()
        return render(request, 'BCP/proced_cont/prcd_crea_serP5.html', {'form': form, 'servicios':proced.servicios_pc})    


#@permission_required('Catalogo.can_mark_returned')
def br_prcd_P5(request, pk, fase):
    """
    Borra Servicios Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision 

    """
    
    servicio_pc = get_object_or_404(Servicios_PC, pk = pk)
    proced = get_object_or_404(Procedimientos, pk = servicio_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_servicios
    #num = num-1
    #proced.sec_servicios = num
    proced.save()

    #Borra Servicio                
    servicio_pc.delete()
    
    if fase == '0':
        return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
    else:
        return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))


from .forms import CreaProc_P6_Form

#@permission_required('Catalogo.can_mark_returned')
def cr_prcd_P6(request, pk, fase):
    """
    Ingresa Contactos Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision 

    """
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

            if fase == '0':
                return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
            else:
                return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))
            
            #proced.servicios_pc.save()
        
        else:
            
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})            
                     
        

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        form = CreaProc_P6_Form()
        return render(request, 'BCP/proced_cont/prcd_crea_conP6.html', {'form': form, 'contactos':proced.contactos_pc})
    

#@permission_required('Catalogo.can_mark_returned')
def br_prcd_P6(request, pk, fase):
    """
    Borra Servicios Criticos para el PC
    pk: pk del Procedimiento
    fase: 0: Creacion 1:Revision
    """
  
    contacto_pc = get_object_or_404(Contactos_PC, pk = pk)
    proced = get_object_or_404(Procedimientos, pk = contacto_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_contactos
    #num = num-1
    #proced.sec_contactos = num
    proced.save()
   
    contacto_pc.delete()

    if fase == '0':
        return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
    else:
        return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))
    
from .forms import CreaProc_P7_Form

#@permission_required('Catalogo.can_mark_returned')
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
            proced.pasos.add(paso)

            #Marca la seccion como completa
            #num = proced.sec_pasos
            #num = num+1
            #proced.sec_pasos = num
            #proced.save()
            
            # redirect to a new URL:
            if fase == '0':
                return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
            else:
                return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))

            
        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
            

    # If this is a GET (or any other method) create the default form.
    else:

        form = CreaProc_P7_Form(initial={'ejecutor':proced.gestor_ejecutor})

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'BCP/proced_cont/prcd_crea_pasP7.html', {'form': form, 'pasos':proced.pasos,
                                                                        'rto':rto,
                                                                        'proc':proced,
                                                                        'proceso':proceso,
                                                                        'acum':acum,
                                                                        'acum_h':acum_h})
    

#@permission_required('Catalogo.can_mark_returned')
def br_prcd_P7(request, pk, fase):
    """
    Borra Pasos del PC
    """
       
    
    paso_pc = get_object_or_404(Pasos_PC, pk = pk)
    proced = get_object_or_404(Procedimientos, pk = paso_pc.pk_padre)

    #Actualiza cantidad de registros    
    #num = proced.sec_pasos
    #num = num-1
    #proced.sec_pasos = num
    #proced.save()
   
    paso_pc.delete()

    if fase == '0':
        print('vuelva a lista-c')
        return HttpResponseRedirect(reverse('lista-c', args=[str(proced.id)]))
    else:
        print('vuelve a rev-proced-v')
        return HttpResponseRedirect(reverse('rev-proced-b', args=[str(proced.id)]))



#*************************************************************
# 2.2.4  Borra el Procedimiento de Contingencia              *
#*************************************************************


    
#*******************************************************
# 3.10 Autorizacion del  Procedimiento de Contingencia *
#*******************************************************


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
    return HttpResponseRedirect(reverse('Lista-Proced') )

    
from .forms import Autoriza_Proced_C_Form
import datetime

def Aut_Proced_C(request, pk):
    """
    Autorizacion del Procedimiento
    Crea o Actualiza el Procedimiento Vigente 
    """
    print('-------- Entra Autoriza Procedimiento ---------')
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso= get_object_or_404(Proceso, pk = proced.pk_padre)

    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos

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

                # Cambia a estado A (Aprobado)
                # ============================
                print('> aprobo C->A')
                proced.status='A'
                print('status=',proced.status)


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


                        # Crea Procedimiento Vigente
                        # ==========================

                        proced_v = Procedimientos_V()
                        print('>  PC vigente  no existe. Crea version inicial del PC vigente.')
                        detalle_log="Version Inicial."
                        proced_v.version = 0
                        

                        proced_v.fecha_c = datetime.date.today()
                        proced_v.pk_padre = proced.pk_padre
                        proced_v.codigo   = proced.codigo

                        #Identificacion del Procedimiento
                        proced_v.nombre = proced.nombre
                        proced_v.tipo = proced.tipo

                        #Contexto
                        proced_v.escenarios = proced.escenarios
                        proced_v.estrategia = proced.estrategia

                        #Responsables
                        proced_v.resp_proceso = proced.resp_proceso
                        proced_v.bck_resp = proced.bck_resp
                        proced_v.gestor_ejecutor = proced.gestor_ejecutor 
                        proced_v.bck_ejecutor  = proced.bck_ejecutor

                        proced_v.enlace_c_crisis = proced.enlace_c_crisis
                        proced_v.bck_enlace = proced.bck_enlace
                        proced_v.gestor_consultor = proced.gestor_consultor
                        proced_v.save()

                        #Servicios  
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

                        
                        # Contactos
                        for con in proced.contactos_pc.all():
                            # Crea entrada de Contactos
                            contactos_pc_v=Contactos_PC_V()

                            contactos_pc_v.pk_padre = con.pk_padre
                            contactos_pc_v.cont_int = con.cont_int
                            contactos_pc_v.nombre = con.nombre
                            contactos_pc_v.correo = con.correo
                            contactos_pc_v.tel_lab = con.tel_lab
                            contactos_pc_v.cel_lab = con.cel_lab

                            contactos_pc_v.save()
                            proced_v.contactos_pc.add(contactos_pc_v)

                        #Pasos del Procedimiento
                        for pas in proced.pasos.all():
                            # Crea entrada de Pasos
                            pasos_v=Pasos_PC_V()

                            pasos_v.pk_padre = pas.pk_padre
                            pasos_v.nro_paso = pas.nro_paso
                            pasos_v.descripcion = pas.descripcion
                            pasos_v.ejecutor = pas.ejecutor
                            pasos_v.tiempo_esp = pas.tiempo_esp

                            pasos_v.save()
                            proced_v.pasos.add(pasos_v)
                        

                        proced.existe_p_vigente=True  # Marca que el Procedimiento Vigente existe
                        
                        proced_v.save()
                        proced.save()

                        #print('PARA', para)


                else:

                        # PC existe. Se modifica 
                        # ======================
                        print('> Existe PC vigente. Modifica el Proceso vigente existente')

                        proced_v=get_object_or_404(Procedimientos_V, codigo=codigo_prcd)

                        proced_v.fecha_c = datetime.date.today()
                        proced_v.version = int(proced_v.version) + 1 
                        detalle_log="Cambios implementados : "

                        nombre_v=proced_v.nombre
                        nombre_o=proced.nombre
                        print('nombre_v=',nombre_v,'- nombre_o =', nombre_o)
                            
                        if proced_v.nombre != proced.nombre:
                            print('Cambio Nombre')
                            detalle_log=detalle_log+'Cambio al Nombre "'+proced_v.nombre+'", por "'+proced.nombre+'". '
                            proced_v.nombre = proced.nombre
                            hay_cambios=True
                        else:
                            print('son iguales')
                            print('detalle log=', detalle_log)


                        if proced_v.tipo != proced.tipo:
                            print('Cambio Tipo')
                            detalle_log=detalle_log+'Cambio al Tipo de PC ['+proced_v.tipo.nombre+'], por ['+proced.tipo.nombre+'].'
                            proced_v.tipo = proced.tipo
                            hay_cambios=True

                        else:
                            print('tipo: son iguales')
                            print('detalle log=', detalle_log)

                        
                        if proced_v.escenarios != proced.escenarios:
                            print('Cambio en Escenarios')
                            detalle_log=detalle_log+'Cambio al Escenario ['+proced_v.escenarios.titulo+'], por ['+proced.escenarios.titulo+']. '
                            proced_v.escenarios = proced.escenarios
                            hay_cambios=True

                        if proced_v.estrategia != proced.estrategia:
                            print('CAmbio en Estrategia')
                            detalle_log=detalle_log+'Cambio a la Estrategia ['+proced_v.estrategia+'], por ['+proced.estrategia+']. '
                            proced_v.estrategia = proced.estrategia
                            hay_cambios=True 

                        print('> Estrategia: detalle log=', detalle_log)
                        print('hay cambios=', hay_cambios)



                        # Roles
                        if proced_v.resp_proceso != proced.resp_proceso:
                            print('Cambio en el Responsable')
                            detalle_log=detalle_log+'Cambio al Responsable -'+proced_v.resp_proceso.user_gestor.last_name+'-, por -'+proced.resp_proceso.user_gestor.last_name+'-. '
                            proced_v.resp_proceso = proced.resp_proceso
                            hay_cambios=True

                        if proced_v.bck_resp != proced.bck_resp:
                            print('Cambio en el Respaldo del Responsable')
                            if proced_v.bck_resp != None and  proced.bck_resp != None:
                                detalle_log=detalle_log+'Cambio al Respaldo del Responsable -'+proced_v.bck_resp.user_gestor.last_name+'-,'+proced_v.bck_resp.user_gestor.first_name+', por '+proced.bck_resp.user_gestor.last_name+','+proced_v.bck_resp.user_gestor.first_name+'.'
                            elif  proced.bck_resp == None:
                                detalle_log=detalle_log+'Se elimino al Respaldo del Responsable sin Asignacion definida. '
                            else:
                                detalle_log=detalle_log+'Se asigna a '+proced.bck_resp.user_gestor.last_name+' Como Respaldo al Responsable.'
                            print(detalle_log)        
                            proced_v.bck_resp = proced.bck_resp
                            hay_cambios=True

                        if proced_v.gestor_ejecutor != proced.gestor_ejecutor:
                            print('Cambio en el Ejecutor')
                            detalle_log=detalle_log+'Cambio al Ejecutor '+proced.gestor_ejecutor.user_gestor.last_name+', por '+proced_v.gestor_ejecutor.user_gestor.last_name+'.'
                            proced_v.gestor_ejecutor = proced.gestor_ejecutor
                            hay_cambios=True

                        if proced_v.bck_ejecutor != proced.bck_ejecutor:
                            print('Cambio en el Respaldo Ejecutor')
                            if proced_v.bck_ejecutor != None :
                                detalle_log=detalle_log+'Cambio al Respaldo del Ejecutor '+proced_v.bck_ejecutor.user_gestor.last_name+','+proced_v.bck_ejecutor.user_gestor.first_name+', por '+proced.bck_ejecutor.user_gestor.last_name+','+proced_v.bck_ejecutor.user_gestor.first_name+'.'
                            elif  proced.bck_ejecutor == None:
                                detalle_log=detalle_log+'Se elimino al Respaldo del Ejecutor sin Asignacion definida. '
                            else:
                                detalle_log=detalle_log+'Se asigna a '+proced.bck_ejecutor.user_gestor.last_name+' Como Respaldo al Ejecutor.'

                            proced_v.bck_ejecutor = proced.bck_ejecutor
                            hay_cambios=True

                        if proced_v.enlace_c_crisis != proced.enlace_c_crisis:
                            print('Cambio en el Enlace CC')
                            detalle_log=detalle_log+'Cambio al Enlace del Comite de Crisis '+proced.enlace_c_crisis.user_gestor.last_name+', por '+proced_v.enlace_c_crisis.user_gestor.last_name+'.'
                            proced_v.enlace_c_crisis = proced.enlace_c_crisis
                            hay_cambios=True


                        if proced_v.bck_enlace != proced.bck_enlace:
                            print('Cambio en el Respaldo Enlace CC')
                            if proced_v.bck_enlace != None :
                                detalle_log=detalle_log+'Cambio al Respaldo del Enlace del Comite de Crisis  '+proced_v.bck_enlace.user_gestor.last_name+','+proced_v.bck_enlace.user_gestor.first_name+', por '+proced.bck_enlace.user_gestor.last_name+','+proced_v.bck_enlace.user_gestor.first_name+'.'
                            elif  proced.bck_ejecutor == None:
                                detalle_log=detalle_log+'Se elimino al Respaldo del Enlace del Comite de Crisis sin Asignacion definida. '
                            else:
                                detalle_log=detalle_log+'Se asigna a '+proced.bck_enlace.user_gestor.last_name+' Como Respaldo del Enlace del Comite de Crisis.'

                            proced_v.bck_enlace = proced.bck_enlace
                            hay_cambios=True

                        print('>Roles: detalle log=', detalle_log)
                        print('hay cambios=', hay_cambios)



                        # Actualiza Servicios
                        # ====================
                        # Verifica si se elimino un Servicio
                        print('> Elimina >>>')
                        for v in proced_v.servicios_pc.all():
                            existe=False
                            print('> **** v=', v.nombre)
                            for o in proced.servicios_pc.all():
                                if v.nombre == o.nombre :    # Si esta en el original 
                                    existe=True
                                print('> v= ', v.nombre,', ', 'o= ', o.nombre, 'existe = ', existe)
                            
                            if  not existe :
                                detalle_log=detalle_log+'Se elimino  el servicio : "'+v.nombre+'", '
                                proced_v.servicios_pc.remove(v)
                                hay_cambios=True


                        # Verifica si se agrego un Servicio
                        print('> Agrega >>>')
                        for o in proced.servicios_pc.all():
                            existe=False
                            for v in proced_v.servicios_pc.all():
                                if o.nombre == v.nombre: 
                                        existe=True
                                print('v= ',v.nombre,', ', 'o= ', o.nombre, 'existe = ', existe)

                            if not existe:
                                detalle_log=detalle_log+'Se agrego el servicio : "'+o.nombre+'", '
                                # Crea entrada a Servicios
                                servicios_pc_v=Servicios_PC_V()

                                servicios_pc_v.pk_padre = o.pk_padre 
                                servicios_pc_v.nombre = o.nombre
                                servicios_pc_v.objetivo = o.objetivo
                                servicios_pc_v.contacto = o.contacto
                                servicios_pc_v.contacto_bck = o.contacto_bck

                                servicios_pc_v.save()
                                proced_v.servicios_pc.add(servicios_pc_v)
                                hay_cambios=True

                        # Actualiza la BD con los Servicios
                        #proced_v.servicios_pc.set(list(proced.servicios_pc.all()))
                        proced_v.save()

                        print('>Servicios: detalle log=', detalle_log)
                        print('hay cambios=', hay_cambios)
                    

                        # Actualiza Contactos
                        # ====================
                        # Verifica si se Elimino un Contacto
                        for v in proced_v.contactos_pc.all():
                            existe=False
                            for o in proced.contactos_pc.all():
                                if o.nombre == v.nombre:
                                        existe=True
                            if not existe:
                                detalle_log=detalle_log+'Se elimino el Contacto : '+v.nombre+', '
                                proced_v.contactos_pc.remove(v)
                                hay_cambios=True



                        # Verifica si se Agego un Contacto
                        for o in proced.contactos_pc.all():
                            existe=False
                            for v in proced_v.contactos_pc.all():
                                if o.nombre == v.nombre: 
                                        existe=True
                            if not existe:
                                detalle_log=detalle_log+'Se agrego  el Contacto : '+o.nombre+', '
                                # Crea entrada de Contactos
                                contactos_pc_v=Contactos_PC_V()

                                contactos_pc_v.pk_padre = o.pk_padre
                                contactos_pc_v.cont_int = o.cont_int
                                contactos_pc_v.nombre = o.nombre
                                contactos_pc_v.correo = o.correo
                                contactos_pc_v.tel_lab = o.tel_lab
                                contactos_pc_v.cel_lab = o.cel_lab

                                contactos_pc_v.save()
                                proced_v.contactos_pc.add(contactos_pc_v)

                                hay_cambios=True

                        # Actualiza la BD de Contactos
                        #proced_v.contactos_pc.set(proced.contactos_pc.all())
                        proced_v.save()
                        
                        print('> Contactos: detalle log=', detalle_log)
                        print('hay cambios=', hay_cambios)



                        # Actualiza Pasos del PC
                        # ======================
                        # Verifica si se Elimino un Paso
                        for v in proced_v.pasos.all():
                            existe=False
                            for o in proced.pasos.all():
                                if o.descripcion  == v.descripcion: 
                                        existe=True
                            if not existe:
                                detalle_log=detalle_log+'Se elimino el Paso nro. : '+str(v.nro_paso)+'.-) '+v.descripcion+'-, '
                                proced_v.pasos.remove(v)
                                hay_cambios=True

                        # Verifica si se Agrego un Paso
                        for o in proced.pasos.all():
                            existe=False
                            for v in proced_v.pasos.all():
                                if o.descripcion == v.descripcion: 
                                        existe=True
                            if not existe:
                                detalle_log=detalle_log+'Se agrego el Paso nro. : '+str(o.nro_paso)+'.-) '+o.descripcion+'-, '
                                # Crea entrada de Pasos
                                pasos_v=Pasos_PC_V()

                                pasos_v.pk_padre = o.pk_padre
                                pasos_v.nro_paso = o.nro_paso
                                pasos_v.descripcion = o.descripcion
                                pasos_v.ejecutor = o.ejecutor
                                pasos_v.tiempo_esp = o.tiempo_esp

                                pasos_v.save()
                                proced_v.pasos.add(pasos_v)

                                hay_cambios=True

                        # Actualiza la BD de Pasos
                        #proced_v.pasos.set(proced.pasos.all())
                        proced_v.save()
                        
                        print('pasos: detalle log=', detalle_log)
                        print('hay cambios=', hay_cambios)



                        if not hay_cambios:
                            detalle_log='Vigenteo sin cambios'

                        print('Detalle log final', detalle_log)

                        proced_v.save()
                        #proceso.subproceso_v.procedimientos_contingencia_v.set([proced_v])
                        proceso.subproceso_v.save()
                        proceso.save()

                        # FIN PC existe. Se modifica 
                  
                # Crea entrada para el Control de Cambios
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
            return HttpResponseRedirect(reverse('Lista-Proced'))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )
                                        
        return render(request, 'BCP/proced_cont/proced_auth.html', {'form': form,
                                                                    'proceso':proceso,
                                                                    'proced':proced,
                                                                    'servicios':servicios,
                                                                    'contactos':contactos,
                                                                    'comentarios':comentarios_pc,
                                                                    'pasos':pasos})



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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
    
        url_ant_obs_aut =request.META['HTTP_REFERER']
        form= Autoriza_obs_Proced_C_Form()
        
        return render(request, 'BCP/proced_cont/proced_obs_auth.html', {'form': form, 'proced':proced, 'item':item, 'valor':valor})



#****************************************************************************
#3.11 Revision Autorizacion RACI de Procedimiento de Contingencia Rechazada *
#****************************************************************************

from .forms import Revisa_Proced_B_Form

def Revisa_Proced_B(request, pk):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))


    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso= get_object_or_404(Proceso, pk = proced.pk_padre)
    escenarios=proceso.subproceso.escenarios
    
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos

    comentarios_pc=Log_Revision.objects.filter(procedimiento=proced)

    print('nombre proceso=', proceso.nombre)
    print('nombre procedimiento=', proced.nombre)

    print('Revisa parte B')
    
    #Asigna el formulario creado en Forrms
    form=Revisa_Proced_B_Form()
    
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = Revisa_Proced_B_Form(request.POST)
        
        # Check if the form is valid:
        
        if form.is_valid():
            
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            #Actualiza el Registro del Proceso

                        
            proced.nombre = form.cleaned_data['nombre']
            proced.tipo = form.cleaned_data['tipo']
            
            proced.escenarios = form.cleaned_data['escenarios']

            proced.estrategia = form.cleaned_data['estrategia']
            
            proced.resp_proceso = form.cleaned_data['resp_proceso']
            proced.bck_resp = form.cleaned_data['bck_resp']

            proced.gestor_ejecutor = form.cleaned_data['gestor_ejecutor']
            proced.bck_ejecutor = form.cleaned_data['bck_ejecutor']

            proced.enlace_c_crisis = form.cleaned_data['enlace_c_crisis']
            proced.bck_enlace = form.cleaned_data['bck_enlace']
            
            
            # Cambia Status a "a" (Por Autorizar)
            
            proced.status = 'a'
            

            #if notifica: (manda correo de notificacion)
            
            #Graba Procedimiento
            proced.save()
            proceso.subproceso.save()
            proceso.save()            

            print('Grabo Procedimiento')
            
            # redirect to a new URL:
        
            return HttpResponseRedirect(reverse('Lista-Proced'))

            
        else:
            
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    # If this is a GET (or any other method) create the default form.
    else:
        print('nombre procedimiento=', proced.nombre)
        form = CreaProc_B_Form(initial= {
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

    
        return render(request, 'BCP/proced_cont/proced_rev_B.html', {'form': form,
                                                                     'proced':proced,
                                                                     'proceso':proceso,
                                                                     'escenarios':escenarios,
                                                                     'servicios':servicios,
                                                                     'contactos':contactos,
                                                                     'pasos':pasos,
                                                                     'comentarios':comentarios_pc})




    
#*******************************************************************************
#1.10 Lista de Servicios, Contactos y Pasos en Creacion de Procedimiento(PC)   *
#*******************************************************************************
def cr_prcd_list(request, pk):
    """
    Generic class-based view listing books on loan to current user.
    """
    print('lista Servicios/Contactos/Pasos')
    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso = get_object_or_404(Proceso, pk=proced.pk_padre)
    escenarios = proceso.subproceso.escenarios
    servicios = proced.servicios_pc
    contactos = proced.contactos_pc
    pasos = proced.pasos
    
    
    return render(request, 'BCP/proced_cont/proced_crea_C.html', {'proced':proced, 'proceso':proceso, 'escenarios':escenarios, 'servicios':servicios,
                                                                  'contactos':contactos, 'pasos':pasos})


#******************************************************
# 1.10 Muestra datos (detalle) del Procedimiento(PC)  *
#******************************************************
def detalle_procedimiento(request, pk ):
    """ Detalle del Procedimiento
    pk: Identificacion del Procedimiento
    """

    proced = get_object_or_404(Procedimientos, pk = pk)
    proceso = get_object_or_404(Proceso, pk=proced.pk_padre)
    return render(request, 'BCP/proced_cont/proced_detalle.html', {'proced':proced, 'proceso':proceso})
    
def detalle_procedimiento_v(request, pk): 
    """ Detalle del Procedimiento Vigente
    pk: Identificacion del Procedimiento
    """

    proced = get_object_or_404(Procedimientos, pk = pk)
    proced_v=get_object_or_404(Procedimientos_V, codigo=proced.codigo)
    proceso = get_object_or_404(Proceso, pk=proced.pk_padre)

    c_cambio=Control_Cambios.objects.filter(procedimiento=proced_v)

    return render(request, 'BCP/proced_cont/proced_detalle_v.html', {'proced':proced_v,
                                                                     'proceso':proceso,
                                                                     'c_cambio':c_cambio})

#******************************************************
# 1.11 Muestra datos (detalle) del Procedimiento(PC)  *
#******************************************************
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

    return HttpResponseRedirect(reverse('Lista-Proced'))


#*******************************
# 1.12 Activa / Desactiva PC   *
#*******************************
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

    return HttpResponseRedirect(reverse('Lista-Proced'))


#*********************************************************************************************************************************************
#***********************************************  6. DRP  ************************************************************************************
#*********************************************************************************************************************************************

#********************************
# 6.1 Lista los DRPs definidos  *
#********************************

def Lista_DRP(request):
    """Lista los DRPs"""

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user,'TI']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[500] ))

    lista_drp = Drp.objects.all()
    
    return render(request, 'BCP/drp/lista_drp.html', context={'lista_drp':lista_drp})

#******************************************************
# 6.2 Muestra el Indice con las Secciones del DRP     *
#******************************************************
def Indice_DRP(request, pk):
    """
    Indice de DRP 
    """
    print('------ Indice_DRP --------')
    #lista_procesos = Proceso.objects.all()
    drp =  get_object_or_404(Drp, pk = pk)
    
    return render(request, 'BCP/drp/indice_drp.html', context={'drp':drp})


#**********************
# 6.3 Crea un DRP     *
#**********************
from .forms import Crea_DRP_Enc_Form

def Crea_Drp(request):

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))

    
    # Determinacion de Codigo a asignar.

    cod = get_object_or_404(Parametros_G, pk = 8)
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        form = Crea_DRP_Enc_Form()
        return render(request, 'BCP/drp/crea_drp.html', {'form':form})

#**********************
# 6.4 Borra un DRP    *
#**********************
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        form = Drp_Sec_1_Form(initial={'objetivo':drp.introduccion})
        return render(request, 'BCP/drp/objetivo_drp.html', {'drp':drp, 'form':form})

 

#*************************************
# 6.6 registra Equipo Gestores  DRP  *
#*************************************
from .forms import Drp_Sec_2_Form

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
                    print('Crea respaldo enlace=', contacto0302.nombre)

            # Cambia status y graba al equipo de Gestores
            drp.status_t='C'
            
            drp.save()

            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print('*** ERROR DE INGRESO ***', form.errors)
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form.errors':form.errors})

    else:

        form = Drp_Sec_2_Form(initial={'resp_drp':drp.resp_drp,
                                       'bck_resp':drp.bck_resp_drp,
                                       'gestor_ejecutor':drp.gestor_ejecutor_drp,
                                       'bck_ejecutor':drp.bck_ejecutor_drp,
                                       'enlace_c_crisis':drp.enlace_c_crisis_drp,
                                       'bck_enlace':drp.bck_enlace_drp})

        return render(request, 'BCP/drp/responsable_drp.html', {'drp':drp, 'form':form})


#*************************************
# 6.7 Definicion Alcance del   DRP   *
#*************************************
from .forms import Drp_Sec_3_Form

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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Drp_Sec_3_url_ant = request.META['HTTP_REFERER']
        print('Drp_Sec_3_url_ant  =', Drp_Sec_3_url_ant)
        p2=drp.procesos_drp.all()

        form = Drp_Sec_3_Form(initial={ 'procesos':set(p2)})
        return render(request, 'BCP/drp/alcance_drp.html', {'drp':drp, 'form':form})



#*******************************************
# 6.8 Definicion la Estrategia del   DRP   *
#*******************************************
from .forms import Drp_Sec_4_Form

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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Drp_Sec_4_url_ant = request.META['HTTP_REFERER']

        form = Drp_Sec_4_Form(initial={ 'tipo_site':drp.tipo_Site,
                                       'tipo_disp':drp.disposicion_componentes,
                                       'desc_estrategia':drp.desc_estrategia
                                       
                                       })
        return render(request, 'BCP/drp/estrategia_drp.html', {'drp':drp, 'form':form})


#**************************************
# 6.9 Especificacion Tecnica  del DRP *
#**************************************
    
#**********************************
# 6.9.1 Lista Componentes del DRP *
#**********************************

def Lista_CMP(request, pk):
    """Lista los Componentes de Hw y Sw del DRPs"""

    print('----- Lista CMP----')
    drp=get_object_or_404(Drp, pk=pk)
    lista_cmp=drp.componentes 

    url_comp=Componentes.get_absolute_url
    print('url ant=', url_ant)

    return render(request, 'BCP/drp/lista_cmp.html', context={'lista_cmp':lista_cmp, 'url_comp':url_comp, 'drp':drp})


#*************************************
# 6.9.2 Asigna Componentes a un  DRP *
#*************************************
from .forms import Drp_Sec_5_Form

def Asigna_CMP(request, pk, accion):
    """Asigna/desasigna Componentes de la BD a un  DRP """

    global Asigna_CMP_ult_url

    print('----- Asigna/Desasigna Componentes ----')
    drp=get_object_or_404(Drp, pk=pk)
    
    form=Drp_Sec_5_Form()

    if request.method == 'POST':

        form = Drp_Sec_5_Form(request.POST)

        if form.is_valid():

            # Crea en BD 
            p1=form.cleaned_data['componentes']
            drp.componentes.set(p1)
            drp.status_t='C'
            if accion =='revisa':
                drp.status_5='a'
            
            drp.save()

            #return HttpResponseRedirect(reverse('Lista-DRP')) reverse('Lista-CMP', args=[str(self.id)])
            #return HttpResponseRedirect(reverse('Lista-CMP', args=[str(drp.id)]))
            return HttpResponseRedirect(Asigna_CMP_ult_url)

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Asigna_CMP_ult_url= request.META['HTTP_REFERER']
        p2=drp.componentes.all()
        form = Drp_Sec_5_Form(initial={'componentes':set(p2)})

        return render(request, 'BCP/drp/asigna_cmp.html', {'drp':drp, 'form':form})
      
#************************************
# 6.9.3.1 Crea Componentes en la BD *
#************************************
from .forms import Crea_CMP_Form

def Crea_CMP(request):
    """
    Crea un Componente de Infraestructura
    de Hw o Sw en la Base de Datos """

    print('----- Crea CMP----')

    # Determinacion de Codigo a asignar.

    cod = get_object_or_404(Parametros_G, pk = 10)
    codigo = 'CMP-'+str(cod.valor_2) 
    cod.valor_2=cod.valor_2+1
    cod.save()

        
    form=Drp_Sec_5_Form()

    if request.method == 'POST':

        form = Crea_CMP_Form(request.POST)

        if form.is_valid():

            # Crea en BD 
            componentes=Componentes()
            componentes.codigo=codigo
            componentes.tipo_act=form.cleaned_data['tipo_act']
            componentes.nombre=form.cleaned_data['nombre']
            componentes.descripcion=form.cleaned_data['descripcion']
            componentes.identificacion=form.cleaned_data['identificacion']
            componentes.fabricante=form.cleaned_data['fabricante']
            componentes.save()
           

            return HttpResponseRedirect(reverse('Lista-DRP'))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        
        form = Crea_CMP_Form()
        return render(request, 'BCP/drp/crea_cmp.html', {'form':form})    

#*************************************
# 6.9.3.2 Borra Componentes de la BD *
#*************************************



#****************************
# 6.9.3.3  Lista la LBC DRP *
#****************************

#def Lista_LBC(request, pk, ulr_comp):
def Lista_LBC(request, pk, pk_drp):
    """Lista la Linea Base de Configuracion de un Componente"""

    print('----- Lista LBC----')
    comp=get_object_or_404(Componentes, pk=pk)
    drp=get_object_or_404(Drp, pk=pk_drp)
    lista_lbc=comp.lbc
    print('comp=',comp)
    print('Lista_lbc=', lista_lbc)


    return render(request, 'BCP/drp/lista_lbc.html', context={'comp':comp, 'lista_lbc':lista_lbc, 'drp':drp})


#***************************
# 6.9.3.4 Crea  la LBC     *
#***************************
from .forms import Crea_LBC_Form

def Crea_LBC(request, pk):
    """Crea una Linea Base de Configuracion para un
    Componente de Infraestructura de Hw o Sw para el
    DRP"""

    print('----- Crea LBC----')

    global Crea_LBC_url_ant

    cmp = get_object_or_404(Componentes, pk=pk)
    
    # Determinacion de Codigo a asignar.
    cod = get_object_or_404(Parametros_G, pk = 11)
    codigo = cmp.codigo+'-'+str(cod.valor_2) 
    cod.valor_2=cod.valor_2+1
    cod.save()
        
    form=Crea_LBC_Form()

    if request.method == 'POST':

        form = Crea_LBC_Form(request.POST)

        if form.is_valid():

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

            cmp.lbc.add(p)

            cmp.save()
           

            return HttpResponseRedirect(Crea_LBC_url_ant)
            #return HttpResponseRedirect(reverse(cmp.get_absolute_url))
            #return HttpResponseRedirect(reverse('Lista-DRP'))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        Crea_LBC_url_ant=request.META['HTTP_REFERER']

        form = Crea_LBC_Form()
        return render(request, 'BCP/drp/crea_lbc.html', {'form':form, 'cmp':cmp})  


#***************************
# 6.9.3.5 Borra la LBC     *
#***************************
def Borra_LBC(request, pk):
    """ 
    Borra un registro de Linea Base de Configuracion asociado a un Componente"""

    url_ant=request.META['HTTP_REFERER']
    lbc=get_object_or_404(LBC, pk=pk)
    lbc.delete()

    return HttpResponseRedirect(url_ant)


#*******************************
# 6.10 Servicios Criticos DRP  *
#*******************************

#****************************************
# 6.10.1 Lista  Servicios Criticos DRP  *
#****************************************

def Lista_Serv_Crtc(request, pk):
    
    """Lista los Servicios Criticos asociados al DRPs"""

    print('----- Lista Servicios Criticos DRP ----')

    drp=get_object_or_404(Drp, pk=pk)
    lista_sc=drp.servicios_drp 

   
    return render(request, 'BCP/drp/lista_sc.html', context={'lista_sc':lista_sc, 'drp':drp})


#**************************************
# 6.10.2 Crea Servicios Criticos DRP  *
#**************************************

#@permission_required('Catalogo.can_mark_returned')
def cr_drp_P5(request, pk, acc):
    """
    Ingresa Servicios Criticos para el DRP
    """
    print('------ Crea Servicio Citico DRP -------')
    print('Accion=',acc)
    global cr_drp_P5_url_ant

    drp = get_object_or_404(Drp, pk = pk)

   
    #Asigna el formulario creado en Forrms
    form=CreaProc_P5_Form()

    
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
                contacto.nombre=contacto_drp + '(' + nombre + ')'
                contacto.save()
                drp.contactos_drp.add(contacto)

            if contacto_bck_drp:
                contacto2=Contactos_PC()
                contacto2.nombre=contacto_bck_drp + '(' + nombre + ')'
                contacto2.save()
                drp.contactos_drp.add(contacto2)  
            
            # en caso de ser una revision cambia el status a autorizar.
            if acc == 'revisa':
                drp.status_6 = 'a'

            #Adiciona el Servicio al Procedimiento
            servicio.save()
            drp.servicios_drp.add(servicio)
            drp.save()

            

            #Marca la seccion como completa
            #num = proced.sec_servicios
            #num = num+1
            #drp.sec_servicios = num
            #proced.save()
            
                     
            # redirect to a new URL:
            
        
            return HttpResponseRedirect(cr_drp_P5_url_ant)
            #return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))
            #return HttpResponseRedirect(drp.get_absolute_url)

        
        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
            

    # If this is a GET (or any other method) create the default form.
    else:

        cr_drp_P5_url_ant=request.META['HTTP_REFERER']
        print(url_ant)
        return render(request, 'BCP/proced_cont/prcd_crea_serP5.html', {'form': form, 'servicios':drp.servicios_drp})    


#***************************************
# 6.10.2 Borra Servicios Criticos DRP  *
#***************************************
    
#@permission_required('Catalogo.can_mark_returned')
def br_drp_P5(request, pk, acc):
    """
    Borra Servicios Criticos para el DRP
    """
    print('---- Borra Servicio Critico DRP --------')
    print('pk=', pk)
    url_ant=request.META['HTTP_REFERER']
    
    servicio_drp = get_object_or_404(Servicios_PC, pk = pk)
    drp = get_object_or_404(Drp, pk = servicio_drp.pk_padre)

    print(servicio_drp)
    #drp = get_object_or_404(Procedimientos, pk = servicio_drp.pk_padre) 

    #Actualiza cantidad de SSCC    
    #num = proced.sec_servicios
    #num = num-1
    #proced.sec_servicios = num
    #proced.save()
    if acc == 'revisa':
        drp.status_6 = 'a'

    #Borra Servicio                
    servicio_drp.delete()
    drp.save()

    

    return HttpResponseRedirect(url_ant)


from .forms import CreaProc_P6_Form

#*******************************
# 6.11 Procedimiento del  DRP  *
#*******************************
#**************************************************
# 6.11.1 Lista Pasos del  Procedimiento del  DRP  *
#**************************************************
def Lista_Pasos_Drp(request, pk):
    """Lista los Componentes de Hw y Sw del DRPs"""

    print('----- Lista Pasos del Procedimiento del  DRP ----')
    drp=get_object_or_404(Drp, pk=pk)
    lista_pasos=drp.pasos_drp 

   
    return render(request, 'BCP/drp/lista_pasos.html', context={'lista_pasos':lista_pasos, 'drp':drp})

#*******************************
# 6.11 Procedimiento del  DRP  *
#*******************************
#@permission_required('Catalogo.can_mark_returned')
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
            

    # If this is a GET (or any other method) create the default form.
    else:

        #url_ant=request.META['HTTP_REFERER']
        return render(request, 'BCP/proced_cont/prcd_crea_pasP7.html', {'form': form, 'pasos':drp.pasos_drp})
    

#@permission_required('Catalogo.can_mark_returned')
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
def Lista_Contactos_DRP(request, pk):
    """Lista de Contactos del DRPs"""

    print('----- Lista de Contactos del  DRP ----')
    drp=get_object_or_404(Drp, pk=pk)
    lista_contactos=drp.contactos_drp 

   
    return render(request, 'BCP/drp/lista_contactos.html', context={'lista_contactos':lista_contactos, 'drp':drp})


#@permission_required('Catalogo.can_mark_returned')
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})            
                     
        

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        return render(request, 'BCP/proced_cont/prcd_crea_conP6.html', {'form': form, 'contactos':drp.contactos_drp})
    

#@permission_required('Catalogo.can_mark_returned')
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})            
                     
        

    # If this is a GET (or any other method) create the default form.
    else:

        url_ant=request.META['HTTP_REFERER']
        form=CreaProc_P6_Form(initial={'nombre':contacto.nombre,
                                       'correo':contacto.correo,
                                       'tel_lab':contacto.tel_lab,
                                       'cel_lab':contacto.cel_lab})
        
        return render(request, 'BCP/drp/drp_mod_conP6.html', {'form': form })
    


#@permission_required('Catalogo.can_mark_returned')
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

    if sec == '1':
        drp.status_1 = 'a'
    elif sec == '2':
        drp.status_2 = 'a'
    elif sec == '3':
        drp.status_3 = 'a'
    elif sec == '4':
        drp.status_4 = 'a'
    elif sec == '5':
        drp.status_5 = 'a'
    elif sec == '6':
        drp.status_6 = 'a'
    elif sec == '7':
        drp.status_7 = 'a'
    elif sec == '8':
        drp.status_A = 'a'

    drp.status_t='a'
    drp.save()
    
    # redirect to a new URL:
    return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)])) 

from .forms import AutorizaRaciForm
import datetime

def Aut_Drp(request, pk, sec):
    """
    Autorizacion de la seccion (sec) del DRP 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Autorizadores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)

        
    #proceso= get_object_or_404(Proceso, pk = proced.pk_padre)

    if sec == '3':
        procesos_asig = drp.procesos_drp
        procesos_disp = SubProceso.objects.all()
        for p in procesos_asig.all():
            print(p.path)

    if sec == '5':
        compo_asig = drp.componentes
        compo_disp = Componentes.objects.all()

    if sec == '6':
        servicios_asig = drp.servicios_drp
        servicios_disp = Servicios_PC.objects.all()

    elif sec == '8':
        contactos = drp.contactos_drp
    elif sec == '7':
        pasos = drp.pasos_drp


    form = AutorizaRaciForm() #Utiliza el Formulario para la autorizacion de Procesos
    aut=LogAut()

    
    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    print('usuario de sesion',aut.gestor_aprobador)

     
    aut.cod_proceso=drp.codigo 

    if request.method=='POST':

        form = AutorizaRaciForm(request.POST)
        
        if form.is_valid():
            
            #Registra autorizacion en log
                                
            aut.fecha=datetime.date.today()
            #aut.p_status=proced.status+'P'
            aut.observacion=form.cleaned_data['comentario']
            aprobado=form.cleaned_data['aprobacion']
            aut.Aprobado=aprobado           
            notifica=form.cleaned_data['notifica']
            
            
            #Actualiza los status
                            
            if aprobado:
                # Aprobado
                if sec == '1':
                    drp.status_1='A'
                    s='Seccio Objetivo del DRP'
                    print('status=',drp.status_1)
                if sec == '2':
                    drp.status_2='A'
                    s='Seccio 2. Organizacion'
                    print('status=',drp.status_2)
                if sec == '3':
                    drp.status_3='A'
                    s='Seccio 3. Alcance'
                    print('status=',drp.status_3)
                if sec == '4':
                    drp.status_4='A'
                    s='Seccio 4. Estrategia'
                    print('status=',drp.status_4)
                if sec == '5':
                    drp.status_5='A'
                    s='Seccio 5. Esp.Tecnica'
                    print('status=',drp.status_5)
                if sec == '6':
                    drp.status_6='A'
                    s='Seccio 6. Serv.Criticos'
                    print('status=',drp.status_6)
                if sec == '7':
                    drp.status_7='A'
                    s='Seccio 7. Procedimiento'
                    print('status=',drp.status_7)
                if sec == '8':
                    drp.status_A='A'
                    s='Anexo A. Contactos'
                    print('status=',drp.status_A)
                
                aut.p_status='A'+'D'
                aut.item=s+' Aprobado por Gestor Responsable'
                

                #Prepara mensaje x correo
                #nombre=proced.resp_proceso.user_gestor.last_name
                #email = proc_rev.subproceso.gestor_R.user_gestor.email
                #accion='dar visto bueno o requerir cambios para el '
                    
            else:
                #Rechazado
                if sec == '1':
                    drp.status_1='x'
                    s='Seccio Objetivo del DRP'
                    print('status=',drp.status_1)
                if sec == '2':
                    drp.status_2='x'
                    s='Seccio 2. Organizacion'
                    print('status=',drp.status_2)
                if sec == '3':
                    drp.status_3='x'
                    s='Seccio 3. Alcance'
                    print('status=',drp.status_3)
                if sec == '4':
                    drp.status_4='x'
                    s='Seccio 4. Estrategia'
                    print('status=',drp.status_4)
                if sec == '5':
                    drp.status_5='x'
                    s='Seccio 5. Esp.Tecnica'
                    print('status=',drp.status_5)
                if sec == '6':
                    drp.status_6='x'
                    s='Seccio 6. Serv.Criticos'
                    print('status=',drp.status_6)
                if sec == '7':
                    drp.status_7='x'
                    s='Seccio 7. Procedimiento'
                    print('status=',drp.status_7)
                if sec == '8':
                    drp.status_A='x'
                    s='Anexo A. Contactos'
                    print('status=',drp.status_A)



                aut.p_status='x'+'D'
                aut.item=s+' Enviado a Gestor Consultor para revision de Observaciones'
                    
                #email = proc_rev.subproceso.gestor_C.user_gestor.email
                #accion='Tomar accion sobre las modificaciones solicitadas por el gestor Autorizador para el'
                    
           
            #Graba en Base de Datos                
            aut.save()
            drp.log_auth_drp.add(aut)      
            drp.save()
            
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = AutorizaRaciForm(initial= {
                                        'aprobacion':False,
                                        'notifica':False
                                        }
                             )

        if sec == '1':    # 2. Objetivo                           
            return render(request, 'BCP/drp/drp_s1_auth.html', {'form': form, 'drp':drp})
        
        if sec == '2':    # 1. Organizacion                            
            return render(request, 'BCP/drp/drp_s2_auth.html', {'form': form, 'drp':drp})
        
        if sec == '3':    # 3. Alcance                           
            return render(request, 'BCP/drp/drp_s3_auth.html',
                        {'form': form, 'drp':drp, 'procesos_disp':procesos_disp, 'procesos_asig':procesos_asig})
        
        if sec == '4':    # 4. Estrategia de Recuperacion                         
            return render(request, 'BCP/drp/drp_s4_auth.html', {'form': form, 'drp':drp})
        
        if sec == '5':    # 5. Especificacion Tecnica del Site de Contingencias                           
            return render(request, 'BCP/drp/drp_s5_auth.html',  {'form': form, 'drp':drp,
                                                                 'compo_asig':compo_asig,
                                                                 'compo_disp':compo_disp})
        
        if sec == '6':   # 6. Servicios Criticos                         
            return render(request, 'BCP/drp/drp_s6_auth.html',   {'form': form, 'drp':drp,
                                                                  'servicios_asig':servicios_asig,
                                                                  'servicios_disp':servicios_disp
                                                                  })
        
        if sec == '7':                            
            return render(request, 'BCP/proced_cont/proced_auth.html',
                        {'form': form, 'proceso':proceso, 'proced':proced, 'servicios':servicios,
                        'contactos':contactos, 'pasos':pasos})
        if sec == 'A':                            
            return render(request, 'BCP/proced_cont/proced_auth.html',
                        {'form': form, 'proceso':proceso, 'proced':proced, 'servicios':servicios,
                        'contactos':contactos, 'pasos':pasos})
        



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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
    
        url_ant_obs_aut =request.META['HTTP_REFERER']
        form= Autoriza_obs_Proced_C_Form()
        
        return render(request, 'BCP/proced_cont/proced_obs_auth.html', {'form': form, 'proced':proced, 'item':item, 'valor':valor})


from .forms import Autoriza_obs_Proced_C_Form
def aut_obs_drp(request, item, pk, valor):
    """
    Registra observaciones por item a la
    Autorizacion de DRP
    """

    global  url_ant_obs_aut

    print('--- Registra Observaciones x Item a autorizaciones DRP---')
    print('item pk :', pk)
    print('item nro:', item)
    print('item nro 2:', valor)
    
    drp = get_object_or_404(Drp, pk = pk)
        
    aut=LogAut()

    #Asigna al usuario de sesion como Autorizador
    print('asigna usuario sesion')
    pk_usr_sesion= request.user.pk
    aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    print('usuario de sesion',aut.gestor_aprobador)

     
    aut.cod_proceso=drp.codigo
    aut.item=item+':'+valor
    

    if request.method=='POST':

        form = Autoriza_obs_Proced_C_Form(request.POST)
        
        print('FORMATO VALID0?',form.is_valid())
        
        if form.is_valid():
            
            #Registra autorizacion en log
                                
            aut.fecha=datetime.date.today()
            # aut.p_status=drp.status+'D'
            aut.observacion=form.cleaned_data['comentario']
            #aut.Aprobado=form.cleaned_data['aprobacion']
            
            #notifica=form.cleaned_data['notifica']
            #aprobado=form.cleaned_data['aprobacion']
            
            #---
                            
           
            #Graba en Base de Datos                
            aut.save()
            drp.log_auth_drp.add(aut)      
            drp.save()
            
                
            # redirect to a new URL:
            return HttpResponseRedirect(url_ant_obs_aut)
        
        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
    
        url_ant_obs_aut =request.META['HTTP_REFERER']
        form= Autoriza_obs_Proced_C_Form()
        
        return render(request, 'BCP/drp/drp_obs_auth.html', {'form': form, 'drp':drp, 'item':item, 'valor':valor})


#*********************************************************
# 6.14  Revision de Observaciones  del DRP               *
#*********************************************************

#*********************************************************
# 6.14.1   Revision de Responsables del DRP              *
#*********************************************************

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
   
    #aut=LogAut()

    
    #Asigna al usuario de sesion como Autorizador
    #print('asigna usuario sesion')
    #pk_usr_sesion= request.user.pk
    #aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    #print('usuario de sesion',aut.gestor_aprobador)
     
    #aut.cod_proceso=drp.codigo 

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
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
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

                                 
        return render(request, 'BCP/drp/drp_s2_rev.html', {'form': form, 'drp':drp})
        

#******************************************************
# 6.14.2   Revision de Objetivo  del DRP              *
#******************************************************

def Rev_S1_Drp(request, pk):
    """
    Revisa la denegacion de autorizacion  para cada  la seccion 2 : Objetivo del  DRP 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
       
    #aut=LogAut()

    
    #Asigna al usuario de sesion como Autorizador
    #print('asigna usuario sesion')
    #pk_usr_sesion= request.user.pk
    #aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    #print('usuario de sesion',aut.gestor_aprobador)
     
    #aut.cod_proceso=drp.codigo 

    if request.method=='POST':

        form=Drp_Sec_1_Form(request.POST)

                      
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            drp.introduccion = form.cleaned_data['objetivo']
            
            drp.status_1 ='a'

            #Graba en Base de Datos                
            drp.save()
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = Drp_Sec_1_Form(initial= {
                                        'objetivo':drp.introduccion
                                        }
                             )

                                 
        return render(request, 'BCP/drp/drp_s1_rev.html', {'form': form, 'drp':drp})
    

#*****************************************************
# 6.14.3   Revision de Alcance  del DRP              *
#*****************************************************

def Rev_S3_Drp(request, pk):
    """
    Revisa las observaciones realizadas 
    para  la seccion 3 : Alcance del  DRP 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
       
    #aut=LogAut()

    
    #Asigna al usuario de sesion como Autorizador
    #print('asigna usuario sesion')
    #pk_usr_sesion= request.user.pk
    #aut.gestor_aprobador=Gestor.objects.get(user_pk=pk_usr_sesion)
    #print('usuario de sesion',aut.gestor_aprobador)
     
    #aut.cod_proceso=drp.codigo 

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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        Drp_Sec_3_url_ant = request.META['HTTP_REFERER']
        print('Drp_Sec_3_url_ant  =', Drp_Sec_3_url_ant)
        p2=drp.procesos_drp.all()

        form = Drp_Sec_3_Form(initial={ 'procesos':set(p2)})

                                 
        return render(request, 'BCP/drp/drp_s3_rev.html', {'form': form, 'drp':drp})


#*****************************************************
# 6.14.4   Revision de Alcance  del DRP              *
#*****************************************************

def Rev_S4_Drp(request, pk):
    """
    Revisa las observaciones realizadas 
    para  la seccion 4 : Estrategia de Recuperacion 
    """

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Consultores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[301] ))
    
    #model = Proceso
    drp = get_object_or_404(Drp, pk = pk)
       

    if request.method=='POST':

        form=Drp_Sec_4_Form(request.POST)

                      
        if form.is_valid():
            
            
            #Registra cambios y Actualiza el status

            drp.tipo_Site = form.cleaned_data['tipo_site']
            drp.desc_estrategia = form.cleaned_data['desc_estrategia']
            drp.disposicion_componentes = form.cleaned_data['tipo_disp']
            
            drp.status_4 ='a'

            #Graba en Base de Datos                
            drp.save()
                
            # Vuelve al Indice del DRP
            return HttpResponseRedirect(reverse('Indice-DRP', args=[str(drp.id)]))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        Drp_Sec_3_url_ant = request.META['HTTP_REFERER']
        print('Drp_Sec_3_url_ant  =', Drp_Sec_3_url_ant)
        p2=drp.procesos_drp.all()

        form = Drp_Sec_4_Form(initial={'tipo_site':drp.tipo_Site,
                                       'desc_estrategia': drp.desc_estrategia,
                                       'tipo_disp':drp.disposicion_componentes
                                       })

                                 
        return render(request, 'BCP/drp/drp_s4_rev.html', {'form': form, 'drp':drp})


#***************************************************************
# 6.14.5 Revision Especificacion Tecnica Site de Contingencias *
#***************************************************************

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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        p2=drp.componentes.all()

        form = Drp_Sec_5_Form(initial={'componentes':set(p2)})

                                 
        return render(request, 'BCP/drp/drp_s5_rev.html', {'form': form, 'drp':drp,
                                                           'lista_cmp':lista_cmp})


#***************************************************************
# 6.14.6  Revision Especificacion de Servicios Criticos del DRP*
#***************************************************************

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

    return render(request, 'BCP/drp/drp_s6_rev.html', {'drp':drp,'lista_sc':lista_sc})

#*********************************************** Fin DRP ************************************************************************************


#*********************************************************************************************************************************************
#***********************************************  7. Administracion de Incidente  ************************************************************
#*********************************************************************************************************************************************



#***************************
#7.1.1  Declara Incidente  *
#***************************
from .forms import Declara_Incidente_Form

#@permission_required('Catalogo.can_mark_returned')
def Declara_Inc(request):
    """
    Registra el Incidente y Selecciona los Procesos relacionados con las amenazas 
    declaradas en el mismo. """
    print('----- Entra a Registro de Incidente ------')

    model = Incidentes
    
    #procesos=get_object_or_404(Proceso)

  
    if request.method=='POST':
        print('metodo POST')
        form = Declara_Incidente_Form(request.POST)
        
        if form.is_valid():
            print('Formato valido')
            
            incidente=Incidentes()
            
            incidente.save()
            
            # Rescata correlativo de Incidente. 
            parametro = get_object_or_404(Parametros_G, pk = 2)

            # Define codigo del incidente
            f_i = incidente.fecha.strftime('%d-%m-%Y')
            #descripcion = form.cleaned_data['descripcion']
            folio=parametro.valor_2
            incidente.codigo = f_i+'/ '+str(folio)
            parametro.valor_2=folio+1
            
            # Graba intancias en Registro (Base de Incidentes)
            incidente.nombre_r = form.cleaned_data['nombre']
            incidente.area_r = form.cleaned_data['area']
            incidente.descripcion = form.cleaned_data['descripcion']
            #incidente.correo = form.cleaned_data['correo']

            amenazas_declaradas = form.cleaned_data['amenazas_i']
            incidente.amenazas_i.set(amenazas_declaradas)



            # Selecciona los Procesos asociados al incidente en base a las amenazas declaradas
            # =================================================================================

            # Recorre amenazas declaradas
            for amenaza in amenazas_declaradas:

                # Recorre los Escenarios de cada "amenaza" declarada
                escenarios_en_amenaza=amenaza.landscape
                for escenario in escenarios_en_amenaza.all():

                    # Identifica a los Procesos Vigentes asociados al "escenario".
                    sprocesos=SubProceso_V.objects.all()
                    for sproc in sprocesos:
                        
                        # Selecciona los Escenarios que estan Asociados al Sproceso
                        esc_en_sproc=sproc.escenarios # Escenarios asociados al Proceso
                        for esc in esc_en_sproc.all():

                            # Si el Escenario en la "amenaza" es igual al Escenario en el Sproceso
                            if escenario == esc:
                                # Asigna el Escenario a los Escenarios del Incidente
                                incidente.escenarios_i.add(esc)

                                # Asigna el Proceso a los Procesos del Incidente
                                pk_padre=sproc.pk_padre
                                proceso=get_object_or_404(Proceso, pk=pk_padre)
                                incidente.procesos_i.add(sproc)

                            
                
            #Graba en BD
            print('Grabo incidente')
            
            incidente.save()
            parametro.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))
            

        else:

            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})

    else:

        form = Declara_Incidente_Form()
        return render(request, 'BCP/inc_mgm/crea_inc.html',{'form':form })


#************************************
#6.2 Lista de Incidentes reportados *
#************************************
def Lista_Incidentes(request):
    """
    Generic class-based view listing books on loan to current user.
    """
    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Gestion de Crisis']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[400] ))

    incidentes=Incidentes.objects.all()
    
    return render(request, 'BCP/inc_mgm/incidentes__list.html', {'incidentes':incidentes})

#****************************
#6.2.1  Modifica Incidente  *
#****************************
from .forms import Modifica_Incidente_Form

#@permission_required('Catalogo.can_mark_returned')
def Modifica_Inc(request, pk):
    """
    Permite modificar la declaracion inicial del incidente
    Elimina los Procesos asociados seleccionados y los selecciona nuevamente
    """
    
    print('Entra Modifica Incidente')


    incidente = get_object_or_404(Incidentes, pk = pk)
   
    #Borra todos los Procesos aociados al incidente
    #for prc in incidente.procesos_i.all():
    #    print('Borra :', prc.path)
    #    prc.delete()
        
        
    #procesos=get_object_or_404(Proceso)

    form = Modifica_Incidente_Form()

    print('llegue al if')
    
    if request.method=='POST':
        print('metodo POST')
        form = Modifica_Incidente_Form(request.POST)
        
        if form.is_valid():
            print('Formato valido')
            
            #Graba intancias en Registro
            p1 = form.cleaned_data['amenazas_i']
            incidente.amenazas_i.set(p1)
            incidente.changed=True

            #Graba en BD
            incidente.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Lista-Incidentes'))                          

        else:

            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
            
              

    else:

        amn_in=incidente.amenazas_i.all()
        form = Modifica_Incidente_Form(initial= {'amenazas_i':set(amn_in)})

        print('GET')
        
        return render(request, 'BCP/inc_mgm/modi_inc.html',{'form':form, 'incidente':incidente })

      

#*************************************
# 6.3 Reporte de Perfil de Incidente *
#*************************************

def Perfil_Inc(request, pk):


    incidente = get_object_or_404(Incidentes, pk = pk)
    print('incidente=', incidente)

    procesos_inc = incidente.procesos_i
    escenarios_inc = incidente.escenarios_i
    amenazas_inc = incidente.amenazas_i


    # Identifica al Comite de Crisis.
    comite=[]
    gestores=Gestor.objects.all()
    for integrante in gestores:
        for grp in integrante.user_gestor.groups.all():
            if grp.name=='Gestion de Crisis':
                comite.append(integrante)
    print('integrantes del comite =', comite)


    #--------------------- Si se agregaron o quitaron amenazas, Recalcula los Escenarios y Procesos involucrados 
    print('cambio en amenazas=',incidente.changed)
    if incidente.changed:

        incidente.escenarios_i.set([])  # Borra todas las relaciones con Escenarios
        incidente.procesos_i.set([])  # Borra todas las relaciones con Procesos

        # Recorre nueva lista de amenazas
        for amenaza in amenazas_inc.all():

                # Recorre los Escenarios de cada "amenaza" declarada
                escenarios_en_amenaza=amenaza.landscape
                for escenario in escenarios_en_amenaza.all():

                    # Identifica los Procesos asociados al "escenario".
                    sprocesos=SubProceso.objects.all()
                    for sproc in sprocesos:
                        
                        # Selecciona los Escenarios que estan Asociados al Sproceso
                        esc_en_sproc=sproc.escenarios # Escenarios asociados al Proceso
                        for esc in esc_en_sproc.all():

                            # Si el Escenario en la "amenaza" es igual al Escenario en el Sproceso
                            if escenario == esc:
                                # Asigna el Escenario a los Escenarios del Incidente
                                incidente.escenarios_i.add(esc)

                                # Asigna el Proceso a los Procesos del Incidente
                                pk_padre=sproc.pk_padre
                                proceso=get_object_or_404(Proceso, pk=pk_padre)
                                incidente.procesos_i.add(sproc)

                            
                
        #Graba en BD
        print('Grabo incidente')
        incidente.changed=False
        incidente.save()
        #-------------------- Fin Si se agregaron o quitaron amenazas

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

    

    return render(request,'BCP/inc_mgm/perfil_inc.html', {'incidente':incidente,
                                                          'comite':comite,
                                                          'amenazas':amenazas_inc,
                                                          'n_procesos':n_procesos,
                                                          'procesos':procesos_inc,
                                                          'puntaje_x':puntaje_x,
                                                          'estadistica_impactos':estadistica_impactos,
                                                          'estadistica_indicadores':estadistica_indicadores,
                                                          'estadistica_escenarios':estadistica_escenarios,
                                                          'estadistica_recursos':estadistica_recursos
                                                          })

from collections import defaultdict

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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Procedimientos  # Asegúrate de importar el modelo correcto
import json

@csrf_exempt
def toggle_procedimiento(request, procedimiento_id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            procedimiento = Procedimientos.objects.get(id=procedimiento_id)
            procedimiento.esta_activo = data.get("esta_activo", False)
            procedimiento.save()
            return JsonResponse({"success": True, "nuevo_estado": procedimiento.esta_activo})
        except Procedimientos.DoesNotExist:
            return JsonResponse({"success": False, "error": "Procedimiento no encontrado"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Error en JSON"}, status=400)

    elif request.method == "GET":
        procedimientos = Procedimientos.objects.values("id", "esta_activo")
        return JsonResponse(list(procedimientos), safe=False)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


#***************************************************
# 6.4 Lista PC asociados a Proceso para Activacion *
#***************************************************

def Lista_PC_Px(request, pk, pk_padre):


    proceso_det = get_object_or_404(SubProceso, pk = pk)
    proceso_enc = get_object_or_404(Proceso, proceso = proceso_det.codigo)
    proced = proceso_det.procedimientos_contingencia

    url_ant = request.META['HTTP_REFERER']

    return render(request,'BCP/inc_mgm/pcxp_inc_list.html',
                  context={'proceso_det':proceso_det, 'proceso_enc':proceso_enc, 'proced':proced,
                           'url_ant':url_ant,'pk_padre':pk_padre}) 

#********************************************************
# 6.5 Activa/Desactiva un Procedimiento de Contingencia *
#********************************************************


def ActivaDesactivaPc(request, pk ):

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

   
#*********************************************** Fin Administracion del Incidente *********************************************************
   
#*********************************************************************************************************************************************
#***********************************************  6. Maestros ********************************************************************************
#*********************************************************************************************************************************************

def Menu_Conf(request):
    """
    Menu para la definicion de Datos Fijos
    """
    print('menu conf')
   
    if not es_del_grupo([request.user, 'Administradores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[100] ))
        
    return render(request,'BCP/conf/menu_conf.html')


#******************************************
#       Mantencion Gestores/Usuarios      *
#******************************************

from .forms import Crea_Gestor_Form, Crea_Gestor2_Form

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
                return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors, 'form2':form2.errors} )
                #form = Crea_Gestor_Form(request.POST, data=form.errors)
                #return render(request, 'BCP/conf/crea_gestor.html', {'form':form} )

    # If this is a GET (or any other method) create the default form.
    else:

        form = Crea_Gestor_Form()
        form2= Crea_Gestor2_Form()
        
        return render(request, 'BCP/conf/crea_gestor.html', {'form':form, 'form2':form2} )


from .forms import Borra_Gestor_Form


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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})   


    else:
        
        form = Borra_Gestor_Form()
        
    return render(request,'BCP/conf/borra_gestor.html', {'form':form})
    


class GestorListView(generic.ListView):
    """
    Generic class-based view listing - Listado de Gestores para asignacion de Grupos.
    """
    model = Gestor
    template_name='BCP/conf/gestor_list.html'

    print('Entra a Listado')

    #def get_queryset(self):
    #    return Proceso.objects.filter(Proceso.es_subproceso=True).filter(Proceso.subproceso.fase_status=='M')|Proceso.objects.filter(proceso.subproceso.fase_status=='B') 


#********************************
#4.2 Asigna Grupos a Usuario    *
#********************************
from .forms import Asigna_Grupo_Form

#@permission_required('Catalogo.can_mark_returned')
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
    
        
    else:
        
        p2 = usuario.groups.all()
        form = Asigna_Grupo_Form(initial= {'grupos':set(p2)})
                                        
        return render(request, 'BCP/conf/asigna_grupos.html', {'form': form, 'usuario':usuario})



# **********************************
# Administracion de Riesgo/Impacto *
# **********************************

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

    return render(request, 'BCP/ria/lista_riesgos.html', {'riesgos':riesgos,
                                                           'menor_a_100':menor_a_100,
                                                           'resto':resto})


from .forms import Crea_Impacto_Form
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
        
        form = Crea_Impacto_Form(initial={'ponderacion':resto})
                                        
        return render(request, 'BCP/ria/crea_impacto.html', {'form':form })


from .forms import Crea_Impacto_Form
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
        
        form = Crea_Impacto_Form(initial={'nombre':impacto.nombre,
                                          'descripcion':impacto.descripcion,
                                          'ponderacion':impacto.ponderacion})
                                        
        return render(request, 'BCP/ria/mod_impacto.html', {'form':form })

def Borra_Impacto(request, pk):
    """
    Borra el Registro de Riesgo/Impacto
    """

    impacto=get_object_or_404(Tipo_Impacto_P, pk=pk)
    impacto.delete()

    return HttpResponseRedirect(reverse('Lista-Impactos') )


def Lista_Nivel_Impactos(request, pk):
    """
    Lista los niveles de impacto del riesgo pk (propuestos)
    """
    print('Entra a Lista Nivel Impactos')

    riesgo=get_object_or_404(Tipo_Impacto_P, pk=pk)
    niveles = Nivel_Impacto_P.objects.filter(tipo=riesgo)



    return render(request, 'BCP/ria/lista_nivel_imp.html', {'niveles':niveles,
                                                            'riesgo':riesgo})


from .forms import Crea_Nivel_Imp_Form
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
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors}) 
        
    else:
        
        form = Crea_Nivel_Imp_Form()
    

    return render(request, 'BCP/ria/crea_nivel_impacto.html', {'riesgo':riesgo, 'form':form})


#*********************************************************************************************************************************************
#***********************************************  7. Proposito General ***********************************************************************
#*********************************************************************************************************************************************


    
#*****************************
#Manda correo de Notificacion*
#*****************************

from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

def Manda_Correo(email,cc_email,nombre,proceso, accion):

    context = {'email':email, 'nombre':nombre,'proceso':proceso, 'accion':accion}
    plantilla = get_template('BCP/mensajes/mensaje1.html')
    contenido = plantilla.render(context)

    correo= EmailMultiAlternatives(
        'DEFCON 5 / BCP - Autorizacion de Proceso',
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
        

    if ce == '100':
        mensaje='Debe estar en sesion con su nombre de usuario y clave y  pertenecer al grupo de Administracion'
        
    elif ce == '200':
        mensaje='Debe estar en sesion con su nombre de usuario y clave y  pertenecer al grupo de Consultores'

    elif ce == '300':
        mensaje='Debe estar en sesion con su nombre de usuario y clave y  pertenecer al grupo de Autorizadores'

    elif ce== '301':
            mensaje='Debe estar en sesion con su nombre de usuario y clave y  pertenecer al grupo de Consultores o  Autorizadores'
            
    elif ce == '400':
         mensaje='Debe estar en sesion con su nombre de usuario y clave y  pertenecer al grupo de Gestion de Crisis'

    elif ce == '500':
         mensaje='Debe estar en sesion con su nombre de usuario y clave y  pertenecer al grupo TI'
         
    elif ce == '600':
        mensaje='Debe abrir una sesion mediante su nombre de usuario y clave'

    elif ce == '3000':
        mensaje='La Poderacion no puede superar el 100 %'
    elif ce == '3001':
        mensaje='Puntaje no puede ser 0'
        
    else:
        mensaje='Error de Sesion no identificado.'
        
 
    return render(request, 'BCP/mensajes/mensajes_error_sesion.html', context={'mensaje':mensaje}) 

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
def reset(request):
    """ Reinicia toda la Base de Datos"""
    print('**** REINICIA BASE DE DATOS *****')
    print('--- Método HTTP recibido:', request.method) 

    # Verifica si el usuario en sesion esta habilitado
    if not es_del_grupo([request.user, 'Administradores']):
        return HttpResponseRedirect(reverse('error-sesion-mgm', args=[100] ))


    modelos = [
        Proceso, SubProceso, SubProceso_V,
        Procedimientos, Contactos_PC, Servicios_PC, Pasos_PC,
        Procedimientos_V, Contactos_PC_V, Servicios_PC_V, Pasos_PC_V
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
            proceso.proceso='root'
            proceso.nombre=raiz
            proceso.nro_hijos=0
            proceso.save()

            # Vuelve a la pagina Principal 
            return HttpResponseRedirect(reverse('index'))

        else:
            print(form.errors)
            return render(request, 'BCP/mensajes/mensajes_error_Form.html', {'form':form.errors})
        
    else:
    
        form = Reset()
                                 
        return render(request, 'reset.html', {'form': form})

