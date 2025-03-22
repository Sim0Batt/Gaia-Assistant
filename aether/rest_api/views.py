from django.shortcuts import render
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gaia import Gaia as g
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import subprocess


@api_view(['GET'])
def hello_vue(request):
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return Response(data)

@api_view(['GET'])
def get_gaia_response_rapid(request, message):
    subprocess.run(["gnome-terminal", "--", "bash", "-c", f"python /home/simone/gaia/gaia_request_app.py 'gaia {message}'"])
    return Response("GetResponse")

@api_view(['GET'])
def get_gaia_response_vocal(request, message):
    subprocess.run(["gnome-terminal", "--", "bash", "-c", f"python /home/simone/gaia/gaia_request_app.py '{message}'"])
    return Response("GetResponse")