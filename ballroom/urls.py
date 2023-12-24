"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ballroom.views import TrainerViewSet, TypeBallroomDancingViewSet, TeamViewSet, MemberViewSet, CompetitionViewSet, \
    CompetitionProgramViewSet, PointViewSet, ParamsViewSet

router = routers.SimpleRouter()

router.register(r'trainer', TrainerViewSet, basename='trainer')
router.register(r'typeballroomdancing', TypeBallroomDancingViewSet, basename='typeballroomdancing')
router.register(r'team', TeamViewSet, basename='team')
router.register(r'member', MemberViewSet, basename='member')
router.register(r'competition', CompetitionViewSet, basename='competition')
router.register(r'competitionprogram', CompetitionProgramViewSet, basename='competitionprogram')
router.register(r'point', PointViewSet, basename='point')

urlpatterns = [
    path('', include(router.urls)),
    path('get_all_params/', ParamsViewSet.as_view({'get': 'get_all_params'}), name='get_all_params'),
    path('set_params/', ParamsViewSet.as_view({'post': 'set_params'}), name='set_params'),
    path('get_by_id/<int:id>', ParamsViewSet.as_view({'get': 'get_by_id'}), name='get_by_id'),
]
