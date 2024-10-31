from django.shortcuts import render

# Create your views here.
def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("search")
    context = {'loginform': form}
    return render(request, 'register/my-login.html', context = context)

def register(request):
    form = CreateUserForm()

    if request.method == "POST": ##Checking to see whether data must be stored in the database
        form = CreateUserForm(request.POST) ##Posts values for all the fields to the database
        if form.is_valid():
            form.save() ##Saves to database

            return redirect("login")

    context = {'registerform':form}

    return render(request, 'register/register.html', context=context)

def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

def intro_view(request):
    return render(request, 'frontend/intro.html')
