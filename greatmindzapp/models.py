from django.db import models
import random
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class University(models.Model):
    level = models.CharField(max_length=30)

    def __str__(self):
       return self.level

class UnderGrad(models.Model):
    undergrad_finished = models.CharField(max_length=20)

    def __str__(self):
       return self.undergrad_finished

class Gender(models.Model):
    gender = models.CharField(max_length=10)

    def __str__(self):
       return self.gender
class Vehicle(models.Model):
    vehicle = models.CharField(max_length=10)

    def __str__(self):
       return self.vehicle
    
class Citizen(models.Model):
    citizen = models.CharField(max_length=10)

    def __str__(self):
       return self.citizen

class Subject(models.Model):
    subject_tutored = models.CharField(max_length=25)

    def __str__(self):
       return self.subject_tutored
    
class Grade(models.Model):
    learner_grade = models.CharField(max_length=25)

    def __str__(self):
       return self.learner_grade

class LessonMode(models.Model):
    lesson_mode = models.CharField(max_length=25)

    def __str__(self):
       return self.lesson_mode 
    
class Syllabus(models.Model):
    learner_syllabus = models.CharField(max_length=25)

    def __str__(self):
       return self.learner_syllabus 

class LessonStart(models.Model):
    lesson_start = models.CharField(max_length=25)

    def __str__(self):
       return self.lesson_start   
   
class JobStatus(models.Model):
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status

class Province(models.Model):
    province = models.CharField(max_length=100)

    def __str__(self):
        return self.province

class CanTutorOnline(models.Model):
    online = models.CharField(max_length=20)

    def __str__(self):
        return self.online
    
class Message(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    contactnumber = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    
    def __str__(self):
        return self.fullname

class Relationship(models.Model):
    relationship = models.CharField(max_length=20)

    def __str__(self):
        return self.relationship


class TutorManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile_number, street_address, bio, profile_pic, password=None):

        if not email:
            raise ValueError('You must provide email address')
        if not first_name:
            raise ValueError('You must provide full name')  
        if not last_name:
            raise ValueError('You must provide last name')        
        if not mobile_number:
            raise ValueError('You must provide mobile number')
        if not street_address:
            raise ValueError('You must provide full physical address')
        if not bio:
            raise ValueError('You must provide a biography')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, mobile_number=mobile_number, 
                          street_address=street_address, bio=bio, profile_pic=profile_pic)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, mobile_number, street_address, bio, profile_pic, password=None, **extra_fields):
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, mobile_number=mobile_number, 
                                street_address=street_address, bio=bio, profile_pic=profile_pic, password=password, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class Tutor(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=50, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=100)
    last_name = models.CharField(verbose_name="last name", max_length=100)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    age = models.CharField(verbose_name="age", max_length=100)
    sa_citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True)
    mobile_number = models.CharField(verbose_name="mobile number", max_length=15)
    subject_tutored = models.ManyToManyField(Subject, verbose_name="subject tutored", null=True)
    can_tutor_online = models.ForeignKey(CanTutorOnline, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    grades_tutored = models.ManyToManyField(Grade, verbose_name="grades tutored", null=True)
    syllabus_tutored = models.ManyToManyField(Syllabus, verbose_name="syllabus tutored", null=True)
    matric_certificate = models.FileField(verbose_name="Matric certificate", upload_to='images/', null=True)
    id_upload = models.FileField(verbose_name="ID upload", upload_to='images/', null=True)

    street_address = models.CharField(max_length=100)

    bio = models.TextField(verbose_name="biography")
    currently_degree = models.CharField(max_length=50, null=True)
    highest_qualification = models.CharField(max_length=50, null=True)
    undergrad_finished = models.ForeignKey(UnderGrad, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/')
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)     

    objects = TutorManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_number', 'bio', 'street_address', 'profile_pic']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label ):
        return True


class PaymentInformation(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)
    bank_branch = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tutor.first_name} {self.tutor.last_name}'s Payment Information"

