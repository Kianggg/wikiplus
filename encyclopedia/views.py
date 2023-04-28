import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files import File

import markdown2

from . import util

# Form for creating a new wiki page
class NewPageForm(forms.Form):
    page = forms.CharField(label="Page Title")
    content = forms.CharField(widget=forms.Textarea())

def index(request):
    if request.method == "POST":
        query = request.POST.get("q")
        entries = util.list_entries()
        matches = []
        for entry in entries:
            if query.lower() == entry.lower():
                return render(request, "encyclopedia/wikipage.html", {
                    "entry": markdown2.markdown(util.get_entry(entry))
                })
            elif query.lower() in entry.lower():
                matches.append(entry)
        if len(matches) > 0:
            return render(request, "encyclopedia/index.html", {
                "entries": matches,
                "title": "Matching Pages:"
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": None,
                "title": "No Matching Pages Found :("
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "title": "All Pages:"
        })

def addpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            pagename = request.POST.get("page")
            for entry in entries:
                if pagename.lower() == entry.lower():
                    return render(request, "encyclopedia/addpage.html", {
                        "form": form
                })
            # Page with that title does not currently exist, safe to create new file
            util.save_entry(pagename, request.POST.get("content"))
            # Successfully created page, redirect to homepage
            return HttpResponseRedirect(reverse("wiki:index"))
        else:
            return render(request, "encyclopedia/addpage.html", {
            "form": form
        })
    else:
        return render(request, "encyclopedia/addpage.html", {
            "form": NewPageForm()
        })
    
def editpage(request):
    if request.method == "GET":
        pagename = request.GET.get("entry")
        previouspage = util.get_entry(pagename)
        return render(request, "encyclopedia/editpage.html", {
            "entry": pagename,
            "editable": previouspage
        })
    else:
        form = NewPageForm(request.POST)
        if form.is_valid:
            pagename = request.POST.get("entry")
            util.save_entry(pagename, request.POST.get("content"))
            return HttpResponseRedirect(f"/{pagename}")
        else:
            return render(request, "encyclopedia/editpage.html", {
                "entry": pagename,
                "editable": form
        })
        
            

def wikipage(request, pagename):
    entry = util.get_entry(pagename)
    if entry == None:
        return render(request, "encyclopedia/wikipage.html", {
            "pagename": pagename,
            "entry": "Error: Requested page was not found"
        })
    else:
        return render(request, "encyclopedia/wikipage.html", {
            "pagename": pagename,
            "entry": markdown2.markdown(entry)
        })

def randompage(request):
    pages = util.list_entries()
    luckynum = random.randint(0, len(pages) - 1)
    return render(request, "encyclopedia/wikipage.html", {
        "pagename": pages[luckynum],
        "entry": markdown2.markdown(util.get_entry(pages[luckynum]))
    })