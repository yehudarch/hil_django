from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views, paginators

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register("note_auth", views.NoteViewSet)


urlpatterns = [
    path("", views.home),
    # path('/notes_pagination2', views.serve_notes_pagination),
    # path('rss_pagination', paginators.RssPagination.as_view()),
    path('rss_pagination', views.serve_rss_pagination),
    path('rss', views.serve_rss),
    path('versions', views.serve_versions),
    path("signup", views.signup),
    # path('', include(router.urls)),
    path('obtain-token', obtain_auth_token),
    path('logout', views.delete_token),
    path('validate-token', views.validate_token),

]
