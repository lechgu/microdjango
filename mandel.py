import sys
from io import BytesIO

import numpy as np
from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from PIL import Image


def mandelbrot(w, h, fro, to):
    x = np.linspace(fro.real, to.real, num=w).reshape((1, w))
    y = np.linspace(fro.imag, to.imag, num=h).reshape((h, 1))
    c = np.tile(x, (h, 1)) + 1j * np.tile(y, (1, w))

    z = np.zeros((h, w), dtype=complex)
    valid = np.full((h, w), True, dtype=bool)
    for i in range(128):
        z[valid] = z[valid] * z[valid] + c[valid]
        valid[np.abs(z) > 2] = False
    arr = np.flipud(1 - valid)
    return np.dstack([arr, arr, arr])


def generate(width, height):
    return mandelbrot(width, height, -2.25 - 1.25j, 0.75 + 1.25j)


# def index(request):
#     return HttpResponse("oh, hai")


def index(request, width=800, height=600):
    width = min(width, 1200)
    width = max(width, 100)
    height = min(height, 1024)
    height = max(height, 50)
    arr = generate(width, height)
    img = Image.fromarray(np.uint8(arr * 255), "RGB")
    bytes = BytesIO()
    img.save(bytes, "PNG")
    bytes.seek(0)
    return HttpResponse(bytes, content_type="image/png")


urlpatterns = [path("", index), path("generate/<int:width>/<int:height>", index)]

settings.configure(ROOT_URLCONF=__name__, ALLOWED_HOSTS=["*"])


app = get_wsgi_application()

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
