from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
# Create your views here.



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def registration(request):
    uf=userform()
    pf=profileform()
    d={'uf':uf,'pf':pf}
    if request.method=="POST" and request.FILES:
        ud=userform(request.POST)
        pd=profileform(request.POST,request.FILES)
        print(1)
        if ud.is_valid() and pd.is_valid():
            pw=ud.cleaned_data['password']
            USO=ud.save(commit=False)
            USO.set_password(pw)
            USO.save()
            print(2)
            PDO=pd.save(commit=False)
            PDO.user=USO
            PDO.save()
            print(3)
            send_mail('reg',
                      'success',
                      'vaddinagarjuna22@gmail.com',
                      [USO.email],
                      fail_silently=False) 
            
            return HttpResponse('registration succssfuly.................................................')
            
    return render(request,'registration.html',d)


def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            username=request.session.get('username')
            return HttpResponseRedirect(reverse('home'))
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def change_password(request):
    if request.method=='POST':
        un=request.session.get('username')
        np=request.POST['npw']
        USO=User.objects.get(username=un)
        USO.set_password(np)
        USO.save()
        import random
        otp=0
        for i in range(5):
            x=random.randrange(0,9)
            otp=otp*10+x
            
        send_mail('VERIFICATION OF OTP',f'OPT no is {otp}','vaddinagrjuna22@gmail.com',[User.email],fail_silently=False)
        
        
        return HttpResponseRedirect(reverse('otp'))
        
        
    
        
        
    return render(request,'change_password.html')
def forgot_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        useo=User.objects.filter(username=username)
        if useo :
            useo[0].set_password(password)
            useo[0].save()
            return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('username is not avaliable in database .........')
    return render(request,'forgot_password.html')



'''
def otp(request):
    if request.method=='POST':
        useotp=request.POST['otp']
        ud=int(useotp)
        if otp==ud:
            
    return render(request,'otp.html')
'''
    
    