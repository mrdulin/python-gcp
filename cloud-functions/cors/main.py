
from flask import json


def cors_enabled_function(request):
    # Set CORS headers for preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
    }

    return (json.dumps({'status': 'sucess'}), 200, headers)


# Deploy
# 1. cd cloud-functions/cors
# 2. gcloud functions deploy cors_enabled_function --runtime python37 --trigger-http --allow-unauthenticated
