#Programa PYTHON
#Definicion de Formularios de la Aplicacion
#Programado por Marco A. Villalobos M.
#============================================



# INDICE

# 1. Procesos
# 2. Procedimientos de Recuperacion
# 3. DRP
# 4. Manejo de Incidentes
# 5. Mantencion de Maestros

# ============================================================================================
from django.contrib.auth.models import User, Group
#from django.contrib.admin.widgets import AutocompleteSelect
#from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
#from django.forms import ValidationError

# from django.utils.translation import ugettext_lazy as _
# Se debe cambiar ugettext_lazy  por version django 4.xx 
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.
from datetime import datetime, date

from .models import Drp, Proceso, SubProceso, LogAut, Recursos, Tipo_RR, Gestor, Escenarios, Amenazas, Estrategias, Grupos
from .models import Tipo_Impacto, Nivel_Impacto, Indicadores_BIA, Procedimientos, Tipo_Proc, User, Area, Cod_Area
from .models import Tipo_Site, Tipo_Disp, Componentes, Tipo_Componente



#************************************************************************************************************************
#***************************************        1. Procesos   ***********************************************************
#************************************************************************************************************************


class CreaProcesoForm(forms.Form):

      
    #nombre = forms.CharField(max_length= 50, widget=forms.Textarea(attrs={'rows':1,'cols':1}))
    #nombre = forms.CharField(max_length= 50)
    nombre = forms.CharField(
        widget=forms.Textarea(
            attrs={
                # El campo ahora tendrá 3 líneas de alto
                'rows': 1,
                # Y aproximadamente 40 caracteres de ancho
                'cols': 20,
                # Puedes añadir más atributos HTML aquí
                'class': 'mi-clase-personalizada'
            }
        )
    )

    objetivo = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':4,'cols':100}))
    
    #Registra el Tipo 
    es_subproceso=forms.BooleanField(label='Indicar si es un Proceso Final (sometido a Evaluacion) ', required=False)


class AsignaRaciForm(forms.Form):

 
    
    
    gestor_R = forms.ModelChoiceField(queryset=Gestor.objects.all(),  help_text='', label='Gestor Responsable ', required=True)
    gestor_A = forms.ModelChoiceField(queryset=Gestor.objects.all())
    #gestor_C = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, help_text='', label='Gestor Consultor   ', required=False)
    gestor_I = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)
    url_ant = forms.URLField(required=False)
    notifica = forms.BooleanField(label='Notifica por correo al Gestor Autorizador?', required=False)

    # Filtra los gestores R y A para pertenecer al grupo Autorizadores
    def __init__(self,initial):

        # Seleccion por grupos
        selec_aut = []

        gestores=Gestor.objects.all()
        for ges in gestores:
            grp=ges.user_gestor.groups
            for g in grp.all():
                if g.name == 'Autorizadores':
                    selec_aut.append(ges.user_pk)


        super(AsignaRaciForm, self).__init__(initial)
        self.fields['gestor_R'].queryset = Gestor.objects.filter(user_pk__in = selec_aut)
        self.fields['gestor_A'].queryset = Gestor.objects.filter(user_pk__in = selec_aut)




class AutorizaRaciForm(forms.Form):

    """
    Autorizacion a Proceso
    """

    aprobacion=forms.BooleanField(label='Autoriza..?:', required=False)
    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)
    

class Autoriza_BIA_Form(forms.Form):
    """
    Autorizacion de asignacion BIA  a Proceso
    """

    aprobacion=forms.BooleanField(label='Autoriza..?:', required=False)
    #comentario=forms.CharField(label='Observaciones:', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':80}))
    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)
    
class Autoriza_Act_x_Proc_Form(forms.Form):
    """
    Autorizacion de asignacion de Activos a Proceso
    """

    aprobacion=forms.BooleanField(label='Autoriza..?:', required=False)
    #comentario=forms.CharField(label='Observaciones:', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':80}))
    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

class Autoriza_Asig_Escenarios_Form(forms.Form):
    """
    Autorizacion de asignacion de Escenarios a Proceso
    """

    aprobacion=forms.BooleanField(label='Autoriza..?:', required=False)
    #comentario=forms.CharField(label='Observaciones:', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':80}))
    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

class Autoriza_Proced_C_Form(forms.Form):
    """
    Autorizacion de Procedimiento de Contingencia
    """

    aprobacion=forms.BooleanField(label='Autoriza..?:', required=False)
    #comentario=forms.CharField(label='Observaciones:', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':80}))
    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

class Autoriza_obs_Proced_C_Form(forms.Form):
    """
    Introduce observaciones x item durante proceso de Autorizacion
    """

    comentario=forms.CharField(label='Observaciones:', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':80}))
    



class RevisaProcesoForm(forms.Form):

    """
    Revision de observaciones de rechazo realizadas por el autorizador RACI
    a las definicion del Proceso
    """

    nombre = forms.CharField(max_length= 50, widget=forms.Textarea(attrs={'rows':1,
                                                                          'style': 'width: 60ch;'}))

    objetivo = forms.CharField(max_length=500, label='Objetivo:',  help_text='Describir objetivo del Proceso.',
                               widget=forms.Textarea(attrs={'class':'caja-texto',
                                                            'rows': 4,
                                                            'style': 'width: 60ch;'}))

    gestor_R = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Gestor Responsable ', required=False)
    gestor_A = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Gestor Autorizador ', required=False)
    #gestor_C = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Gestor Consultor   ', required=False)
    gestor_I = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Gestor Informado   ', required=False)

    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)


