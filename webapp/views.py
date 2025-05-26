from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Music
from django.core.paginator import Paginator

# Create your views here.

NUMROWS=10

@login_required
def index(request):
    return render(request, 'index.html')


def register(request):
    # if request.method != 'POST':
    #     form = MemberForm()
    # else:
    #     form = MemberForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.created_at = datetime.today().strftime('%Y-%m-%d')
    #         user.password = make_password(form.cleaned_data['password'])
    #         user.save()
    #         return HttpResponseRedirect(reverse('index'))
    #     else:
    #         print(form.cleaned_data.get("photo"))
    
    # context = {'form': form}

    return render(request, 'register.html')



@login_required
def logout_view(request):
    # if request.session.get("id_event", False):
    #     del request.session["id_event"]
    logout(request)
    return redirect('/accounts/login')


@login_required
def musics(request):
    """List all musics."""
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Musicas', 'url': reverse('musics')},
    ]
    try:
        musics = Music.objects.all()
        paginator = Paginator(musics, NUMROWS)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
    except Music.DoesNotExist:
        musics = None
        page_obj = None
    
    context = {
        'page_obj': page_obj, 
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'musics.html', context)

@login_required
def music_detail(request, music_id):
    """Show details of a specific music."""
    breadcrumbs = [
        {'name': 'Home', 'url': reverse('index')},
        {'name': 'Musics', 'url': reverse('musics')},
    ]
    music = get_object_or_404(Music, id=music_id)
    context = {'music': music, 'breadcrumbs': breadcrumbs}
    return render(request, 'music_detail.html', context)