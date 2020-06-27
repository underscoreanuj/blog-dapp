from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView

from Utils.constants import FREE, PLUS


class BlogList(TemplateView):
    def get(self, request):
        blogs = Blog.objects.all()

        context = {
            'blogs': blogs,
            'user': request.user
        }

        return render(request, 'index.html', context=context)


class BlogView(TemplateView):
    def post(self, request):
        return redirect('/blogs')

    def get(self, request, blog_id):
        if not request.user.is_authenticated:
            return render(request, 'web3auth/login.html')

        blog_obj = Blog.objects.get(blog_id=blog_id)

        if blog_obj.blog_type == PLUS and not request.user.has_perm('Blog.view_blog'):
            return render(request, "web3auth/goplus.html")

        context = {
            'blog_obj': blog_obj,
            'user': request.user
        }

        return render(request, 'blog.html', context=context)
