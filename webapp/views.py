from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Music, Event, Notice, Member, User, MusicMember
from django.core.paginator import Paginator
from .forms import RegisterForm, ProfileForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Count, Sum, F

# Create your views here.

NUMROWS=10

@login_required
def index(request):
    my_musics = MusicMember.objects.filter(member_id=request.user.id)
    num_my_musics = len(my_musics)
    musics = Music.objects.all().order_by("-created_at")
    num_musics = len(musics)
    delta = timedelta(days=30)
    start = datetime.today().strftime('%Y-%m-%d')
    end = (datetime.today()+delta).strftime('%Y-%m-%d')
    try: 
        last_event = Event.objects.filter(date__range=(start,end)).order_by("date")[0] # se não tiver evento vai dar erro
    except:
        last_event = Event.objects.all().order_by('date')[0]
    # como pegar a média das músicas ??? num_hits / num_total_hits / N * 100
    results = (MusicMember.objects
              .values('member_id')
              .annotate(dcount=Sum('hits'))
              .order_by()
            )
    
    summation = 0
    for result in results:
        summation += result['dcount']

    di = 0
    for music in my_musics:
        di += music.hits

    try:
        dc = summation / len(results) # desempenho coletivo
        di_dc = round((di / dc) * 100, 2)
    except Exception as e:
        print(e)
        di_dc = 0

    context = {
        'num_my_musics': num_my_musics,
        'num_musics': num_musics,
        'di_dc': di_dc,
        'last_music': musics[0],
        'last_event':last_event,
    }

    return render(request, 'index.html', context)

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
        my_musics = []
        musics = Music.objects.all()
        favorited_musics = MusicMember.objects.filter(favorited=True, member_id=request.user.id)
        for music in favorited_musics:
            my_musics.append(music.music.id)
        paginator = Paginator(musics, NUMROWS)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
    except Music.DoesNotExist:
        musics = None
        page_obj = None
    
    context = {
        'page_obj': page_obj, 
        'breadcrumbs': breadcrumbs,
        'my_musics': my_musics,
    }
    return render(request, 'musics.html', context)


@login_required
def favorited(request):
    """List all musics favorited."""
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Musicas Favoritas', 'url': reverse('musics')},
    ]
    try:
        my_musics = []
        favorited_musics = MusicMember.objects.filter(favorited=True, member_id=request.user.id)
        for music in favorited_musics:
            my_musics.append(Music.objects.get(id=music.music.id))
        paginator = Paginator(my_musics, NUMROWS)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
    except Music.DoesNotExist:
        my_musics = None
        page_obj = None
    
    context = {
        'page_obj': page_obj, 
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'favorited.html', context)

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


@login_required
def edit_password(request):
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('index')},
        {'title': 'Perfil', 'url': reverse('profile')},
        {'title': 'Editar Senha', 'url': None},
    ]
    try:
        logged_user = Member.objects.get(id=request.user.id)
    except Member.DoesNotExist:
        logged_user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        if  request.POST['new_password1'] == request.POST['new_password2']:
            logged_user.password = make_password(request.POST['new_password1'])
            logged_user.save()
            messages.success(request, "Senha alterada com sucesso!")
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, "As senhas não conferem. Tente novamente.")
            return HttpResponseRedirect(reverse('edit_password'))
        
    context = {'breadcrumbs':breadcrumbs }
    return render(request, 'edit_password.html', context)
        

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

@login_required
def favorite_music(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    try: 
        member = Member.objects.get(id=request.user.id)
    except:
        messages.error(request,"Por favor, conclua seu cadastro para usar essa função.")
        return HttpResponseRedirect(reverse('musics'))
    try:
        musicmember = MusicMember.objects.get(music_id=music_id, member_id=member.id)
    except:
        musicmember = MusicMember()
        musicmember.music_id = music.id
        musicmember.member_id = member.id
    
    if musicmember.favorited == True:
        musicmember.favorited = False
        messages.success(request, "Música removida de seus favoritos")
    else:
        musicmember.favorited = True
        messages.success(request, "Música salva em seus favoritos")

    musicmember.save()

    return HttpResponseRedirect(reverse('musics'))


@login_required
def listen_music(request):
    if request.method == "POST":
        music_id = request.POST.get("music_id", False)        
        music = get_object_or_404(Music, id=music_id)
        try: 
            member = Member.objects.get(id=request.user.id)
        except:
            messages.error(request,"Por favor, conclua seu cadastro para usar essa função.")
            return JsonResponse({"status": "Error"})
        try:
            musicmember = MusicMember.objects.get(music_id=music_id, member_id=member.id)
        except:
            musicmember = MusicMember()
            musicmember.music_id = music.id
            musicmember.member_id = member.id

        musicmember.hits = F("hits") + 1
        messages.success(request, "Ensaio confirmado com sucesso!")
        musicmember.save()
        return JsonResponse({"status": "Success"})

    
    