class Revisa_AsigAct_x_Proc_Form(forms.Form):
    """
    Revision de observaciones de rechazo realizadas por el autorizador RACI
    a las asignaciones de Activos al Proceso
    """
    activos = forms.ModelMultipleChoiceField(queryset=Recursos.objects.all().order_by('tipo'),
                                          label=_('Activos Seleccionados :'),
                                          required=False,
                                          widget=FilteredSelectMultiple(
                                                    _('Activos'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']
    

    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)
    

class Revisa_Asig_Esc_Form(forms.Form):
    """
    Revision de observaciones de rechazo realizadas por el autorizador RACI
    a las asignaciones de Escenarios al Proceso
    """
    escenarios = forms.ModelMultipleChoiceField(queryset=Escenarios.objects.all().order_by('titulo'),
                                          label=_('Escenarios Seleccionados :'),
                                          required=True,
                                          widget=FilteredSelectMultiple(
                                                    _('Escenarios'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']
    

    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

class Revisa_Asig_BIA_Form(forms.Form):
    """
    Revision de observaciones de rechazo a la Asignacion
    BIA al Proceso.
    """

    
    impacto_1 = forms.ModelChoiceField(queryset=Nivel_Impacto.objects.filter(cod=1), label='Financiero')
    impacto_2 = forms.ModelChoiceField(queryset=Nivel_Impacto.objects.filter(cod=2), label='Reputacional')
    impacto_3 = forms.ModelChoiceField(queryset=Nivel_Impacto.objects.filter(cod=3), label='Legal')
    impacto_4 = forms.ModelChoiceField(queryset=Nivel_Impacto.objects.filter(cod=4), label='Operacional')



    rto = forms.ModelChoiceField(queryset=Indicadores_BIA.objects.filter(cod=1))
    rpo = forms.ModelChoiceField(queryset=Indicadores_BIA.objects.filter(cod=2))
    mtd = forms.ModelChoiceField(queryset=Indicadores_BIA.objects.filter(cod=3))

    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

   
class CreaActivoForm(forms.Form):
    """
    Crea Activo/Recurso
    """
    nombre = forms.CharField(max_length= 50, label='Nombre de Activo:', widget=forms.Textarea(attrs={'rows':1, 'cols':50}))
    descripcion = forms.CharField(max_length=500, label='Descripcion:',  help_text='Describir objetivo del Proceso.', widget=forms.Textarea(attrs={'rows':8, 'cols':70}))
    tipo = forms.ModelChoiceField(queryset=Tipo_RR.objects.all(), label='Clase de Activo', empty_label='Ingrese una clase de Activo', help_text='',  required=False)
    
    #class MyModelChoiceField(ModelChoiceField):
    #    def label_from_instance(self, obj):
    #        return obj.name


#*******************************************************************
#Formulario de Asignacion de Servicios Criticos (Activos) a Proceso*
#*******************************************************************
class Act_x_Proc_Form(forms.Form):
    """
     Asignacion de Activos (Servicios Criticos) a Proceso
    """
        
    #activos = forms.ModelMultipleChoiceField(widget=widgets.FilteredSelectMultiple('nombre', False), queryset=Recursos.objects.all())

    activos = forms.ModelMultipleChoiceField(queryset=Recursos.objects.all().order_by('tipo'),
                                          label=_('Activos Seleccionados :'),
                                          required = False,
                                          widget=FilteredSelectMultiple(
                                                    _('Activos'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

    #class Meta:
    #    model = Recursos
    #    fields = ['nombre', 'Activo']


    #def clean_activos(self):

        #print('Entra a validacion')
        #servicios = self.cleaned_data['activos']
    
        #if not servicios:
            #raise ValidationError(_('** Debe elegir al menos un Servicio Critico. En caso de no identificar ningun servicio seleccione SCNI:SERVICIO CRITICO NO IDENTIFICADO  **'))
            

from django import forms
from .models import SubProceso, Recursos

class ServicioForm(forms.Form):

    pass     # Utilizado para pasar los datos de Recursos directo a JS

    #recursos = forms.ModelMultipleChoiceField(
    #    queryset=Recursos.objects.all(),
    #    required=False,
    #    widget=forms.SelectMultiple(attrs={'id': 'id_recursos_seleccionados'})  # Se usará en JS
    #)

    #class Meta:
    #    model = SubProceso
    #    fields = []

class EscenarioForm(forms.Form):
    pass


#***********************************************************
#Formulario de Asignacion de Escenario y Amenazas a Proceso*
#***********************************************************
class Asig_Esc_Form(forms.Form):
    """
     Asignacion de Escenarios y Amenazas a Proceso
    """
        
    escenarios = forms.ModelMultipleChoiceField(queryset=Escenarios.objects.all().order_by('titulo'),
                                          label=_('Escenarios Seleccionados :'),
                                          required= True,
                                          widget=FilteredSelectMultiple(
                                                    _('Escenarios'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

    #def clean_escenarios(self):

        #print('Entra a validacion de Escenario')
        #escenarios = self.cleaned_data['escenarios']
    
        #if not escenarios:
            #raise ValidationError(_('Debe elegir al menos un Escenario de Riesgo. En caso de no identificar un Escenario seleccione ERNI: ESCENARIO DE RIESGO NO IDENTIFICADO '))
            

    
class Asig_Imp_Form(forms.Form):
    """
    Asignacion de Impactos al Proceso
    """
    
    nivel=forms.ModelChoiceField(queryset=Nivel_Impacto.objects.all())
    

    # Selecciona que los niveles sean del Riesgo/Impacto
    def __init__(self, *args, **kwargs):
        # Extraemos los parámetros 'param' (instancia del Modelo Contrato)
        self.param = kwargs.pop('param', None)
        print('self.param =', self.param)
        
        # Llamamos al constructor de la clase base
        super().__init__(*args, **kwargs)

        # Si tenemos una referencia, configuramos los queryset correspondientes
        if self.param:

            # Selecciona solo los Gestores asociados al Contrato.
            self.fields['nivel'].queryset = Nivel_Impacto.objects.filter(tipo=self.param)



class Asig_Ind_Form(forms.Form):
    """
    Asignacion de Indicadores de Recuperacion  al Proceso
    """
    
    nivel=forms.ModelChoiceField(queryset=Indicadores_BIA.objects.all())
    

    # Selecciona que los niveles sean del Riesgo/Impacto
    def __init__(self, *args, **kwargs):
        # Extraemos los parámetros 'param' (instancia del Modelo Contrato)
        self.param = kwargs.pop('param', None)
        print('self.param =', self.param)
        
        # Llamamos al constructor de la clase base
        super().__init__(*args, **kwargs)

        # Si tenemos una referencia, configuramos los queryset correspondientes
        if self.param:

            # Selecciona solo los Gestores asociados al Contrato.
            self.fields['nivel'].queryset = Indicadores_BIA.objects.filter(tipo=self.param)



#************************************************************************************************************************************************************
#************************************************** 2. Procedimientos de Recuperacion **************************************************************************
#************************************************************************************************************************************************************
        
#******************************************
#Creacion de Procedimiento de Recuperacion*
#******************************************

class CreaProc_A_Form(forms.Form):
#class CreaProc_A_Form(forms.ModelForm):

    #Identificacion del Procedimiento
    nombre = forms.CharField(max_length= 100, label='Nombre :', widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
    #tipo = forms.ModelChoiceField(queryset=Tipo_Proc.objects.all())

    

    #class Meta:
        #model= Procedimientos
        #fields ='__all__'        

    # Validaciones
    def clean_nombre(self):
        print('Entro a validacion')
        nombre = self.cleaned_data['nombre']

        existe = Procedimientos.objects.filter(nombre=nombre).exists()

        if existe:
            raise forms.ValidationError(_('Este nombre ya existe'))

        return nombre

    
    
    #archivo = forms.FileField()

class CreaProc_B_Form(forms.Form):
    "Datos de Contexto del Procedimiento"

    #Identificacion del Procedimiento
    nombre = forms.CharField(max_length= 50)
    #tipo = forms.ModelChoiceField(queryset=Tipo_Proc.objects.all())

    #Contexto
    escenarios = forms.ModelChoiceField(queryset=Escenarios.objects.all(),
                                          label=_('Escenarios del Proceso :'),
                                          required= True)

    #class Media:
        #css = {
            #'all':['admin/css/widgets.css',
                   #'css/uid-manage-form.css'],
        #}
        # Adding this javascript is crucial
        #js = ['/admin/jsi18n/']


    #escenarios = forms.CharField(max_length=500, help_text = 'Identifique cual(es) de los Escenarios asociados al  Proceso seran abordados por este Procedimiento',
                                 #widget=forms.Textarea(attrs={'rows':4, 'cols':100, 'class':'inbox_2'}))
    
    estrategia = forms.CharField(help_text='Describa la estrategia a ser aplicada por el Procedimiento', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':100, 'class':'inbox_2'}))

    resp_proceso = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Resp Proceso', required=True) 
    bck_resp     = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)

    gestor_ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Gestor E.', required=True)
    bck_ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)

    enlace_c_crisis = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', label='Enlace CC', required=True)
    bck_enlace = forms.ModelChoiceField(queryset=Gestor.objects.all(),  required=False)


    def __init__(self, *args, **kwargs):

        # Extraemos los parámetros 'param' (instancia del Modelo Contrato)
        self.param = kwargs.pop('param', None)

        #Selecciona Gestores por grupos
        gestores = Gestor.objects.all()
        lista_autorizadores = [] 
        lista_ejecutores = [] 
        lista_c_crisis  = [] 
        
        for ges in gestores:
            grp=ges.user_gestor.groups
            for g in grp.all():
                if g.name == 'Autorizadores':
                    lista_autorizadores.append(ges.user_pk)
                if g.name == 'Ejecutores':
                    lista_ejecutores.append(ges.user_pk)
                if g.name == 'Gestion de Crisis':
                    lista_c_crisis.append(ges.user_pk)


        super(CreaProc_B_Form, self).__init__(*args, **kwargs )

        self.fields['resp_proceso'].queryset=Gestor.objects.filter(user_pk__in=lista_autorizadores)
        self.fields['bck_resp'].queryset=Gestor.objects.filter(user_pk__in=lista_autorizadores)
        self.fields['gestor_ejecutor'].queryset=Gestor.objects.filter(user_pk__in=lista_ejecutores)
        self.fields['bck_ejecutor'].queryset=Gestor.objects.filter(user_pk__in=lista_ejecutores)
        self.fields['enlace_c_crisis'].queryset=Gestor.objects.filter(user_pk__in=lista_c_crisis)
        self.fields['bck_enlace'].queryset=Gestor.objects.filter(user_pk__in=lista_c_crisis)

        if self.param:

            # Selecciona solo los Escenarios asignados al Proceso.
            self.fields['escenarios'].queryset = Escenarios.objects.filter(id__in=self.param)

    # --------------------------------------------

        # Selecciona que los niveles sean del Riesgo/Impacto
    # def __init__(self, *args, **kwargs):
        # Extraemos los parámetros 'param' (instancia del Modelo Contrato)
        # self.param = kwargs.pop('param', None)
        # print('self.param =', self.param)
        
        # Llamamos al constructor de la clase base
        # super().__init__(*args, **kwargs)

        # Si tenemos una referencia, configuramos los queryset correspondientes
        # if self.param:

            # Selecciona solo los Gestores asociados al Contrato.
            # self.fields['nivel'].queryset = Nivel_Impacto.objects.filter(tipo=self.param)

    
    #archivo = forms.FileField()


class CreaProc_P5_Form(forms.Form):
    "Datos de Servicios requeridos para el PC y DRP"

    nombre = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows':1, 'cols':200}))
    objetivo = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows':2, 'cols':200}))
    contacto = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows':1, 'cols':50}))
    contacto_bck = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows':1, 'cols':50}))

    
class CreaProc_P6_Form(forms.Form):
    "Datos de Contactos requeridos para el PC y DRP"

    nombre = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows':1, 'cols':200}))
    correo = forms.CharField(max_length=50, required=False, widget=forms.Textarea(attrs={'rows':1, 'cols':50}))
    tel_lab = forms.CharField(max_length=30, required=False, widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    cel_lab = forms.CharField(max_length=30, required=False, widget=forms.Textarea(attrs={'rows':1, 'cols':30}))

class CreaProc_P7_Form(forms.Form):
    "Pasos del Procedimiento de Contingencia"

    nro_paso = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'style': 'width: 60px;'}))
    descripcion = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':120,
                                                        'placeholder':'Describe el paso a realizar... '},
                                                        ),
                                  )
    
    ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', required=True)

    tiempo_esp = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'style': 'width: 60px;'}))

    # Filtra los gestores R y A para pertenecer al grupo Autorizadores
    def __init__(self,initial):

        # Seleccion por grupos
        ejecutores = []

        gestores=Gestor.objects.all()
        for ges in gestores:
            grp=ges.user_gestor.groups
            for g in grp.all():
                if g.name == 'Ejecutores':
                    ejecutores.append(ges.user_pk)


        super(CreaProc_P7_Form, self).__init__(initial)
        self.fields['ejecutor'].queryset = Gestor.objects.filter(user_pk__in = ejecutores)

class CreaProc_P8_Form(forms.Form):
    "Pruebas del Procedimiento"

    codigo   = forms.CharField(max_length=30, required=False, widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    objetivo = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':180,
                                                        'placeholder':'ej. Validar transaccion de compra en POS'},
                                                        ))
    alcance  = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':1200,
                                                        'placeholder':'ej. La prueba contempla el proceso de autorización y validación de '
                                                        'compras en terminales POS, desde la lectura de la tarjeta hasta la confirmación '
                                                        'de la transacción en el sistema central. No incluye la conciliación contable '
                                                        'posterior ni la reversa de transacciones, que serán probadas en una fase independiente.'},
                                                        ))
    
    criterios_exito = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':1200,
                                                        'placeholder':'ej. La prueba se considerará exitosa si al menos el 95% de las '
                                                        'transacciones son autorizadas correctamente, los tiempos de respuesta del POS'
                                                        ' no superan los 5 segundos y no se presentan rechazos por pérdida de '
                                                        'conectividad. Además, las terminales deben registrar las operaciones de forma '
                                                        'local para su sincronización posterior sin pérdida de información.'},
                                                        ))
    
    responsable = forms.ModelChoiceField(queryset=Gestor.objects.all(), empty_label=None, help_text='', required=True)

    
    # Filtra los gestores R y A para pertenecer al grupo Autorizadores
    def __init__(self,initial):

        # Seleccion por grupos
        responsables = []

        gestores=Gestor.objects.all()
        for ges in gestores:
            grp=ges.user_gestor.groups
            for g in grp.all():
                if g.name == 'Consultores':
                    responsables.append(ges.user_pk)


        super(CreaProc_P8_Form, self).__init__(initial)
        self.fields['responsable'].queryset = Gestor.objects.filter(user_pk__in = responsables)

