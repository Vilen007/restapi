from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer,UserLoginSerializer,AddBookSerializer
from .models import Book


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'message':'Registration Successful', "data": serializer.data}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'username': user.username,'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors)
class BookView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        books= Book.objects.all()
        serializer = AddBookSerializer(books,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddBookView(APIView):
    def post(self, request):
        serializer = AddBookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UpdateBookView(APIView):
    def put(self,request,id):
        detail= Book.objects.get(pk=id)
        serializer = AddBookSerializer(detail,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DeleteBookView(APIView):
    def get(self, request, format=None, id=None):
        book = Book.objects.get(pk=id)
        book.delete()
        return Response(
            {
                "success": " Book Successfully Deleted"
            }
        )
