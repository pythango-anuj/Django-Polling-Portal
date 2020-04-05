from django.shortcuts import render, HttpResponse, redirect,render_to_response
from .forms import customuserform
from .models import Vote,Laws
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
def home(request):
    return render(request, 'Democracy/home.html')


def signinview(request):
    return render(request, 'Democracy/signin.html')


def signupview(request):
    return render(request, 'Democracy/signup.html')


def aboutus(request):
    return render(request, 'Democracy/about.html')


def Services(request):
    return render(request, 'Democracy/services.html')


def blog(request):
    return render(request, 'Democracy/blog.html')


def contact(request):
    return render(request, 'Democracy/contact.html')


def loginview(request):
    cn=0
    cy=0
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('Home')

        else:
            return HttpResponse("Sorry! Your account in Permanentaly Dishabled.")
    else:
        return render(request, 'Democracy/signin.html', {'message': 'Invalid Username or password'})


def registerview(request):
    if request.method == 'POST':
        form = customuserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Signin')
        else:
            return HttpResponse("!!Invalid Credential!!<br>"
                                "your password can't be too similar to your other personal information.")

@login_required
def logoutview(request):
    if request.method =='POST':
        logout(request)
        redirect('Home')

def count(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        vote_objects = Vote.objects.get_or_create(id=id)
        opinion = request.POST.get('opinion')
        if opinion:
            vote_objects.yes = vote_objects.yes + 1
            vote_objects.save()

@login_required
def voting(request):
    return render(request, 'Democracy/voting_portal.html')


def save_response(request):
    cy=0
    cn=0
    if request.method == "POST":
        law_code = request.POST['bills']
        user_opinion = request.POST['opinion']
        comment = request.POST['detail']
        user = request.user
        print(user_opinion, user)

        created = Laws.objects.filter(user=user)
        #law_obj = created.all().filter(law_code=law_code)
        k=0
        if len(created)!=0:
            for obj in created:
                if int(obj.law_code) == int(law_code):
                    k = 1
                    break
        if k==1:
            return render(request, "Democracy/voting_portal.html", {"message":'you have already voted for this law'})
        else:
            law_obj = Laws()
            law_obj.law_code = law_code
            law_obj.user = user
            law_obj.save()

            if user_opinion:
                cy+=1
            else:
                cn+=1
            return render(request, "Democracy/voting_portal.html", {'message':"your vote is recorded"})

def fun():
    pass