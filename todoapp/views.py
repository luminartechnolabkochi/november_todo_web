from django.shortcuts import render,redirect

# Create your views here.


from todoapp.forms import UserRegistrationForm,LoginForm,TodoForm,TodoChangeForm
from django.views.generic import CreateView,View,TemplateView,ListView,DetailView,UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from todoapp.models import Todos

#TEmplateView
#CreateView
#UpdateView
#ListView
#detailView
class SignUpView(CreateView):
    model=User
    form_class = UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})
        else:
            return render(request, "login.html", {"form": form})


class UserHome(TemplateView):
    template_name = "userhome.html"

class TodoCreateView(CreateView):
    model=Todos
    form_class = TodoForm
    template_name = "add_todo.html"
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=request.user
            todo.save()
            return redirect("home")
        else:
            return render(request,self.template_name,{"form":form})

class MyTodos(ListView):
    model = Todos
    template_name = "list_todos.html"
    context_object_name = "todos"

class TodoDetail(DetailView):
    model = Todos
    template_name = "todo_detail.html"
    context_object_name = "todo"
    pk_url_kwarg = "id"

class EditTodo(UpdateView):
    model = Todos
    form_class = TodoChangeForm
    template_name = "edit_todo.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("alltodos")

def remove_todo(request,id):
    todo=Todos.objects.get(id=id)
    todo.delete()
    return redirect("alltodos")
