from django.urls import include, path, register_converter
from . import converters, views
from django.views.generic import TemplateView, RedirectView

register_converter(converters.BoolConverter, 'bool')
register_converter(converters.DateConverter, 'date')
register_converter(converters.TimeConverter, 'time')

app_name = 'server'
urlpatterns = [

    path('clubes/', TemplateView.as_view(template_name='clubes.html')),
    path('jogos/', TemplateView.as_view(template_name='jogos.html')),

    path('info_user/<str:email>/', views.infoUserView, name='info'),
    path('adversario_nome/<int:form_id>/', views.advNome, name='adversarionome'),

    path('clube/<str:nome>/<str:cor>/<str:simbolo>/', views.clubeView, name='clube'),
    path('change_clube/<int:id>/<str:cor>/<str:simbolo>/', views.cClubeView, name='cclube'),
    path('get_clubes/', views.gClubesView, name='gclubes'),
    path('get_clube/<str:id>/', views.gClubeView, name='gclube'),

    path('gestor/<int:clube>/<str:email>/<str:nome>/<str:password>/', views.gestorView, name='gestor'),

    path('formacao/<str:clube>/<str:nome>/', views.formacaoView, name='formacao'),
    path('del_formacao/<str:id>/', views.dFormacaoView, name='dformacao'),
    path('get_formacoes/<int:clube>/', views.gFormacoesView, name='gformacoes'),
    path('get_formacao/<int:id>/', views.gFormacaoView, name='gformacao'),

    path('atleta/<int:licenca>/<str:nome>/<str:formacao>/<int:camisola>/', views.atletaView, name='atleta'),
    path('change_atleta/<int:id>/<int:formacao>/<int:camisola>/', views.cAtletaView, name='catleta'),
    path('del_atleta/<int:id>/', views.dAtletaView, name='datleta'),
    path('get_atletas/<int:formacao>', views.gAtletas, name='gatletas'),
    path('get_atleta/<int:id>/', views.gAtleta, name='gatleta'),

    path('tecnico/<int:clube>/<str:email>/<str:nome>/<str:password>/', views.tecnicoView, name='tecnico'),
    path('change_tecnico/<int:id>/<str:grelhaC>/<str:grelhaB>/', views.cTecnicoView, name='ctecnico'),

    path('jogo/<int:clube>/<int:formacao>/<int:formacaoAdv>/<bool:casa>/<date:data>/<time:hora>/<str:tipo>/', views.jogoView, name='jogo'),
    path('change_jogo/<int:idJogo>/<str:grelhaC>/<str:grelhaB>/', views.cJogoView, name='cjogo'),
    path('get_jogos/<str:clube>/', views.gJogosView, name='gjogos'),
    path('get_jogo/<int:id>/', views.gJogoView, name='gjogo'),

    path('convocado/<int:jogo>/<int:atleta>/<bool:emCampo>/', views.convocadoView, name='convocado'),
    path('change_convocado/<int:jogo>/<int:atleta>/<bool:emCampo>/', views.cConvocadoView, name='cconvocado'),
    path('get_convocados/<int:idJogo>/', views.gConvocadosView, name='gconvocados'),

    path('evento/', views.eventoView, name='evento'),
    path('change_evento/', views.cEventoView, name='cevento'),
    path('del_evento/<int:id>/', views.dEventoView, name='devento'),
    path('get_eventos/<int:idJogo>/', views.gEventosView, name='geventos'),
    path('get_evento/<int:id>/', views.gEventoView, name='gevento'),

    path('tipo_evento/<str:tipo>/<bool:atleta1>/<bool:atleta2>/<bool:zonaC>/<bool:zonaB>/<bool:novoinst>/', views.tipoEventoView, name='tipoevento'),
    path('get_tipos_eventos/', views.gTiposEventosView, name='gtiposeventos'),

    path('tipo_selecionado/<int:tipo>/<int:tecnico>/', views.tipoSelecionadoView, name='tiposelecionado'),
    path('del_tipo_selecionado/<int:id>/', views.dTipoSelecionadoView, name='dtiposelecionado'),
    path('get_tipos_selecionados/<int:tecnico>', views.gTiposSelecionadosView, name='gtiposselecionados'),
]
