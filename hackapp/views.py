import os
from django.conf import settings
from django.shortcuts import render

def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        file_path = os.path.join(settings.BASE_DIR, 'media', image.name)
        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return render(request, 'success.html')
    return render(request, 'image.html')
