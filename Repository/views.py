from django.shortcuts import render
from Repository.models import Questions,Submissions
from Repository.serializers import QuestionSerializers,SubmmisionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class QuestionListCreateView(APIView):
    def get(self,request):
        qs=Questions.objects.all()
        serializers_instance = QuestionSerializers(qs,many=True)
        return Response(serializers_instance.data)
    
    def post(self,request):
        form_data= request.data # form_data dictionary --> python native type
        serializer_instance = QuestionSerializers(data=form_data) #  create serializer instance with form data
        if serializer_instance.is_valid(): #check if the data is valid according to the serializers validation rules
            actual_data= serializer_instance.validated_data #get the validated data from the serializer
            Questions.objects.create(**actual_data)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class QuestionRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):       #pk is the primary key of the question to retrieve
        qs=Questions.objects.get(id=pk)         #get the question object with the given primary key
        serializer_instance= QuestionSerializers(qs)      #seriaalize the question object
        return Response(data=serializer_instance.data)      #return the serialized data as a record
    
    def put(self,request,pk):
        form_data = request.data
        serializer_instance = QuestionSerializers(data=form_data)
        if serializer_instance.is_valid():
            actual_data = serializer_instance.validated_data

            Questions.objects.filter(id=pk).update(**actual_data)

            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class SubmissionListCreateView(APIView):
    def get(self,request):

        qs = Submissions.objects.all()

        serializer_instance = SubmmisionSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    

class EvaluateSubmissionView(APIView):
    def put(self,request,pk):
        form_data=request.data
        Submissions.objects.filter(id=pk).update(**form_data)
        return Response(data={
            "message":"updated..."
        })

        