class Caso_P8_Form(forms.Form):
    """
    Creacion/Modificacion de Caso de Prueba
    """
    
    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]


    descripcion = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':180,
                                                        'placeholder':'ej.descripcion'},
                                                        ))
    
    resultado_esperado = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':180,
                                                        'placeholder':'ej. resultado esperado'},
                                                        ))

    precondiciones = forms.CharField(max_length=480,
                                  widget=forms.Textarea(attrs={'rows':4, 'cols':180,
                                                        'placeholder':'ej. (precondiciones) '},
                                                        ))

    prioridad = forms.ChoiceField(
        choices=PRIORIDAD_CHOICES,
        initial='Media'
    )


class Revisa_Proced_B_Form(forms.Form):
    """
    Revision de observaciones de rechazo a la parte 1 del
    Procedimientos de Recuperacion
    """

    #Identificacion del Procedimiento
    nombre = forms.CharField(max_length= 100, label='Nombre :', widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
    tipo = forms.ModelChoiceField(queryset=Tipo_Proc.objects.all())

    #Contexto
    #escenarios = forms.ModelMultipleChoiceField(queryset=Escenarios.objects.all(),
                                          #label=_('Escenarios del Proceso :'),
                                          #required= False,
                                          #widget=FilteredSelectMultiple(
                                                    #_('Escenarios'),
                                                    #False,
                                                 #))

    #class Media:
        #css = {
            #'all':['admin/css/widgets.css',
                   #'css/uid-manage-form.css'],
        #}
        # Adding this javascript is crucial
        #js = ['/admin/jsi18n/']


    escenarios = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':100}))
    
    estrategia = forms.CharField(max_length=500, help_text = 'Describa la Estrategia a ser aplicada por el Procedimiento ',
                                 widget=forms.Textarea(attrs={'rows':4, 'cols':100}))


    #Responsables
    resp_proceso = forms.ModelChoiceField(queryset=Gestor.objects.all())
    bck_resp = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)

    gestor_ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all())
    bck_ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)

    enlace_c_crisis = forms.ModelChoiceField(queryset=Gestor.objects.all())
    bck_enlace = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)


    #archivo = forms.FileField()
    notifica = forms.BooleanField(label='Notifica por correo..?', required=False)

        
        

