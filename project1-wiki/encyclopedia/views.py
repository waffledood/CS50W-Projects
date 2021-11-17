from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse 

import markdown2, random, re

from . import util

wikiTitles = util.list_entries()


class NewPageForm(forms.Form):
    title = forms.CharField(label="Wiki Title")
    entry = forms.CharField(label="Wiki Entry", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    
    '''
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid:
            
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]

            util.save_entry(title, entry)

            #return render(request)
            return redirect('wiki:entry', entry=title)
    '''    

    wikiEntry = util.get_entry(entry)

    if wikiEntry != None:
        return render(request, "encyclopedia/entry.html", {
            "wikiTitle": entry,
            "wikiEntry": markdown2.markdown(wikiEntry)
        })
    return render(request, "encyclopedia/error.html", {
        "errorRequest": True
    })

def edit(request, entry):
    
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]

            util.save_entry(title, entry)

            return redirect('wiki:entry', entry=title)
            #return HttpResponseRedirect(reverse("wiki:index"))
    
    else:
        if entry.lower() in [x.lower() for x in wikiTitles]:

            details = util.get_entry(entry)
            
            #data = {'title': entry, 'entry': markdown2.markdown(details)}
            #form = NewPageForm(data) 
            # reference link 
            # https://docs.djangoproject.com/en/3.1/ref/forms/fields/#initial

            form = NewPageForm(initial={'title': entry, 'entry': markdown2.markdown(details)})

            return render(request, "encyclopedia/editpage.html", {
                "item": entry,
                "form": form
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "errorRequest": True
            })


def randomEntry(request):
    wikiTitles = util.list_entries()
    index = random.randrange(0, len(wikiTitles))
    wikiTitle = wikiTitles[index]

    '''
    return render(request, "encyclopedia/entry.html", {
        "wikiTitle": wikiTitle,
        "wikiEntry": markdown2.markdown(util.get_entry(wikiTitle))
    })'''
    return redirect('wiki:entry', wikiTitle)

def newpage(request):
    if request.method == "POST":
        # does this when the data in the textarea is sent by post, after the user has inputted details
        # the code that follows should be similar to the one covered in lecture 3, tasks, specifically add in views.py
        
        #print("it is post!")

        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]

            if title.lower in [x.lower() for x in wikiTitles]:
                util.save_entry(title, entry)

                return HttpResponseRedirect(reverse("wiki:index"))
            else:
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "available": True
                })

    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm
    })

def search(request):
    if request.method == "POST":
        term = request.POST
        term = term['q']
        searchList = []

        for item in wikiTitles:
            if item.lower() == term.lower():
                return redirect('wiki:entry', entry=term)

            if re.search(term.lower(), item.lower()):
                searchList.append(item)

        if len(searchList) == 0:
            return render(request, "encyclopedia/error.html", {
                "errorSearch":  True
            })

        return render(request, "encyclopedia/search.html", {
            "result": searchList
        })

def error(request):
    return render(request, "encyclopedia/error.html", {
        "errorRequest": True
    })