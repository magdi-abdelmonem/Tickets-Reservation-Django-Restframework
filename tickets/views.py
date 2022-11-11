from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *



def no_rest_no_model (request):
    data={'name':'magdi','age':25,"address":"egypt"}
    return JsonResponse(data)

def no_rest_from_model(request):

    data=Movie.objects.all()
    dataa={
        'results':list(data.values('hall','movie'))
    }
    return JsonResponse(dataa)

#-----------------------------------------------------------------
# 3.function based view

# 3.1 GET POST

@api_view(('GET','POST'))
def FBV_List(request):                          #function based view
    #GET
    if request.method=='GET':
        guests=Guest.objects.all()
        serializer =GuestSerializer(guests,many=True)
        return Response(serializer.data)

    #POST
    elif request.method=='POST':
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.data, status=status.HTTP_404_BAD_REQUEST)

# 3.2 GET PUT DELETE

@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):                          #function based view with particular pk
    #GET
    guest=get_object_or_404(Guest, pk=pk)
    if request.method=='GET':
        serializer =GuestSerializer(guest)
        return Response(serializer.data)

    #PUT                                           #update
    elif request.method=='PUT':
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


    #DELETE
    elif request.method=='DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT )

#--------------------------------------------------------------

#CBV                                    class Based View

# GET POST
class CBV_List(APIView):
    def get(self, request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests, many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
          
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


#GET PUT DELETE                         class Based View

class CVB_pk(APIView):
    def get(self, request,pk):
        guest=get_object_or_404(Guest, pk=pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)

    def put(self,request,pk):
        guest=get_object_or_404(Guest, pk=pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


    def delete(self,request,pk):
        guest=get_object_or_404(Guest, pk=pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#--------------------------------------------------------------

#  mixins طريقة سهلة عشان متكررش الكود 
#    

class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
   queryset=Guest.objects.all()
   serializer_class=GuestSerializer

   def get(self,request):
       return self.list(request) 

   def post(self,request):
       return self.create(request)
        

class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
   queryset=Guest.objects.all()
   serializer_class=GuestSerializer


   def get(self,request,pk):
       return self.retrieve(request) 

   def put(self,request,pk):
       return self.update(request)

   def delete(self,request,pk):
       return self.destroy(request)


#--------------------------------------------------------
#generics
#=get post                      خد بالك كل مدي الكود بيصغر وبيبقي اسهل 

class generic_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

class generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
#------------------------------------------------------------

#viewset

class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    


class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer


class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=reservationSerializer

#------------------------------------------------------------------

#find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall  = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer=MovieSerializer(movies,many=True)
    return Response(serializer.data)


#new reservation    
@api_view(['POST'])
def new_resv(request):
    movie=Movie()
    movie.hall=request.data['hall'],
    movie.movie=request.data['movie']
    
    
    guest=Guest()
    guest.name=request.data['name'],
    guest.mobile=request.data['mobile']
    guest.save()

    reserv=Reservation()
    reserv.guest=guest
    reserv.movie=movie
    reserv.save()

    return Response(status=status.HTTP_201_CREATED)