import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from schoolboxauth.models import User
import bs4
from .constants import friendly_subject_names


# Create your views here.

@login_required
def dashboard(request):
    cookies = {
        'PHPSESSID': f'{request.user.cookie}',
    }
    response = requests.get("https://schoolbox.donvale.vic.edu.au", cookies=cookies)
    duework = get_upcoming_due_work(response, request.user)
    timetable = get_timetable(response, request.user)
    return render(request, 'dashboard/dashboard.html', context={'duework': duework, 'timetable': timetable})


def get_upcoming_due_work(response, current_user):

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
        return map(str, elements)
    except AttributeError:
        return None


def get_timetable(response, current_user):

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
        except AttributeError:
            elements.append(tag)

    if len(elements) == 0:
        return []

    return map(str, elements)