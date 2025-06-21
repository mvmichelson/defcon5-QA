#Sistema  defcon5
#Definicion de Links urls
#Programado por Marco A. Villalobos Michelson
#=============================================

from django.urls import re_path as url
from django.urls import path

from . import views

from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [

    # Redirigir raíz a bcp
    #path('', RedirectView.as_view(url='/bcp/', permanent=False)),

    # Admin (Obviar si ya esta en Url principal)
    #path('admin/', admin.site.urls),

    # Pagina Principal y utilidades
    path('', views.index, name='index'),         # Pagina Principal
    path('reinicia/', views.reset, name='reinicia_bd'),     # Reinicia la Base de Datos

    path('get_chart/', views.get_chart, name='get_chart'),
    #url(r'^$', views.Base_GenericPageView.as_view(), name='base_generic'),
    path('mensajes/', views.En_Construccion, name='En-Construccion'),

    #url(r'^request.META['HTTP_REFERER']', name='volver'),

    # Diagramas Metodologicos
    # -----------------------
    path('mapeo/', views.Mapeo, name='Mapeo'),            # Diagrama Metodologia bcp/DRP
    path('ria/mapa/', views.Mapa_RIA, name='Mapa-RIA'),    # Diagrama Metodologia RIA

   
    #url(r'^procesos/$', views.ProcesoListView.as_view(), name='Lista-Procesos'),
    #url(r'^proceso/(?P<pk>[-\w]+)/renew/$', views.crea_proceso.as_view(), name='Crea-Procesos'),

]

# Creacion y Aprobacion de Procesos
# ---------------------------------
urlpatterns += [
    path('procesos/', views.Lista_Procesos, name='Lista-Procesos'),
    #url(r'^procesos/$', views.Lista_Procesos, name='Lista-Procesos'),
    #url(r'^proceso/(?P<pk>\d+)$', views.ProcesoDetailView.as_view(), name='Detalle-Procesos'),
    path('proceso/<int:pk>/detalle_proceso/', views.Detalle_Proceso, name='Detalle-Proceso'),
    path('proceso/<int:pk>/det_proceso_v/', views.Detalle_Proceso_V, name='Detalle-Proceso-V'),
    path('proceso/<slug:pk>/crea_p/', views.crea_proceso, name='crea-procesos'),

    path('proceso/<slug:pk>/act_p/', views.Actualiza_Mapeo, name='actualiza-mapeo'),

    path('proceso/<slug:pk>/borra_p/', views.borra_proceso, name='borra-procesos'),
    path('proceso/<slug:pk>/auth_raci/', views.Autoriza_M, name='auth_m-raci'),
    path('proceso/<slug:pk>/revisa_proceso/', views.Revisa_Proceso, name='proceso-revisa'),
    path('proceso/<slug:pk>/borra_obs/', views.borra_obs_proceso, name='borra-obs-proceso'),
    url(r'^proceso/(?P<item>[\w-]+)/(?P<pk>\d+)/(?P<valor>[\w-]+)/$', views.aut_obs_proceso, name='obs-proceso'),
    #url(r'^proceso/(?P<pk>\d+)/revisa_auth/$', views.LogAutRevListView.as_view(), name='revisa-auth'),

]


# Evaluaciones BIA a Procesos
# ---------------------------
urlpatterns += [
    #url(r'^map_eval/$', views.Map_evalListView.as_view(), name='Mapeo-Evaluaciones'),

    path('map_eval/', views.Lista_Evaluaciones, name='Lista-Evaluaciones'),
    path('map_eval/<int:pk>/asig_eval/', views.Asigna_Imp_Ind, name='Asigna-Evaluacion'),
    path('map_eval/<int:pk>/aut_asig_eval/', views.Aut_Asig_BIA, name='Aut-Asigna-Eval-BIA'),
    path('map_eval/<int:pk>/asig_eval_rev/', views.Revisa_Asig_BIA, name='Rev-Asig-BIA'),

    url(r'^ria/asig_nivel_impacto/(?P<pk>\d+)/(?P<status>[\w-]+)/$', views.Asig_Imp, name='Asig-Nivel-Imp'),
    url(r'^ria/asig_nivel_indicador/(?P<pk>\d+)/(?P<status>[\w-]+)/$', views.Asig_Ind, name='Asig-Nivel-Ind'),
    url(r'^ria/envia_raci/(?P<pk>\d+)/(?P<etapa>[\w-]+)/$', views.Envia_Ev_RACI, name='Envia_Ev_RACI'),
    url(r'^ria/envia_auth/(?P<pk>\d+)/(?P<etapa>[\w-]+)/$', views.Envia_Auth, name='Envia-Auth'),

]


