from rest_framework import routers
from server.viewsets import *
router = routers.DefaultRouter()
router.register(r'clube', ClubeViewSet)
router.register(r'formacao', FormacaoViewSet)
router.register(r'atleta', AtletaViewSet)
router.register(r'gestor', GestorViewSet)
router.register(r'tecnico', TecnicoViewSet)
router.register(r'jogo', JogoViewSet)
router.register(r'convocado', ConvocadoViewSet)
router.register(r'tipo_evento', TipoEventoViewSet)
router.register(r'tipos_selecionados', TiposSelecionadosViewSet)
router.register(r'evento', EventoViewSet)