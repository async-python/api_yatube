from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as v

from api.views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('v1/posts', PostViewSet)
router.register(r'v1/posts/(?P<post_id>[0-9]+)/comments', CommentViewSet)

urlpatterns = [
    path('v1/api-token-auth/', v.obtain_auth_token),
    path('', include(router.urls)),
]
