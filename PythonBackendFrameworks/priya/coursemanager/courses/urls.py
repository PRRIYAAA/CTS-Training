from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("students", StudentViewSet)
router.register("enrollments", EnrollmentViewSet)

url_patterns = router.urls


urlpatterns = [
    #path("courses/" , CourseListView.as_view()),
    #path("courses/<int:pk>/" , CourseDetailView.as_view())
    path('v1/', include(router.urls)),
    path('v1/auth/register/', RegisterView.as_view(), name='jwt-register'),
    path('v1/auth/login/', LoginView.as_view(), name='jwt-login'),
]
