#Modelo de Datos Modelo bcp del Sistema Defcon5.

from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User, Group
from datetime import date, datetime
from django.utils import timezone


#====================================
# ENTIDADES o MODELOS
#====================================

# ===========================================================
# PROCESO
# ===========================================================
  
class Proceso(models.Model):
    """
    Entidad: Proceso
             Registra los atributos del Proceso a ser considerado por el bcp
    """

    
    path= models.CharField(max_length=200, blank=True)
    proceso_padre = models.CharField(max_length=30, blank=True)
    pk_padre = models.IntegerField(default=0)
    ni= models.CharField(max_length=20, blank=True) 
    proceso = models.CharField(max_length=30, blank=True)
    nro_hijos = models.IntegerField()
    nombre = models.CharField(max_length=50)
    objetivo = models.TextField(max_length=500, blank=True, help_text='Describa el principal objetivo del Proceso')
    fecha_crea = models.DateField(auto_now_add=True)
    fecha_ult_mod = models.DateField(auto_now_add=True)


    #Registra el Tipo 
    es_subproceso=models.BooleanField(default=False)
    
    subproceso = models.OneToOneField('SubProceso', on_delete=models.CASCADE, blank=True, null=True)
    subproceso_v = models.OneToOneField('SubProceso_V', on_delete=models.CASCADE, blank=True, null=True)

    log_auth=models.ManyToManyField('LogAut', blank=True)
    
    
    class Meta:
        ordering = ["proceso"]


    def __str__(self):
        """
        String que representa al objeto 
        """
        return self.proceso


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular 
        """
        return reverse('Detalle-Procesos', args=[str(self.id)])


class SubProceso(models.Model):
    """
    Datos de Proceso Evaluable
    """

    pk_padre = models.IntegerField(default=0)
    codigo = models.CharField(max_length=30, blank=True)
    path=models.CharField(max_length=200, blank=True)
    
    #Campos para implementar un modelo RACI
    gestor_R = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_r', null=True, blank=True)
    gestor_A = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_a', null=True, blank=True)
    gestor_C = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_c', null=True, blank=True)
    gestor_I = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_i', null=True, blank=True)

    #Campos para impactos e indicadores de Contingencia.

    #Impactos e Indicadores de recuperacion
 
    impact_subp = models.ManyToManyField('Impactos_Asig', related_name= 'impactos', blank=True) 
    indicador_subp= models.ManyToManyField('Indicadores_Asig', related_name= 'indicadores', blank=True) 

    ranking =  models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    
    #Registra el estado de Autorizacion RACI
    PROC_STATUS = (
        ('R', 'Vigenteado'),
        ('r', 'x Vigentear R'),
        ('A', 'x Aprobar A'),
        ('C', 'En Dfncn C'),
        ('x', 'En Revision C'), 
    )
    status = models.CharField(max_length=1, choices=PROC_STATUS, blank=True, default='C', help_text='Estado de la definicion del Proceso')

    #Registra la Fase en el desarrollo del  bcp
    FASE_STATUS = (
        ('M', 'Fase Procesos'),
        ('V', 'Fase BIA'),
        ('B', 'Fase Activos'),
        ('E', 'Fase Escenarios'),
    )

    fase_status = models.CharField(max_length=1, choices=FASE_STATUS, blank=True, default='M', help_text='Fase del bcp')

    recursos=models.ManyToManyField('Recursos', blank=False)

    escenarios=models.ManyToManyField('Escenarios', blank=False)

    #procedimientos_contingencia = models.ManyToManyField('Procedimientos',  blank=True, null=True)
    nro_prdto = models.IntegerField(default=0)

    log_revision=models.ManyToManyField('Log_Revision', blank=True)
    
    actualiza=models.BooleanField(default=False) # Identifica si el proceso esta siendo actualizado


    class Meta:
        ordering = ["path"]
    
    def __str__(self):
        """
        String que representa al objeto 
        """
        return self.path


    #def get_absolute_url(self):
    #    """
    #    Devuelve el URL a una instancia particular 
    #    """
    #    return reverse('book-detail', args=[str(self.id)])


class SubProceso_V(models.Model):
    """
    Datos de Proceso Evaluable Vigente (aprobado)
    """""
    # Campos del Proceso
    nombre = models.CharField(max_length=50, default="")
    objetivo = models.TextField(max_length=500, blank=True, help_text='Describa el principal objetivo del Proceso')
    version= models.IntegerField(default=0)
    
    pk_padre = models.IntegerField(default=0)
    codigo = models.CharField(max_length=50, blank=True) # Codigo del Proceso original
    path=models.CharField(max_length=200, blank=True)
    fecha_ult_aut=models.DateField(auto_now_add=True)
    
    #Campos para implementar un modelo RACI
    gestor_R = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_v_r', null=True, blank=True)
    gestor_A = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_v_a', null=True, blank=True)
    gestor_C = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_v_c', null=True, blank=True)
    gestor_I = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_v_i', null=True, blank=True)

    #Impactos e Indicadores de recuperacion
 
    impact_subp = models.ManyToManyField('Impactos_Asig_v', related_name= 'impactos_v', blank=True) 
    indicador_subp= models.ManyToManyField('Indicadores_Asig_v', related_name= 'indicadores_v', blank=True) 

    ranking =  models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    
    recursos=models.ManyToManyField('Recursos', blank=False)

    escenarios=models.ManyToManyField('Escenarios', blank=False)

    procedimientos_contingencia = models.ManyToManyField('Procedimientos', blank=True)
    procedimientos_contingencia_v = models.ManyToManyField('Procedimientos_V', blank=True)

    nro_prdto = models.IntegerField(default=0) # Cantidad de Procedimientos 

    log_revision=models.ManyToManyField('Log_Revision', blank=True)

    #log_control_cambio=models.ManyToManyField('Log_Revision', blank=False, null=False)
    



    class Meta:
        ordering = ["path"]
    
    def __str__(self):
        """
        String que representa al objeto 
        """
        return self.path


    #def get_absolute_url(self):
    #    """
    #    Devuelve el URL a una instancia particular 
    #    """
    #    return reverse('book-detail', args=[str(self.id)])