# Asignacion de Activos a Procesos (Servicios Criticos)
# -----------------------------------------------------
urlpatterns += [

    path('map_act/', views.Lista_Recursos, name='Lista-Recursos'),
    path('map_act/crea_activo/', views.Crea_Activo, name='Crea-Activo'),

    path('map_act/<int:pk>/asig_serv/', views.asigna_servicio, name='Asigna-Servicio'),
    path('map_act/<int:pk>/aut_asig_act/', views.Aut_Asig_Act, name='Aut-Asigna-Activos'),
    path('map_act/<int:pk>/rev_asig_serv/', views.rev_asigna_servicio, name='Rev-Asigna-Servicios'),

]

# Asignacion de Escenarios a Procesos
# ------------------------------------
urlpatterns += [
    #url(r'^map_esc/$', views.Map_escenariosListView.as_view(), name='Mapeo-Escenarios'),
    path('map_esc/', views.Lista_Escenarios, name='Lista-Escenarios'),
    path('map_esc/<int:pk>/asig_esc/', views.Asigna_Escenarios, name='Asigna-Escenarios'),
    path('map_esc/<int:pk>/aut_asig_esc/', views.Aut_Asig_Esc, name='Aut-Asigna-Escenarios'),
    path('map_esc/<int:pk>/rev_asig_esc/', views.Revisa_Asig_Esc, name='Rev-Asigna-Escenarios'),

]

# Asignacion RACI
# ----------------
urlpatterns += [
    #url(r'^proceso/(?P<pk>[-\w]+)/(?P<etapa>)[\w-]+/$', views.Asigna_Raci, name='asigna-raci'),
    #path(r'^proceso/(?P<pk>[-\w]+)/(?P<etapa>)[\w-]+/$', views.Asigna_Raci, name='asigna-raci'),
    path('proceso/<slug:pk>/<path:etapa>/', views.Asigna_Raci, name='asigna-raci'),

]

# Comentarios de Revision
# ----------------------- 

urlpatterns += [

    path('revisa/', views.Crea_Rev_OC, name='Crea-Rev-OC'),
    path('revisa/<int:pk>/borra_rev_oc/', views.Borra_Rev_OC, name='Borra-Rev-OC'),
    path('revisa/<int:pk>/ok_rev_oc/', views.OK_Rev_OC, name='OK-Rev-OC'),

]


# Administracion de incidentes
urlpatterns += [
    path('inc_mgm/', views.Lista_Incidentes, name='Lista-Incidentes'),
    
    path('inc_mgm/<int:pk>/reporte_inc/', views.Perfil_Inc, name='Perfil-Incidente'),
    path('incidentes/', views.Declara_Inc, name='Declara-Incidente'),
    path('incidentes/<int:pk>/modi_inc/', views.Modifica_Inc, name='Modifica-Incidente'),

]

