from .models import Subject
def add_variable_to_context(request):
    subjects=Subject.objects.all()
    return {
        'subjects': subjects
    }