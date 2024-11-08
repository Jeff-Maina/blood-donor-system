# users/decorators.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def is_facility_user(user):
    return user.role == 'facility'


def facility_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_facility_user(request.user):
            return redirect('user-dashboard')
        
        if request.user.is_approved:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('awaiting-approval')
        

    return _wrapped_view
