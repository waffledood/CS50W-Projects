from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from markdown2 import markdown

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(
            label="Title of Wiki Entry:",
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Enter the title for your new Wiki entry...',
                    'class': 'form-control w-75 mb-2'
                }
            )
        )
    content = forms.CharField(
            label="Content of Wiki Entry:",
            widget=forms.Textarea(
                attrs={
                    'placeholder': 'Enter the Markdown content for your new Wiki entry...',
                    'class': 'form-control w-75'
                }
            )
        )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # retrieve the Wiki entry's contents
    entryContents = util.get_entry(title)
    # if the entry doesn't exist, generate the error page
    if entryContents == None:
        return render(request, "encyclopedia/error.html")
    # else generate the Wiki entry's page
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entryContents": markdown(entryContents)
        })

def search(request):
    if request.method == "POST":
        # retrieve the query keyword
        query = request.POST['q']

        # check if the query keyword exactly matches any of the Wiki entries (case insensitive)
        if util.check_entry_match_title(query):
            return entry(request, query)

        # else find entries that match or contain the query string (case insensitive)
        entriesContainingQuery = util.check_entries_contain_query(query)
        # generate the search page with matching Wiki entries
        return render(request, "encyclopedia/search.html", {
            "entryContents": entriesContainingQuery,
            "query": query
        })
    # if the search page was reached through a GET method
    else:
        return render(request, "encyclopedia/search.html", {
            "default": True
        })

def add(request):
    if request.method == "POST":
        # create a NewEntryForm from the POST request
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # retrieve the form's data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # check if the query keyword exactly matches any of the Wiki entries (case insensitive)
            if util.check_entry_match_title(title):
                return render(request, "encyclopedia/add.html", {
                    "error": True ,
                    "form": form
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', kwargs={'title':title}))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })

def edit(request):
    if request.method == "GET":
        title = request.GET["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": NewEntryForm(initial={"title": title, "content": content})
        })
    elif request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # retrieve the form's data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', kwargs={'title':title}))
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })
    return render(request, "encyclopedia/edit.html")

def random(request):
    allWikiEntries = util.list_entries()
    randomWikiEntry = choice(allWikiEntries)
    return HttpResponseRedirect(reverse('entry', kwargs={'title':randomWikiEntry}))
