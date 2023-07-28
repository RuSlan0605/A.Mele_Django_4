from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from post.models import Post, Comment
from post.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/post_list.html'


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug,\
         status=Post.Status.PUBLISHED)
    # Список активных комментариев к этому посту
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)



def post_share(request, post_id):

    post = get_object_or_404(Post,
     id=post_id,
      status=Post.Status.PUBLISHED)
    
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read"\
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'phantomdrug06@gmail.com',
                [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'post/share.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'post/comment.html', context)

