import os
import subprocess
from django.shortcuts import render
from .forms import ReviewForm


def run_pylint(code):
    try:
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        if not code.endswith('\n'):
            code += '\n'
        project_directory = os.path.dirname(os.path.abspath(__file__))
        temp_filename = os.path.join(project_directory, 'users_code.py')
        with open(temp_filename, 'w', newline='\n') as file:
            file.write(code)
        pylint_output_bytes = subprocess.check_output(
            ['pylint', temp_filename],
            stderr=subprocess.STDOUT
        )
        pylint_output = pylint_output_bytes.decode('utf-8')
    except subprocess.CalledProcessError as e_e:
        pylint_output = e_e.output.decode('utf-8')
    finally:
        os.remove(temp_filename)
    return pylint_output


def home(request):
    pylint_output = None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            code_to_review = form.cleaned_data['code']
            pylint_output = run_pylint(code_to_review)
    else:
        form = ReviewForm()
    return render(request, 'code_review.html', {'form': form, 'pylint_output': pylint_output})
