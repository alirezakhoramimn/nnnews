from django.shortcuts import render

from .models import Post
from .forms import CommentForm, PostForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin 
from django.shortcuts import render, get_object_or_404
# Create your views here.
from taggit.models import Tag 

from django.views import generic 
from django.views.generic import (ListView,
                                  DeleteView,
                                  CreateView,
                                  UpdateView,
                                  DetailView
                                  )



def post_list(request): 
    
    object_list = Post.objects.order_by('-created_on')
    paginator = Paginator(object_list, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.slug = Slugify(new_post.title)
        new_post.save()
        # IMPORTENT 
        form.save_m2m()

    context = {
           'posts':object_list,
           'page_obj': page_obj,
           'common_tags':common_tags,
           'form':form

       }
    return render(request, 'blog/home.html', context)



def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Flter posts by the tag name 
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'blog/home.html',context)

def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

class PostCreateView(LoginRequiredMixin, CreateView, generic.base.RedirectView):
    model = Post
    fields = ['title', 'content', 'image', 'tags' ]

    # adding the author to every post that is going to be created
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = self.request.slug
        form.instance.image = self.request.image

        form.instance.title = self.request.title

        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'tags']

    # adding the author to every post that is going to be created
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # till this place well everything is good but if you attention enough you can see that everyone can change any post
    # To avoid this we can import UserPassesTestMixin  and this and the other things we do will avoid fucking up
    #  including this function

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView, UserPassesTestMixin, LoginRequiredMixin):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# this is built in order to show every profile that has created a post


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    # let's set the context in here as well
    context_object_name = 'posts'
    # now for having the latest post we add the ordering
    paginate_by = 5

    # we can overwirte a method and change the queryset
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('created_on')















