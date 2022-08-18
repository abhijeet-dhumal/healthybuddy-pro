from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.views.static import serve 

urlpatterns = [
    path('', views.home,name="home"),
    path('base/', views.home1,name="base"),
    path('login/', views.LoginForm,name="LoginForm"),
    path('signup/', views.registerPage,name="registerPage"),
    # path('user_dashboard/', views.dashboard,name="dashboard"),
    path('logout/', views.logoutuser, name ='logoutuser'),
    path('home/', views.DoctorListView.as_view(),name="home_page"),
    path('notifications/', views.NotificationListView,name="notifications"),
    path('about/', views.about,name="about"),
    path('userpage/', views.first_page,name="first_page"),
    path('usernames/', views.usernames,name="usernames"),

    path('doctor_userdetails/<str:pk>/', views.doctor_details,name="doctordetails"),
    path('patient_userdetails/<str:pk>/', views.patient_details,name="patientdetails"),
    path('update_profile/',views.updateprofile,name="updatedetails"),
     path('users/<int:pk>/', UpdateUserView.as_view(), name='users-update'),
    # path('update_patient_details/<str:pk>/',views.updatepatientdetails,name="updatepatientdetails"),
    path('delete_doctor_details/<str:pk>/',views.deletedoctordetails,name="deletedoctordetails"),
    path('delete_patient_details/<str:pk>/',views.deletepatientdetails,name="deletepatientdetails"),

    path('blogs_view/',views.blogs_view,name="blogs_view"),
    path('blogs_drafts/',views.blogs_draft_view,name="blogs_drafts"),
    path('blogs_update/',views.blogs_update,name="blogs_update"),
    path('blog/update/<int:pk>/', UpdateBlogView.as_view(), name='blog-update'),
    path('blog/create/', CreateBlogView.as_view(), name='blog-create'),

    path('appointment_slots/', views.AppointmentSlotListView,name="appointment_slots"),
    path('appointment_slot/create/', CreateAppointmentSlotView.as_view(), name='appointment_slot-create'),
    path('appointment_slot/update/<int:pk>/', UpdateAppointmentSlotView.as_view(), name='appointment_slot-update'),
    path('appointment_slot/delete/<int:pk>/', views.deleteAppointmentSlot, name='appointment_slot-delete'),

    path('appointments/', views.AppointmentListView,name="appointments"),
    path('appointment/create/', CreateAppointmentView.as_view(), name='appointment-create'),
    path('appointment/update/<int:pk>/', UpdateAppointmentView.as_view(), name='appointment-update'),
    path('appointment/delete/<int:pk>/', views.deleteAppointment, name='appointment-delete'),

    path('doctors_list/', views.DoctorListView.as_view(),name="doctorslist"),
    path('review/create/', CreateReviewView.as_view(), name='review-create'),
    
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)