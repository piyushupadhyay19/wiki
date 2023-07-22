from django.shortcuts import render
import markdown2
from django.http import HttpResponse
import random
from . import util


def index(request):
    try:
        if request.GET['save_edit']=="Save":
            file = request.GET['title_edit']
            content = (request.GET['content_edit'])
            with open(f'entries/{file}.md', 'w') as f:
                f.writelines([content])
            return render(request, f"encyclopedia/entry.html", {
                "title":request.GET['title_edit'],
                "content":markdown2.markdown(content)
            })

    except KeyError:
        try:
            if request.GET['title'].strip() not in util.list_entries() and request.GET['title'].strip() != '' and request.GET['content'].strip() and request.GET['save']=="Save":
                file = request.GET['title']
                content = request.GET['content']
                with open(f'entries/{file}.md', 'w') as f:
                    f.writelines([content])
                return render(request, "encyclopedia/entry.html", {
                    "title": file,
                    "content": markdown2.markdown(content)
                })
            else:
                return render(request, "encyclopedia/create.html", {
                    "message":"Error: This encyclopedia entry already exist"
                })
        except KeyError:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
        })

def take(request, title):
    
        if text := util.get_entry(title):
            html = markdown2.markdown(text)
        else:
            return HttpResponse("<h1 style=\"color:red\">Error: Requested page not found</h1> <h2>Please feel free to add content about this topic by clicking the <a href=\"/create\">Create New Page</a> option on our sidebar.</h2>")

        return render(request, f"encyclopedia/entry.html", {
            "title":title,
            "content":html
        })

def create(request):
        return render(request, "encyclopedia/create.html")

def random_page(request):
    title = random.choice(util.list_entries())
    text = util.get_entry(title)
    html = markdown2.markdown(text)

    return render(request, f"encyclopedia/entry.html", {
        "title":title,
        "content":html
    })

def results(request):
    search = request.GET['q']
    if search.upper() in util.list_entries() or search.capitalize() in util.list_entries():
        return render(request, f"encyclopedia/entry.html", {
        "title":search,
        "content":markdown2.markdown(util.get_entry(search))
        })
    else:
        return render(request, "encyclopedia/results.html", {
            "q":search,
            "entries": util.list_entries()
        })

def edit(request):
    title = request.GET['title']
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "markdown": util.get_entry(title)
    })