from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from home.models import Blog
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from .models import Contact
import random
import re
from django.template import RequestContext

# Create your views here.
def index (request):
    blogs = Blog.objects.all()
    random_blogs = random.sample(list(blogs), 3)
    context = {'random_blogs': random_blogs}
    return render(request, 'index.html', context)

def about (request):
    return render(request, 'about.html')

def thanks(request):
    return render(request, 'thanks.html')

def contact (request):
    if request.method == 'POST':
        contact=Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        if len(message) != 0 and len(name) != 0 and len(email) != 0 and len(phone) != 0:
            contact.name=name
            contact.email=email
            contact.phone=phone
            contact.message=message
            contact.save()
            alert = True
            return render(request, 'contact.html', {
                'alert':alert
            })
        else:
            wrong = True
            return render(request, 'contact.html', {
                'wrong':wrong
            })
    return render(request, "contact.html")

def projects (request):
    return render(request, 'projects.html')

def blog(request):
    blogs = Blog.objects.all().order_by('time')
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {'blogs': blogs}
    return render(request, 'blog.html', context)

def category(request, category):
    category_posts = Blog.objects.filter(category=category).order_by('-time')
    if not category_posts:
        message = f"No posts found in category: '{category}'"
        return render(request, "category.html", {"message": message})
    paginator = Paginator(category_posts, 3)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    return render(request, "category.html", {"category": category, 'category_posts': category_posts})

def categories(request):
    all_categories = Blog.objects.values('category').distinct().order_by('category')
    return render(request, "categories.html", {'all_categories': all_categories})

def search(request):
    query = request.GET.get('q')

    query_list = query.split()
    results = Blog.objects.none()
    for word in query_list:
        results = results | Blog.objects.filter(Q(title__contains=word) | Q(content__contains=word)).order_by('-time')
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    if len(results) == 0:
        message = "Sorry, no results found for your search query."
    else:
        message = ""
    return render(request, 'search.html', {'results': results, 'query': query, 'message': message})


def privacy(request):
    return render(request, 'privacy.html')
def disclaimer(request):
    return render(request, "disclaimer.html")

def blogpost (request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
        context = {'blog': blog}
        return render(request, 'blogpost.html', context)
    except Blog.DoesNotExist:
        context = {'message': 'Blog post not found'}
        return render(request, '404.html', context, status=404)

# def blogpost (request, slug):
#     blog = Blog.objects.filter(slug=slug).first()
#     context = {'blog': blog}
#     return render(request, 'blogpost.html', context)
