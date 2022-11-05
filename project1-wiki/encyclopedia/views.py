from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entryContents = util.get_entry(title)
    # if the entry doesn't exist, generate the error page
    if entryContents == None:
        return render(request, "encyclopedia/error.html")
    # else generate the Wiki entry's page
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entryContents": entryContents
        })