#************************************************************************************************************************************************************
#**************************************************           3. DRP     **********************************************************************************
#************************************************************************************************************************************************************

class Crea_DRP_Enc_Form(forms.Form):
    """
    Creacion del registro inicial del DRP
    """

    nombre = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':1, 'cols':100})) 


    # Validaciones

    def clean_nombre(self):
        
        nombre=self.cleaned_data['nombre']
        existe = Drp.objects.filter(nombre=nombre)

        if existe:
            raise ValidationError(_('*** Nombre de DRP ya existe ***'))
            
        return nombre 


class Drp_Sec_1_Form(forms.Form):
    """
    Definicion de Objetivo del Drp
    """

    objetivo = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows':10, 'cols':200, "class": "inbox_1"})) 
 
    #objetivo.widget.attrs.update(size='40')


class Drp_Sec_2_Form(forms.Form):
    """
    Definicion de Responsables  del Drp
    """

   
    resp_drp = forms.ModelChoiceField(queryset=Gestor.objects.all())
    
    bck_resp = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)

    gestor_ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all())
    bck_ejecutor = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)

    enlace_c_crisis = forms.ModelChoiceField(queryset = Gestor.objects.all())
    bck_enlace = forms.ModelChoiceField(queryset=Gestor.objects.all(), required=False)


    def __init__(self, initial):

        # Seleccion por grupos
        #selec_TI = []
        #selec_ejecutor = []
        #ejecutor_TI = []

        selec_Gestion_de_Crisis=[]

        Autorizadores_TI=[]
        Ejecutores_TI=[]

        gestores=Gestor.objects.all()
        for ges in gestores:
            grp=ges.user_gestor.groups
            es_TI=False
            es_Aut=False
            es_Ejec=False

            for g in grp.all():
            # Analiza los grupos asociados al gestor
                if g.name == 'TI':
                    es_TI=True
                    #selec_TI.append(ges.user_pk)
                if g.name== 'Autorizadores':
                    es_Aut=True
                if g.name == 'Ejecutores':
                    es_Ejec=True
                    #selec_ejecutor.append(ges.user_pk)

                if g.name == 'Gestion de Crisis':
                    selec_Gestion_de_Crisis.append(ges.user_pk)
            
            if es_TI and es_Aut:
                Autorizadores_TI.append(ges.user_pk)
            if es_TI and es_Ejec:
                Ejecutores_TI.append(ges.user_pk)



            #if ges.user_pk in selec_TI and ges.user_pk in selec_ejecutor:
            #    ejecutor_TI.append(ges.user_pk) 


        super(Drp_Sec_2_Form, self).__init__(initial)
        self.fields['resp_drp'].queryset = Gestor.objects.filter(user_pk__in = Autorizadores_TI)
        self.fields['bck_resp'].queryset = Gestor.objects.filter(user_pk__in = Autorizadores_TI)
        self.fields['gestor_ejecutor'].queryset = Gestor.objects.filter(user_pk__in = Autorizadores_TI)
        self.fields['bck_ejecutor'].queryset = Gestor.objects.filter(user_pk__in = Autorizadores_TI)
        self.fields['enlace_c_crisis'].queryset = Gestor.objects.filter(user_pk__in = selec_Gestion_de_Crisis)
        self.fields['bck_enlace'].queryset = Gestor.objects.filter(user_pk__in = selec_Gestion_de_Crisis)
        


