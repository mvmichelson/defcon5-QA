#Programa PYTHON
#Definicion de Links urls
#Programado por Marco A. Villalobos Michelson
#=============================================

from django.urls import re_path as url
from django.urls import path

from . import views

from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),          # Pagina Principal
    url(r'^/reinicia/$', views.reset, name='reinicia_bd'),    # Reinicia la Base de Datos

    url(r'^get_chart/$', views.get_chart, name='get_chart'),
    url(r'^$', views.Base_GenericPageView.as_view(), name='base_generic'),
    path('^mensajes/$', views.En_Construccion, name='En-Construccion'),

    #url(r'^request.META['HTTP_REFERER']', name='volver'),

    # Diagramas Metodologicos
    # -----------------------
    url(r'^/mapeo/$', views.Mapeo, name='Mapeo'),            # Diagrama Metodologia BCP/DRP
    url(r'^ria/mapa/$', views.Mapa_RIA, name='Mapa-RIA'),    # Diagrama Metodologia RIA

   
    #url(r'^procesos/$', views.ProcesoListView.as_view(), name='Lista-Procesos'),
    #url(r'^proceso/(?P<pk>[-\w]+)/renew/$', views.crea_proceso.as_view(), name='Crea-Procesos'),

]

# Creacion y Aprobacion de Procesos
# ---------------------------------
urlpatterns += [
    url(r'^procesos/$', views.Lista_Procesos, name='Lista-Procesos'),
    #url(r'^proceso/(?P<pk>\d+)$', views.ProcesoDetailView.as_view(), name='Detalle-Procesos'),
    url(r'^proceso/(?P<pk>\d+)/detalle_proceso/$', views.Detalle_Proceso, name='Detalle-Proceso'),
    path(r'^proceso/(?P<pk>\d+)/det_proceso_v/$', views.Detalle_Proceso_V, name='Detalle-Proceso-V'),
    url(r'^proceso/(?P<pk>[-\w]+)/crea_p/$', views.crea_proceso, name='crea-procesos'),
    url(r'^proceso/(?P<pk>[-\w]+)/borra_p/$', views.borra_proceso, name='borra-procesos'),
    url(r'^proceso/(?P<pk>[-\w]+)/auth_raci/$', views.Autoriza_M, name='auth_m-raci'),
    url(r'^proceso/(?P<pk>[-\w]+)/revisa_proceso/$', views.Revisa_Proceso, name='proceso-revisa'),
    path(r'^proceso/(?P<item>)[\w-]+/(?P<pk>\d+)/(?P<valor>)[\w-]+/$', views.aut_obs_proceso, name='obs-proceso'),
    path(r'^proceso/(?P<pk>[-\w]+)/borra_obs/$', views.borra_obs_proceso, name='borra-obs-proceso'),
    #url(r'^proceso/(?P<pk>\d+)/revisa_auth/$', views.LogAutRevListView.as_view(), name='revisa-auth'),

]


# Evaluaciones BIA a Procesos
# ---------------------------
urlpatterns += [
    #url(r'^map_eval/$', views.Map_evalListView.as_view(), name='Mapeo-Evaluaciones'),
    url(r'^map_eval/$', views.Lista_Evaluaciones, name='Lista-Evaluaciones'),
    url(r'^map_eval/(?P<pk>\d+)/asig_eval/$', views.Asigna_Imp_Ind, name='Asigna-Evaluacion'),
    url(r'^map_eval/(?P<pk>\d+)/aut_asig_eval/$', views.Aut_Asig_BIA, name='Aut-Asigna-Eval-BIA'),
    url(r'^map_eval/(?P<pk>\d+)/asig_eval_rev/$', views.Revisa_Asig_BIA, name='Rev-Asig-BIA'),

    path(r'^ria/asig_nivel_impacto/(?P<pk>\d+)/(?P<status>)[\w-]+/$', views.Asig_Imp, name='Asig-Nivel-Imp'),
    path(r'^ria/asig_nivel_indicador/(?P<pk>\d+)/(?P<status>)[\w-]+/$', views.Asig_Ind, name='Asig-Nivel-Ind'),
    path(r'^ria/envia_raci/(?P<pk>\d+)/(?P<etapa>)[\w-]+/$', views.Envia_Ev_RACI, name='Envia_Ev_RACI'),

    path(r'^ria/envia_auth/(?P<pk>\d+)/(?P<etapa>)[\w-]+/$', views.Envia_Auth, name='Envia-Auth'),

]


