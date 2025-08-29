from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum
from .models import Post, Comment, Vote
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.score = post.vote_set.aggregate(score=Sum('value'))['score'] or 0
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    comment_form = CommentForm()
    score = post.votes.aggregate(score=Sum('value'))['score'] or 0
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'score': score,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post_detail', pk=pk)


@login_required
@require_POST
def vote_post(request, pk, value):
    post = get_object_or_404(Post, pk=pk)
    vote, created = Vote.objects.get_or_create(post=post, user=request.user)

    if not created and vote.value == value:
        vote.delete()  # Toggle off
    else:
        vote.value = value
        vote.save()

    score = post.vote_set.aggregate(score=Sum('value'))['score'] or 0
    return JsonResponse({'score': score})
