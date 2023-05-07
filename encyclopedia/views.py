import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import *

import markdown2

from . import util

# Form for creating a new wiki page
class NewPageForm(forms.Form):
    pagename = forms.CharField(label="Page Title", initial="NewEntryTitle", required=True)
    content = forms.CharField(widget=forms.Textarea(), label="Content", initial="Information about your new entry.", required=True)
    images = forms.CharField(label="Image URLs (separate with new lines)", initial="https://imgur.com/a/thisisanexample")

def index(request):
    entries = WikiEntry.objects.all()

    if request.method == "POST":
        query = request.POST.get("q")
        matches = []
        queryLower = query.lower()

        for entry in entries:
            if queryLower == entry.title.lower():
                return redirect('wiki:wikipage', pagename = entry.title)
            elif queryLower in entry.title.lower():
                matches.append(entry.title)

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
        edits = 0
        for entry in entries:
            edits = edits + entry.edits

        return render(request, "encyclopedia/index.html", {
            "entries": WikiEntry.objects.values_list("title", flat=True).order_by("title"),
            "title": "All Pages:",
            "numberOfEntries": len(entries),
            "numberOfEdits": edits
        })

def addpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        newTitle = form.data["pagename"]
        newContent = form.data["content"]
        newImages = form.data["images"]

        # Check to see if a page with that title already exists
        existingTitles = WikiEntry.objects.values_list("title", flat=True).order_by("title")
        titleLower = newTitle.lower()
        for existingTitle in existingTitles:
            if titleLower == existingTitle.lower():
                # TODO: Add an error message here
                return render(request, "encyclopedia/addpage.html", {
                            "form": form
                })
        
        # Page with that title does not currently exist, safe to create new file
        e = WikiEntry(
            title=newTitle,
            content=newContent,
            images=newImages
        )
        e.save()

        # Successfully created page, load the newly-created page
        return HttpResponseRedirect(reverse("wiki:wikipage", args=(newTitle,)))
    else:
        return render(request, "encyclopedia/addpage.html", {
            "form": NewPageForm()
        })
    
def editpage(request):
    if request.method == "GET":
        pagename = request.GET.get("entry")
        previouspage = WikiEntry.objects.get(title=pagename)

        return render(request, "encyclopedia/editpage.html", {
            "entry": pagename,
            "editable": previouspage.content,
            "editable_image_links": previouspage.images
        })
    else:
        form = NewPageForm(request.POST)

        if form.is_valid:
            newPagename = request.POST.get("entry")
            newContent = request.POST.get("content")
            newImages = request.POST.get("images")

            pageToBeEdited = WikiEntry.objects.get(title=newPagename)

            pageToBeEdited.title = newPagename
            pageToBeEdited.content = newContent
            pageToBeEdited.images  = newImages
            pageToBeEdited.edits = pageToBeEdited.edits + 1

            pageToBeEdited.save()

            return HttpResponseRedirect(f"/{newPagename}")
        else:
            return render(request, "encyclopedia/editpage.html", {
                "entry": form.data["pagename"],
                "editable": form,
                "editable_image_links": newImages
        })

def wikipage(request, pagename):
    try:
        entry = WikiEntry.objects.get(title=pagename)

        # Parse image URLs
        images = []
        for url in entry.images.splitlines():
            images.append(url)

        return render(request, "encyclopedia/wikipage.html", {
            "pagename": pagename,
            "entry": markdown2.markdown(entry.content),
            "gallery": images
        })
    except ObjectDoesNotExist:
        return render(request, "encyclopedia/wikipage.html", {
            "pagename": pagename,
            "entry": "Error: Requested page was not found"
        })

def randompage(request):
    pages = WikiEntry.objects.all()
    if len(pages) > 0:
        luckynum = random.randint(0, len(pages) - 1)

        return redirect('wiki:wikipage', pagename = pages[luckynum].title)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": None,
            "title": "There are no pages :("
        })
    
def replace(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        oldWord = form.data["toBeReplaced"]
        newWord = form.data["toReplaceWith"]

        # Validate the form

        # No spaces (single word only)
        if ( " " in oldWord) or ( " " in newWord ):
            return render(request, "encyclopedia/replace.html", {
                "error": "Words cannot include spaces (single words only, please!)"
            })
        
        # Minimum length
        if (len(oldWord) < 3) or (len(newWord) < 3):
            return render(request, "encyclopedia/replace.html", {
                "error": "Word must be at least 3 characters in length.)"
            })
        
        # Search pages and make changes
        entries = WikiEntry.objects.all()
        for entry in entries:
            newContent = entry.content.replace(oldWord, newWord)
            entry.content = newContent
            entry.save()

        # Successfully made changes, return to home page
        return redirect('wiki:index')
    else:
        return render(request, "encyclopedia/replace.html", {
            "error": ""
        })