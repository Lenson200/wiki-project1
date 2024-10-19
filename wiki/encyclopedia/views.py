from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import util
from django.urls import reverse
import markdown2
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_detail(request, title):
    content = util.get_entry(title)#utilizes the get_entry function in util.py
    if content==None:
        content="## page was not found"
    content=markdown2.markdown(content)
    return render(request,"encyclopedia/entry_detail.html",{"content":content,'title':title})

     # after util.search(q) returns matching entries  it renders the page  in my list of entries else a list of possible entries  
def search_results(request):
    q= request.GET.get('q', '').strip() 
    entries = util.list_entries()
    if q in entries:
        return redirect("entry_detail", title=q)
    else:
        results = util.search(query=q)  
    return render(request, "encyclopedia/search_results.html", {"entries":util.search(q), "q": q})
    #saves the page taking in  title and content written in markup language
def create_new(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        content = request.POST.get('content')

        if not title or not content:
            return render(request, "encyclopedia/create_new.html",
                          {"message": "Title and content cannot be empty.", "title": title, "content": content})

        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            return render(request, "encyclopedia/error.html",
                          {"message": "The title '{}' already exists.".format(title), "title": title, "content": content})

        util.save_entry(title, content)
        return redirect("entry_detail", title=title)

    return render(request, "encyclopedia/create_new.html")
#returns a pre populated content on the text area of the same title and user can only edit the content but not the title.
def edit_content(request, title):
    if not title:
        return render(request, "encyclopedia/edit.html", {"message": "Title cannot be empty."})

    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/edit.html", {"title": title})

    if request.method == "POST":
        new_content = request.POST.get("content").strip()
        if new_content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, new_content)
        return redirect(reverse("entry_detail", args=[title]))

    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})
#generates a random page everytime its called
def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry_detail", title=random_title)