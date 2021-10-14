from django.urls import path, re_path

from . import views

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('', views.index, name='index'),
    path('medidas/', views.medidas, name='medidas'),
    #path('entrenamientos/(?P<id>.*)$', views.entrenamientos, name='entrenamientos'),
    path('entrenamientos/<int:calendario_id>/', views.entrenamientos, name="entrenamientos"),
    path('historico/<str:param1>/<int:calendario_id>/', views.historico, name="historico"),
    path('historico/all/', views.historico_all, name="historico_all"),
    path('oauth/', views.call_view_googlefit, name="googlefit"),
    path('oauth/login/', views.call_view_googlefit_authenticate, name="google"),
    path('google/', views.call_view_google, name="googlefit_authenticate"),
    path('googlefit_ajax/', views.get_data_json_google, name="googlefit_get_data_ajax"),
    path('googlefit_ajax_save_data/', views.set_data_json_google, name="googlefit_set_data_ajax"),
    path('googlefit_ajax_save_session/', views.set_session_json_google, name="googlefit_set_data_ajax"),
    path('googlefit_ajax_connect/', views.get_connect_json_google, name="googlefit_set_data_ajax"),
    path('googlefit_activities_types/', views.get_activities_types_json_google, name="get_activities_types_json_google"),
    path('sentry-debug/', trigger_error),
    #path('entrenamiento_completado/', views.entrenamiento_completado, name="entrenamiento_completado"),
    # path('medidas/nuevas/', views.medidas_nuevas, name="medidas_nuevas"),

]