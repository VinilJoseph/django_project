from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Create your views here.
@login_required(login_url='signin')
@never_cache
def home(request):
    return render(request, "app1/index.html")


@never_cache
def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']            

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists!")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "Username too long !")

        if not fname.isalnum():
            messages.error(request, " First name must be alphanumeric !")

        if not lname.isalnum():
            messages.error(request, "Last name must be alphanumeric !")
        
        
        
        if pass1 != pass2:
            messages.error(request, "Password missmatch!")

        if not username.isalnum():
            messages.error(request, "User name must be alphanumerical !")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account is successfully created.")

        return redirect('signin')

    return render(request,"app1/signup.html")

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "app1/index.html", {'fname': fname})
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request,"app1/signin.html")


# ===============================
@never_cache
def admin_login(request):
    
    if request.user.is_authenticated:
        return redirect('admine')
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username,password=pass1)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admine')
        else:
            # If user doesn't exist or is not a superuser, show an error message
            # error_message = "Invalid credentials or insufficient privileges."

            # messages.error(request, "Invalid credentials or insufficient privileges.")
            return redirect('admin_login')
    return render(request, "app1/admin_login.html ")

@never_cache
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

@never_cache
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('admin_login')

@login_required(login_url='admin_login')
@never_cache
def admine(request):
    if request.user.is_authenticated:
        us = User.objects.all()
        context = {

            'us':us,
        }
        return render(request, "app1/admin.html",context)
    # else:
    #     return HttpResponse("The site is only accessible through admin_login page!")


def ADD(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        return redirect('admine')

    return render(request, "app1/admin.html")

def Edit(request):
    us = User.objects.all()
    context = {
        'us':us
    }
    return render(request,"app1/admin.html",context)


def Update(request,id):
    myuser = get_object_or_404(User, pk=id)
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']     

        myuser.username = username
        myuser.email = email
        myuser.first_name = fname
        myuser.last_name = lname

        # Change the password 
        if pass1:
            myuser.set_password(pass1)
        myuser.save()
        return redirect('admine')
    return redirect(request, 'app1/admin.html')

def Delete(request,id):
    us = User.objects.filter(id=id)
    us.delete()
    
    context = {
        'us':us,
    }
    return redirect('admine')
    # return redirect(request, 'app1/admin.html',context)

@never_cache
def search(request):
    query = request.GET['query']
    us = User.objects.filter(first_name__icontains = query)
    context = {'us':us}
    return render(request, 'app1/search.html', context )
    # return HttpResponse(" This is search")