from django.shortcuts import render, HttpResponse, redirect
from .forms import customuserform
from .models import UserVote, Opinion, CodeVote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'Democracy/home.html')


def signinview(request):
    return render(request, 'Democracy/signin.html')


def signupview(request):
    return render(request, 'Democracy/signup.html')


def aboutus(request):
    return render(request, 'Democracy/about.html')


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
            return render(request, 'Democracy/signup.html', {'message': 'Invalid Credential!!. '
                                                                        'Your UID should be a valid Aadhar Number!. '
                                                                        'Password should be of min 8 characters and not similar to any other credential!'})


def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('Home')

        else:
            return HttpResponse("Sorry! Your account is Permanently Dishabled.")
    else:
        return render(request, 'Democracy/signin.html', {'message': 'Invalid Username or password'})


@login_required
def logoutview(request):
    logout(request)
    print(request.user)
    return redirect('Home')


def save_response(request):
    if request.method == "POST":
        code_id = request.POST['bills']

        user_opinion = request.POST['opinion']
        user_comment = request.POST.get('comment')
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

            opinion.comment = user_comment

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
    sets = set()
    bills = Opinion.objects.all()
    for bill in bills:
        sets.add(bill.code_id)
    for item in sets:
        codevote = CodeVote()
        codevote.code_id = item
        codevote.yes = 0
        codevote.no = 0
        codevote.do_not_know = 0
        vote_obj = Opinion.objects.filter(code_id=item)
        for obj in vote_obj:
            if (obj.Yes == True):
                codevote.yes += 1
            elif (obj.No == True):
                codevote.no += 1
            elif (obj.Do_Not_Know == True):
                codevote.do_not_know += 1
        codevote.save()


vote_count()


def history(request):
    vote_list = UserVote.objects.filter(username=request.user)
    return render(request, 'Democracy/history.html', context={'vote_list': vote_list})


def result(request):
    if request.method == "POST":
        bill = request.POST['bill']
        count = CodeVote.objects.get(code_id=bill)
    return render(request, 'Democracy/result.html', context={'count': count})
