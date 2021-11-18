import re
from rest_framework.response import Response
from rest_framework import status

class RandomURL(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request):
         if(re.match(r'/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g',request.data['url'])==False):
            data={}
            data["error"] = "A requisição precisa ser do tipo POST para que seja aceita"
            return Response(data = data, status = status.HTTP_400_BAD_REQUEST)
    
            