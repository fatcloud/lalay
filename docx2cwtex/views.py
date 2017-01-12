from django.shortcuts import render
from django.http import HttpResponse


from docx2cwtex.process_docx import docx2cwtex

from wsgiref.util import FileWrapper
from django.core.files.base import ContentFile

from django.core.files import File
from django.views.static import serve
from os.path import basename, getsize


def uploadpage(request):
    # Handle file upload
    if request.method == 'POST':
        
        docxfile = request.FILES['docxin']
        try:
            cw = docx2cwtex(docxfile)
        except:
            return HttpResponse(docxfile.name + " 這檔案業障太深，淨化不來。")
        cwTexfile = ContentFile(cw)
        
        filename = '/home/cloud/Github/lalay/media/README.md'
        wrapper = FileWrapper(File(cwTexfile))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=' + docxfile.name + '.txt'
        # response['Content-Length'] = getsize(filename)
        return response

    # Render list page with the documents and the form
    return render(
        request,
        'uploadpage.html',
        {}
    )
