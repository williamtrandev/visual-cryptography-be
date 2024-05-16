import base64
from io import BytesIO

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
from applications.tasks import task_generate_shares_from_color, task_combine_shares_from_color, \
    task_generate_shares_from_binary


from datetime import datetime

from django.http import HttpResponse


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)


@api_view(['POST'])
def api_encrypt_image(request):
    body = request.data
    image = body.get('image')
    image_type = body.get('image_type')
    print(image, image_type)
    if not image:
        return Response({'error': 'Image is empty'}, status=status.HTTP_400_BAD_REQUEST)
    input_image = Image.open(image)
    if image_type == 'color':
        share1, share2 = task_generate_shares_from_color(image=input_image)
    else:
        input_image = input_image.convert('1')
        share1, share2 = task_generate_shares_from_binary(image=input_image)
    return Response(data={'share1': share1, 'share2': share2}, status=status.HTTP_200_OK)


@api_view(['POST'])
def api_decrypt_image(request):
    body = request.data
    share1 = body.get('share1')
    share2 = body.get('share2')
    if not share1 or not share2:
        return Response({'error': 'Shares cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
    share1_data = base64.b64decode(share1)
    share1 = Image.open(BytesIO(share1_data))
    share2_data = base64.b64decode(share2)
    share2 = Image.open(BytesIO(share2_data))
    reconstructed_image = task_combine_shares_from_color(share1, share2)
    return Response({'reconstructed_image': reconstructed_image}, status=status.HTTP_200_OK)
