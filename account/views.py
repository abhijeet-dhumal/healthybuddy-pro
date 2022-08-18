
from django import contrib
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.db.models import Q
from .filters import BlogFilter
from .forms import *
# create your views here 
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
# for flash message
from .decorators import *
from django.contrib import messages


def home(request):
    try:
        userdetails=User.objects.get(id=request.user.id)
    except:
        userdetails=request.user
    users_count=User.objects.all().count()
    doctor_count=User.objects.filter(user_type='Doctor').count()
    blog_count=Blog.objects.all().count()
    appointment_count=Appointment.objects.all().count()
    boolean=request.user.is_authenticated

    doctors=User.objects.filter(user_type='Doctor')[0:6]

    reviews=Review.objects.all()[0:6]
    contactform = ContactForm(request.POST)
    if request.method =='POST':
        print("came")
        name=request.POST.get('name')
        print(contactform)
        if contactform.is_valid():
            print("Not vaid")
            contactform.save()
            context={'userdetails':userdetails,'boolean':boolean,'users_count':users_count,'doctor_count':doctor_count,'blog_count':blog_count,'appointment_count':appointment_count,'doctors':doctors,'reviews':reviews,'contactform':contactform}
            messages.success(request, f'Entered contact data is saved for user {name}')

            return render(request,"account/home.html",context)

        else:
            messages.warning(request, f'Entered contact data is not saved for user {name}')

            context={'userdetails':userdetails,'boolean':boolean,'users_count':users_count,'doctor_count':doctor_count,'blog_count':blog_count,'appointment_count':appointment_count,'doctors':doctors,'reviews':reviews,'contactform':contactform}
            return render(request,"account/home.html",context)
    else:
        context={'userdetails':userdetails,'boolean':boolean,'users_count':users_count,'doctor_count':doctor_count,'blog_count':blog_count,'appointment_count':appointment_count,'doctors':doctors,'reviews':reviews,'contactform':contactform}
        return render(request,"account/home.html",context)

def home1(request):
    context={'current_user':request.user}
    return render(request,"account/base.html",context)


# import httplib2
# import os

# from apiclient import discovery
# import oauth2client
# from oauth2client import client
# from oauth2client import tools
# from oauth2client import file 

# import datetime

# tr
#     import argparse
#     flags = tools.argparser.parse_args([])
# except ImportError:
#     flags = None

# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/calendar-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/calendar'
# CLIENT_SECRET_FILE = 'C:\\Users\\aksha\\Downloads\\client_secret_web.json'
# APPLICATION_NAME = 'HealthManager'

# def get_credentials():
#     """Gets valid user credentials from storage.

#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.

#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'C:\\Users\\aksha\\OneDrive\\Desktop\\myform\\form\\calendar-python-quickstart.json')

#     store = oauth2client.file.Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#         else: # Needed only for compatibility with Python 2.6
#             credentials = tools.run(flow, store)
#         print('Storing credentials to ' + credential_path)
#     return credentials

    
# """Shows basic usage of the Google Calendar API.

# Creates a Google Calendar API service object and outputs a list of the next
#     10 events on the user's calendar.
# """

# # Refer to the Python quickstart on how to setup the environment:
# # https://developers.google.com/google-apps/calendar/quickstart/python
# # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# # stored credentials.



# from datetime import datetime, timedelta

def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

# @unauthenticated_user
def LoginForm(request):
    try:
        if request.method =='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email,password)
            user = authenticate_user(email, password)
            print(user)
            # user = authenticate(request, email= email , password = password)     
            if user is not None:
                login(request, user)
                return redirect('home')

    except Exception as e:
        messages.warning(request, f'{e}')
        return render(request,"account/LoginForm.html")             
    context={}
    return render(request,"account/LoginForm.html",context)


# @unauthenticated_user   
def registerPage(request):
#     f=open("C:\\Users\\aksha\\OneDrive\\Desktop\\myform\\form\\calendar-python-quickstart.json","r+")
#     f.truncate()
    if request.method=='POST':
        form1 = UserRegisterForm(request.POST)
        # doctor_reg_form = UserForm(request.POST)
        if form1.is_valid():
            form1.save()
            user = form1.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # doctor_reg_form = UserForm(request.POST,request.FILES,instance=profile)
            # doctor_reg_form.full_clean()
            # doctor_reg_form.save()
            name = User.objects.get(email=form1.cleaned_data.get('email')).name


            if form1.cleaned_data.get('user_type')=='Doctor':
            # to assign group name 
                group=Group.objects.get(name='Doctor')
                user.groups.add(group)
                
            if form1.cleaned_data.get('user_type')=='Patient':
            # to assign group name 
                group=Group.objects.get(name='Patient')
                user.groups.add(group)
            
            messages.success(request, 'Account is created for ' + name)

