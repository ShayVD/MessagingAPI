from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication import views as auth_views
from messaging import views as msg_views


router = DefaultRouter()
router.register('users', auth_views.UserViewSet)
router.register('conversations', msg_views.ConversationViewSet)
router.register('messages', msg_views.MessageViewSet)
router.register('likes', msg_views.LikeViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
