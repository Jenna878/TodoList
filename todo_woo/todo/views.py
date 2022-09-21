from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate
from .forms import TodoForm
from .models import Todo
from django.shortcuts import get_object_or_404
from django.utils import timezone

def home(request):
    return render(request, 'todo/home.html') 

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) 
                user.save()
                login(request, user) 
                return redirect('currenttodos') 
            except IntegrityError:
               return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Пользователь с таким именем уже зарегистрирован'}) 
        else:
            print('Ошибка!') 
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Пароль не совпадает'})

def currenttodos(request):
    # ! не подходит
    #todos = Todo.objects.all()

    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)  
    return render(request, 'todo/currenttodos.html', {'todos':todos}) 

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home') 

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()}) 
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 
            'error':'Такой пользователь не найден'}) 
        else:
            login(request, user)
            return redirect('currenttodos') 

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()}) 
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('currenttodos') 

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) 
    if request.method == 'GET':
        form = TodoForm(instance=todo) 
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form}) 
    else:
        form = TodoForm(request.POST, instance=todo) 
        form.save()
        return redirect('currenttodos')

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) 
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) 
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos') 

def completedtodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')  
    return render(request, 'todo/completedtodo.html', {'todos':todos}) 
    


    

 