#             credentials = get_credentials()
#             http = credentials.authorize(httplib2.Http())
#             global service
#             service = discovery.build('calendar', 'v3', http=http)  

            return redirect('LoginForm')  
    else:
        form1 = UserRegisterForm()
        # doctor_reg_form = UserForm()           

    context = {}   
    context.update({'form1':form1}) 
    return render(request, 'account/registerPage.html',context)


# def create_event(start_time,patient,summary=None,duration=45,description=None,location=None):
#         # matches=list(datefinder.find_dates(start_time))
#         # if len(matches):
#         #     start_time=matches[0]
#     end_time=start_time + timedelta(minutes=duration)
#     timeZone='Asia/Kolkata'
#     event = {
#     'summary': f'Appointment with {patient.name}',
#     'location': 'Pune',
#     'description': description,
#     'start': {
#         'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
#         'timeZone': timeZone,
#     },
#     'end': {
#         'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
#         'timeZone': timeZone,
#     },
#     'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#     ],
#     # 'attendees': [
#     #     # {'email': 'abhijeetdhumal652@gmail.com'},
#     #     # {'email':'akshaydhumal652@'}
#     # ],
#     'reminders': {
#         'useDefault': False,
#         'overrides': [
#         {'method': 'email', 'minutes': 24 * 60},
#         {'method': 'popup', 'minutes': 10},
#         ],
#     },
#     }

#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print ('Event created: %s' % (event.get('htmlLink')))

# def dashboard(request,pk):
#     userdetails=User.objects.get(id=pk)
#     profiledetails=Profile.objects.get(id=pk)
#     current_user=request.user
#     context={'current_user':current_user,'userdetails':userdetails,'profiledetails':profiledetails}
#     return render(request, 'UserDashboard.html',context) 

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def afterloginhome(request):
    userdetails=User.objects.all()
    doctordetails=User.objects.filter(user_type='Doctor')
    patientdetails=User.objects.filter(user_type='Patient')
    current_user = request.user
    
    context={"userdetails":userdetails,"doctordetails":doctordetails,'patientdetails':patientdetails,"current_user":current_user}
    return render(request,"account/after_login_home.html",context)

@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def about(request):
    userdetails=User.objects.all()
    doctordetails=User.objects.filter(user_type='Doctor')
    patientdetails=User.objects.filter(user_type='Patient')
    current_user = request.user
    
    context={"userdetails":userdetails,"doctordetails":doctordetails,'patientdetails':patientdetails,"current_user":current_user}
    return render(request,"account/about.html",context)

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def usernames(request):
    userdetails=User.objects.all()
    doctordetails=User.objects.filter(user_type='Doctor')
    patientdetails=User.objects.filter(user_type='Patient')
    current_user = request.user
    
    context={"userdetails":userdetails,"doctordetails":doctordetails,'patientdetails':patientdetails,"current_user":current_user}
    return render(request,"account/doctorusername.html",context)

# @login_required
# @allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def first_page(request):
    try:
        pk=request.user.id
        userdetails=User.objects.get(id=pk)
        current_user=request.user
        boolean=request.user.is_authenticated
        context={"userdetails":userdetails,'boolean':boolean,'current_user':current_user}
        return render(request,"account/profile.html",context)
        
    except Exception as e:
        print(e)
        messages.warning(request, f'Something is wrong here, credentials might not be filled completely !!!')
        return render(request,"account/home.html")


@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def doctor_details(request,pk):
    userdetails=User.objects.get(id=pk)
    doctordetails=User.objects.filter(user_type='Doctor')
    current_user = request.user
    context={'userdetails':userdetails,"doctordetails":doctordetails,"current_user":current_user}
    return render(request,"account/doctor_userdetails.html",context)

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def patient_details(request,pk):
    userdetails=User.objects.get(id=pk)
    

    patientdetails=User.objects.filter(user_type='Patient').get(id=pk)
    
    context={'userdetails':userdetails,'patientdetails':patientdetails}
    return render(request,"account/patient_userdetails.html",context)

@login_required   
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def updateprofile(request):
    pk=request.user.id
    profiledetail=User.objects.get(id=pk)
    
    profileform=UserRegisterForm(instance=request.user)
    if request.method=='POST':
        profileform=UserRegisterForm(request.POST,instance=request.user)
        if profileform.is_valid():
            profileform.save()
            return redirect('first_page')
        else:
            messages.warning(request,f'Username or Password is incorrect !!! ')


    context={'profiledetail':profiledetail,'profileform':profileform}
    return render(request,"account/userdetailsform.html",context)

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UserForm

class CreateUserView(CreateView):
    model = User
    template_name = 'account/userdetailsform.html'
    form_class = UserForm

    def get_success_url(self):
        return '/userpage'

class CreateBlogView(CreateView):
    model = Blog
    template_name = 'account/blogs_update.html'
    form_class = BlogForm

    def get_success_url(self):
        return '/blogs_view'