# Asignacion de Activos a Procesos (Servicios Criticos)
# -----------------------------------------------------
urlpatterns += [
    #url(r'^map_act/$', views.Map_activosListView.as_view(), name='Mapeo-Activos'),
    url(r'^map_act/$', views.Lista_Recursos, name='Lista-Recursos'),
    url(r'^map_act/crea_activo/$', views.Crea_Activo, name='Crea-Activo'),

    #url(r'^map_act/(?P<pk>\d+)/asig_act/$', views.Asigna_Activos, name='Asigna-Activos'),
    path(r'^map_act/(?P<pk>\d+)/asig_serv/$', views.asigna_servicio, name='Asigna-Servicio'),
    
    url(r'^map_act/(?P<pk>\d+)/aut_asig_act/$', views.Aut_Asig_Act, name='Aut-Asigna-Activos'),
    #url(r'^map_act/(?P<pk>\d+)/rev_asig_act/$', views.Revisa_AsigActxProceso, name='Rev-Asigna-Activos'),
    path(r'^map_act/(?P<pk>\d+)/rev_asig_serv/$', views.rev_asigna_servicio, name='Rev-Asigna-Servicios'),
    
]

# Asignacion de Escenarios a Procesos
# ------------------------------------
urlpatterns += [
    #url(r'^map_esc/$', views.Map_escenariosListView.as_view(), name='Mapeo-Escenarios'),
    url(r'^map_esc/$', views.Lista_Escenarios, name='Lista-Escenarios'),
    url(r'^map_esc/(?P<pk>\d+)/asig_esc/$', views.Asigna_Escenarios, name='Asigna-Escenarios'),
    url(r'^map_esc/(?P<pk>\d+)/aut_asig_esc/$', views.Aut_Asig_Esc, name='Aut-Asigna-Escenarios'),
    url(r'^map_esc/(?P<pk>\d+)/rev_asig_esc/$', views.Revisa_Asig_Esc, name='Rev-Asigna-Escenarios'),
    
]

# Asignacion RACI
# ----------------
urlpatterns += [
    path(r'^proceso/(?P<pk>[-\w]+)/(?P<etapa>)[\w-]+/$', views.Asigna_Raci, name='asigna-raci'),
    
]

# Comentarios de Revision
# ----------------------- 

urlpatterns += [

    path('revisa/', views.Crea_Rev_OC, name='Crea-Rev-OC'),
    path('^revisa/(?P<pk>\d+)/borra_rev_oc/$', views.Borra_Rev_OC, name='Borra-Rev-OC'),
    path('^revisa/(?P<pk>\d+)/ok_rev_oc/$', views.OK_Rev_OC, name='OK-Rev-OC'),


    #path('Auditorias/revisa/', views.Crea_Rev_OC, name='Crea-Rev-OC'),
    #path('^Auditorias/(?P<pk>\d+)/borra_rev_oc/$', views.Borra_Rev_OC, name='Borra-Rev-OC'),


]



# Administracion de incidentes
urlpatterns += [
    url(r'^inc_mgm/$', views.Lista_Incidentes, name='Lista-Incidentes'),
    url(r'^inc_mgm/(?P<pk>\d+)/reporte_inc/$', views.Perfil_Inc, name='Perfil-Incidente'),
    url(r'^incidentes/$', views.Declara_Inc, name='Declara-Incidente'),
    url(r'^incidentes/(?P<pk>\d+)/modi_inc/$', views.Modifica_Inc, name='Modifica-Incidente'),
    
]

