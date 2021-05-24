from .models import Profile, Relationship





def profile_pic(request):
    if request.user.is_authenticated:
        #profile_obj = Profile.objects.filter(slug=slug)
        profile_obj = Profile.objects.filter(user=request.user)
        if profile_obj: 
            pic = profile_obj[0].avatar
            return {'picture':pic}
        else:
            pic = "No Matching Profile"
            return {'picture' : pic}

      # pic = profile_obj.avatar
       #return {'picture':pic}
    return {}

def invitations_received_no(request):
    if request.user.is_authenticated:
        #profile_obj = Profile.objects.filter(slug=slug)
        
        profile_obj = Profile.objects.filter(user=request.user)
        if profile_obj:
            qs_count = Relationship.objects.invitations_received(profile_obj).count()
            return {'invites_num':qs_count}
        else:
            qs_count = "No counter"
            return {'invites_num':qs_count}
    return {}