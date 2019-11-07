from django.shortcuts import render, redirect
from .models import Student

# Create your views here.



# def studentlist(request):

#     return render(request, 'students/studentlist.html')

def addstudent(request):
    return render(request, 'students/addstudent.html')

def studentadded(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    birthday = request.POST.get("birthday")
    age = request.POST.get("age")
    Student.objects.create(name=name, email=email, birthday=birthday, age=age)
    return redirect('/students/studentlist/')

def studentlist(request):
    students = Student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'students/studentlist.html', context)