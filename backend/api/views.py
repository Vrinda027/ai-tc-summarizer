from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class SummarizeView(APIView):
    def post(self,request):
        text=request.data.get("text","")
        if not text:
            return Response({"error":"No text provided"},status=400)
        return Response({"summary":"This will be your AI-generated summary"})