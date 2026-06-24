from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Student, Enrollment, User
from .serializers import (
    CourseSerializer,
    StudentSerializer,
    EnrollmentSerializer,
    RegisterSerializer,
)
from .utils import create_access_token, get_current_user, verify_password


""" Using API view (class based view)
class CourseListView(APIView):
    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course , many = True)
        return Response(serializer.data)
        

    def post(self, request):
        serializer = CourseSerializer(data = request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data , status= 201)

        return Response(serializer.errors ,status=400)


class CourseDetailView(APIView):

    def get_object(self, pk):
        return Course.objects.get(pk=pk)


    def get(self, request, pk):

        course = self.get_object(pk)

        serializer = CourseSerializer(course)

        return Response(serializer.data)


    def delete(self, request, pk):

        course = self.get_object(pk)
        course.delete()
        return Response(status= 204)

    def update(self, request, pk):

        serializer = CourseSerializer(data = request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data , status= 201)

        return Response(serializer.errors ,status=400)
 """


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Student, Enrollment
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer

# Step 31: Create a single ViewSet for Courses
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        # DRF equivalent of FastAPI's `current_user = Depends(get_current_user)`.
        request.current_user = get_current_user(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only create and delete require a valid JWT; list/retrieve remain public.
        request.current_user = get_current_user(request)
        return super().destroy(request, *args, **kwargs)

    # Step 34: Add custom GET action endpoint /api/courses/{id}/students/
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        # Fetch the specific course using the incoming ID (pk)
        course = self.get_object()
        
        # Pull only students linked to this course through the Many-to-Many relationship
        enrolled_students = course.students.all() 
        
        # Serialize the filtered list of students
        serializer = StudentSerializer(enrolled_students, many=True)
        return Response(serializer.data, status=200)


# Step 33: Create ViewSets for Student and Enrollment models
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer




class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # This endpoint must be public
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # 1. Validate structure input
        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 2. Look up the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid email or password.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 3. Verify credentials using verify_password utility
        if not verify_password(password, user.password):
            return Response(
                {'detail': 'Invalid email or password.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # 4. Generate the JWT token payload
        token_payload = {"sub": str(user.email)}
        token = create_access_token(data=token_payload)
        
        # 5. Return JSON payload matching specifications
        return Response({
            'access_token': token, 
            'token_type': 'bearer'
        }, status=status.HTTP_200_OK)


# OAuth2 Authorization Code flow redirects a user to an authorization server,
# which authenticates the user and returns a short-lived authorization code.
# A trusted backend exchanges that code for access/refresh tokens. It supports
# delegated access, client registration, redirect URI checks, consent, scopes,
# and (for public clients) PKCE. This API's simpler login accepts credentials
# directly and immediately issues its own JWT, so it is not an OAuth2
# Authorization Code flow and should not be described as one.
#
# JWT payloads are base64-encoded, not encrypted. Never put passwords, payment
# details, or other secrets in them. CORS is a browser-enforced origin policy;
# it does not prevent non-browser clients from calling an API.


    
    
