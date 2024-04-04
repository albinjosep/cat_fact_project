from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import fetch_cat_fact

@api_view(['GET'])
def health_check(request):
    return Response(status=200)

@api_view(['GET', 'POST'])
def fetch_fact(request):
    if request.method == 'POST':
        # Queue an async task to fetch data
        fetch_cat_fact.send()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)


@api_view(['GET'])
def get_fact(request):
    # Logic to retrieve the latest cat fact
    # This can vary depending on how you store the fetched facts
    # For simplicity, assume there's a global variable to store the last fetched fact
    try:
        last_fact = fetch_cat_fact.get_result(blocking=False)
        if last_fact:
            return Response(last_fact[0])  # Return the first fact
    except Exception as e:
        pass

    return Response({'error': 'no_task_has_been_queued_yet'})