class Drp_Sec_3_Form(forms.Form):
    """
    Definicion del alcance del  Drp. 
    El alcance se determina  por los Procesos seleccionados
    """
   
    

    #Contexto
    procesos = forms.ModelMultipleChoiceField(queryset=SubProceso.objects.all(),
                                          label=_('Escenarios del Proceso :'),
                                          required= False,
                                          widget=FilteredSelectMultiple(
                                                    _('Escenarios'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']


    def __init__(self, initial):

        # Seleccion de Procesos
        selec_procesos = []

        sproc=SubProceso.objects.all()

        for prc in sproc:
            print('SProceso =', prc.codigo)
            for p_cont in prc.procedimientos_contingencia.all():
                print('-- PC:', p_cont)
                if p_cont.tipo.nombre == 'Automatico':
                    selec_procesos.append(prc.codigo)
                        
        print('procesos=', selec_procesos)

        super(Drp_Sec_3_Form, self).__init__(initial)
        self.fields['procesos'].queryset = SubProceso.objects.filter(codigo__in = selec_procesos)


 
class Drp_Sec_4_Form(forms.Form, list):
    """
    Definicion de la Estrategia de REcuperacion del Drp.

    """
    
    desc_estrategia = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows':10, 'cols':100}))
    tipo_site = forms.ModelChoiceField(queryset=Tipo_Site.objects.all())
    tipo_disp = forms.ModelChoiceField(queryset=Tipo_Disp.objects.all()) 

class Drp_Sec_5_Form(forms.Form, list):
    """
    Asignacion del Componente  al  DRP. """
    
    componentes = forms.ModelMultipleChoiceField(queryset=Componentes.objects.all(),
                                          label=_('Componentes:'),
                                          required= False,
                                          widget=FilteredSelectMultiple(
                                                    _('Componentes'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']
    



class Crea_CMP_Form(forms.Form, list):
    """
    Creacion de un Componente  en la  BD. """
    
    tipo_act = forms.ModelChoiceField(queryset=Tipo_Componente.objects.all())
    nombre = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
    descripcion = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows':4, 'cols':25}))
    identificacion= forms.CharField(max_length=30, widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    fabricante=forms.CharField(max_length=30, widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    codigo_inv=forms.CharField(max_length=25, widget=forms.Textarea(attrs={'rows':1, 'cols':25}))

class Crea_LBC_Form(forms.Form, list):
    """
    Creacion de un parametro de la LBC de un  Componente. """
    
    nombre = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
    descripcion = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'rows':2, 'cols':150}))
    metodo_acceso = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'rows':2, 'cols':150}))
    valor = forms.CharField(max_length=30, widget=forms.Textarea(attrs={'rows':1, 'cols':50}))
    

#************************************************************************************************************************
#*************************************** 4. Manejo de Incidentes *********************************************************
#************************************************************************************************************************

class Declara_Incidente_Form(forms.Form):
    """
    Declaracion de un Incidente
    """
    nombre = forms.CharField(max_length= 25, label='Nombre :')
    area = forms.CharField(max_length= 25, label='Area:')
    #correo = forms.EmailField(required=True)
    descripcion = forms.CharField(max_length=500, label='Descripcion:',  help_text='Describir Incidente :', widget=forms.Textarea(attrs={'rows':8, 'cols':70}))
    #amenazas_i = forms.ModelMultipleChoiceField(queryset=Amenazas.objects.all().order_by('titulo'),
    #                                      label=_('Amenazas Ocurridas :'),
    #                                      required= True,
    #                                      widget=FilteredSelectMultiple(
    #                                                _('Amenazas'),
    #                                                False,
    #                                            ))

    #class Media:
    #    css = {
    #       'all':['admin/css/widgets.css',
    #               'css/uid-manage-form.css'],
    #   }
        # Adding this javascript is crucial
    #    js = ['/admin/jsi18n/']


from django import forms
from datetime import datetime, date

class Plan_Pruebas_A_Form(forms.Form):
    """
    Form para programar pruebas: fecha + hora separados,
    con mensajes de error personalizados.
    """

    fecha = forms.DateField(
        widget=forms.TextInput(attrs={
            "class": "form-control flatpickr-date",
            "placeholder": "Seleccione fecha",
            "autocomplete": "off", 
        }),
        input_formats=["%Y-%m-%d"],
        error_messages={
            "required": "Debe definir una fecha de ejecución.",
            "invalid": "Formato de fecha inválido. Use AAAA-MM-DD."
        }
    )

    hora = forms.TimeField(
        widget=forms.TextInput(attrs={
            "class": "form-control flatpickr-time",
            "placeholder": "Seleccione hora",
            "autocomplete": "off",
        }),
        input_formats=["%H:%M"],
        error_messages={
            "required": "Debe definir una hora de inicio de la Prueba.",
            "invalid": "Formato de hora inválido. Use HH:MM (24h)."
        }
    )

    fecha_hora = None

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        hoy = date.today()
        # ejemplo: prohibir hoy o anterior
        if fecha and fecha <= hoy:
            raise forms.ValidationError("La fecha no puede ser hoy o anterior.")
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data.get("hora")
        # Nota: si el campo está vacío no llegas aquí porque el validator 'required' ya levantó.
        # Aquí validaciones extra (rango, etc.)
        if hora is None:
            # Esto normalmente no se ejecuta si el campo está vacío porque required ya lo cubre,
            # pero lo dejamos por si quieres detectar un valor None explícito.
            raise forms.ValidationError("Debe definir una hora de inicio de la Prueba.")
        return hora

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        hora = cleaned_data.get("hora")

        if fecha and hora:
            cleaned_data["fecha_hora"] = datetime.combine(fecha, hora)

            # Ejemplo extra: si la fecha es hoy, la hora debe ser futura
            if fecha == date.today():
                ahora = datetime.now().time()
                if hora <= ahora:
                    self.add_error('hora', "La hora debe ser posterior a la hora actual.")
        return cleaned_data


class Plan_Pruebas_B_Form(forms.Form):

    pass


class EjecucionPruebasForm(forms.Form):
    """
    Ejecucion de la Prueba
    """

    descripcion_ejecucion = forms.CharField(
        label="Descripción de la ejecución",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "ej.: Se requiere revisar el alcance de la prueba incorporando el caso de...",
        }),
        error_messages={
            "required": "Debe ingresar una descripción de la ejecución.",
        }
    )

    incidentes = forms.CharField(
        label="Incidentes de la ejecución",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Ej.: Durante la ejecucion de la Prueba se interrumpio la operacion del Site de Contingencias ...",
        }),
        error_messages={
            "required": "Debe ingresar una descripción de la ejecución.",
        }
    )

    resultados_obtenidos = forms.CharField(
        label="Resultados obtenidos",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "ej.: Para los casos 001 y 003 las pruebas resultaron fallidas debido a ....",
        })
    )

    evaluacion_final = forms.ChoiceField(
        label="Evaluación final",
        required=False,
        choices=[
            ('Exitosa', 'Exitosa'),
            ('Parcial', 'Parcial'),
            ('Fallida', 'Fallida'),
            ('En Ejecucion', 'En Ejecucion'),
        ],
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )

    lecciones_aprendidas = forms.CharField(
        label="Lecciones aprendidas",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Lecciones aprendidas, oportunidades de mejora o recomendaciones",
        })
    )

    evidencia_general = forms.FileField(
        label="Evidencia general",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
        })
    )



