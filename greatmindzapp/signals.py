from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tutor, GetTutor
from .views import send_email

@receiver(post_save, sender=Tutor)
def post_save_tutor(sender, instance, created, **kwargs):
    if instance.is_approved:
          # Import send_email here to avoid circular import
        send_email("Tutor Account Approval", "Your Tutor Account has been approved.", [instance.email])
    if instance.is_active:
        send_email("Tutor Account Activation", "Your Tutor Account has been activated.", [instance.email])


@receiver(post_save, sender=GetTutor)
def match_and_notify_tutors(sender, instance, created, **kwargs):
    if instance.jobstatus and instance.jobstatus.status == 'pending':
        tutors = Tutor.objects.filter(
            subject_tutored__in=instance.subject.all(),
            grades_tutored__in=instance.grade.all(),
            # can_tutor_online=instance.lesson_mode 
        ).distinct()

        for tutor in tutors:
            subject = f"New Tutoring Opportunity for {instance.first_name} {instance.last_name}"
            message = f"""
            Dear {tutor.first_name},

            We have a new tutoring opportunity that matches your profile.

            Job Details:
            Job ID: {instance.job_id}
            Street Address: {instance.street_address}
            Street Address: {instance.suburb}
            Street Address: {instance.town}
            Street Address: {instance.province.province}
            Online: {instance.lesson_mode}
            Subjects: {', '.join([subject.subject_tutored for subject in instance.subject.all()])}
            Grades: {', '.join([grade.learner_grade for grade in instance.grade.all()])}
            Syllabus: {', '.join([syllabus.learner_syllabus for syllabus in instance.syllabus.all()])}
            When the parents or learner want to start: {instance.start}
            Length of Lesson: {instance.length_of_lesson}
            Number of Lessons a week: {instance.lesson_per_week}
            

            Please log in to your account for more details.

            Best regards,
            GreatMindzTutor Team
            """
            send_email(
                subject,
                message,
                [tutor.email]
            )