class UpdateBlogView(UpdateView):
    model = Blog
    template_name = 'account/blogs_update.html'
    form_class = BlogForm

    def get_success_url(self):
        return '/blogs_view'

class UpdateUserView(UpdateView):
    model = User

    form_class = UserForm
    template_name = 'account/userdetailsform.html'
    success_url = '/userpage'

class DoctorListView(ListView):
    queryset = User.objects.filter(user_type = 'Doctor').all()
    model = User
    template_name = 'account/doctorusername.html'


def NotificationListView(request):
    details=Notification.objects.filter(user=request.user).all()
    boolean=request.user.is_authenticated

    context={"details":details,'boolean':boolean}
    return render(request,"account/notifications.html",context)

# class NotificationListView(ListView):
#     model = Notification
#     template_name = 'account/notifications.html'

#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Notification.objects.filter(user=request.user).all()
        
class CreateAppointmentSlotView(CreateView):
    model = AppointmentSlot
    template_name = 'account/appointment_slot_form.html'
    form_class = AppointmentSlotForm

    def get_success_url(self):
        return '/appointment_slots'

class UpdateAppointmentSlotView(UpdateView):
    model = AppointmentSlot
    template_name = 'account/appointment_slot_form.html'
    form_class = AppointmentSlotForm

    def get_success_url(self):
        return '/appointment_slots'


class CreateReviewView(CreateView):
    model = Review
    template_name = 'account/reviewsform.html'
    form_class = ReviewForm

    def get_success_url(self):
        return '/'

def AppointmentSlotListView(request):
    details=AppointmentSlot.objects.filter(user=request.user).all()
    current_user=request.user
    boolean=request.user.is_authenticated
   
    context={"details":details,'boolean':boolean}
    return render(request,"account/appointment_slot.html",context)

def deleteAppointmentSlot(request,pk=None):
    appointment_slot = AppointmentSlot.objects.get(id=pk)
    if request.method == 'POST':
        appointment_slot.delete()
        return redirect('appointment_slots')
    context={'item':appointment_slot}
    return render(request,'account/delete.html', context)
            
# class AppointmentListView(ListView):
#     model= Appointment

#     def get_context_data(self, **kwargs):
#         context = super(AppointmentListView, self).get_context_data(**kwargs)
#         classroom_blocks = Appointment.objects.all()
#         context = {'appointments': classroom_blocks}
#         return context
from django.shortcuts import render, get_object_or_404

def AppointmentListView(request):
    users_count=User.objects.all().count()
    doctor_count=User.objects.filter(user_type='Doctor').count()
    blog_count=Blog.objects.all().count()
    appointment_count=Appointment.objects.all().count()
    authenticated=request.user.is_authenticated
    if authenticated:
        try:
            userdetails=User.objects.get(id=request.user.id)
        except:
            userdetails=request.user
        details=Appointment.objects.filter(user=request.user).all()
        current_user=request.user
        boolean=True
        if  User.objects.get(id=current_user.id).user_type=='Patient':
            boolean=False
        context={"details":details,'doctor':boolean}
        return render(request,"account/appointments.html",context)
        
    else:
        messages.success(request, f'Please login first as a authenticated user !')
        
        context={'users_count':users_count,'doctor_count':doctor_count,'blog_count':blog_count,'appointment_count':appointment_count}
        return render(request,"account/home.html",context)

class CreateAppointmentView(CreateView):
    model = Appointment
    template_name = 'account/appointment_form.html'
    form_class = AppointmentForm

    def get_success_url(self):
        return '/appointments'

class UpdateAppointmentView(UpdateView):
    model = Appointment
    template_name = 'account/appointment_form.html'
    form_class = AppointmentForm

    def get_success_url(self):
        return '/appointments'