from django import forms


class EjecucionCasoPruebaForm(forms.Form):

    resultado = forms.ChoiceField(
        label="Resultado del caso",
        required=False,
        choices=[
            ('Exitosa', 'Exitosa'),
            ('Fallida', 'Fallida'),
            ('En Proceso', 'En Proceso'),
            ('No Aplica', 'No Aplica'),
        ],
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )

    observaciones = forms.CharField(
        label="Observaciones",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Observaciones, incidencias o comentarios relevantes durante la ejecución del caso",
        })
    )

    evidencia = forms.FileField(
        label="Evidencia del caso",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
        })
    )



class Modifica_Incidente_Form(forms.Form):
    """
    Modificacion de Amenazas en Declaracion de un Incidente
    """
    pass

    #amenazas_i = forms.ModelMultipleChoiceField(queryset=Amenazas.objects.all().order_by('titulo'),
    #                                      label=_('Amenazas Ocurridas :'),
    #                                      required= True,
    #                                      widget=FilteredSelectMultiple(
    #                                                _('Amenazas'),
    #                                                False,
    #                                            ))

    #class Media:
    #    css = {
    #       'all':['admin/css/widgets.css',
    #               'css/uid-manage-form.css'],
    #   }
        # Adding this javascript is crucial
    #    js = ['/admin/jsi18n/']

