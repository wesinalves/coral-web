from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Music, Event, Notice, Member, User
from django.core.paginator import Paginator
from .forms import RegisterForm, ProfileForm
from datetime import datetime

# Create your views here.

NUMROWS=10

@login_required
def index(request):
    return render(request, 'index.html')

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
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Musics', 'url': reverse('musics')},
        {'title': 'Detalhes', 'url': None},
    ]
    music = get_object_or_404(Music, id=music_id)
    files = music.file_set.all()  # Assuming you have a File model related to Music
    context = {'music': music, 'breadcrumbs': breadcrumbs, 'files': files}
    return render(request, 'music_detail.html', context)

@login_required
def calendar(request):
    """Show calendar."""
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Agenda', 'url': None},
    ]

    events = Event.objects.all().order_by('-date')[:7]

    context = {'breadcrumbs': breadcrumbs, 'events': events}
    return render(request, 'calendar.html', context)

@login_required
def profile(request):
    """Show user profile."""
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Perfil', 'url': None},
    ]

    try:
        member = Member.objects.get(id=request.user.id)
    except Member.DoesNotExist:
        member = None

    
    context = {
        'breadcrumbs': breadcrumbs,
        'member': member,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Perfil', 'url': reverse('profile')},
        {'title': 'Editar Perfil', 'url': None},
    ]
    try:
        logged_user = Member.objects.get(id=request.user.id)
    except Member.DoesNotExist:
        logged_user = get_object_or_404(User, id=request.user.id)

    if request.method != 'POST':
        form = ProfileForm(instance=logged_user)
    else:
        form = ProfileForm(request.POST, instance=logged_user)
        if form.is_valid():
            user = form.save(commit=False)

            # quando ainda não há cadastro de membro
            try:
                member = Member.objects.get(email = form.cleaned_data['email'])
            except:
                member = Member(id=user.id)
                member.phone = form.cleaned_data['phone']
                member.birthday = form.cleaned_data['birthday']
                member.address = form.cleaned_data['address']
                member.suit = form.cleaned_data['suit']
                member.created_at = datetime.today().strftime('%Y-%m-%d')
                member.save()
            
            
            user.save()

            return HttpResponseRedirect(reverse('profile'))
        
    context = {'breadcrumbs':breadcrumbs, 'form': form}
    return render(request, 'edit_profile.html', context)
        

def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.created_at = datetime.today().strftime('%Y-%m-%d')
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.cleaned_data.get("formulário não é válido"))
    
    context = {'form': form}

    return render(request, 'register.html', context)
    