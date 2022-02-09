import requests
import os

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# from selenium.webdriver.firefox.options import Options

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def test(request):
    data = [
        "adfadf",
        "adfadf",
        "adfadf",
        "adfadf",
        "adfadf",
        "adfadf",
        "adfadf",
        "adfadf",
        "adfadf",
    ]
    return render(request, "test.html", {"data" : data})

def test_request(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

def selenium_test(request):

    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path=r'/app/vendor/firefox/firefox')

    options = webdriver.FirefoxOptions()
    
    # enable trace level for debugging 
    # options.log.level = "trace"

    # options.add_argument("-remote-debugging-port=9224")
    options.add_argument("-headless")
    options.add_argument("-disable-gpu")
    options.add_argument("-no-sandbox")

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    
    driver = webdriver.Firefox(
        options=options, 
        firefox_binary=binary,
        executable_path=os.environ.get('GECKODRIVER_PATH')
    )

    # driver.get("http://google.com/")
    # print ("Headless Chrome Initialized")
    # driver.quit()

    # driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    data = "success"
    assert "No results found." not in driver.page_source
    driver.close()

    return HttpResponse(data)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
