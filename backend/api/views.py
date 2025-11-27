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


            response = model.generate_content(f"""
Summarize the following Terms and Conditions for a non-legal reader.
- Include **only the 6 most essential points**.
- Use **short, 1-line sentences** per point.
- Format as **HTML**:
    - Bold only the "⚠️ Risk:" label: <b>⚠️ Risk:</b>
    - Keep other icons normal: ℹ️ Info:, ✅ Allowed:
    - Each point should be on a **new line** using <br> at the end
- Do not use <ul>, <li>, or Markdown (*)
- Headings optional: <h3>...</h3>
- Keep it concise, readable, and actionable.

Text:
{text}
""")


            summary=response.text
            return Response({"summary":summary})
        except Exception as e:
            return Response({"error":str(e)},status=500)