#Modelo de Datos Modelo bcp del Sistema Defcon5.

from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User, Group
from datetime import date

#====================================
# ENTIDADES o MODELOS
#====================================

   
class Proceso(models.Model):
    """
    Entidad: Proceso
             Registra los atributos del Proceso a ser considerado por el bcp
    """

    
    path= models.CharField(max_length=200, blank=True)
    proceso_padre = models.CharField(max_length=10, blank=True)
    pk_padre = models.IntegerField(default=0)
    ni= models.CharField(max_length=20, blank=True) 
    proceso = models.CharField(max_length=10, blank=True)
    nro_hijos = models.IntegerField()
    nombre = models.CharField(max_length=50)
    objetivo = models.TextField(max_length=500, blank=True, help_text='Describa el principal objetivo del Proceso')
    fecha_crea = models.DateField(null=True, default=date.today(), blank=True)
    fecha_ult_mod = models.DateField(null=True, blank=True)


    #Registra el Tipo 
    es_subproceso=models.BooleanField(default=False)
    
    subproceso = models.OneToOneField('SubProceso', on_delete=models.CASCADE, blank=True, null=True)


    log_auth=models.ManyToManyField('LogAut', blank=True, null=True)
    

    
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

    pk_padre = models.IntegerField(default=0)
    codigo = models.CharField(max_length=10, blank=True)
    path=models.CharField(max_length=200, blank=True)
    
    #Campos para implementar un modelo RACI
    gestor_R = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_r', null=True, blank=True)
    gestor_A = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_a', null=True, blank=True)
    gestor_C = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_c', null=True, blank=True)
    gestor_I = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='subproceso_i', null=True, blank=True)

    #Campos para impactos e indicadores de Contingencia.

    #Impactos

    impacto_1 = models.ForeignKey('Nivel_Impacto', on_delete=models.SET_NULL, related_name='impacto_1', null=True, blank=True)
    impacto_2 = models.ForeignKey('Nivel_Impacto', on_delete=models.SET_NULL, related_name='impacto_2', null=True, blank=True)
    impacto_3 = models.ForeignKey('Nivel_Impacto', on_delete=models.SET_NULL, related_name='impacto_3', null=True, blank=True)
    impacto_4 = models.ForeignKey('Nivel_Impacto', on_delete=models.SET_NULL, related_name='impacto_4', null=True, blank=True)
    
    rto = models.ForeignKey('Indicadores_BIA', on_delete=models.SET_NULL, related_name='RTO', null=True, blank=True)
    rpo = models.ForeignKey('Indicadores_BIA', on_delete=models.SET_NULL, related_name='RPO', null=True, blank=True)
    mtd = models.ForeignKey('Indicadores_BIA', on_delete=models.SET_NULL, related_name='MTD', null=True, blank=True)


    ranking =  models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    
    #Registra el estado 
    PROC_STATUS = (
        ('R', 'Vigenteado'),
        ('r', 'X Vigentear R'),
        ('A', 'X Aprobar A'),
        ('C', 'En Dfncn C'),
        ('x', 'En Revision C'), 
        
    )
    #Registra la Fase en el desarrollo del  bcp
    FASE_STATUS = (
        ('M', 'Fase Procesos'),
        ('V', 'Fase BIA'),
        ('B', 'Fase Activos'),
        ('E', 'Fase Escenarios'),
        
                
    )

    status = models.CharField(max_length=1, choices=PROC_STATUS, blank=True, default='C', help_text='Estado de la definicion del Proceso')
    fase_status = models.CharField(max_length=1, choices=FASE_STATUS, blank=True, default='M', help_text='Fase del bcp')

    recursos=models.ManyToManyField('Recursos', blank=False, null=False)
    escenarios=models.ManyToManyField('Escenarios', blank=False, null=False)

    procedimientos_contingencia = models.ManyToManyField('Procedimientos',  blank=True, null=True)
    nro_prdto = models.IntegerField(default=0)
    


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



class LogAut(models.Model):
    """
    Entidad:    Log de Autorizaciones.
                Registra las Autorizaciones dadas al Proceso durante
                las distintas fases de definicion.     
    """

    cod_proceso = models.CharField(max_length=10, blank=True)
    gestor_aprobador= models.ForeignKey('Gestor', on_delete=models.SET_NULL, null=True)
    p_status=models.CharField(max_length=2, blank=True)
    fecha=models.DateField(null=True, default=date.today(), blank=True)
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
        return '['+self.tipo.nombre+'].:'+self.nombre+':{'+self.descripcion+'}'



class Tipo_RR(models.Model):
    """
    Entidad:    Tipos de Recursos
    """

    nombre= models.CharField(max_length=25, blank=True)
    descripcion=models.TextField(max_length=200, blank=True, help_text='Describa el Recurso')


    def __str__(self):
        return self.nombre+' / '+self.descripcion



