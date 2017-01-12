from django.conf.urls import include, url
from docx2cwtex.views import uploadpage

urlpatterns = [
    url(r'^list/$', uploadpage, name='list'),
]
