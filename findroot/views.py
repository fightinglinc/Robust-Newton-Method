import json
from django.shortcuts import render, HttpResponse

from methods.newton_for_all_roots import find_all_roots
from methods.newton_method import main


def index(request):
    return render(request, "index.html")


def find_root(request):
    if request.method == 'POST':
        coefficients = request.POST.get('coefficients', None)
        real = request.POST.get('real', None)
        imagine = request.POST.get('imagine', None)
        if 'one-root' in request.POST:
            result = main(coefficients, real, imagine)

            if result.get('flag'):
                method = 'robust newton method'
            else:
                method = 'newton method'

            return render(request, 'result.html', {'start_point': result.get('start_point'),
                                                   'iterations': result.get('iteration'),
                                                   'root': result.get('root'),
                                                   'method': method,
                                                   'steps': result.get('steps'),
                                                   'errors': result.get('errors'),
                                                   })
        elif 'all-roots' in request.POST:
            result = find_all_roots(coefficients, real, imagine)

            return render(request, 'total-result.html', {'start_point': result.get('start_point'),
                                                         'iterations': result.get('total_iterations'),
                                                         'roots': result.get('roots'),
                                                         'steps': result.get('steps'),
                                                         'errors': result.get('errors'),
                                                         })

    return HttpResponse('Error')
