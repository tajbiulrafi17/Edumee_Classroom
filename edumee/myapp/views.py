from django.shortcuts import render, redirect
from django.views import View
from .models import Student, Teacher, User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator


# Create your views here.

def index(request):
    return render(request, 'myapp/index.html')


#Register View
class TeacherRegister(View):
    def get(self,reqeust,*args,**kwargs):
        # is_teacher = Teacher.objects.filter(is_teacher= True)
        # if reqeust.user.is_authenticated and is_teacher:
        #     return redirect('t_dash')
        context ={

        }
        return render(reqeust,'myapp/t_register.html',context)
    
    def post(self,request,*args,**kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mail_check = User.objects.filter(email = email)
        if mail_check:
            messages.warning(request,'Already have an account. Please login!')
            return redirect('teacher_register')
        elif password1 != password2:
            messages.warning(request,'Sorry! Password didnot match.')
            return redirect('teacher_register')
        elif len(password1) < 5:
            messages.warning(request,'Password too short! Atleast 5 character nedeed.')
            return redirect('teacher_register')
        else:
            auth_info ={
                'email':email,
                'password':make_password(password1)
            }
            user = User(**auth_info)
            user.is_teacher = True
            user.save()
        user_obj = Teacher(user=user, name=name)
        user_obj.save()
        messages.success(request, 'Thanks for Signup ! Please Login')
        return redirect ('teacher_login')




class StudentRegister(View):
    def get(self,request,*args,**kwargs):
        # is_student = Student.objects.filter(is_student=True)
        # if request.user.is_authenticated and is_student:
        #     return redirect('s_dash')
        context ={
            
        }
        return render(request,'myapp/s_register.html',context)
    def post(self,request,*args,**kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        photo = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mail_check = User.objects.filter(email=email)
        if mail_check:
            messages.warning(request,'Already have an account. Please login!')
            return redirect('teacher_register')
        elif password1 != password2:
            messages.warning(request,'Sorry! Password didnot match.')
            return redirect('teacher_register')
        elif len(password1) < 5:
            messages.warning(request,'Password too short! Atleast 5 character nedeed.')
            return redirect('teacher_register')
        else:
            auth_info ={
                'email':email,
                'password':make_password(password1)
            }
            user = User(**auth_info)
            user.is_student = True
            user.save()
        user_obj = Student(user=user, name=name, photo=photo)
        user_obj.save()
        messages.success(request,'Thanks for Signup! Please Login')
        return redirect ('student_login')
    

#Login View
class TeacherLogin(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return redirect('')
        return render(request, 'myapp/t_login.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username = email, password=password)

        email_check = User.objects.filter(email = email)
        
        if not email_check :
                messages.warning(request, 'User Not found. Please Signup!!')
                return redirect('teacher_login')
        
        elif user is not None :
            check_teacher = User.objects.get(email = user)

            if check_teacher.is_teacher == True:
                login(request, user)
                return redirect('t_dash')
            
            elif check_teacher.is_student == False:
                messages.warning(request, 'You are an Admin. Login from Admin Panel!')
                return redirect('teacher_login')
            else:
                messages.warning(request, 'You are not a Teacher. Please Login as a Student!')
                return redirect('teacher_login')
        else:
            messages.warning(request, 'Wrong Password!!')
            return redirect('teacher_login')



class StudentLogin(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return redirect('')
        return render(request, 'myapp/s_login.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        email_check = User.objects.filter(email = email)
        
        if not email_check:
                messages.warning(request, 'User Not found. Please Signup!!')
                return redirect('student_login')
       
        elif user is not None:           
            check_teacher = User.objects.get(email = user)
            if check_teacher.is_student == True:
                login(request, user)
                return redirect('s_dash')
            elif check_teacher.is_teacher == False:
                messages.warning(request, 'You are an Admin. Login from Admin Panel!')
                return redirect('student_login')
            else:
                messages.warning(request, 'You are not a Student. Please Login as a Teacher!')
                return redirect('student_login')
        else:
            messages.warning(request, 'Wrong Password!!')
            return redirect('student_login')

#Logout View 
class LogoutView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('/')


#Dashboard View

class TeacherDashboard(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        user = request.user.teachers
        return render(request,'myapp/t_dashboard.html')

class StudentDashboard(View):
    @method_decorator(login_required(login_url='student_login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        user = request.user.students
        return render(request,'myapp/s_dashboard.html')   
    
