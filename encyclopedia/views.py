
from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from . import util
import random
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

class NewEntryForm(forms.Form):
    article=forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder': 'Search'}))

class Article(forms.Form):
    title=forms.CharField(max_length=40)
    content=forms.CharField(widget=forms.Textarea)

def index(request):
    entries=util.list_entries()
    searched = []
    if request.method=="POST":
        form= NewEntryForm(request.POST)
        if form.is_valid():
            article = form.cleaned_data["article"]
            for entry in entries:
                if article.casefold() == entry.casefold():
                    page = util.get_entry(article)
                    page_mark = Markdown().convert(page)
                    return render(request, "encyclopedia/entrypage.html", {
                        'page': page_mark,
                        'title': article,
                        'form': NewEntryForm()
                    })
                if article.casefold() in entry.casefold():
                        searched.append(entry)
            return render(request, "encyclopedia/search.html", {
                "searched": searched,
                "form": NewEntryForm()
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
                })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewEntryForm()
        })

def entrypage(request, title):
    entries=util.list_entries()
    if title in entries:
        page=util.get_entry(title)
        page_mark=Markdown().convert(page)
        return render(request, "encyclopedia/entrypage.html", {
            'page': page_mark,
            'title': title,
            'form': NewEntryForm()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Page was not found!",
            "form": NewEntryForm()
        })

def new(request):
    entries=util.list_entries()
    if request.method == "POST":
        form = Article(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exist!",
                    "form": form
                    })
            else:
                util.save_entry(title, content)
                page=util.get_entry(title)
                page_mark=Markdown().convert(page)
                return render(request, "encyclopedia/entrypage.html", {
                    "form": form,
                    "title": title,
                    "page": page_mark
                })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": Article()
            })

def edit(request, title):
    if request.method=="POST":
        form = Article(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            page=util.get_entry(title)
            page_mark=Markdown().convert(page)
            return render(request, 'encyclopedia/entrypage.html', {
            "form": Article(),
            "title": title,
            "page": page_mark
            })
    else:
        page=util.get_entry(title)
        form=Article(initial={
        "title": title.capitalize(),
        "content": page
        })
        return render(request, "encyclopedia/edit.html", {
                    "title": page.capitalize(),
                    "form": form
                })

def randomPage(page):
    page=random.choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{page}")
