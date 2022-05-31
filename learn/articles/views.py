from audioop import reverse
from enum import auto
from shutil import register_unpack_format
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.urls import reverse
#from matplotlib.style import context
from articles.models import UserDetails, Category, Articles
from articles.fun import compute_sim_users, give_keywords, compute_sim_article
from django.contrib import messages
import datetime
#from datetime import datetime

def register(request):
    if request.method == "POST":
        emailid = request.POST['email']
        password = request.POST['password']
        fullname = request.POST['fullName']
        role = request.POST['role']
        interests = request.POST.getlist('i')
        usern = emailid
        a = User.objects.filter(username=usern)
        if(len(a)>0):
            return HttpResponse("This is Email id already registered<br>Please, <a href='login'>SignIN</a>")
        user = User.objects.create_user(usern,emailid,password)
        user.save()
        Ud = UserDetails.objects.create(user=user,fullName=fullname,role=int(role))
        for i in interests:
            loc = Category.objects.get(catid = int(i))
            Ud.interests.add(loc)
        Ud.save()
        login(request,user)
        return HttpResponseRedirect(reverse("home"))

    return render(request,"register.html")

def loginUser(request):
    if request.method == "POST":
        username = request.POST['usern']
        password = request.POST['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("home"))
       # else:

    return render(request,"login.html")

def home(request):
    popl = Articles.objects.order_by('-likes' ,'-pdate')[0]
    pd ={}
    pd['ptitle'] = popl.title 
    pd['pcon'] = popl.content.split('.')[0]
    pd['pcat'] = popl.cat.all()[0].name
    pd['pid'] = popl.id

    rec = Articles.objects.exclude(id=pd['pid']).order_by('-pdate')[0:2]
    rlist =[]
    for i in range(0,2):
        d ={}
        d['title']= rec[i].title 
        d['con'] = rec[i].content.split('.')[0]
        d['cat'] = rec[i].cat.all()[0].name
        d['id'] = rec[i].id
        d['date'] = rec[i].pdate.strftime("%b") + " " + rec[i].pdate.strftime("%d")
        rlist.append(d)

    if request.user.is_authenticated:
        x = request.user.username
        x= x.split('@')[0]
        interests = UserDetails.objects.get(user = request.user).interests.all()
        spcl = Articles.objects.exclude(id__in=(pd['pid'],rec[0].id,rec[1].id)).order_by('-pdate')
        c =0
        slist =[]
        for a in spcl:
            if a.cat.all()[0] in interests:
                c = c+1
                d ={}
                d['title']= a.title 
                d['con'] = a.content.split('.')[0]
                d['cat'] = a.cat.all()[0].name
                d['id'] = a.id
                d['date'] = a.pdate.strftime("%b") + " " + a.pdate.strftime("%d")
                slist.append(d)
            if c==2:
                break
        context = {"usern": x,
        'pd':pd,
        'rlist':rlist,
        'slist':slist
        }
        return render(request,"userhome.html",context)

    context = {
        'pd':pd,
        'rlist':rlist
        }
    
    return render(request,"home.html",context)

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def catdisplay(request,category):
    popl = Articles.objects.order_by('-likes' ,'-pdate')[0:5]
    plist = []
    for i in range(0,5):
        d ={}
        d['title']= popl[i].title 
        d['cat'] = popl[i].cat.all()[0].name
        d['id'] = popl[i].id
        plist.append(d)
    
    c = Category.objects.get(name=category).articles_set.all().order_by('-pdate')
    if request.user.is_authenticated:
        u = UserDetails.objects.get(user = request.user)
        usern = request.user.username
        usern= usern.split('@')[0]
        sim_users = compute_sim_users(u)
        ulist = []
        for i in sim_users:
            x = UserDetails.objects.get(id=i)
            diff = ((x.likes.all()).difference(u.likes.all())).order_by('-likes')
            for j in diff:
                d ={}
                d['title']= j.title 
                d['cat'] = j.cat.all()[0].name
                d['id'] = j.id
                if (d not in ulist) and (d not in plist):
                    ulist.append(d)
            if (len(ulist)>=4):
                break
        context = {"usern": usern, "alist":c,"cat":category,'plist':plist[0:3],'ulist':ulist[0:3]}
        return render(request,"ucatpage.html",context)
    context = { "alist":c,"cat":category,'plist':plist}
    return render(request,"catpage.html",context)

def articledisplay(request,category,aid):
    obj = Articles.objects.get(id= aid)
    l= obj.likes
    if request.method == "POST":
        if request.user.is_authenticated:
            ud = UserDetails.objects.get(user=request.user)
            if(request.POST.get('like', False)=='1'):
                if obj not in ud.likes.all():
                    obj.likes = l+1
                    obj.save()
                    ud.likes.add(obj)
                    ud.save()
            elif obj in ud.likes.all():
                obj.likes = l-1
                obj.save()
               # print("Happenning")
                ud.likes.remove(obj)
                ud.save()
        else:
            return HttpResponse("<h1>Glad that you liked the article :)<br>Please,<a href='../login'>LogIn</a> or <a href='../register'>Register</a><br>to give a like<h1>")

    title = obj.title
    writer = obj.writer
    content = obj.content 
    odate = obj.pdate
    date = odate.strftime("%B") + " " + odate.strftime("%d") + ", " + odate.strftime("%Y") 
    likes = obj.likes
    sim_article = compute_sim_article(obj)
    alist = []
    for i in sim_article:
        j = Articles.objects.get(id=i)
        d ={}
        d['title']= j.title 
        d['cat'] = j.cat.all()[0].name
        d['id'] = j.id
        alist.append(d)
    if request.user.is_authenticated:
        ud = UserDetails.objects.get(user=request.user)
        x = request.user.username
        x= x.split('@')[0]
        if obj in ud.likes.all():
            l = 1
        else:
            l = 0
        context = {'title':title,
                    'writer':writer,
                    'content':content,
                    'date':date,
                    'likes':likes,
                    "usern": x,
                    'line': l,
                    'alist':alist[0:5]}
        return render(request,"uarticlepage.html",context)
    context = {'title':title,
                'writer':writer,
                'content':content,
                'date':date,
                'likes':likes,
                'alist':alist[0:5]}
    return render(request,"articlepage.html",context)

def submit(request):
    if request.user.is_authenticated:
        if(request.method =="POST"):
            post = request.POST
            title = post['title']
            content = post['content']
            tags = give_keywords(content+" "+title)
            writer = UserDetails.objects.get(user=request.user).fullName
            cat = Category.objects.get(name=post['category'])
            
            u = authenticate(username=request.user.username,password=post['password'])
            if u is not None:
                a = Articles.objects.create(title=title,content=content,tags=tags,writer=writer)
                a.cat.add(cat)
                a.save()
                messages.success(request, 'Thankyou, Successfully submitted!')
            else:
                messages.warning(request, 'Wrong Password')
            #return HttpResponseRedirect(reverse('home'))
        cat = []
        obj = Category.objects.all()
        for i in obj:
            cat.append(i.name)
        context = {'emailid':request.user.email, 'cat':cat}
        return render(request,"submit.html",context)
    else:
        return HttpResponse("<h1>Oops! No access. Sorry.<br><a href='login'>LogIn</a> or <a href='register'>Register</a><h1>")

