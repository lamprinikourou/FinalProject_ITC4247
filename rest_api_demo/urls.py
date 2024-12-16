from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# A simple view for the root URL
def root_view(request):
    return HttpResponse("<h1>Welcome to the API</h1><p>Visit <a href='/api/'>/api/</a> for the API endpoints.</p>")

urlpatterns = [
    path('', root_view, name='root'), 
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  
]
 