#  Procedimientos de Recuperacion
urlpatterns += [
    path(r'^proced_cont/$', views.Lista_Procedimientos, name='Lista-Proced'),
    url(r'^proced_cont/(?P<pk>\d+)/crea_proc_a/$', views.cr_prcd_a, name='crea-prcd-a'),
    url(r'^proced_cont/(?P<pk>\d+)/crea_proc_b/$', views.cr_prcd_b, name='crea-proced-B'),
    path(r'^proced_cont/(?P<pk>\d+)/listas_c/$', views.cr_prcd_list, name='lista-c'),
    url(r'^proced_cont/(?P<pk>\d+)/(?P<fase>\d+)/crea_p5/$', views.cr_prcd_P5, name='crea-P5'),
    url(r'^proced_cont/(?P<pk>\d+)/(?P<fase>\d+)/borra_p5/$', views.br_prcd_P5, name='borra-P5'),
    url(r'^proced_cont/(?P<pk>\d+)/(?P<fase>\d+)/crea_p6/$', views.cr_prcd_P6, name='crea-P6'),
    url(r'^proced_cont/(?P<pk>\d+)/(?P<fase>\d+)/borra_p6/$', views.br_prcd_P6, name='borra-P6'),
    url(r'^proced_cont/(?P<pk>\d+)/(?P<fase>\d+)/crea_p7/$', views.cr_prcd_P7, name='crea-P7'),
    url(r'^proced_cont/(?P<pk>\d+)/(?P<fase>\d+)/borrap7/$', views.br_prcd_P7, name='borra-P7'),
    url(r'^proced_cont/(?P<pk>\d+)/env_aut_proced/$', views.Env_Aut_Proced, name='env-aut-proced'),
    
    url(r'^proced_cont/(?P<pk>\d+)/aut_proced/$', views.Aut_Proced_C, name='aut-proced'),
    url(r'^proced_cont/(?P<pk>\d+)/rev_proced/$', views.Revisa_Proced_B, name='rev-proced-b'),
        
    path(r'^proced_cont/(?P<item>)[\w-]+/(?P<pk>\d+)/(?P<valor>)[\w-]+/$', views.aut_obs_proced, name='obs-proced'),
    url(r'^proced_cont/(?P<pk>\d+)/det_proced/$', views.detalle_procedimiento, name='det-proced'),
    url(r'^proced_cont/(?P<pk>\d+)/det_proced_v/$', views.detalle_procedimiento_v, name='det-proced-v'),
    path(r'^proced_cont/(?P<pk>\d+)/(?P<pk_padre>\d+)/lis_proced/$', views.Lista_PC_Px, name='lis-pc-px'),
    path(r'^proced_cont/(?P<pk>\d+)/activa_pc/$', views.ActivaDesactivaPc, name='act-des-pc'),
    path(r'^proced_cont/(?P<pk>\d+)/ok_activa_pc/$', views.ConfirmaActivacionPC, name='ok-act-pc'),

    # Actualiza PC
    path(r'^proced_cont/(?P<pk>\d+)/actualiza_pc/$', views.ActualizaPC, name='actualiza-pc'),

    # Activa/Desactiva PC
    path("procedimientos/toggle/", views.toggle_procedimiento, name="toggle_procedimiento"),  # Obtener estados
    path("procedimientos/toggle/<int:procedimiento_id>/", views.toggle_procedimiento, name="toggle_procedimiento"),  # Cambiar estado
    #path("procedimientos/toggle/<int:procedimiento_id>/", views.toggle_procedimiento, name="toggle_procedimiento"),
]


# DRP
urlpatterns += [
    path(r'^drp/$', views.Lista_DRP, name='Lista-DRP'),
    
    path(r'^drp/crea_drp/$', views.Crea_Drp, name='Crea-DRP'),
    path(r'^drp/borra_drp/(?P<pk>\d+)/$', views.Borra_Drp, name='Borra-DRP'),
    path(r'^drp/(?P<pk>\d+)/indice/$', views.Indice_DRP, name='Indice-DRP'),
    path(r'^drp/(?P<pk>\d+)/objetivo/$', views.Drp_Sec_1, name='Objetivo-DRP'),
    path(r'^drp/(?P<pk>\d+)/responsable/$', views.Drp_Sec_2, name='Responsables-DRP'),
    path(r'^drp/(?P<pk>\d+)/alcance/$', views.Drp_Sec_3, name='Alcance-DRP'),
    path(r'^drp/(?P<pk>\d+)/estrategia/$', views.Drp_Sec_4, name='Estrategia-DRP'),
    path(r'^drp/(?P<pk>\d+)/listaCmp/$',  views.Lista_CMP, name='Lista-CMP'),
    path(r'^drp/(?P<pk>\d+)/(?P<accion>\d+)/asigna_cmp/$',  views.Asigna_CMP, name='Asigna-CMP'),

    path(r'^drp/(?P<pk>\d+)/listaServCrtc/$', views.Lista_Serv_Crtc, name='Lista-SC'),
    path(r'^drp/(?P<pk>\d+)/(?P<acc>\d+)/crea_p5_drp/$', views.cr_drp_P5, name='crea-P5-DRP'),
    path(r'^drp/(?P<pk>\d+)/(?P<acc>\d+)/$', views.br_drp_P5, name='borra-P5-DRP'),

    path(r'^drp/(?P<pk>\d+)/listaPasos/$', views.Lista_Pasos_Drp, name='Lista-Pasos-DRP'),
    path(r'^drp/(?P<pk>\d+)/crea_p7_drp/$', views.cr_drp_P7, name='crea-P7-DRP'),
    path(r'^drp/(?P<pk>\d+)/borra_p7_drp/$', views.br_drp_P7, name='borra-P7-DRP'),

    path(r'^drp/(?P<pk>\d+)/listaContactos/$', views.Lista_Contactos_DRP, name='Lista-Contactos-DRP'),
    path(r'^drp/(?P<pk>\d+)/crea_p6_drp/$', views.cr_drp_P6, name='crea-P6-DRP'),
    path(r'^drp/(?P<pk>\d+)/borra_p6_drp/$', views.br_drp_P6, name='borra-P6-DRP'),
    path(r'^drp/(?P<pk>\d+)/modifica_p6_drp/$', views.md_drp_P6, name='modifica-P6-DRP'),

    path(r'^drp/(?P<pk>\d+)/(?P<sec>\d+)/$', views.Env_Aut_DRP, name='Envia-Aut-DRP'),

    path(r'^drp/(?P<pk>\d+)/(?P<sec>\d+)/aut_drp/$', views.Aut_Drp, name='Autoriza-DRP'),
    path(r'^drp/(?P<item>)[\w-]+/(?P<pk>\d+)/(?P<valor>)[\w-]+/$', views.aut_obs_drp, name='obs-drp'),

    path(r'^drp/(?P<pk>\d+)/revisa_resp_drp/$', views.Rev_S2_Drp, name='Revisa-Resp-DRP'),
    path(r'^drp/(?P<pk>\d+)/rev_obj_drp/$', views.Rev_S1_Drp, name='Revisa-Obj-DRP'),
    path(r'^drp/(?P<pk>\d+)/rev_alc_drp/$', views.Rev_S3_Drp, name='Revisa-Alcance-DRP'),
    path(r'^drp/(?P<pk>\d+)/rev_est_drp/$', views.Rev_S4_Drp, name='Revisa-Estrategia-DRP'),
    path(r'^drp/(?P<pk>\d+)/rev_cmp_drp/$', views.Rev_S5_Drp, name='Revisa-Especif_Tec-DRP'),
    path(r'^drp/(?P<pk>\d+)/rev_sc_drp/$', views.Rev_S6_Drp, name='Revisa-SC-DRP'),

]

