import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from schoolboxauth.models import User
from schoolboxauth.views import logout
import bs4
from .constants import friendly_subject_names


# Create your views here.

@login_required
@require_http_methods(["GET"])
def dashboard(request):
    cookies = {
        'PHPSESSID': f'{request.user.cookie}',
    }
    response = requests.get("https://schoolbox.donvale.vic.edu.au", cookies=cookies)
    if check_logout(response):
        messages.error(request, "Your Schoolbox session has expired. Please log in again.")
        logout(request)
        return redirect("/")
    duework = get_upcoming_due_work(response)
    timetable = get_timetable(response)
    timetable_headers = ["<div class=\"timetable-top\">Homegroup<br>8:40am-8:55am</div>", "<div class=\"timetable-top\">Period 1<br>9:00am-10:10am</div>",
                         "<div class=\"timetable-top\">Period 2<br>10:30am-11:40am</div>", "<div class=\"timetable-top\">Period 3<br>11:45am-12:55pm</div>",
                         "<div class=\"timetable-top\">Period 4<br>1:50pm-3:05pm</div>"]
    if timetable is not None:
        ziptable = zip(timetable, timetable_headers)
    else:
        ziptable = None
    return render(request, 'dashboard/dashboard.html', context={'duework': duework, 'timetable': ziptable})


def get_upcoming_due_work(response):

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    elements = []

    try:
        for tag in soup.find(attrs={'id': 'component52396'}).find("div").find("div").find("section").find("ul").find_all("li"):
            tag.name = "div"
            tag.find("div")["style"] = "padding: 10px; margin-bottom: 10px;"
            tag.find("div").find_all()[0]["style"] = "font-size: 22px;"
            tag.find("div").find_all()[1]["style"] = "font-size: 18px;"
            tag.find("div").find_all()[2]["style"] = "font-size: 15px;"

            tag.find("div").find_all()[0].find("a")['href'] = "https://schoolbox.donvale.vic.edu.au" + tag.find("div").find_all()[0].find("a")['href']
            tag.find("div").find_all()[0].find("a")['style'] = "text-decoration: none;"
            tag.find("div").find_all()[0].find("a")['target'] = "_blank"

            for subject, subject_value in friendly_subject_names.items():
                if subject in tag.find("div").find_all()[2].text:
                    tag.find("div").find_all()[0].string.replace_with(subject_value + " - " + tag.find("div").find_all()[0].text)
                    break

            if "homework" in tag.find("div").find_all()[2].text.lower():
                tag.find("div").find_all()[2].clear()
                tag.find("div").find_all()[2].append("Homework")
            elif "assessment" in tag.find("div").find_all()[2].text.lower():
                tag.find("div").find_all()[2].clear()
                tag.find("div").find_all()[2].append("Assessment Task")
            elif "class work" in tag.find("div").find_all()[2].text.lower():
                tag.find("div").find_all()[2].clear()
                tag.find("div").find_all()[2].append("Class Work")
            else:
                tag.find("div").find_all()[2].clear()
                tag.find("div").find_all()[2].append("Other")

            elements.append(tag)
        if len(elements) == 0:
            return None
        return list(map(str, elements))
    except AttributeError:
        return None


def get_timetable(response):

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    elements = []

    for tag in soup.find_all(attrs={'class': 'timetable-subject'}):

        if len(tag.find_all()) == 2:
            tag.append(soup.new_tag("br"))

        tag.find_all()[0]['style'] = "display: inline; text-decoration: none;"
        tag.find_all()[0]['target'] = "_blank"
        for subject, subject_value in friendly_subject_names.items():
            if subject in tag.find_all()[0].text:
                tag.find_all()[0].string.replace_with(subject_value)
                break
        try:
            tag.find_all()[0]['href'] = "https://schoolbox.donvale.vic.edu.au" + tag.find_all()[0]['href']
            elements.append(tag)
        except:
            elements.append(tag)

    if len(elements) == 0:
        return None
    return list(map(str, elements))


def check_logout(request):
    if "userNameInput.placeholder = 'Sample.User@donvale.vic.edu.au';" in request.text:
        return True
    return False
