from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv

import os
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Create your views here.
class SummarizeView(APIView):
    def post(self,request):
        text=request.data.get("text","")
        if not text:
            return Response({"error":"No text provided"},status=400)
        try:
            model = genai.GenerativeModel("models/gemini-flash-latest")


            response=model.generate_content(f"""
Summarize the following Terms & Conditions into **short, simple bullet points**.
- Keep each bullet **under 20 words**.
- Focus on the **main points users need to know**.
- Avoid legal jargon, make it easy to read.
- Keep all sections like agreements, modifications, age, and intellectual property.
Text:
{text}
"""
)

            summary=response.text
            return Response({"summary":summary})
        except Exception as e:
            return Response({"error":str(e)},status=500)