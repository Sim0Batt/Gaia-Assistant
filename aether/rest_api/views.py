from django.shortcuts import render
import sys
import os
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from datetime import datetime
import subprocess


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hello_vue(request):
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return Response(data)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_gaia_response_rapid(request, message):
    subprocess.run(["gnome-terminal", "--", "bash", "-c", f"python /home/simone/gaia/gaia_request_app.py 'gaia {message}'"])
    return Response(f"Resolved: {message}")

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_gaia_response_vocal(request, message):
    subprocess.run(["gnome-terminal", "--", "bash", "-c", f"python /home/simone/gaia/gaia_request_app.py '{message}'"])
    return Response(f"Resolved: {message}")


