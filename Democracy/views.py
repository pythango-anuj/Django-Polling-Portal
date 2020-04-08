from django.shortcuts import render, HttpResponse, redirect, render_to_response
from .forms import customuserform
from .models import UserVote, Opinion, CodeVote, Custom_User_Model
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

@login_required
def voting(request):
    return render(request, 'Democracy/voting_portal.html')


def registerview(request):
    if request.method == 'POST':
        form = customuserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Signin')
        else:
            return HttpResponse("!!Invalid Credential!!<br>"
                                "your password can't be too similar to your other personal information.")


def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('Home')

        else:
            return HttpResponse("Sorry! Your account in Permanentaly Disabled.")
    else:
        return render(request, 'Democracy/signin.html', {'message': 'Invalid Username or password'})



@login_required
def logoutview(request):
    if request.method == 'POST':
        logout(request)
        redirect('Home')


def save_response(request):
    if request.method == "POST":
        code_id = request.POST['bills']

        user_opinion = request.POST['opinion']
        comment = request.POST['comment']
        check_list = Opinion.objects.filter(username=request.user)

        flag = 0
        if (len(check_list) != 0):
            for obj in check_list:
                if obj.code_id == code_id:
                    flag = 1
                    break
        if flag == 1:
            return render(request, 'Democracy/voting_portal.html',
                          {'message': "Sorry!\nYou have already responded to this Law!"})
        else:
            opinion = Opinion()
            uservote = UserVote()

            opinion.username = request.user
            uservote.username = request.user
            opinion.code_id = code_id

            opinion.comment = comment

            if (user_opinion == 'True'):
                opinion.Yes = True
                uservote.Yes = True

            elif (user_opinion == 'False'):
                opinion.No = True
                uservote.No = True
            elif (user_opinion == 'None'):
                opinion.Do_Not_Know = True
                uservote.Do_Not_Know = True
            opinion.save()
            uservote.code_id = Opinion.objects.filter(username=request.user).filter(code_id=code_id).get(
                code_id=code_id)
            uservote.save()
            vote_count()
            return render(request, 'Democracy/voting_portal.html', {'message': "Thanks for giving your response!"})

def vote_count():
    CodeVote.objects.all().delete()
    sets=set()
    bills=Opinion.objects.all()
    for bill in bills:
        sets.add(bill.code_id)
    for item in sets:
        codevote = CodeVote()
        codevote.code_id = item
        codevote.yes=0
        codevote.no=0
        codevote.do_not_know=0
        vote_obj=Opinion.objects.filter(code_id=item)
        for obj in vote_obj:
            if(obj.Yes == True):
                codevote.yes+=1
            elif(obj.No == True):
                codevote.no+=1
            elif(obj.Do_Not_Know == True):
                codevote.do_not_know+=1
        codevote.save()



