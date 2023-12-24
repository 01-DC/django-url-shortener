from django.shortcuts import render
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime
import random
import string
# Create your views here.


def home(request):
    return render(request, 'home.html')


def createShortUrl(request):
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            random_chars_list = list(string.ascii_letters)
            random_chars = ''.join(random.choices(random_chars_list, k=6))

            while len(ShortURL.objects.filter(short_url=random_chars)) != 0:
                random_chars = ''.join(random.choices(random_chars_list, k=6))

            d = datetime.now()
            s = ShortURL(original_url=original_website,
                         short_url=random_chars, time_date_created=d)
            s.save()
            return render(request, 'urlcreated.html', {'chars': random_chars})
    else:
        form = CreateNewShortURL()
        return render(request, 'create.html', {'form': form})


def redirect(request, url):
    current_obj = ShortURL.objects.filter(short_url=url)
    if len(current_obj) == 0:
        return render(request, 'pagenotfound.html')
    return render(request, 'redirect.html', {'obj': current_obj[0]})
