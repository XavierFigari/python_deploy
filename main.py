import os
import fizzbuzz
import subprocess
import requests
from os.path import join

from bottle import route, run, debug, template, request, static_file, default_app, error


@route('/fizzbuzz', method='GET')
def fb_access():
    print("request : " + request.GET.number)
    if request.GET.num:
        number = request.GET.number

        return template('display-result', number=number, result=fizzbuzz.main(number))
    else:
        return template('fb_access.tpl')


application = default_app()

# if __name__ == '__main__':
#     debug(True)
#     run()
