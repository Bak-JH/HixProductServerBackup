from django.shortcuts import render

error_messages = {
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Page Not Found',
    500: 'Server Error',
    }

def show_error(request, errcode, message=None):
    message = error_messages[errcode] if message is None else message
    print(message)
    return render(request, 'error/error_page.html', status=errcode, 
                              context={'status': errcode, 'message': message})