import os
import mimetypes
from taskmanagement import models
from django.http import HttpResponse, HttpResponseRedirect


def getTCFile(request,file_id,extension):
  allow_access = True
  #if request.user.is_superuser:
  file_record = models.TaskCommentAttachment.objects.get(id=file_id)

  if allow_access == True:
      file_name_path = file_record.upload.path
      if os.path.isfile(file_name_path) is True:
              the_file = open(file_name_path, 'rb')
              the_data = the_file.read()
              the_file.close()
              if extension == 'msg':
                  return HttpResponse(the_data, content_type="application/vnd.ms-outlook")
              if extension == 'eml':
                  return HttpResponse(the_data, content_type="application/vnd.ms-outlook")


              return HttpResponse(the_data, content_type=mimetypes.types_map['.'+str(extension)])
  else:
              return

