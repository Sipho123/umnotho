from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def follow_unfollow_profile(request):
    #print(request.method)
    if request.method== "POST":
       # my_profile = Profile.objects.filter(slug=slug)
        my_profile = Profile.objects.get(user=request.user)

        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)

@login_required
def accept_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

@login_required
def reject_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/to_invite_list.html', context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/profile_list.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/details.html'


    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.filter(slug=slug)
        if profile:
            print(slug)
        # to get data #
        # print profile[0].id 
        else:
            error = "no data found"
            return error

@login_required
def get_context_data(self, **kwargs):
    context = super.get_context_data(**kwargs)
    user = User.objects.get(username__iexact=self.request.user)
    profile = Profile.objects.get(user=user)
    rel_r = Relationship.objects.filter(sender=profile)
    rel_s = Relationship.objects.filter(receiver=profile)
    rel_receiver = []
    rel_sender = []
    for item in rel_r:
        rel_receiver.append(item.receiver.user)
    for item in rel_s:
        rel_sender.append(item.sender.user)
    context["rel_receiver"] = rel_receiver
    context["rel_sender"] = rel_sender
    context['is_empty'] = False
    #context['len_posts'] = True 
    #if len(self.get_object().get_all_authors_posts()) > 0 
    #else False
    if len(self.get_queryset()) == 0:
        context['is_empty'] = True
        
    #follow
    view_profile = self.get_object()
    my_profile = Profile.objects.get(user=self.request.user)
    if view_profile.user in my_profile.following.all():
        follow = True
    else:
        follow = False
    context["follow"] = follow
    return context



class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

@login_required   
def send_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-invites-view')

@login_required
def remove_from_connections(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profile-view')

