from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from core.models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate
from .permission import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": True,
                "message": "User created successfully",
                "user": {
                    "email": user.email,
                    "full_name": user.full_name,
                    "phone_no": user.phone_no,
                    'refres':str(refresh),
                    'access':str(refresh.access_token)
                },
                "status_code": status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Validation failed",
            "errors": serializer.errors,
            "status_code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    if request.method=='POST':
        request.user.auth_token.delete()
        return Response({"status":True,"status_code":HTTP_200_OK,"message":"logout successfully!"})
        

class Home(APIView):
    def get(self,request):
        return Response({"status":True,"message":"Welcome to home page!"})



class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrReadOnly] 


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrReadOnly]



# # Retrieve, Update, and Delete View
# class EnrolledCourseUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = EnrolledCourseUser.objects.all()
#     serializer_class = EnrolledCourseUserSerializer
#     permission_classes = [IsAuthenticated]


#List and Create View
class EnrolledCourseUserListCreateView(generics.ListCreateAPIView):
    queryset = EnrolledCourseUser.objects.all()
    serializer_class = EnrolledCourseUserSerializer
    permission_classes = [IsAuthenticated]


class EnrollUserInCourseView(generics.CreateAPIView):
    queryset = EnrolledCourseUser.objects.all()
    serializer_class = EnrolledCourseUserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can enroll

    def create(self, request, *args, **kwargs):
        # Get the course ID from the request
        course_id = request.data.get("course_id")
        
        # Check if course ID is provided, if not, return an error
        if not course_id:
            return Response({
                "status": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Course ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get the course object
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                "status": False,
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Course not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is enrolled in the course
        enrolled_course_user, created = EnrolledCourseUser.objects.get_or_create(
            # Here, we do not set enrolled_users directly; it's handled differently.
        )

        # Add the course to the enrolled courses and associate the user with the course
        enrolled_course_user.enrolled_users.add(request.user)
        enrolled_course_user.enrolled_courses.add(course)
        enrolled_course_user.save()

        return Response({
            "status": True,
            "status_code": status.HTTP_201_CREATED,
            "message": f"Successfully enrolled in {course.title}",
            "course": course.title
        }, status=status.HTTP_201_CREATED)



## FAQ APi
class FAQList(generics.ListAPIView):
    serializer_class=FAQSerializers
    queryset=FAQ.objects.all().order_by("-created_at")

class FAQCreate(generics.CreateAPIView):
    serializer_class=FAQSerializers
    queryset=FAQ
    permission_classes=[IsAdminUser]
