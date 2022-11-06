from django.shortcuts import render

from . import util


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
            "entryContents": entryContents
        })

def search(request):
    if request.method == "POST":
        # retrieve the current list of Wiki entries
        wikiEntries = util.list_entries()
        # retrieve the query keyword
        query = request.POST['q']

        # check if the query keyword exactly matches any of the Wiki entries (case insensitive)
        if query.lower() in (entry.lower() for entry in wikiEntries):
            return entry(request, query)

        # else find entries that match or contain the query string (case insensitive)
        entriesContainingQuery = [entry for entry in wikiEntries if query.lower() in entry.lower()]
        print(f"entriesContainingQuery = {entriesContainingQuery}")
        # generate the search page with matching Wiki entries
        return render(request, "encyclopedia/search.html", {
            "entryContents": entriesContainingQuery
        })
    # if the search page was reached through a GET method
    else:
        return render(request, "encyclopedia/search.html")