#  Procedimientos de Recuperacion
urlpatterns += [
    
    path('proced_cont/', views.Lista_Procedimientos, name='Lista-Proced'),
    path('proced_cont/<int:pk>/crea_proc_a/', views.cr_prcd_a, name='crea-prcd-a'),
    path('proced_cont/<int:pk>/crea_proc_b/', views.cr_prcd_b, name='crea-proced-B'),
    path('proced_cont/<int:pk>/listas_c/', views.cr_prcd_list, name='lista-c'),
    path('proced_cont/<int:pk>/<int:fase>/crea_p5/', views.cr_prcd_P5, name='crea-P5'),
    path('proced_cont/<int:pk>/<int:fase>/borra_p5/', views.br_prcd_P5, name='borra-P5'),
    path('proced_cont/<int:pk>/<int:fase>/crea_p6/', views.cr_prcd_P6, name='crea-P6'),
    path('proced_cont/<int:pk>/<int:fase>/borra_p6/', views.br_prcd_P6, name='borra-P6'),
    path('proced_cont/<int:pk>/<int:fase>/crea_p7/', views.cr_prcd_P7, name='crea-P7'),
    path('proced_cont/<int:pk>/<int:fase>/borrap7/', views.br_prcd_P7, name='borra-P7'),
    path('proced_cont/<int:pk>/env_aut_proced/', views.Env_Aut_Proced, name='env-aut-proced'),
    path('proced_cont/<int:pk>/aut_proced/', views.Aut_Proced_C, name='aut-proced'),
    path('proced_cont/<int:pk>/rev_proced/', views.Revisa_Proced_B, name='rev-proced-b'),
    path('proced_cont/<int:pk>/det_proced/', views.detalle_procedimiento, name='det-proced'),
    path('proced_cont/<int:pk>/det_proced_v/', views.detalle_procedimiento_v, name='det-proced-v'),
    path('proced_cont/<int:pk>/<int:pk_padre>/lis_proced/', views.Lista_PC_Px, name='lis-pc-px'),
    path('proced_cont/<int:pk>/activa_pc/', views.ActivaDesactivaPc, name='act-des-pc'),
    path('proced_cont/<int:pk>/ok_activa_pc/', views.ConfirmaActivacionPC, name='ok-act-pc'),

    url(r'^proced_cont/(?P<item>[\w-]+)/(?P<pk>\d+)/(?P<valor>[\w-]+)/$', views.aut_obs_proced, name='obs-proced'),

    # Actualiza PC
    url('proced_cont/<int:pk>/actualiza_pc/', views.ActualizaPC, name='actualiza-pc'),

    # Activa/Desactiva PC
    path("procedimientos/toggle/", views.toggle_procedimiento, name="toggle_procedimiento"),  # Obtener estados
    path("procedimientos/toggle/<int:procedimiento_id>/", views.toggle_procedimiento, name="toggle_procedimiento"),  # Cambiar estado
    #path("procedimientos/toggle/<int:procedimiento_id>/", views.toggle_procedimiento, name="toggle_procedimiento"),
]


