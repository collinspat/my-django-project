from django.conf import settings


# Defines a context processor function named ElectionTitle
def ElectionTitle(request):
    context = {}  # Initializes an empty dictionary to hold context variables
    title = "No Title Yet"  # Sets a default title in case the title cannot be retrieved from a file
    
    try:
        file = open(settings.ELECTION_TITLE_PATH, 'r')  # Attempts to open a file specified by ELECTION_TITLE_PATH setting in read mode
        title = file.read()  # Reads the content of the file (the election title) into the title variable
    except:
        pass  # If any exception occurs (e.g., file not found), it silently ignores the error and keeps the default title
    
    context['TITLE'] = title  # Adds the title (either retrieved from the file or the default one) to the context dictionary under the key 'TITLE'
    return context  # Returns the context dictionary, now containing the election title, to be used in templates