class Control_Cambios(models.Model):
    """
    Log de Control de Cambios de Procesos y Procedimientos vigentes """

    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    proceso= models.ForeignKey(SubProceso_V, on_delete=models.CASCADE, null=True)
    procedimiento= models.ForeignKey('Procedimientos_V', on_delete=models.CASCADE, null=True)

    gestor_aut = models.ForeignKey('Gestor', on_delete=models.CASCADE, null=True)

    descripcion=models.TextField(max_length=200)

    class Meta:
        ordering = ["-fecha", "-hora"]



class Impactos_Asig(models.Model):
    """
    Impactos Asignados al Proceso (Nub de relacion entre un Subprocesos, los Impactos (Riesgos)
    y Nivel de cada uno)
    """

    #subproceso=models.ForeignKey(SubProceso, on_delete=models.SET_NULL, related_name='Subproceso', null=True, blank=True)
    pk_proc=models.IntegerField(default=0)
    impacto=models.ForeignKey('Tipo_Impacto', on_delete=models.SET_NULL, related_name='riesgo', null=True, blank=True)
    nivel=models.ForeignKey('Nivel_Impacto', on_delete=models.SET_NULL, related_name='nivel_imp', null=True, blank=True)


class Impactos_Asig_v(models.Model):
    """
    Impactos Asignados al Proceso vigente (Nub de relacion entre un Subprocesos, los Impactos (Riesgos)
    y Nivel de cada uno)
    """

    #subproceso=models.ForeignKey(SubProceso, on_delete=models.SET_NULL, related_name='Subproceso', null=True, blank=True)
    pk_proc=models.IntegerField(default=0)
    impacto=models.ForeignKey('Tipo_Impacto', on_delete=models.SET_NULL, related_name='riesgo_vigente', null=True, blank=True)
    nivel=models.ForeignKey('Nivel_Impacto', on_delete=models.SET_NULL, related_name='nivel_imp_vigente', null=True, blank=True)


class Indicadores_Asig(models.Model):
    """
    Indicadores asignados al Proceso (Nub)
    """
    pk_proc=models.IntegerField(default=0)
    indicador=models.ForeignKey('Tipo_Indicador', on_delete=models.SET_NULL, related_name='indicador', null=True, blank=True)
    nivel = models.ForeignKey('Indicadores_BIA', on_delete=models.SET_NULL, related_name='nivel_bia', null=True, blank=True)

class Indicadores_Asig_v(models.Model):
    """
    Indicadores asignados al Proceso vigente (Nub)
    """
    pk_proc=models.IntegerField(default=0)
    indicador=models.ForeignKey('Tipo_Indicador', on_delete=models.SET_NULL, related_name='indicador_vigente', null=True, blank=True)
    nivel = models.ForeignKey('Indicadores_BIA', on_delete=models.SET_NULL, related_name='nivel_bia_vigente', null=True, blank=True)


class LogAut(models.Model):
    """
    Entidad:    Log de Autorizaciones.
                Registra las Autorizaciones dadas al Proceso durante
                las distintas fases de definicion.     
    """

    cod_proceso = models.CharField(max_length=10, blank=True)
    gestor_aprobador= models.ForeignKey('Gestor', on_delete=models.SET_NULL, null=True)
    p_status=models.CharField(max_length=2, blank=True)
    fecha=models.DateField(auto_now_add=True)
    Aprobado=models.BooleanField(default=False, blank=True)
    item = models.CharField(max_length=10, blank=True)
    observacion=models.TextField(max_length=200)