# DRP
urlpatterns += [

    path('drp/', views.Lista_DRP, name='Lista-DRP'),
    path('drp/crea_drp/', views.Crea_Drp, name='Crea-DRP'),
    path('drp/borra_drp/<int:pk>/', views.Borra_Drp, name='Borra-DRP'),
    path('drp/<int:pk>/indice/', views.Indice_DRP, name='Indice-DRP'),
    path('drp/<int:pk>/objetivo/', views.Drp_Sec_1, name='Objetivo-DRP'),
    path('drp/<int:pk>/responsable/', views.Drp_Sec_2, name='Responsables-DRP'),
    path('drp/<int:pk>/alcance/', views.Drp_Sec_3, name='Alcance-DRP'),
    path('drp/<int:pk>/estrategia/', views.Drp_Sec_4, name='Estrategia-DRP'),
    path('drp/<int:pk>/listaCmp/', views.Lista_CMP, name='Lista-CMP'),
    path('drp/<int:pk>/<int:accion>/asigna_cmp/', views.Asigna_CMP, name='Asigna-CMP'),
    path('drp/<int:pk>/listaServCrtc/', views.Lista_Serv_Crtc, name='Lista-SC'),
    path('drp/<int:pk>/<int:acc>/crea_p5_drp/', views.cr_drp_P5, name='crea-P5-DRP'),
    path('drp/<int:pk>/<int:acc>/', views.br_drp_P5, name='borra-P5-DRP'),
    path('drp/<int:pk>/listaPasos/', views.Lista_Pasos_Drp, name='Lista-Pasos-DRP'),
    path('drp/<int:pk>/crea_p7_drp/', views.cr_drp_P7, name='crea-P7-DRP'),
    path('drp/<int:pk>/borra_p7_drp/', views.br_drp_P7, name='borra-P7-DRP'),
    path('drp/<int:pk>/listaContactos/', views.Lista_Contactos_DRP, name='Lista-Contactos-DRP'),
    path('drp/<int:pk>/crea_p6_drp/', views.cr_drp_P6, name='crea-P6-DRP'),
    path('drp/<int:pk>/borra_p6_drp/', views.br_drp_P6, name='borra-P6-DRP'),
    path('drp/<int:pk>/modifica_p6_drp/', views.md_drp_P6, name='modifica-P6-DRP'),
    path('drp/<int:pk>/<int:sec>/', views.Env_Aut_DRP, name='Envia-Aut-DRP'),
    path('drp/<int:pk>/<int:sec>/aut_drp/', views.Aut_Drp, name='Autoriza-DRP'),
    path('drp/<int:pk>/revisa_resp_drp/', views.Rev_S2_Drp, name='Revisa-Resp-DRP'),
    path('drp/<int:pk>/rev_obj_drp/', views.Rev_S1_Drp, name='Revisa-Obj-DRP'),
    path('drp/<int:pk>/rev_alc_drp/', views.Rev_S3_Drp, name='Revisa-Alcance-DRP'),
    path('drp/<int:pk>/rev_est_drp/', views.Rev_S4_Drp, name='Revisa-Estrategia-DRP'),
    path('drp/<int:pk>/rev_cmp_drp/', views.Rev_S5_Drp, name='Revisa-Especif_Tec-DRP'),
    path('drp/<int:pk>/rev_sc_drp/', views.Rev_S6_Drp, name='Revisa-SC-DRP'),

    url(r'^drp/(?P<item>[\w-]+)/(?P<pk>\d+)/(?P<valor>[\w-]+)/$', views.aut_obs_drp, name='obs-drp'),

]

# Manejo de Componentes
# =====================

urlpatterns += [

    path('drp/crea_cmp/', views.Crea_CMP, name='Crea-CMP'),
    path('drp/<int:pk>/crea_lbc/', views.Crea_LBC, name='Crea-LBC'),
    path('drp/<int:pk>/borra_lbc/', views.Borra_LBC, name='Borra-LBC'),

    path('drp/<int:pk>/<int:pk_drp>/listaLBC/', views.Lista_LBC, name='Lista-LBC'),

]

# Datos Fijos
# ===========
urlpatterns += [
    # Gestores

    path('conf/', views.Menu_Conf, name='menu-conf'),
    path('conf/crea_gestor/', views.Crea_G, name='crea-g'),
    path('conf/borra_gestor/', views.Borra_Gestor, name='borra-g'),
    path('conf/lista_gestores/', views.GestorListView.as_view(), name='lista-gestores'),
    path('conf/<int:pk>/asigna_grupo/', views.Asigna_Grupo, name='asigna-grupo'),

    # Impactos (RIA)

    path('ria/lista_impactos/', views.Lista_riesgos, name='Lista-Impactos'),
    path('ria/crea_impacto/', views.Crea_Impacto, name='Crea-Impacto'),
    path('ria/mod_impacto/<int:pk>/', views.Mod_Impacto, name='Mod-Impacto'),
    path('ria/borra_impacto/<int:pk>/', views.Borra_Impacto, name='Borra-Impacto'),

    path('ria/lista_nivel_impacto/<int:pk>/', views.Lista_Nivel_Impactos, name='Lista-Nivel-Imp'),
    path('ria/crea_nivel_impacto/<int:pk>/', views.Crea_Nivel_Impacto, name='Crea-Nivel-Imp'),

]

# Manejo de Errores
# =================
urlpatterns += [
    #path(r'^mensajes/(?P<err>)[\w-]+/(?P<ce>\d+)/$', views.err_mgm, name='error-mgm'),
    url(r'^mensajes/(?P<ce>\d+)/$', views.Err_Sesion_Mgm, name='error-sesion-mgm'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# y ahí le especifico a Django el directorio que voy a utilizar para subir
# ficheros.