class Gestor(models.Model):
    """
    Entidad: Gestor
            Registra los atributos de un gestor del Sistema
    """

    user_pk = models.IntegerField(null=True)
    user_gestor = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    #user_grupos = models.ManyToManyField(Group) No se puede hacer esta definicion!!
    
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
    amenazas = models.ManyToManyField('Amenazas')
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
    Define indicadores RTO, RPO, MTD
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
    Define tipo de indicadores RTO, RPO, MTD
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


    def defcon_est(self):

        parametro_g = get_object_or_404(Parametros_G , pk=1)
        self.defcon_est = parametro_g.valor_2 

        return self.defcon_est 

class Incidentes(models.Model):
    """
    Registro del Incidente
    """

    codigo = models.CharField(max_length= 100, blank=True)
    fecha=models.DateField(null=True, default=date.today(), blank=True)

    nombre_r  = models.CharField(max_length= 25, blank=True)
    area_r = models.CharField(max_length= 25, blank=True)
    correo = models.EmailField(max_length = 254, blank=True)
    
    descripcion = models.CharField(max_length= 500, blank=True)

    amenazas_i = models.ManyToManyField('Amenazas', null=False, blank=False)
    procesos_i = models.ManyToManyField('SubProceso')
    escenarios_i = models.ManyToManyField('Escenarios')
    

class Procedimientos(models.Model):
    """
    Registro de Procedimientos de Contingencia
    """

    codigo = models.CharField(max_length= 25, blank=False, default='0000')
    pk_padre = models.IntegerField(default=0)

    #Fechas
    fecha_c=models.DateField(null=True, default=date.today(), blank=True)
    fecha_ult_mod =models.DateField(null=True, default=date.today(), blank=True)

    #Identificacion del Procedimiento
    nombre = models.CharField(max_length= 100, blank=False)
    tipo = models.ForeignKey('Tipo_Proc', on_delete=models.SET_NULL, null=True)
    version = models.CharField(max_length= 5, blank=False, default='00.00')

    #Contexto
    #escenarios = models.ManyToManyField('Escenarios')
    escenarios = models.CharField(max_length= 400, blank=False)
    estrategia = models.CharField(max_length= 400, blank=False)

    #Responsables
    resp_proceso = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='resp_proceso', null=True)
    bck_resp = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_resp', null=True)

    gestor_ejecutor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_ejecutor', null=True)
    bck_ejecutor  = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_ejecutor', null=True)

    enlace_c_crisis = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='enlace_c_crisis',  null=True)
    bck_enlace = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='bck_enlace', null=True)

    gestor_consultor = models.ForeignKey('Gestor', on_delete=models.SET_NULL, related_name='gestor_consultor', null=True)

    #Servicios y Contactos necesarios                                       
    servicios_pc = models.ManyToManyField('Servicios_PC')
    contactos_pc = models.ManyToManyField('Contactos_PC')


    #Pasos del Procedimiento
    pasos = models.ManyToManyField('Pasos_PC')


    #Marcadores para verificar completitud del ingreso de datos Servicios, Contactos y Pasos del Procedimiento
    sec_1_completa = models.BooleanField(default=False)
    sec_servicios  = models.IntegerField(default=0)
    sec_contactos  = models.IntegerField(default=0)
    sec_pasos      = models.IntegerField(default=0)



    #Estado del Procedimiento y Archivo adjunto                                            
    esta_activo=models.BooleanField(default=False)
    archivo = models.FileField(upload_to="archivos/", null=True, blank=True)


    PROCED_STATUS = (
        ('R', 'Vigenteado'),
        ('r', 'X Vigentear R'),
        ('A', 'X Aprobar A'),
        ('a', 'x Aprobar A'),
        ('C', 'En Dfncn C'),
        ('x', 'En Revision C'), 
        
    )
    status = models.CharField(max_length=1, choices=PROCED_STATUS, blank=True, default='C', help_text='Estado de la definicion del Proceso')


    #Log de Autorizaciones
    log_auth=models.ManyToManyField('LogAut')
    
    
class Servicios_PC(models.Model):
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


class Drp(models.Model):
    """
    Datos del DRP
    """

    codigo  = models.CharField(max_length= 8, blank=False, default='0000')
    version = models.CharField(max_length= 5, blank=False, default='0000')
    
    #Fechas
    fecha_c=models.DateField(null=True, default=date.today(), blank=True)
    fecha_ult_mod =models.DateField(null=True, default=date.today(), blank=True)

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

    procesos_drp=models.ManyToManyField('SubProceso')

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

    lbc=models.ManyToManyField('LBC')  # Linea Base de Configuracion

    url= models.SlugField(max_length = 200, blank=True) 

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular 
        """
        return reverse('Lista-CMP', args=[str(self.id)])
    
    def __str__(self):
        
        return self.tipo_act.tipo+':'+self.codigo+':'+self.nombre+':'+self.descripcion


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
    

