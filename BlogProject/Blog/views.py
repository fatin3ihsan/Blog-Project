from django.shortcuts import render,get_object_or_404,redirect
from Blog.models import Post,Comment
from Blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView,View

# Create your views here.

class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")


class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    login_url='/login/'
    redirect_field_name='Blog/post_detail.html'
    form_class=PostForm

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model=Post
    login_url='/login/'
    redirect_field_name='Blog/post_detail.html'
    form_class=PostForm



class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

class PostDraftView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='Blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by("create_date")




@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

#######################################################
###############Comment Section#########################
#######################################################


@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        form=CommentForm(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()

            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'Blog/comment_form.html',{'form':form})


@login_required
def approve_comment(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    comment.save()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