class GetTutor(models.Model):
    class LengthofLesson(models.TextChoices):
        HOUR = "h", _("1 Hour")
        HOUR_AND_30_MINUTES = "hm", _("1 Hour 30 Minutes")
        TWO_HOURS = "2h", _("2 Hours")
    class LessonPerWeek(models.TextChoices):
        ONE = "1", _("1")
        TWO = "2", _("2")
        THREE = "3", _("3")
        FOUR = "4", _("4")
        FIVE = "5", _("5")
        SIX = "6", _("6")
        SEVEN = "7", _("7")
        EIGHT = "8", _("8")
        NINE = "9", _("9")
        TEN = "10", _("10")

    syllabus = models.ManyToManyField(Syllabus, verbose_name="syllabus")
    grade = models.ManyToManyField(Grade, verbose_name="grades")
    subject = models.ManyToManyField(Subject, verbose_name="subject")
    first_name = models.CharField(max_length=50)   
    last_name = models.CharField(max_length=50)      
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=12)
    relationship = models.ForeignKey(Relationship, on_delete = models.CASCADE)
    relationship_full_name = models.CharField(max_length=40, null=True,default='None')

    street_address = models.CharField(max_length=100) 
    suburb = models.CharField(max_length=100, blank=True, default='None') 
    town = models.CharField(max_length=100, blank = True, default='None')   
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, default='None')
     
         
    lesson_mode = models.ForeignKey(LessonMode, on_delete=models.CASCADE)
    start = models.ForeignKey(LessonStart, on_delete=models.CASCADE)
    additional_details= models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    pay_rate = models.CharField(max_length=7)
    job_id = models.CharField(max_length=5, unique=True, null=True)
    length_of_lesson = models.CharField(max_length=2, choices=LengthofLesson.choices, default=LengthofLesson.HOUR, null=True, blank=True)
    lesson_per_week = models.CharField(max_length=2, choices=LessonPerWeek.choices, default=LessonPerWeek.ONE, null=True, blank=True)
    jobstatus = models.ForeignKey(JobStatus, on_delete=models.CASCADE, null=True)    
    applicant = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True) 

    def save(self, *args, **kwargs):
        if not self.job_id:
            while True:
                random_number = ''.join(random.choices('0123456789', k=5))
                
                if not GetTutor.objects.filter(job_id=random_number).exists():
                    self.job_id = random_number
                    break

        super(GetTutor, self).save(*args, **kwargs)

    def match_and_notify_tutors(self):
        tutors = Tutor.objects.filter(
            subject_tutored__in=self.subject.all(),
            grades_tutored__in=self.grade.all(),
            can_tutor_online=self.lesson_mode
        ).distinct()

        for tutor in tutors:
            subject = f"New Tutoring Opportunity for {self.first_name} {self.last_name}"
            message = f"""
            Dear {tutor.first_name},

            We have a new tutoring opportunity that matches your profile.

            Student Details:
            Name: {self.first_name} {self.last_name}
            Subjects: {', '.join([subject.name for subject in self.subject.all()])}
            Grades: {', '.join([grade.name for grade in self.grade.all()])}
            Street Address: {self.street_address}
            Online: {self.lesson_mode}

            Please log in to your account for more details.

            Best regards,
            Your Tutoring Platform Team
            """
            send_mail(
                subject,
                message,
                'from@example.com',  # Replace with your 'from' email
                [tutor.email],
                fail_silently=False,
            )
        

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Blog(models.Model):
    title= models.CharField(max_length=50)    
    slug = models.SlugField(max_length=250, unique = True)
    body = models.TextField(max_length=1500)
    author = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable = False)

    def get_absolute_url(self):
        return reverse("blog_single", kwargs = {"slug": self.slug})

    def snippet(self):
        return self.body[0:50] + '...'

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
class Review(models.Model):
    review = models.TextField(max_length = 300)
    parent_name = models.CharField(max_length=50)
    learner_name = models.CharField(max_length=50)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tutor.first_name + ' ' + self.tutor.last_name
        
    
