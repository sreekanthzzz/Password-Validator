from django.shortcuts import render
from django.http import HttpResponse
from checkerapp.models import CheckerModel
import requests
import hashlib


def index(request):
    return render(request, 'index.html')


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(password):
    count = pwned_api_check(password)
    if count:
        j = f'{password} was found {count} times... you should probably change your password!'
        return j
    else:
        j = f'{password} was NOT found. Carry on!'
        return j


def checker_post(request):
    if request.method == 'POST':
        try:
            lst = list((request.POST.get('pass')).split())
            msg=''
            for password in lst:
                msg = msg + main(password) + "\n"

            CheckerModel(password=str(lst), data=msg, ).save()
            return render(request, 'index.html', {'posts': msg}, )

        except ValueError:
            msg = "INVALID.."
            return render(request, 'index.html', {'posts': [msg]}, )


def checker_archive(request):
    posts = CheckerModel.objects.all()
    return render(request, 'index.html', {'posts': posts})