class Recursos(models.Model):
    """
    Entidad:    Activos asociados a Procesos.
                Registra todos los activos (Sistemas de Aplicacion,
                Componentes de infraestructura, Entidades, etc)
                asociados a Procesos.      
    """

    cod_rec = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=200, blank=True)
    descripcion=models.TextField(max_length=500, blank=True, help_text='Describa el Recurso')
    tipo=models.ForeignKey('Tipo_RR', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String que representa al objeto 
        """
        return  self.nombre+': '+self.descripcion
    
    class Meta:
        ordering = ["tipo", "nombre"]



class Tipo_RR(models.Model):
    """
    Entidad:    Tipos de Recursos
    """

    nombre= models.CharField(max_length=50, blank=True)
    descripcion=models.TextField(max_length=200, blank=True, help_text='Describa el Recurso')

    class Meta:
            ordering = ["nombre"]

    def __str__(self):
        return self.nombre+' / '+self.descripcion
    
        



class Gestor(models.Model):
    """
    Entidad: Gestor
            Registra los atributos de un gestor del Sistema
    """

    user_pk = models.IntegerField(null=True)
    user_gestor = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    cargo = models.CharField(max_length= 50, blank=True)
    apellido= models.CharField(max_length= 50, blank=True)
    area =  models.ForeignKey('Area', on_delete=models.SET_NULL, null=True)
    fono_t = models.CharField(max_length= 50, blank=True)
    cod_area = models.ForeignKey('Cod_Area', on_delete=models.SET_NULL, null=True)
    fono_c = models.CharField(max_length= 50, blank=True) 
    
    class Meta:
        ordering = ["apellido"]

    def __str__(self):
        return self.apellido+', '+self.user_gestor.first_name+'- '+ self.cargo
        #return self.apellido+self.cargo


class Escenarios(models.Model):
    """
    Entidad: Escenarios
             Registra los posibles escenarios catatroficos al
             que pueden ser expuestos los Procesos
    """

    titulo = models.CharField(max_length= 50, blank=True)
    descripcion = models.TextField(max_length=500, blank=True, help_text='Describa el escenarios')
    #amnzas = models.ManyToManyField('Amenazas', related_name= 'Amenazas_Escenarios')
    estrategias = models.ManyToManyField('Estrategias')

    def __str__(self):
        return self.titulo+' :'+self.descripcion

class Amenazas(models.Model):
    """
    Entidad: Escenarios
             Registra los posibles amenazas presentes en los escenarios catatroficos al
             que pueden ser expuestos los Procesos
    """
    titulo = models.CharField(max_length= 50, blank=True)
    descripcion = models.TextField(max_length=500, blank=True, help_text='Describa la amenaza')
    landscape = models.ManyToManyField(Escenarios)

    def __str__(self):
        return self.titulo+' / '+self.descripcion
    
class Estrategias(models.Model):
    """
    Entidad: Escenarios
             Registra los posibles estrategias para la recuperacion
             de la continuidad operativa de manera alternativa
            
    """
    titulo = models.CharField(max_length= 50, blank=True)
    descripcion = models.TextField(max_length=500, blank=True, help_text='Describa la Estrategia')
    activa_drp=models.BooleanField(default=False)


    def __str__(self):
        return self.titulo+' / '+self.descripcion

 

class Nivel_Impacto(models.Model):
    """
    Define niveles de impacto x Riesgo vigentes (aprobadas por Comite)
    """

    tipo =  models.ForeignKey('Tipo_Impacto', on_delete=models.SET_NULL, null=True)  
    cod = models.IntegerField(null=True)
    nombre = models.CharField(max_length= 25, blank=True)
    descripcion = models.CharField(max_length= 150, blank=True)
    valor = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)


    def __str__(self):
        return self.nombre+' / '+self.descripcion

    class Meta:
        ordering = ["valor"]

class Nivel_Impacto_P(models.Model):
    """
    Define niveles de impacto x Riesgo Propuestas
    """

    tipo =  models.ForeignKey('Tipo_Impacto', on_delete=models.SET_NULL, null=True)  
    cod = models.IntegerField(null=True)
    nombre = models.CharField(max_length= 25, blank=True)
    descripcion = models.CharField(max_length= 150, blank=True)
    valor = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)


    def __str__(self):
        return self.nombre+' / '+self.descripcion

    class Meta:
        ordering = ["valor"]

    
class Tipo_Impacto(models.Model):
    """
    Define el Riesgo RIA vigente (Aprobado por el CGC)
    """

    nombre = models.CharField(max_length= 100, blank=True)
    descripcion = models.CharField(max_length= 300, blank=True)
    ponderacion = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    

    class Meta:
        ordering = ["ponderacion"]

    def __str__(self):
        return self.nombre+' / '+self.descripcion

class Tipo_Impacto_P(models.Model):
    """
    Define el Riesgo RIA propuesto.
    """

    nombre = models.CharField(max_length= 100, blank=True)
    descripcion = models.CharField(max_length= 300, blank=True)
    ponderacion = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    

    class Meta:
        ordering = ["ponderacion"]

    def __str__(self):
        return self.nombre+' / '+self.descripcion

    
class Indicadores_BIA(models.Model):
    """
    Define los Niveles de indicadores RTO, RPO, MTD (Aprobados)
    """
    tipo =  models.ForeignKey('Tipo_Indicador', on_delete=models.SET_NULL, null=True)
    cod = models.IntegerField(null=True)
    nivel = models.CharField(max_length= 15, blank=True)
    definicion = models.CharField(max_length= 50, blank=True)
    valor = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    
    def __str__(self):
        return self.nivel+' / '+self.definicion

class Indicadores_BIA_P(models.Model):
    """
    Define los Niveles de indicadores RTO, RPO, MTD (Propuestos)
    """
    tipo =  models.ForeignKey('Tipo_Indicador', on_delete=models.SET_NULL, null=True)
    cod = models.IntegerField(null=True)
    nivel = models.CharField(max_length= 15, blank=True)
    definicion = models.CharField(max_length= 50, blank=True)
    valor = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    
    def __str__(self):
        return self.nivel+' / '+self.definicion
    

class Tipo_Indicador(models.Model):
    """
    Define los indicadores RTO, RPO, MTD (Aprobados)
    """

    nombre = models.CharField(max_length= 3, blank=True)
    descripcion = models.CharField(max_length= 400, blank=True)
    
    ponderacion= models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    
    def __str__(self):
        return self.nombre+' / '+self.descripcion

        
class Tipo_Indicador_P(models.Model):
    """
    Define los indicadores RTO, RPO, MTD (Propuestos)
    """

    nombre = models.CharField(max_length= 3, blank=True)
    descripcion = models.CharField(max_length= 400, blank=True)
    
    ponderacion= models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    
    def __str__(self):
        return self.nombre+' / '+self.descripcion


class Parametros_G(models.Model):
    """
    Parametros Generales del Sistema
    """
    nombre = models.CharField(max_length= 25, blank=True)
    valor_1 = models.CharField(max_length= 15, blank=True)
    valor_2 = models.IntegerField(null=True)
    #valor_3 = models.DecimalField(max_digits=7, decimal_places=4, default=000.00)

# ===========================================================
#  REGISTRO DE INCIDENTES 
# ===========================================================

class Incidentes(models.Model):
    """
    Registro del Incidente
    """

    codigo = models.CharField(max_length= 100, blank=False)
    fecha=models.DateField(auto_now_add=True)
    fecha_creacion = models.DateTimeField(auto_now_add=False)

    # Identificacion de quien registra el incidente
    nombre_r  = models.CharField(max_length= 25, blank=True)
    area_r = models.CharField(max_length= 25, blank=True)
    correo = models.EmailField(max_length = 254, blank=True)
    
    descripcion = models.CharField(max_length= 500, blank=True)

    # Registro de la amenazas identificadas ocurridas en el incidente
    amenazas_i = models.ManyToManyField('Amenazas', blank=False)

    # Procesos y Escenarios de Riesgo asociados al Incidente
    procesos_i = models.ManyToManyField('SubProceso_V')
    escenarios_i = models.ManyToManyField('Escenarios')
 
    estado =models.BooleanField(default=True)  #Indica si el incidente esta abierto (True) o Cerrado
    changed=models.BooleanField(default=False) #Indica si el incidente ha sido modificado
    test=models.BooleanField(default=False)    #Indica si el incidente es una Prueba

    
# ===========================================================
# PROCEDIMIENTOS DE CONTINGENCIA EN DESARROLLO / ACTUALIZACION
# ===========================================================

class Procedimientos(models.Model):
    """
    Registro de Procedimientos de Contingencia en Desarrollo / Actualizacion 
    """

    codigo = models.CharField(max_length= 25, blank=False, default='0000')
    pk_padre = models.IntegerField(default=0)

    #Fechas
    fecha_c=models.DateField(auto_now_add=True)
    fecha_ult_mod =models.DateField(auto_now_add=True)

    #Identificacion del Procedimiento
    nombre = models.CharField(max_length= 100, blank=False)
    tipo = models.ForeignKey('Tipo_Proc', on_delete=models.SET_NULL, null=True)

    #Contexto
    #escenarios = models.ManyToManyField('Escenarios')
    escenarios = models.ForeignKey(Escenarios, on_delete=models.SET_NULL, related_name='escenarios_en_procedimiento', null=True)
    estrategia = models.CharField(max_length= 400, blank=False)

    #Responsables
    resp_proceso = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='resp_proceso', null=True)
    bck_resp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_resp', null=True, blank=True)

    gestor_ejecutor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_ejecutor', null=True)
    bck_ejecutor  = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_ejecutor', null=True, blank=True)

    enlace_c_crisis = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='enlace_c_crisis',  null=True)
    bck_enlace = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_enlace', null=True, blank=True)

    gestor_consultor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_consultor', null=True)

    #Servicios y Contactos necesarios                                       
    servicios_pc = models.ManyToManyField('Servicios_PC')
    contactos_pc = models.ManyToManyField('Contactos_PC')


    #Pasos del Procedimiento
    pasos = models.ManyToManyField('Pasos_PC')


    PROCED_STATUS = (
        ('R', 'Vigenteado'),
        ('r', 'X Vigentear R'),
        ('A', 'Aprobado'),   # Aprobado por Gestor Ejecutor.
        ('a', 'x Aprobar A'),
        ('C', 'En Dfncn C'),
        ('x', 'En Revision C'), 
        
    )
    status = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C', help_text='Estado de la definicion del Proceso')

    existe_p_vigente=models.BooleanField(default=False)  # Marca para verificar si tiene un Procedimiento vigente

    #Log de Autorizaciones
    log_auth=models.ManyToManyField('LogAut')
    es_borrable=models.BooleanField(default=True) # Indica que el Procedimiento es Borrable
    corr_prbas=models.IntegerField(default=1)     # Correlativo de Pruebas de Procedimiento


# ===========================================================
# PROCEDIMIENTOS DE CONTINGENCIA VIGENTES
# ===========================================================

class Procedimientos_V(models.Model):
    """
    Registro de Procedimientos de Contingencia Autorizados Vigentes
    """

    subproceso=models.ForeignKey('SubProceso_V', on_delete=models.SET_NULL, null=True)
    codigo = models.CharField(max_length= 25, blank=False, default='0000')
    pk_padre = models.IntegerField(default=0) 
    version  = models.IntegerField(default=0)

    #Fechas
    fecha_c=models.DateField(auto_now_add=True)        # Fecha de Autorizacion
    fecha_ult_mod =models.DateField(auto_now_add=True) 

    #Identificacion del Procedimiento
    nombre = models.CharField(max_length= 100, blank=False)
    tipo = models.ForeignKey('Tipo_Proc', on_delete=models.SET_NULL, null=True)

    #Contexto
    #escenarios = models.ManyToManyField('Escenarios')
    escenarios = models.ForeignKey(Escenarios, on_delete=models.SET_NULL, related_name='escenarios_en_procedimiento_v', null=True)
    estrategia = models.CharField(max_length= 400, blank=False)

    #Responsables
    resp_proceso = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='resp_proceso_v', null=True)
    bck_resp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_resp_v', null=True, blank=True)

    gestor_ejecutor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_ejecutor_v', null=True)
    bck_ejecutor  = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_ejecutor_v', null=True, blank=True)

    enlace_c_crisis = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='enlace_c_crisis_v',  null=True)
    bck_enlace = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_enlace_v', null=True, blank=True)

    gestor_consultor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_consultor_v', null=True)

    #Servicios y Contactos necesarios                                       
    servicios_pc = models.ManyToManyField('Servicios_PC_V')
    contactos_pc = models.ManyToManyField('Contactos_PC_V')

    #Pasos del Procedimiento
    pasos = models.ManyToManyField('Pasos_PC_V')

    #Estados del Procedimiento y Archivo adjunto durante Contingencia                                           
    esta_activo=models.BooleanField(default=False)     # Activado por Comite de Crisis
    esta_confirmado=models.BooleanField(default=False) # Confirmado por Gestor Ejecutor
    archivo = models.FileField(upload_to="archivos/", null=True, blank=True)


    #Log de Autorizaciones
    log_auth=models.ManyToManyField('LogAut')

    correlativo_chk = models.IntegerField(default=0) # Correlativo de Checklist


class Servicios_PC(models.Model):
    """
    Servicios necesarios para el Procedimiento de Contingencia
    """
    pk_padre = models.IntegerField(default=0)
    nombre = models.CharField(max_length= 200, blank=False)
    objetivo = models.CharField(max_length= 400, blank=False)
    contacto = models.CharField(max_length= 50, blank=False)
    contacto_bck = models.CharField(max_length= 50, blank=True)


class Servicios_PC_V(models.Model):
    """
    Servicios necesarios para el Procedimiento de Contingencia
    """
    pk_padre = models.IntegerField(default=0)
    nombre = models.CharField(max_length= 200, blank=False)
    objetivo = models.CharField(max_length= 400, blank=False)
    contacto = models.CharField(max_length= 50, blank=False)
    contacto_bck = models.CharField(max_length= 50, blank=True)


class Contactos_PC(models.Model):
    """
    Datos de contacto necesarios para el Procedimiento de Contingencia
    """
    pk_padre = models.IntegerField(default=0)
    cont_int = models.CharField(max_length= 20, blank=True)
    nombre = models.CharField(max_length= 200, blank=True)
    correo = models.CharField(max_length= 50, blank=True)
    tel_lab = models.CharField(max_length= 30, blank=True)
    cel_lab = models.CharField(max_length= 30, blank=True)
    
class Contactos_PC_V(models.Model):
    """
    Datos de contacto necesarios para el Procedimiento de Contingencia
    """
    pk_padre = models.IntegerField(default=0)
    cont_int = models.CharField(max_length= 20, blank=True)
    nombre = models.CharField(max_length= 200, blank=True)
    correo = models.CharField(max_length= 50, blank=True)
    tel_lab = models.CharField(max_length= 30, blank=True)
    cel_lab = models.CharField(max_length= 30, blank=True)

class Pasos_PC(models.Model):
    """
    Pasos del Procedimiento de Contingencia
    """
    pk_padre = models.IntegerField(default=0)
    nro_paso = models.IntegerField(default=0)
    descripcion = models.CharField(max_length= 500, blank=False)
    ejecutor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, null=True)
    tiempo_esp = models.IntegerField(default=0)


    class Meta:
        ordering = ["nro_paso"]

class Pasos_PC_V(models.Model):
    """
    Pasos del Procedimiento de Contingencia
    """
    pk_padre = models.IntegerField(default=0)
    nro_paso = models.IntegerField(default=0)
    descripcion = models.CharField(max_length= 500, blank=False)
    ejecutor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, null=True)
    tiempo_esp = models.IntegerField(default=0)

    class Meta:
        ordering = ["nro_paso"]    


# ===========================================================
#  REGISTRO DE EJECUCION DE PROCEDIMIENTO DE CONTINGENCIA
# ===========================================================


class CheckList(models.Model):
    """
    Checklist de ejecucion de Procedimiento de Contingencia
    """
    nro_chk = models.CharField(max_length= 5, blank=False, default='0000')
    incidente=models.ForeignKey(Incidentes, on_delete=models.SET_NULL, null=True)
    procedimiento = models.ForeignKey(Procedimientos_V, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # NOTA: Para fecha de actualizacion : fecha_modificacion = models.DateTimeField(auto_now=True)
    completado=models.BooleanField(default=False)  # Indica que el Checklist se ha completado

    class Meta:
        ordering = ["-nro_chk"]    
    
    
class Check_Pasos(models.Model):

    checklist=models.ForeignKey(CheckList, on_delete=models.SET_NULL, null=True)

    paso=models.ForeignKey(Pasos_PC_V, on_delete=models.SET_NULL, null=True)
    comentario = models.CharField(max_length= 400, blank=True)
    terminado=models.BooleanField(default=False)  # Indica que el Item (paso) fue ejecutado
    fecha_ter=models.DateTimeField(default=timezone.now)



# ===========================================================
# 1. PRUEBA DE CONTINGENCIA (PLANIFICACIÓN)
# ===========================================================
class PruebaContingencia(models.Model):
    """
    Representa la planificación de una prueba de contingencia
    asociada a un Procedimiento de Contingencia.
    El Proceso y Escenario se derivan del Procedimiento.
    """
    procedimiento = models.ForeignKey(
        Procedimientos, on_delete=models.CASCADE, related_name='procedimientos_des', null=True
    )
    codigo = models.CharField(max_length=255)  #Nombre Procedimiento + codigo asignado x Sist.
    objetivo = models.TextField()
    alcance = models.TextField(blank=True, null=True)
    criterios_exito = models.TextField(blank=True, null=True)
    fecha_programada = models.DateTimeField(default=timezone.now)
    responsable = models.ForeignKey('Gestor', on_delete=models.SET_NULL, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En ejecución', 'En ejecución'),
            ('Completada', 'Completada'),
        ],
        default='Pendiente',
    )
    corr_casos=models.IntegerField(default=0)


    class Meta:
        verbose_name = "Prueba de Contingencia"
        verbose_name_plural = "Pruebas de Contingencia"
        ordering = ['fecha_programada']

    #def __str__(self):
    #    return f"{self.codigo} ({self.fecha_programada})"

    # --- Propiedades derivadas ---
    @property
    def proceso(self):
        """Acceso directo al Proceso asociado al Procedimiento."""
        return self.procedimiento.proceso

    @property
    def escenario(self):
        """Acceso directo al Escenario de Riesgo asociado al Procedimiento."""
        return self.procedimiento.escenario


class PruebaContingencia_V(models.Model):
    """
    Representa la planificación de una prueba de contingencia
    asociada a un Procedimiento de Contingencia VIGENTE.
    El Proceso y Escenario se derivan del Procedimiento.
    """
    procedimiento = models.ForeignKey(
        Procedimientos_V, on_delete=models.CASCADE, related_name='procedimientos_vigente', null=True
    )
    codigo = models.CharField(max_length=255)  #Nombre Procedimiento + codigo asignado x Sist.
    objetivo = models.TextField()
    alcance = models.TextField(blank=True, null=True)
    criterios_exito = models.TextField(blank=True, null=True)
    fecha_programada = models.DateTimeField(default=timezone.now)
    responsable = models.ForeignKey('Gestor', on_delete=models.SET_NULL, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En ejecución', 'En ejecución'),
            ('Completada', 'Completada'),
        ],
        default='Pendiente',
    )
    corr_casos=models.IntegerField(default=0)


    class Meta:
        verbose_name = "Prueba de Contingencia"
        verbose_name_plural = "Pruebas de Contingencia"
        ordering = ['fecha_programada']

    #def __str__(self):
    #    return f"{self.codigo} ({self.fecha_programada})"

    # --- Propiedades derivadas ---
    @property
    def proceso(self):
        """Acceso directo al Proceso asociado al Procedimiento."""
        return self.procedimiento.proceso

    @property
    def escenario(self):
        """Acceso directo al Escenario de Riesgo asociado al Procedimiento."""
        return self.procedimiento.escenario


# ===========================================================
# 2. CASO DE PRUEBA
# ===========================================================
class CasoPrueba(models.Model):
    """
    Define los casos o escenarios específicos dentro de una prueba de contingencia.
    Ejemplo: Caso 1 = ingresar compra por $1000; Caso 2 = ingresar compra por $5000.
    """
    prueba = models.ForeignKey(
        PruebaContingencia, on_delete=models.CASCADE, related_name='prueba_des'
    )
    #numero = models.PositiveIntegerField()
    codigo = models.CharField(max_length=4, default='0000')
    descripcion = models.TextField()
    resultado_esperado = models.TextField()
    precondiciones = models.TextField(blank=True, null=True)
    prioridad = models.CharField(
        max_length=10,
        choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')],
        default='Media'
    )

    class Meta:
        verbose_name = "Caso de Prueba"
        verbose_name_plural = "Casos de Prueba"
        ordering = ['prueba', 'codigo']
        unique_together = ('prueba', 'codigo')

    #def __str__(self):
    #    return f"Caso {self.codigo} - {self.prueba.nombre}"

class CasoPrueba_V(models.Model):
    """
    Define los casos o escenarios específicos dentro de una prueba de contingencia.
    Ejemplo: Caso 1 = ingresar compra por $1000; Caso 2 = ingresar compra por $5000.
    """
    prueba = models.ForeignKey(
        PruebaContingencia_V, on_delete=models.CASCADE, related_name='prueba_vigente'
    )
    #numero = models.PositiveIntegerField()
    codigo = models.CharField(max_length=4, default='0000')
    descripcion = models.TextField()
    resultado_esperado = models.TextField()
    precondiciones = models.TextField(blank=True, null=True)
    prioridad = models.CharField(
        max_length=10,
        choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')],
        default='Media'
    )

    class Meta:
        verbose_name = "Caso de Prueba"
        verbose_name_plural = "Casos de Prueba"
        ordering = ['prueba', 'codigo']
        unique_together = ('prueba', 'codigo')

    #def __str__(self):
    #    return f"Caso {self.codigo} - {self.prueba.nombre}"


# ===========================================================
# 3. EJECUCIÓN DE PRUEBA
# ===========================================================
class EjecucionPrueba(models.Model):
    """
    Registra el Checklist de la Ejecucion de  una Prueba de PC vigente.
    Puede haber múltiples ejecuciones por cada prueba.
    Cada ejecucion esta asociada a un Incidente de tipo Prueba
    """
    nro_ejecucion = models.CharField(max_length= 5, blank=False, default='0000')

    # Relaciones otros modelos
    incidente=models.ForeignKey(Incidentes, on_delete=models.SET_NULL, null=True)
    prueba = models.ForeignKey(
        PruebaContingencia_V, on_delete=models.CASCADE, related_name='ejecuciones'
    )
    checklist=models.ForeignKey(CheckList, on_delete=models.SET_NULL, null=True)
    fecha_real = models.DateTimeField(null=True, blank=True)

    # Datos 

    incidentes = models.TextField(blank=True, null=True)
    descripcion_ejecucion = models.TextField()
    resultados_obtenidos = models.TextField(blank=True, null=True)
    evaluacion_final = models.CharField(
        max_length=20,
        choices=[
            ('Exitosa', 'Exitosa'),
            ('Parcial', 'Parcial'),
            ('Fallida', 'Fallida'),
            ('En Ejecucion', 'En Ejecucion'),
        ],
        blank=True,
        null=True,
        default='En Ejecucion'
    )
    lecciones_aprendidas = models.TextField(blank=True, null=True)
    evidencia_general = models.FileField(upload_to='evidencias_pruebas/', blank=True, null=True)

    class Meta:
        verbose_name = "Ejecución de Prueba"
        verbose_name_plural = "Ejecuciones de Pruebas"
        ordering = ['-fecha_real']

    #def __str__(self):
    #    return f"Ejecución #{self.id} - {self.prueba.nombre}"


# ===========================================================
# 4. EJECUCIÓN DE CASO DE PRUEBA
# ===========================================================
class EjecucionCasoPrueba(models.Model):
    """
    Registra los resultados individuales de cada caso dentro de una ejecución de prueba.
    Permite trazabilidad detallada y almacenamiento de evidencias.
    """
    nro_ejecucion = models.CharField(max_length= 7, blank=False, default='0000')
    ejecucion = models.ForeignKey(
        EjecucionPrueba, on_delete=models.CASCADE, related_name='casos_ejecutados'
    )
    caso = models.ForeignKey(
        CasoPrueba_V, on_delete=models.CASCADE, related_name='ejecuciones'
    )

    
    resultado = models.CharField(
        max_length=20,
        choices=[
            ('Exitosa', 'Exitosa'),
            ('Fallida', 'Fallida'),
            ('Parcial', 'Parcial'),
            ('En Proceso', 'En Proceso'),
            ('No Aplica', 'No Aplica'),
        ],
        default='En Proceso',
        blank=True,
        null=True
    )
    
    observaciones = models.TextField(blank=True, null=True)
    evidencia = models.FileField(upload_to='evidencias_casos/', blank=True, null=True)



    class Meta:
        verbose_name = "Ejecución de Caso de Prueba"
        verbose_name_plural = "Ejecuciones de Casos de Prueba"
        unique_together = ('ejecucion', 'caso')

    #def __str__(self):
    #    return f"{self.caso} / Ejecución {self.ejecucion.id}"





    
class Tipo_Proc(models.Model):
    """
    Define tipo de Procedimiento
    """

    nombre = models.CharField(max_length= 10, blank=True)
    descripcion = models.CharField(max_length= 50, blank=True)
    
     
    def __str__(self):
        return self.nombre+' / '+self.descripcion

    
class Area(models.Model):
    """
    Areas de la Organizacion
    """

    nivel  = models.CharField(max_length= 100, blank=False)
    nombre = models.CharField(max_length= 50, blank=False)

    def __str__(self):
        return self.nivel+' / '+self.nombre


class Cod_Area(models.Model):
    """
    Codigo de Area Celular
    """

    codigo = models.CharField(max_length= 5,  blank=True)
    ciudad = models.CharField(max_length= 50, blank=True)
    pais = models.CharField(max_length= 50, blank=True)

    def __str__(self):
        return self.codigo+' / '+self.pais+'/'+self.ciudad

class Grupos(models.Model):
    """
    Datos complementarios del Grupo
    """

    grupo       = models.OneToOneField(Group, on_delete=models.DO_NOTHING, blank=True, null=True)
    descripcion = models.CharField(max_length= 100, blank=True)

    def __str__(self):
        return self.grupo.name+ ' / '+ self.descripcion


# ===========================================================
# DRP
# ===========================================================


class Drp(models.Model):
    """
    Datos del DRP en Desarrollo / Actualizacion 
    """

    codigo  = models.CharField(max_length= 8, blank=False, default='0000')
    
    #Fechas
    fecha_c=models.DateField(auto_now_add=True)
    fecha_ult_mod =models.DateField(auto_now_add=True)

    #Identificacion del DRP
    nombre = models.CharField(max_length= 100, blank=False)
    introduccion = models.CharField(max_length= 2000, blank=True)

    #Responsables
    resp_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='resp_drp', null=True, blank=True)
    bck_resp_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_resp_drp', null=True, blank=True)

    gestor_ejecutor_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_ejecutor_drp', null=True)
    bck_ejecutor_drp  = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_ejecutor_drp', null=True)

    enlace_c_crisis_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='enlace_c_crisis_drp',  null=True)
    bck_enlace_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_enlace_drp', null=True)

    gestor_consultor_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_consultor_drp', null=True)

    #Servicios y Contactos necesarios                                       
    servicios_drp = models.ManyToManyField('Servicios_PC')
    contactos_drp = models.ManyToManyField('Contactos_PC')

    #Pasos del DRP
    pasos_drp = models.ManyToManyField('Pasos_PC')

 
    #Estado del Procedimiento y Archivo adjunto                                            
    esta_activo=models.BooleanField(default=False)
    modo_test=models.BooleanField(default=False)
    #archivo = models.FileField(upload_to="archivos/", null=True, blank=True)

    
    PROCED_STATUS = (
        ('R', 'Vigenteado'),
        ('r', 'X Vigentear R'),
        ('A', 'Aprobado'),
        ('a', 'x Aprobar A'),
        ('C', 'En Dfncn C'),
        ('x', 'En Revision C'), 
        
    )
    status_1 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C') 
    status_2 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_3 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_4 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_5 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_6 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_7 = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_A = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C')
    status_t = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True)


    # Log de Autorizaciones
    log_auth_drp=models.ManyToManyField('LogAut')

    #Alcance

    procesos_drp=models.ManyToManyField('SubProceso_V')

    # Estrategia de Recuperacion

    tipo_Site = models.ForeignKey('Tipo_Site', on_delete=models.SET_NULL, related_name='tipo_site', null=True)
    desc_estrategia = models.CharField(max_length= 1000, blank=True)
    disposicion_componentes=models.ForeignKey('Tipo_Disp', on_delete=models.SET_NULL, related_name='tipo_disp', null=True)

    # Especificacion Tecnica (Componentes Sw/Hw del DRP)

    componentes=models.ManyToManyField('Componentes')

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular 
        """
        return reverse('Indice-DRP', args=[str(self.id)])


class Drp_V(models.Model):
    """
    Datos del DRP Aprobado Vigente 
    """

    codigo  = models.CharField(max_length= 8, blank=False, default='0000')
    version = models.CharField(max_length= 5, blank=False, default='0000')
    
    #Fechas
    fecha_c=models.DateField(auto_now_add=True)
    fecha_auth = models.DateField(auto_now_add=True)

    #Identificacion del DRP
    nombre = models.CharField(max_length= 100, blank=False)
    introduccion = models.CharField(max_length= 2000, blank=True)

    #Responsables
    resp_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='resp_drp_v', null=True, blank=True)
    bck_resp_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_resp_drp_v', null=True, blank=True)

    gestor_ejecutor_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_ejecutor_drp_v', null=True)
    bck_ejecutor_drp  = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_ejecutor_drp_v', null=True)

    enlace_c_crisis_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='enlace_c_crisis_drp_v',  null=True)
    bck_enlace_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_enlace_drp_v', null=True)

    gestor_consultor_drp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_consultor_drp_v', null=True)

    #Servicios y Contactos necesarios                                       
    servicios_drp = models.ManyToManyField('Servicios_PC')
    contactos_drp = models.ManyToManyField('Contactos_PC')

    #Pasos del DRP
    pasos_drp = models.ManyToManyField('Pasos_PC')

 
    #Estados del Procedimiento y Archivo adjunto durante Contingencia                                           
    esta_activo=models.BooleanField(default=False)     # Activado por Comite de Crisis
    esta_confirmado=models.BooleanField(default=False) # Confirmado por Gestor Ejecutor
    archivo = models.FileField(upload_to="archivos/", null=True, blank=True)
    
    #Alcance

    procesos_drp=models.ManyToManyField('SubProceso_V')

    # Estrategia de Recuperacion

    tipo_Site = models.ForeignKey('Tipo_Site', on_delete=models.SET_NULL, related_name='tipo_site_v', null=True)
    desc_estrategia = models.CharField(max_length= 1000, blank=True)
    disposicion_componentes=models.ForeignKey('Tipo_Disp', on_delete=models.SET_NULL, related_name='tipo_disp_v', null=True)

    # Especificacion Tecnica (Componentes Sw/Hw del DRP)

    componentes=models.ManyToManyField('Componentes')

    # Log de Autorizaciones
    log_auth_drp=models.ManyToManyField('LogAut')


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular 
        """
        return reverse('Indice-DRP', args=[str(self.id)])


class Tipo_Site(models.Model):
    """
    Registra los Tipos de Sites para el DRP
    
    """
    nombre=models.CharField(max_length=50,  blank=True)
    resumen=models.CharField(max_length=60, blank=True)
    descripcion=models.CharField(max_length=250, blank=True)

    def __str__(self):
        
        return self.nombre+':'+self.resumen
    
class Tipo_Disp(models.Model):
    """
    Registra los Tipos de Disposicion de los Sites involucrados
    en el DRP
    """

    nombre=models.CharField(max_length=50,  blank=True)
    resumen=models.CharField(max_length=60, blank=True)
    descripcion=models.CharField(max_length=250, blank=True)

    def __str__(self):
        
        return self.nombre+':'+self.resumen

class Componentes(models.Model):
    """
    Registra los Componentes de la Infraestructura del 
    Site de Contingencias """

    codigo=models.CharField(max_length=12,  blank=True)
    tipo_act=models.ForeignKey('Tipo_Componente', on_delete=models.SET_NULL, related_name='tipo_disp', null=True)
    nombre=models.CharField(max_length=100,  blank=True)
    descripcion=models.CharField(max_length=100, blank=True)
 
    identificacion=models.CharField(max_length=30,  blank=True) # Nro. del fabricante, nro. licencia, nro. de serie, etc.
    fabricante= models.CharField(max_length=30,  blank=True)
    codigo_inv =models.CharField(max_length=20,  blank=True) # Codigo de Inventario asignado


    lbc=models.ManyToManyField('LBC')  # Linea Base de Configuracion

    url= models.SlugField(max_length = 200, blank=True) 

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular 
        """
        return reverse('Lista-CMP', args=[str(self.id)])
    
    #def __str__(self):
        
        #return self.tipo_act+':'+self.codigo+':'+self.nombre+':'+self.descripcion