#************************************************************************************************************************************************************
#************************************************** 5. Mantencion de Maestros **********************************************************************************
#************************************************************************************************************************************************************

#******************************************
#       Mantencion Gestores/Usuarios      *
#******************************************

class Crea_Gestor_Form(UserCreationForm):
    """
    Crea un usuario gestor en la Base
    Utiliza el formulario estandar para la creacion
    de usuarios provisto por Django
    """

    class Meta:
        model = User
        fields = [ 'email', 'username', 'password1', 'password2', 'first_name', 'last_name']


    # Validaciones


    
    def clean_username(self):
        
        usuario=self.cleaned_data['username']
        existe = User.objects.filter(username=usuario)

        if existe:
            raise ValidationError(_('*** Gestor usuario ya existe ***'))
            
        return usuario        

    def clean_password1(self):
        username =  self.data.get('username')
        password1 = self.cleaned_data['password1']
        
        
        if password1 == username:
            raise ValidationError(_('*** La Clave no puede ser igual al nombre de usuario  ***'))


        return password1   


    def clean_password2(self):
        
        password1 =self.data.get('password1')
        password2 =self.cleaned_data['password2']
                     
       
        if password1 != password2:
            raise ValidationError(_('*** Clave repetida no coincide ***'))

        if len(password1)<= 8 :
            raise ValidationError(_('*** Clave no puede ser menor a 8 caracteres ***'))


    def clean_email(self):
        
        correo =self.data.get('email')

        print('valida email--:', correo)
        
        if len(correo) < 2:
            
            raise ValidationError(_('*** Debe ingresar un correo valido ***'))

        return correo      
        