# Manejo de Componentes
# =====================

urlpatterns += [

    path(r'^drp/crea_cmp/$',  views.Crea_CMP, name='Crea-CMP'),
    #path(r'^drp/(?P<pk>\d+)/listaLBC/$',  views.Lista_LBC, name='Lista-LBC'),
    path(r'^drp/(?P<pk>\d+)/(?P<pk_drp>\d+)/listaLBC/$',  views.Lista_LBC, name='Lista-LBC'),
    path(r'^drp/(?P<pk>\d+)/crea_lbc/$',  views.Crea_LBC, name='Crea-LBC'),
    path(r'^drp/(?P<pk>\d+)/borra_lbc/$',  views.Borra_LBC, name='Borra-LBC'),

]

# Datos Fijos
# ===========
urlpatterns += [
    # Gestores
    url(r'^conf/$', views.Menu_Conf, name='menu-conf'),
    url(r'^conf/crea_gestor/$', views.Crea_G, name='crea-g'),
    url(r'^conf/borra_gestor/$', views.Borra_Gestor, name='borra-g'),
    url(r'^conf/lista_gestores/$', views.GestorListView.as_view(), name='lista-gestores'),
    url(r'^conf/(?P<pk>\d+)/asigna_grupo/$', views.Asigna_Grupo, name='asigna-grupo'),

    # Impactos (RIA)
    path(r'^ria/lista_impactos/$', views.Lista_riesgos, name='Lista-Impactos'),
    path(r'^ria/crea_impacto/$', views.Crea_Impacto, name='Crea-Impacto'),
    path(r'^ria/mod_impacto/(?P<pk>\d+)/$', views.Mod_Impacto, name='Mod-Impacto'),
    path(r'^ria/borra_impacto/(?P<pk>\d+)/$', views.Borra_Impacto, name='Borra-Impacto'),

    path(r'^ria/lista_nivel_impacto/(?P<pk>\d+)/$', views.Lista_Nivel_Impactos, name='Lista-Nivel-Imp'),
    path(r'^ria/crea_nivel_impacto/(?P<pk>\d+)/$', views.Crea_Nivel_Impacto, name='Crea-Nivel-Imp'),


]

# Manejo de Errores
# =================
urlpatterns += [
    #path(r'^mensajes/(?P<err>)[\w-]+/(?P<ce>\d+)/$', views.err_mgm, name='error-mgm'),
    path(r'^mensajes/(?P<ce>\d+)/$', views.Err_Sesion_Mgm, name='error-sesion-mgm'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# y ahí le especifico a Django el directorio que voy a utilizar para subir
# ficheros.




