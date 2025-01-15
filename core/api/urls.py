from django.urls import path,include
from .api import * 
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("",Home.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token, name='login'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegistrationAPIView.as_view(), name='registration'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('enrollments/', EnrollUserInCourseView.as_view(), name='enrollment-create'),
    path('list/enrollments/', EnrolledCourseUserListCreateView.as_view(), name='enrollment-list-create'),
    # path('enrollments/<int:pk>/', EnrolledCourseUserRetrieveUpdateDestroyView.as_view(), name='enrollment-detail'),
    path('list/faq/', FAQList.as_view(), name='FAQList'),
    path('create/faq/', FAQCreate.as_view(), name='FAQCreate'),
]
