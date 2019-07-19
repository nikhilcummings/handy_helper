from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job, Categories
import bcrypt
from itertools import chain
from operator import attrgetter

def index(request):
    return render(request, 'handyHelper/index.html')

def register(request):
    if request.method == 'POST':
        isValid = True
        data = request.POST.dict()
        fName = data.get('first_name')
        lName = data.get('last_name')
        email = data.get('email')
        pw = data.get('pw')
        cpw = data.get('cpw')
        errors = User.objects.basic_validator(request.POST)
        hash1 = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        if errors['fName']:
            messages.error(request, errors['fName'], extra_tags='fName')
            isValid = False
        if errors['lName']:
            messages.error(request, errors['lName'], extra_tags='lName')
            isValid = False
        if errors['email']:
            messages.error(request, errors['email'], extra_tags='email')
            isValid = False
        if errors['pw']:
            messages.error(request, errors['pw'], extra_tags='pw')
            isValid = False
        if errors['cpw']:
            messages.error(request, errors['cpw'], extra_tags='cpw')
            isValid = False
        if isValid == False:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/login')
        else:
            newUser = User.objects.create(first_name=fName,last_name=lName,email=email,password=hash1)
            request.session['id'] = newUser.id
            return redirect('/home')

def login(request):
    if request.method == 'POST':
        errors = {}
        data = request.POST.dict()
        user = User.objects.filter(email=data.get('loginEmail'))
        login = False
        if len(user) < 1:
            errors['loginFail'] = 'Email address is not registered'
            messages.error(request, errors['loginFail'], extra_tags='logFail')
        else:
            errors['loginFail'] = 'Password validation failed'
            if bcrypt.checkpw(data.get('loginPW').encode(), user[0].password.encode()):
                request.session['id'] = user[0].id
                print(user[0].id)
                login = True
                errors = {}
                return redirect('/home')
            messages.error(request, errors['loginFail'], extra_tags='pwFail')
        return redirect('/login')

def home(request):
    user = User.objects.get(id=request.session['id'])
    fn = user.first_name
    jobs = Job.objects.all().order_by('-created_at')
    ownedJobs = Job.objects.filter(owned_by=user)
    context ={
        'user': user,
        'fn': fn,
        'jobs': jobs,
        'ownedJobs': ownedJobs,
    }
    return render(request, 'handyHelper/home.html', context)

def newJob(request):
    return render(request, 'handyHelper/newjob.html')

def createJob(request):
    if request.method == 'POST':
        is_valid = True
        data = request.POST.dict()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        user = User.objects.get(id=request.session['id'])
        admin = User.objects.get(id=4)
        errors = Job.objects.basic_validator(request.POST)      
        print(errors['description'])
        if errors['title']:
            messages.error(request, errors['title'], extra_tags='fName')
            is_valid = False
        if errors['description']:
            messages.error(request, errors['description'], extra_tags='fName')
            is_valid = False
        if errors['location']:
            messages.error(request, errors['location'], extra_tags='fName')
            is_valid = False
        if is_valid == True:
            newJob = Job.objects.create(title=title,description=description,location=location,posted_by=user,owned_by=admin)
            if request.POST.get('home', False):
                category= Categories.objects.create(title='Home')
                category.attached_to.add(newJob)
                print(newJob.categories.all())
            if request.POST.get('petcare', False):
                category= Categories.objects.create(title='Pet Care')
                category.attached_to.add(newJob)
                print(newJob.categories.all())
            if request.POST.get('outdoor', False):
                category= Categories.objects.create(title='Outdoor')
                category.attached_to.add(newJob)
                print(newJob.categories.all())
            if request.POST.get('other', False):
                category= Categories.objects.create(title=request.POST.get('otherInput'))
                category.attached_to.add(newJob)
                print(newJob.categories.all())                
            return redirect('/home')
    return redirect('/home/newjob')

def addJob(request, jobID):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id=jobID)
    user.jobs_owned.add(job)
    return redirect('/home')

def removeJob(request, jobID):
    job = Job.objects.get(id=jobID)
    job.delete()
    return redirect('/home')

def editJob(request, jobID):
    job = Job.objects.get(id=jobID)
    user = User.objects.get(id=request.session['id'])
    context = {
        'title': job.title,
        'description': job.description,
        'location': job.location,
        'id': job.id,
        'user': user
    }
    return render(request, 'handyHelper/edit.html', context)

def updateJob(request, jobID):
    if request.method == 'POST':
        data = request.POST.dict()
        job = Job.objects.get(id=jobID)
        is_valid = True
        errors = Job.objects.basic_validator(request.POST) 
        if errors['title']:
            messages.error(request, errors['title'], extra_tags='fName')
            is_valid = False
        if errors['description']:
            messages.error(request, errors['description'], extra_tags='fName')
            is_valid = False
        if errors['location']:
            messages.error(request, errors['location'], extra_tags='fName')
            is_valid = False
        if is_valid == True:
            job.title = data.get('title')
            job.description = data.get('description')
            job.location = data.get('location')
            job.save()
            return redirect('/home')
    return redirect('/home/editjob/'+jobID)

def view(request, jobID):
    job = Job.objects.get(id=jobID)
    fn = User.objects.get(id=request.session['id']).first_name
    if len(job.categories.all())>0:
        categories = job.categories.all()
    context = {
        'job': job,
        'fn': fn,
        'categories':categories
    }
    return render(request, 'handyHelper/view.html', context)

def giveUpJob(request, jobID):
    job = Job.objects.get(id=jobID)
    admin = User.objects.get(id=4)
    print('user' ,admin.id)
    job.owned_by = admin
    job.save()
    return redirect('/home')

def finishJob(request, jobID):
    job = Job.objects.get(id=jobID)
    job.delete()
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/login')