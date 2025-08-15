from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.defaulttags import comment
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from board.filters import PostFilter
from board.forms import PostForm, CommentForm
from board.models import Post, User


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            send_mail(
                subject='Отзыв на ваше объявление!',
                message=f'Привет! На ваше объявление {post.title} был оставлен отклик {comment.content} пользователем {comment.author.username}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[post.author.email],
            )
            return redirect('post_detail', post.pk)
        return render(request, 'post.html', {'form' : form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = request.POST['code']
            user = User.objects.filter(code=code)
            if user.exists():
                user.update(is_active=True)
                user.update(code='confirmed')
            else:
                return render(request, 'invalid_confirm.html', {})

        return redirect('account_login')


