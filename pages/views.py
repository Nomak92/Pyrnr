from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from scripts.models import Script, NewScriptForm
import os
import subprocess
import json


# Create your views here.

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect(scriptdash_view)
    else:
        return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect(request, 'home')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def newscript_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewScriptForm(request.POST)
        print(f'received data: {request.POST}')
        print(f'new form: {form}')
        if form.is_valid():
            print('form is valid')
            save_script = Script(name=request.POST['name'], description=request.POST['description'],
                                 content=request.POST['content'], user=request.user)
            print(f'script: {save_script}')
            save_script.save()
            print('script saved')
            return redirect(scriptdash_view)
        else:
            return render(request, 'newscript.html', {'form': form})
    elif request.method == 'GET':
        form = NewScriptForm()
    else:
        return HttpResponse(status=404)
    return render(request, 'newscript.html', {'form': form})


@login_required
def scriptdash_view(request, *args, **kwargs):
    script_list = Script.objects.filter(user_id=request.user.id)
    return render(request, "scriptdash.html", {'scripts': script_list})


@login_required
def deleter_view(request, *args, **kwargs):
    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        print(f'received data: {request_data}')
        request_script = Script.objects.filter(id__exact=request_data['script_id']).first()
        if not request_script:
            return HttpResponse(404)
        else:
            request_script.delete()
            return redirect(scriptdash_view)
    else:
        return HttpResponseBadRequest()
@login_required
def saver_view(request, *args, **kwargs):
    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        print(f'received data: {request_data}')
        request_script = Script.objects.filter(id__exact=request_data['script_id']).first()
        if not request_script:
            return HttpResponse(404)
        else:
            request_script.content = request_data['script_content']
            request_script.save()
            return HttpResponse('Script Saved', status=201)
    else:
        return HttpResponseBadRequest()


@login_required
def runner_view(request, *args, **kwargs):
    if request.method == 'POST':
        script = "runner_script.py"
        shell = "./venv/py/bin/python"
        request_data = json.loads(request.body.decode('utf-8'))
        with open(script, 'w') as f:
            f.write(request_data['script_content'])
            f.close()
        file_path = os.path.abspath(script)

        def _send_command(cmd):
            with subprocess.Popen(cmd, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  universal_newlines=True) as proc:
                result, err = proc.communicate()
                proc.wait()
                return result

        results = _send_command([shell, file_path]).encode('utf-8')
        print(results)
        os.remove(file_path)
        return HttpResponse(results, status=200)
    else:
        return HttpResponse(status=404)
