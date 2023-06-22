import os
import re
import sys
import fileinput


#cd project_dj/eggmart && python manage.py startapp main



try:
    app_names = sys.argv[1]
    create_project = os.popen(f"cd project_dj && django-admin startproject {app_names}").read()
    print(f"[+] Membuat project {app_names}")   
    migrate_project = os.popen(f"python project_dj/{app_names}/manage.py migrate").read()
    create_main_project = os.popen(f"cd project_dj/{app_names} && python manage.py startapp main").read()
    print("[+] Memasang database dan membuat folder main")   
    file_views = f'project_dj/{app_names}/main/views.py'
    views_code = '''
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Tech with tim!")
'''
    
    urls_code = '''
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
'''
    
    create_main_urls = os.popen(f"touch project_dj/{app_names}/main/urls.py").read()
    
    # Membuka file dengan mode write
    with fileinput.FileInput(file_views, inplace=True) as file_views:
        for line in file_views:
            if line.strip() == '# Create your views here.':
                with open(f'project_dj/{app_names}/main/views.py', "a") as file_view:
                    file_view.write(views_code)
                    file_view.close()
    
    with open(f"project_dj/{app_names}/main/urls.py", "a") as file_urls:
        file_urls.write(urls_code)
        file_urls.close()
    
    print("[+] Modifikasi file pada folder main")   
    with open(f'project_dj/{app_names}/{app_names}/urls.py', 'r') as file_project_urls:
        content = file_project_urls.read()
        file_project_urls.close()
    
    updated_content = content.replace("from django.urls import path", "from django.urls import path, include")
    
    with open(f'project_dj/{app_names}/{app_names}/urls.py', 'w') as file_project_url:
        file_project_url.write(updated_content)
        file_project_url.close()
    
    with open(f'project_dj/{app_names}/{app_names}/urls.py', 'r') as file_project:
        content = file_project.read()
        file_project.close()
    
    pattern = r"urlpatterns\s*=\s*\[[^\]]*?\]"
    match = re.search(pattern, content, re.DOTALL)
    print(f"[+] Modifikasi file pada folder {app_names}")   
    if match:
        urlpatterns_content = match.group()
        updated_urlpatterns = re.sub(r"path\('admin/'\s*,\s*admin.site.urls\)", "path('', include('main.urls')),\n    path('admin/', admin.site.urls)", urlpatterns_content)
        updated_content = re.sub(pattern, updated_urlpatterns, content, flags=re.DOTALL)
        
        with open(f'project_dj/{app_names}/{app_names}/urls.py', 'w') as file_projects:
            file_projects.write(updated_content)
            file_projects.close()
    else:
        print("Unable to find urlpatterns in the file.")
    print("[+] Modifikasi berhasil project siap digunakan")   
        
except IndexError:
    print("Empty set")
    exit()
