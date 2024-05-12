from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, GetTutorForm, BecomeTutorForm, LoginForm, TutorUpdateForm, PaymentInformationForm
from . models import Tutor, GetTutor, Blog, JobStatus, Review, PaymentInformation
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from hashids import Hashids
def send_email(subject, message, recipient_list):
    """
    Function to send email using Gmail SMTP server.
    :param subject: Subject of the email
    :param message: Email message
    :param recipient_list: List of recipients' email addresses
    :return: True if the email was sent successfully, False otherwise
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def home(request):
    # maths_tutors = Tutor.objects.filter(subject_tutored = "Mathematics")
    return render(request, "home.html")

def becomeatutor(request):
    return render(request, "becomeatutor.html")

class BlogListView(ListView):
    model = Blog   
    template_name = "blog.html"

class BlogDetailView(DetailView):
    model = Blog   
    template_name = "viewblogpost.html"

def post_single(request, blog):  
    blog = get_object_or_404(Blog, slug=blog) 
    return render(request, "viewblogpost.html", {'blog':blog})

def contact(request):
    submitted = False
    if request.method == 'POST':
      form = MessageForm(request.POST)
      if form.is_valid():         
          form.save()
          name = form.cleaned_data['fullname']
          email = form.cleaned_data['email']
          contactnumber = form.cleaned_data['contactnumber']
          message = form.cleaned_data['message']

          send_email("Thank You for Contacting GreatMindz", "Thanks For Contacting Us.", [email])

          admin_email = 'mosianets@gmail.com'

          send_email("New Contact Form Submission", f"A new message has been received from {name} ({email}).\n\nMessage: {message}", [admin_email])
      
          return HttpResponseRedirect('/contact?submitted=True')
        
      else:
          messages.error(request, f'Na na na')
          return redirect('contact')

    else:
        form = MessageForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "contact.html", {'form':form, 'submitted':submitted})

def about(request):
    return render(request, "about.html")

def getatutor(request):
    submitted = False
    if request.method == 'POST':
        form = GetTutorForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            name = instance.first_name 
            email = instance.email
            mobile = instance.mobile
            physical_address = instance.street_address

            form.save()

            send_email("Thank You for using GreatMindz", "Thank you for reaching out to us. We will get back you in no time", [email])

            admin_email = 'mosianets@gmail.com'

            send_email("New Get Tutor Request", f"Hello Admin,\n\n"\
                "A new tutor request has been received:\n\n"\
                f"Name: {name}\n"\
                f"Email: {email}\n"\
                f"Mobile Number: {mobile}\n"\
                f"Physical Address: {physical_address}\n\n"\
                "Please review and respond accordingly.\n\n"\
                "Thank you.\n\n"\
                "Best regards,\n"\
                "GreatMindz Team",
                [admin_email])
            
            messages.success(request, f'Thank you for reaching out to us. We will get back to you in no time')
            return redirect('getatutor')
        else:
            messages.error(request)    
    else:
        form = GetTutorForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "getatutor.html", {'form':form, 'submitted':submitted})

#def activate(request, uidb64, to_email):
 #   return redirect('home')


#def activateEmail(request, user, to_email):
    #mail_subject = "Activate your user account."
   # message = render_to_string("template_activate_account.html", {
      # 'user': user.username,
      # 'domain': get_current_site(request).domain,
      # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
      # 'token': account_activation_token.make_token(user),
      # 'protocol': 'https' if request.is_secure() else 'http'
  #  })
  #  email = EmailMessage(mail_subject, message, to = [to_email])
  #  if email.send():
      #  messages.success(request, f'Dear {user}, please go to your email inbox and click on \
                    # received activation link to confirm and complete registration' )
   # else:
       # messages.error(request, f'Problem sending email to your email. Check if typed correctly')

def confirmEmail(request,encoded_email):
    if encoded_email=='':
        return render(request, "404.html")
    
    email=hashids.decode(encoded_email)[0]
    Tutor.objects.filter(email=email).update(is_completed=True)

    return render(request, "application_completed.html")
def tutorapplication(request):
    context = {}
    if request.method == 'POST':
        form = BecomeTutorForm(request.POST, request.FILES)
        if form.is_valid():
          instance = form.save()
          name = instance.first_name
          email = instance.email
          base_url=request.get_host()
          email_encoded=hashids.encode(email)
          confirm_link=base_url+"/confirm-email/"+email_encoded
          send_email(f"Profile Creation", "Your profile has been created successfully please confirm your email to complete application by clicking this \n <a href='{confirm_link}'>confirm email</a>", [email])

          admin_email = 'mosianets@gmail.com'

          send_email("Tutor Approval Request", f"Hello Admin,\n\n"\
          f"{name} has submitted a request to become a tutor on the website.\n\n"\
          "Please review their profile and approve their request.\n\n"\
          "Thank you.\n\n"\
          "Best regards,\n"\
          "GreatMindz Team", [admin_email])           
          return redirect('home')
        context['tutor_form'] = form
    else:
        form = BecomeTutorForm()
        context['tutor_form'] = form

    return render(request, "tutorapplication.html", context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')   
        else:
            context['login_form'] = form        
        
    else:
        form = LoginForm()
        context['login_form'] = form
    return render(request, "login.html", context)

def alltutors(request):
    tutors = Tutor.objects.filter(is_approved=True).filter(is_active=True) 
    for tutor in tutors:
        first_name_letter = tutor.first_name[0]
        last_name_letter = tutor.last_name[0] 
        subjects = tutor.subject_tutored
    online_tutors = Tutor.objects.filter(can_tutor_online='1')
    return render(request, "alltutors.html", {'tutors': tutors, 'online_tutors':online_tutors, 'first_name_letter':first_name_letter,'last_name_letter':last_name_letter, 'subjects':subjects})


def logout_view(request):
    logout(request)
    return redirect('login')
from django.core.exceptions import ObjectDoesNotExist
def dashboard(request):      
    try:
        validcolor = JobStatus.objects.first()
        validjobs = validcolor.gettutor_set.all()
        number_of_jobs = validjobs.count()  

        payment_information = PaymentInformation.objects.get(tutor=request.user)
    except ObjectDoesNotExist:
        
        return redirect('payment_info')
    
    return render(request, "tutordashboard.html", {'valid_jobs':validjobs, 'number_of_jobs':number_of_jobs, 'payment_information':payment_information})

def payment_info(request):
    tutor = request.user
    try:
        payment_info = PaymentInformation.objects.get(tutor=tutor)
        form = PaymentInformationForm(request.POST or None, instance=payment_info)
    except PaymentInformation.DoesNotExist:
        form = PaymentInformationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            payment_info = form.save(commit=False)
            payment_info.tutor = tutor
            payment_info.save()

            send_email("Payment Information Updated", f"Hello {request.user.first_name},\n\n"\
           "We're happy to inform you that your payment information has been successfully updated.\n"\
           "Thank you for keeping your details current.\n"\
           "Please send an email to notify the GreatMindz team.\n\n"\
           "Best regards,\n"\
           "GreatMindz Team",
           [request.user.email])

            admin_email = 'mosianets@gmail.com'

            send_email("Payment Information Updated", f"Hello Admin,\n\n"\
           f"The payment information for tutor {request.user.first_name} {request.user.last_name} has been updated.\n"\
           "Please review the changes and ensure all information is accurate.\n\n"\
           "Best regards,\n"\
           "GreatMindz Team",
           [admin_email])
            

            return redirect('dashboard')
    
    return render(request, 'payment_info.html', {'form': form})

def available_jobs(request):
    validcolor = JobStatus.objects.first()
    validjobs = validcolor.gettutor_set.all()
    number_of_jobs = validjobs.count()   

    return render(request, "availablejobs.html", {'valid_jobs':validjobs, 'number_of_jobs':number_of_jobs})

def myjobs(request):       
        tutor_name = Tutor.objects.filter(request.user == request.user)
        tutor_jobs = tutor_name.gettutor_set.all()
        return render(request, "myjobs.html", {'tutor_jobs':tutor_jobs})

def terms(request):      
    return render(request, "terms.html")

def client_terms(request):      
    return render(request, "client_terms.html")

def tutor_terms(request):      
    return render(request, "tutor_terms.html")

def privacy(request):      
    return render(request, "privacy_policy.html")

def apply_job(request, pk):
    if request.method == 'POST':
        job = GetTutor.objects.get(id=pk)
        form = GetTutorForm(request.POST, instance=job)   
        if form.is_valid():
            instance = form.save(commit=False)
            instance.applicant = request.user
            instance.save()
            applications = GetTutor.objects.filter(id=pk).count()
            return redirect('/dashboard')
        else:
            print(form.errors)
            return HttpResponse("Invalid Form Data")
    else:
        job = GetTutor.objects.get(id=pk) 
        form = GetTutorForm(instance=job)       
        return render(request, "apply_job.html", {'job': job, 'form': form})
##################
# Start of profile
##################

def update_profile(request):
    if request.method == 'POST':      
      tutor_form = TutorUpdateForm(request.POST, request.FILES, instance = request.user)
      if tutor_form.is_valid():
          instance = tutor_form.save()
          name = instance.first_name
          email = instance.email

          send_email("Profile Update Confirmation", f"Hello {name},\n\n"\
           "We are delighted to inform you that your profile on GreatMindz has been successfully updated.\n"\
           "Thank you for keeping your information current.\n\n"\
           "Best regards,\n"\
           "GreatMindz Team",
           [email])

          admin_email = 'mosianets@gmail.com'

          send_email("New Profile Update", f"Hello Admin,\n\n"\
           f"A profile update has been made for {name}.\n"\
           "Please review the changes and ensure all information is accurate.\n\n"\
           "Best regards,\n"\
           "GreatMindz Team",
           [admin_email])

          messages.success(request, f'Your profile has been updated successfully')
          return redirect('dashboard')
    else:        
        tutor_form = TutorUpdateForm(instance = request.user)
    return render(request, "update_profile.html", {'tutor_form':tutor_form})

def view_profile(request, id):
    reviews = Review.objects.all()
    tutor = Tutor.objects.get(pk = id)
    first_name_letter = tutor.first_name[0]
    last_name_letter = tutor.last_name[0]
    return render(request, "view_profile.html", {'tutor':tutor, 'reviews':reviews, 'first_name_letter':first_name_letter, 'last_name_letter':last_name_letter})

################
# End of profile
###############

def current_applications(request):    
    count = GetTutor.objects.filter(applicant = request.user).count()  
    applications = GetTutor.objects.filter(applicant = request.user)  
    return render(request, "current_applications.html", {'applications':applications, 'count':count})

def current_jobs(request):    
    count = GetTutor.objects.filter(applicant = request.user, jobstatus__status='approved').count()  
    applications = GetTutor.objects.filter(applicant=request.user, jobstatus__status='approved')  
    return render(request, "current_jobs.html", {'applications':applications, 'count':count})

######################################
# Start of filtering tutors by subject
######################################

def maths_tutors(request):
    maths_tutors = Tutor.objects.filter(subject_tutored = "Mathematics")
    return render(request, "subject_filtering/maths_tutors.html", {'maths_tutors':maths_tutors})

def life_sciences_tutors(request):
    life_sciences_tutors = Tutor.objects.filter(subject_tutored = "Life Sciences")
    return render(request, "subject_filtering/life_sciences_tutors.html", {'life_sciences_tutors': life_sciences_tutors})