class Crea_Gestor2_Form(forms.Form):
    """
    Complementa datos de la creacion del Gestor
    """

    cargo = forms.CharField(max_length=30)  #, widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    area =  forms.ModelChoiceField(queryset=Area.objects.all())
    fono_t = forms.CharField(max_length=15) #,  widget=forms.Textarea(attrs={'rows':1, 'cols':15}))
    cod_area = forms.ModelChoiceField(queryset=Cod_Area.objects.all(), blank=False, required=True )
    fono_c = forms.CharField(max_length=15) #, widget=forms.Textarea(attrs={'rows':1, 'cols':15}))
    
   
class Borra_Gestor_Form(forms.Form):
    """
    Pantalla de Ingreso Nombre de Usuario
    """

    gestores=Gestor.objects.all().order_by('apellido')
    
    usuario = forms.ModelChoiceField(gestores)
    confirma_borra  = forms.BooleanField(required=False)
    confirma_desactiva = forms.BooleanField(required=True)

    def clean_usuario(self):

        print('Entra a validacion')
        usuario = self.cleaned_data['usuario']

        print('usuario =', usuario.user_gestor.username)

        # en_proceso_R = SubProceso.objects.filter(gestor_R == usuario.user_gestor).exist()


        # Validaciones
        #==============

        """ Revisa si el usuario esta asociado a  Procesos """
        en_proceso = False 
        subP = SubProceso.objects.all()
        for sp in subP.all():
            if  usuario == sp.gestor_R or usuario == sp.gestor_A or usuario == sp.gestor_C or usuario == sp.gestor_I:
                en_proceso = True

                
        print('en proceso =', en_proceso)    

        """ Revisa si el usuario esta asociado a
        Procedimientos de Contingencia """
        
        en_procedimiento = False 
        procedimientos = Procedimientos.objects.all()
        for prcd in procedimientos.all():
            if  usuario == prcd.resp_proceso or usuario == prcd.bck_resp or usuario == prcd.gestor_ejecutor or usuario == prcd.bck_ejecutor or usuario == prcd.enlace_c_crisis or usuario == prcd.bck_enlace:
                en_procedimiento = True


        print('en procedimiento =', en_procedimiento)

        if usuario.user_pk == 1:
            raise ValidationError(_('*** Este Usuario no puede ser eliminado por este medio.  ***'))
            
         
        if en_proceso:
            raise ValidationError(_('*** El Usuario Gestor esta asociado a uno o varios Procesos de Negocio vigentes. No puede ser eliminado ***'))

        if en_procedimiento:
            raise ValidationError(_('*** El Usuario Gestor esta asociado a un o varios Procedimientos de Recuperacio vigentes. No puede ser eliminado ***'))
            



        return usuario

    
#******************************************
#       Gestion de Grupos                 *
#******************************************
    

class Asigna_Grupo_Form(forms.Form):    
    """
    Asignacion/Desasignacion de Grupo
    """

    grupos = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                          label=_('Grupos Seleccionados :'),
                                          required = False,
                                          widget=FilteredSelectMultiple(
                                                    _('Grupos'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']
    

#*************************************
#     Mantencion Riesgo/Impactos     *
#*************************************

class Crea_Impacto_Form(forms.Form):
    """
    Formulario para la Creacion / Modificacion  de impactos"""

    nombre = forms.CharField(max_length= 100)
    descripcion = forms.CharField(max_length= 300, widget=forms.Textarea(attrs={'rows':3, 'cols':100}))
    ponderacion = forms.DecimalField(widget=forms.NumberInput(attrs={'step': '00.01'}))

class Crea_Nivel_Imp_Form(forms.Form):
    """
    Creacion/Modificacion de Nivel de Impacto"""

    nombre = forms.CharField(max_length= 100)
    descripcion = forms.CharField(max_length= 300, widget=forms.Textarea(attrs={'rows':3, 'cols':100}))
    valor = forms.DecimalField(widget=forms.NumberInput(attrs={'step': '00.01'}))

#*****************
# Reinicio de BD *
#*****************

class Reset(forms.Form):
    """
    Reinicio de la Base de Datos"""

    raiz = forms.CharField(max_length= 30, required=True)


