from django.urls import path, include
from .views import PrisonerSearchAPIView, UserDetailAPIView
from rest_framework.routers import DefaultRouter
from .views import PrisonerViewSet, ActivityTypeViewSet, RequestTemplateViewSet, ApprovalProcessViewSet, DepartmentRoleViewSet

router = DefaultRouter()
router.register(r'prisoners', PrisonerViewSet)
router.register(r'activity-types', ActivityTypeViewSet)
router.register(r'requests', RequestTemplateViewSet)
router.register(r'approval-process', ApprovalProcessViewSet)
router.register(r'departments', DepartmentRoleViewSet)

urlpatterns = [
    path('api/prisoners/search/', PrisonerSearchAPIView.as_view(), name='prisoner-search'),
    path('api/', include(router.urls)),
    path('api/user/', UserDetailAPIView.as_view(), name='user-detail'),
]
