from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
from .models import Summary
import os
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class HistoryView(APIView):

    def get(self, request):

        summaries = Summary.objects.all().order_by("-created_at")[:10]

        data = []

        for item in summaries:
            data.append({
                "title": item.title,
                "url": item.url,
                "summary": item.summary,
                "created_at": item.created_at
            })

        return Response(data)
    
# Create your views here.
class SummarizeView(APIView):
    def post(self,request):
        text=request.data.get("text","")
        url=request.data.get("url","")
        title=request.data.get("title","")
        if not text:
            return Response({"error":"No text provided"},status=400)

        cached=Summary.objects.filter(url=url).first()
        if cached:
            print("✅ Summary loaded from database")
            return Response({
                "summary":cached.summary,
                "cached":True
            })
        print("🤖 Calling Gemini...")
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

            Summary.objects.get_or_create(
                url=url,
                defaults={
                    "title":title,
                    "summary":summary
                }
            )
            return Response({"summary":summary,"cached":False})
        except Exception as e:
            import traceback

            print("\n========== ERROR ==========")
            traceback.print_exc()
            print("===========================\n")

            return Response({"error": str(e)}, status=500)