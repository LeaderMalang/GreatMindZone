from django import forms
from django.forms import ModelForm
from . models import Message, GetTutor, Tutor, PaymentInformation
from django.contrib.auth import authenticate
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError


class GetTutorForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = GetTutor
        fields = ('syllabus', 'grade', 'subject', 'first_name', 'last_name','email', 'relationship_full_name',  'mobile', 'relationship', 'street_address','suburb','town', 'province', 'lesson_mode', 'start', 'additional_details',)
        widgets = {
            'syllabus':forms.SelectMultiple(attrs={'class':'form-control'}),
            'grade': forms.SelectMultiple(attrs={'class':'form-control'}),
            'subject': forms.SelectMultiple(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'relationship_full_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),
            'relationship': forms.Select(attrs={'class':'form-control'}),
            'street_address': forms.TextInput(attrs={'class':'form-control'}),
            'suburb': forms.TextInput(attrs={'class':'form-control'}),
            'town': forms.TextInput(attrs={'class':'form-control'}),
            'province': forms.Select(attrs={'class':'form-control'}),
            'lesson_mode': forms.Select(attrs={'class':'form-control'}),
            'start': forms.Select(attrs={'class':'form-control'}),
            'additional_details': forms.Textarea(attrs={'class':'form-control'}),
            'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
            
        }
        labels = {
            'grade': 'Grade',
            'subject': 'Subject',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'relationship_full_name': 'His/Her Name',
            'email': 'Email address',
            'mobile': 'Contact Number',
            'relationship': ' Relationship to learner',
            'lesson_mode': 'Mode of lessons',
            'street_address': 'Physical Address',
            'start': 'When would you like to start?',
            'additional_details': 'Any additional details?',
            'tutor_application': 'Why would you be perfect for this job?'
        }
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError("First name cannot be blank.")
        if any(char.isdigit() for char in first_name):
            raise ValidationError("First name should not contain numbers.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError("Last name cannot be blank.")
        if any(char.isdigit() for char in last_name):
            raise ValidationError("Last name should not contain numbers.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("Email cannot be blank.")
        if '@' not in email:
            raise ValidationError("Please enter a valid email address.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile:
            raise ValidationError("Mobile number cannot be blank.")
        if not mobile.replace("+", "").isdigit():
            raise ValidationError("Only numbers and a leading plus sign (+) are allowed in the mobile field.")
        return mobile

    def clean_relationship(self):
        relationship = self.cleaned_data['relationship']
        if not relationship:
            raise ValidationError("Relationship to learner cannot be blank.")
        return relationship

    def clean_street_address(self):
        street_address = self.cleaned_data['street_address']
        if not street_address:
            raise ValidationError("Physical Address cannot be blank.")
        return street_address

    def clean_suburb(self):
        suburb = self.cleaned_data['suburb']
        if not suburb:
            raise ValidationError("Suburb cannot be blank.")
        return suburb

    def clean_town(self):
        town = self.cleaned_data['town']
        if not town:
            raise ValidationError("Town cannot be blank.")
        return town

    def clean_province(self):
        province = self.cleaned_data['province']
        if not province:
            raise ValidationError("Province cannot be blank.")
        return province

    def clean_lesson_mode(self):
        lesson_mode = self.cleaned_data['lesson_mode']
        if not lesson_mode:
            raise ValidationError("Lesson mode cannot be blank.")
        return lesson_mode

    def clean_start(self):
        start = self.cleaned_data['start']
        if not start:
            raise ValidationError("Start date cannot be blank.")
        return start

    def clean_additional_details(self):
        additional_details = self.cleaned_data['additional_details']
        if not additional_details:
            raise ValidationError("Additional details cannot be blank.")
        return additional_details
    
class MessageForm(ModelForm):
    
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'contactnumber': forms.TextInput(attrs={'class':'form-control'}),
            'message': forms.Textarea(attrs={'class':'form-control'})
        }
        labels = {
            'fullname': 'Full Name',
            'email': 'Email address',
            'contactnumber': 'Contact Number',
            'message': 'Your message'
        }

    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not fullname:
            raise ValidationError("Full name cannot be blank.")
        return fullname

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("Email address cannot be blank.")
        return email

    def clean_contactnumber(self):
        contactnumber = self.cleaned_data['contactnumber']
        if not contactnumber:
            raise ValidationError("Contact number cannot be blank.")
        return contactnumber

    def clean_message(self):
        message = self.cleaned_data['message']
        if not message:
            raise ValidationError("Message cannot be blank.")
        return message

class BecomeTutorForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Tutor
        fields = ('first_name', 'last_name', 'email', 'gender', 'age', 'sa_citizen', 'mobile_number', 'subject_tutored', 'can_tutor_online', 'can_tutor_in_person', 'grades_tutored', 'syllabus_tutored', 'street_address','suburb','town','province', 'undergrad_finished', 'highest_qualification', 'currently_degree', 'bio', 'profile_pic', 'vehicle', 'password', 'matric_certificate', 'id_upload')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email':'Email Address',
            'gender':'Gender',
            'age': 'Age',
            'vehicle': 'Do you have your own vehicle to travel to lessons with?',
            'sa_citizen':'Are you a South African citizen?',
            'mobile_number':'Contact Number',
            'subject_tutored': 'Subject Tutored',
            'can_tutor_online': 'Can you tutor online?',
            'can_tutor_in_person': 'Can you tutor in person?',
            'grades_tutored': 'Grades Tutored',
            'syllabus_tutored': 'Syllabus Tutored',
            'street_address': 'Physical Address',
            'suburb':"Suburb",
            'town':"City/Town",
            'province':"Province",
            'undergrad_finished': 'Are you still an undergraduate student?',
            'highest_qualification': 'What is your highest qualification?',
            'currently_degree': 'Which degree are you currently pursuing?',
            'bio': 'Biography',
            'profile_pic': 'Profile Picture',
            'password': 'Password',
            'matric_certificate': 'Matric Certificate',
            'id_upload': 'ID Upload',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'age': forms.TextInput(attrs={'class':'form-control'}),
            'sa_citizen': forms.Select(attrs={'class':'form-control'}),
            'vehicle': forms.Select(attrs={'class':'form-control'}),
            'mobile_number':forms.TextInput(attrs={'class':'form-control'}),
            'subject_tutored': forms.SelectMultiple(attrs={'class':'form-control'}),
            'can_tutor_online': forms.Select(attrs={'class':'form-control'}),
            'can_tutor_in_person': forms.Select(attrs={'class':'form-control'}),
            'grades_tutored': forms.SelectMultiple(attrs={'class':'form-control'}),
            'syllabus_tutored': forms.SelectMultiple(attrs={'class':'form-control'}),
            'street_address': forms.TextInput(attrs={'class':'form-control'}),
            'suburb': forms.TextInput(attrs={'class':'form-control'}),
            'town': forms.TextInput(attrs={'class':'form-control'}),
            'province': forms.Select(attrs={'class':'form-control'}),
            
            'bio': forms.Textarea(attrs={'class':'form-control','maxlength':200,'minlength':50}),  
            'undergrad_finished':forms.Select(attrs={'class':'form-control'}),     
            'highest_qualification': forms.TextInput(attrs={'class':'form-control'}),  
            'currently_degree': forms.TextInput(attrs={'class':'form-control'}),  
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'matric_certificate': forms.FileInput(attrs={'class':'form-control'}),
            'id_upload': forms.FileInput(attrs={'class':'form-control'}),
            'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError("First name cannot be blank.")
        if any(char.isdigit() for char in first_name):
            raise ValidationError("First name should not contain numbers.")
        return first_name
    def can_tutor_in_person(self):
        can_tutor_in_person = self.cleaned_data['can_tutor_in_person']
        if not can_tutor_in_person:
            raise ValidationError("This cannot be blank.")

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError("Last name cannot be blank.")
        if any(char.isdigit() for char in last_name):
            raise ValidationError("Last name should not contain numbers.")
        return last_name

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if not mobile_number:
            raise ValidationError("Mobile number cannot be blank.")
        if any(char.isalpha() for char in mobile_number):
            raise ValidationError("Mobile number cannot contain alphabets.")
        return mobile_number
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("Email address cannot be blank.")
        return email
    
    def clean_vehicle(self):
        vehicle = self.cleaned_data['vehicle']
        if not vehicle:
            raise ValidationError("vehicle address cannot be blank.")
        return vehicle

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if not gender:
            raise ValidationError("Gender cannot be blank.")
        return gender

    def clean_age(self):
        age = self.cleaned_data['age']
        if not age:
            raise ValidationError("Age cannot be blank.")
        return age

    def clean_sa_citizen(self):
        sa_citizen = self.cleaned_data['sa_citizen']
        if not sa_citizen:
            raise ValidationError("South African citizenship status cannot be blank.")
        return sa_citizen

    def clean_subject_tutored(self):
        subject_tutored = self.cleaned_data['subject_tutored']
        if not subject_tutored:
            raise ValidationError("Subject tutored cannot be blank.")
        return subject_tutored

    def clean_can_tutor_online(self):
        can_tutor_online = self.cleaned_data['can_tutor_online']
        if not can_tutor_online:
            raise ValidationError("Online tutoring availability cannot be blank.")
        return can_tutor_online

    def clean_street_address(self):
        street_address = self.cleaned_data['street_address']
        if not street_address:
            raise ValidationError("Physical Address cannot be blank.")
        return street_address

    def clean_undergrad_finished(self):
        undergrad_finished = self.cleaned_data['undergrad_finished']
        if not undergrad_finished:
            raise ValidationError("Undergraduate student status cannot be blank.")
        return undergrad_finished

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if not bio:
            raise ValidationError("Biography cannot be blank.")
        return bio

    def clean_grades_tutored(self):
        grades_tutored = self.cleaned_data['grades_tutored']
        if not grades_tutored:
            raise ValidationError("grades_tutored cannot be blank.")
        return grades_tutored

    def clean_syllabus_tutored(self):
        syllabus_tutored = self.cleaned_data['syllabus_tutored']
        if not syllabus_tutored:
            raise ValidationError("syllabus_tutored cannot be blank.")
        return syllabus_tutored

    def clean_matric_certificate(self):
        matric_certificate = self.cleaned_data['matric_certificate']
        if not matric_certificate:
            raise ValidationError("matric_certificate cannot be blank.")
        return matric_certificate

    def clean_id_upload(self):
        id_upload = self.cleaned_data['id_upload']
        if not id_upload:
            raise ValidationError("id_upload cannot be blank.")
        return id_upload

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise ValidationError("Password cannot be blank.")
        return password

class TutorUpdateForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Tutor
        fields = ('first_name', 'last_name', 'email', 'gender', 'age', 'sa_citizen', 'mobile_number', 'subject_tutored', 'can_tutor_online', 'can_tutor_in_person', 'grades_tutored', 'syllabus_tutored', 'street_address', 'undergrad_finished', 'highest_qualification', 'currently_degree', 'bio', 'profile_pic', 'vehicle','matric_certificate', 'id_upload')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email':'Email Address',
            'gender':'Gender',
            'age': 'Age',
            'vehicle': 'Do you have your own vehicle to travel to lessons with?',
            'sa_citizen':'Are you a South African citizen?',
            'mobile_number':'Contact Number',
            'subject_tutored': 'Subject Tutored',
            'can_tutor_online': 'Can you tutor online?',
            'can_tutor_in_person': 'Can you tutor in person?',
            'grades_tutored': 'Grades Tutored',
            'syllabus_tutored': 'Syllabus Tutored',
            'street_address': 'Physical Address',
            'undergrad_finished': 'Are you still an undergraduate student?',
            'highest_qualification': 'What is your highest qualification?',
            'currently_degree': 'Which degree are you currently pursuing?',
            'bio': 'Biography',
            'profile_pic': 'Profile Picture',
            'matric_certificate': 'Matric Certificate',
            'id_upload': 'ID Upload',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'age': forms.TextInput(attrs={'class':'form-control'}),
            'sa_citizen': forms.Select(attrs={'class':'form-control'}),
            'vehicle': forms.Select(attrs={'class':'form-control'}),
            'mobile_number':forms.TextInput(attrs={'class':'form-control'}),
            'subject_tutored': forms.SelectMultiple(attrs={'class':'form-control'}),
            'can_tutor_online': forms.Select(attrs={'class':'form-control'}),
            'can_tutor_in_person': forms.Select(attrs={'class':'form-control'}),
            'grades_tutored': forms.SelectMultiple(attrs={'class':'form-control'}),
            'syllabus_tutored': forms.SelectMultiple(attrs={'class':'form-control'}),
            'street_address': forms.TextInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}),  
            'undergrad_finished':forms.Select(attrs={'class':'form-control'}),     
            'highest_qualification': forms.TextInput(attrs={'class':'form-control'}),  
            'currently_degree': forms.TextInput(attrs={'class':'form-control'}),
            'matric_certificate': forms.FileInput(attrs={'class':'form-control'}),
            'id_upload': forms.FileInput(attrs={'class':'form-control'}),
            'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError("First name cannot be blank.")
        if any(char.isdigit() for char in first_name):
            raise ValidationError("First name should not contain numbers.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError("Last name cannot be blank.")
        if any(char.isdigit() for char in last_name):
            raise ValidationError("Last name should not contain numbers.")
        return last_name

    def can_tutor_in_person(self):
        can_tutor_in_person = self.cleaned_data['can_tutor_in_person']
        if not can_tutor_in_person:
            raise ValidationError("This cannot be blank.")

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if not mobile_number:
            raise ValidationError("Mobile number cannot be blank.")
        if any(char.isalpha() for char in mobile_number):
            raise ValidationError("Mobile number cannot contain alphabets.")
        return mobile_number
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("Email address cannot be blank.")
        return email
    
    def clean_vehicle(self):
        vehicle = self.cleaned_data['vehicle']
        if not vehicle:
            raise ValidationError("vehicle address cannot be blank.")
        return vehicle

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if not gender:
            raise ValidationError("Gender cannot be blank.")
        return gender

    def clean_age(self):
        age = self.cleaned_data['age']
        if not age:
            raise ValidationError("Age cannot be blank.")
        return age

    def clean_sa_citizen(self):
        sa_citizen = self.cleaned_data['sa_citizen']
        if not sa_citizen:
            raise ValidationError("South African citizenship status cannot be blank.")
        return sa_citizen

    def clean_subject_tutored(self):
        subject_tutored = self.cleaned_data['subject_tutored']
        if not subject_tutored:
            raise ValidationError("Subject tutored cannot be blank.")
        return subject_tutored

    def clean_can_tutor_online(self):
        can_tutor_online = self.cleaned_data['can_tutor_online']
        if not can_tutor_online:
            raise ValidationError("Online tutoring availability cannot be blank.")
        return can_tutor_online

    def clean_street_address(self):
        street_address = self.cleaned_data['street_address']
        if not street_address:
            raise ValidationError("Physical Address cannot be blank.")
        return street_address

    def clean_undergrad_finished(self):
        undergrad_finished = self.cleaned_data['undergrad_finished']
        if not undergrad_finished:
            raise ValidationError("Undergraduate student status cannot be blank.")
        return undergrad_finished

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if not bio:
            raise ValidationError("Biography cannot be blank.")
        return bio

    def clean_grades_tutored(self):
        grades_tutored = self.cleaned_data['grades_tutored']
        if not grades_tutored:
            raise ValidationError("grades_tutored cannot be blank.")
        return grades_tutored

    def clean_syllabus_tutored(self):
        syllabus_tutored = self.cleaned_data['syllabus_tutored']
        if not syllabus_tutored:
            raise ValidationError("syllabus_tutored cannot be blank.")
        return syllabus_tutored

    def clean_matric_certificate(self):
        matric_certificate = self.cleaned_data['matric_certificate']
        if not matric_certificate:
            raise ValidationError("matric_certificate cannot be blank.")
        return matric_certificate

    def clean_id_upload(self):
        id_upload = self.cleaned_data['id_upload']
        if not id_upload:
            raise ValidationError("id_upload cannot be blank.")
        return id_upload

class LoginForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Tutor
        fields = ('email', 'password',)
        labels = { 
            'email': 'Email address',
            'password':'Password'
        }
        widgets = {        
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        'password': forms.PasswordInput(attrs={'class':'form-control'}),
        'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
        }
        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password = password):
                raise forms.ValidationError("Invalid Credentials")

class PaymentInformationForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = PaymentInformation
        fields = ['account_holder_name', 'bank_name', 'account_number', 'account_type', 'bank_branch']
        labels = {
            'account_holder_name': 'Name of Account Holder',
            'bank_name': 'Bank Name',
            'account_number': 'Account Number',
            'account_type': 'Account Type',
            'bank_branch': 'Bank Branch',
        }
        widgets = {
            'account_holder_name': forms.TextInput(attrs={'class':'form-control'}),
            'bank_name': forms.TextInput(attrs={'class':'form-control'}),
            'account_number': forms.TextInput(attrs={'class':'form-control'}),
            'account_type': forms.TextInput(attrs={'class':'form-control'}),
            'bank_branch': forms.TextInput(attrs={'class':'form-control'}),
            'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
        }

    def clean_account_holder_name(self):
        account_holder_name = self.cleaned_data['account_holder_name']
        if not account_holder_name:
            raise ValidationError("account_holder_name cannot be blank.")
        if any(char.isdigit() for char in account_holder_name):
            raise ValidationError("account_holder_name should not contain numbers.")
        return account_holder_name

    def clean_bank_name(self):
        bank_name = self.cleaned_data['bank_name']
        if not bank_name:
            raise ValidationError("bank_name cannot be blank.")
        if any(char.isdigit() for char in bank_name):
            raise ValidationError("bank_name should not contain numbers.")
        return bank_name
    
    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']
        if not account_number:
            raise ValidationError("account_number cannot be blank.")
        return account_number
    
    def clean_account_type(self):
        account_type = self.cleaned_data['account_type']
        if not account_type:
            raise ValidationError("account_type cannot be blank.")
        return account_type
    
    def clean_bank_branch(self):
        bank_branch = self.cleaned_data['bank_branch']
        if not bank_branch:
            raise ValidationError("bank_branch cannot be blank.")
        return bank_branch

