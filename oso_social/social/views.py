from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Group

from .models import Post
from .forms import PostForm

# Create your views here.


def list_posts(request):
    groups = Group.objects.all()
    posts = Post.objects.all().order_by("-created_at")

    # STEP 1: Add check that user is an admin before they can see a post.

    return render(request, "social/list.html", {"posts": posts, "groups": groups})

@login_required
def list_group(request, group_id):
    pass

@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        post = form.save(commit=False)

        # STEP 3: Restrict post creation by group.
        post.created_by = request.user
        post.save()

        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        form = PostForm()
        return render(request, "social/new_post.html", {"form": form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])