class Tipo_Componente(models.Model):

    tipo=models.CharField(max_length=50,  blank=True)
    descripcion=models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        
        return self.tipo+':'+self.descripcion   

class LBC(models.Model):
    """
    Registra la Linea Base de Configuracion por Componente. """ 

    codigo = models.CharField(max_length=20,  blank=True)
    nombre =models.CharField(max_length=100,  blank=True)        #Nombre del Parametro
    descripcion=models.CharField(max_length=300,  blank=True)
    metodo_acceso=models.CharField(max_length=300,  blank=True)
    valor=models.CharField(max_length=50,  blank=True) 
    

class Log_Revision(models.Model):
    """
    Comentarios de Revision de Auditoria y  Objetivos de Control
    """
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    proceso= models.ForeignKey(Proceso, on_delete=models.CASCADE, null=True)
    procedimiento= models.ForeignKey(Procedimientos, on_delete=models.CASCADE, null=True)
    procedimiento_v= models.ForeignKey(Procedimientos_V, on_delete=models.CASCADE, null=True)
    drp= models.ForeignKey(Drp, on_delete=models.CASCADE, null=True)

    gestor_aut = models.ForeignKey(Gestor, on_delete=models.CASCADE, null=True)
    seccion=models.CharField(max_length=2, blank=True)
                                                        # seccion = 
                                                        #    ('M', 'Fase Procesos'),
                                                        #    ('V', 'Fase BIA'),
                                                        #    ('B', 'Fase Activos'),
                                                        #    ('E', 'Fase Escenarios'),
                                                        #    ('P', 'Fase PC' )
 
    campo= models.CharField(max_length=200, blank=True)  # Referencia al Nombre del Campo al que se hace referencia
    comentario = models.TextField()
    #obj_ries = models.ForeignKey(Obj_Ries, on_delete=models.CASCADE, null=True, related_name="comentarios")
    resuelto=models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ["-fecha", "-hora"]