def deleteAppointment(request,pk=None):
    appointment= Appointment.objects.get(id=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_slots')
    context={'item':appointment}
    return render(request,'account/delete.html', context)



@login_required    
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def updatepatientdetails(request,pk):
    userdetail=User.objects.get(id=pk)
    profiledetail=User.objects.filter(user_type='Patient').get(id=pk)

    imgs=User.objects.filter(email=profiledetail.email,user_type='Patient')
    
    registerform=UserRegisterForm(instance=userdetail)
    profileform=User(instance=profiledetail)
    if request.method=='POST':
        registerform=UserRegisterForm(request.POST,instance=userdetail)
        profileform=User(request.POST,instance=profiledetail)
        if registerform.is_valid() and profileform.is_valid():
            registerform.save()
            profileform.save()
            return redirect('patientusernames')
        else:
            messages.warning(request,f'Username or Password is incorrect !!! ')


    context={'userdetail':userdetail,'profiledetail':profiledetail,'registerform':registerform,'profileform':profileform,'imgs':imgs}
    return render(request,"account/userdetailsform.html",context)

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def deletedoctordetails(request,pk):
    userdetails=User.objects.get(id=pk)
    
    if request.method=='POST':
        userdetails.delete()
        return redirect('usernames')

    return render(request,"account/delete.html",{'obj':userdetails})

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def deletepatientdetails(request,pk):
    userdetails=User.objects.get(id=pk)
    
    if request.method=='POST':
        userdetails.delete()
        return redirect('patientusernames')

    return render(request,"account/delete.html",{'obj':userdetails})

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')

def blogs_view(request):
    try:
        userdetails=User.objects.get(id=request.user.id)
    except:
        userdetails=request.user
    users_count=User.objects.all().count()
    doctor_count=User.objects.filter(user_type='Doctor').count()
    blog_count=Blog.objects.all().count()
    appointment_count=Appointment.objects.all().count()
    boolean=request.user.is_authenticated
    if boolean:
        userdetails=User.objects.get(id=request.user.id)
        blogdetail=Blog.objects.filter(draft=False).all()
        myFilter = BlogFilter(request.GET, queryset= blogdetail)
        blogdetail = myFilter.qs
        current_user=request.user
        
    else:
        messages.success(request, f'Please login first as a authenticated user !')
        
        context={'userdetails':userdetails,'boolean':boolean,'users_count':users_count,'doctor_count':doctor_count,'blog_count':blog_count,'appointment_count':appointment_count}
        return render(request,"account/home.html",context)

    context={'boolean':boolean,'userdetails':userdetails,'blogdetail':blogdetail,'current_user':current_user,'myfilter':myFilter,'doctor':boolean}
    return render(request,"account/blogs_view.html",context)

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def blogs_draft_view(request):
    blogdetail=Blog.objects.filter(draft=True).all()
    myFilter = BlogFilter(request.GET, queryset= blogdetail)
    blogdetail = myFilter.qs
    current_user=request.user
    boolean=True
    if User.objects.get(id=current_user.id).user_type=='Patient':
        boolean=False
    # imgs=Blog.objects.filter(title=blogdetail.title)

    
    context={'blogdetail':blogdetail,'current_user':current_user,'myfilter':myFilter,'doctor':boolean}
    return render(request,"account/blogs_draft_view .html",context)

@login_required
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def blogs_drafts(request):
    boolean=True
    blogdetail=Blog.objects.filter(draft=True).all()
    myFilter = BlogFilter(request.GET, queryset= blogdetail)
    blogdetail = myFilter.qs
    current_user=request.user
    # imgs=Blog.objects.filter(title=blogdetail.title)

    
    context={'blogdetail':blogdetail,'current_user':current_user,'myfilter':myFilter}
    return render(request,"account/blogs_drafts.html",context)


@login_required
@allowed_users(allowed_roles=['Admin','Doctor'])
def blogs_update(request):
    blogdetail=Blog.objects.all()
    blogform=BlogForm(request.POST)
    if request.method=='POST':
        if blogform.is_valid():
            action = blogform.cleaned_data.get('draft')
            if not action:
                blogform.save()
                return redirect('blogs_view')
            
        else:
            messages.warning(request,f'Username or Password is incorrect !!! ')
    
    context={'blogdetail':blogdetail,'blogform':blogform}
    return render(request,"account/blogs_update.html",context)


# for appointments 
@login_required    
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def doctorslist(request):
    userdetails=User.objects.all()
    
    doctordetails=User.objects.filter(user_type='Doctor').all()
    
    context={'userdetails':userdetails,"doctordetails":doctordetails}
    return render(request,"account/doctors_list.html",context)
    
@login_required  
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def appointment_form(request):
    current_user=request.user
    appointment_details=AppointmentForm(request.POST)
    if request.method=='POST':
        appointment_details=AppointmentForm(request.POST)
        if appointment_details.is_valid():
            appointment_details.save()
#             start_time=appointment_details.cleaned_data.get('Starttime_of_appointment')
#             end_time=start_time + timedelta(minutes=45)
#             patient=appointment_details.cleaned_data.get('patient')
#             speciality=appointment_details.cleaned_data.get('speciality')
#             print(start_time)
#             create_event(start_time,patient,"Appointment",45,f"Appointment with 'Mr/Ms.{patient.name}' regarding '{speciality}'-required speciality cure.")
            return redirect('appointments') 

    context={'current_user':current_user,"appointment_details":appointment_details}
    return render(request,"account/appointments_form.html",context)

@login_required   
@allowed_users(allowed_roles=['Admin','Doctor','Patient'])
def appointments(request):
    current_user=request.user
    appointment_details=Appointment.objects.all()

    context={'current_user':current_user,"appointment_details":appointment_details}
    return render(request,"account/appointments.html",context)
    
