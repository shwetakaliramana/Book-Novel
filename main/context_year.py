from datetime import datetime

def context_year(request):
    return {'year': datetime.now().year}
