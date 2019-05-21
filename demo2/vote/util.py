from django.shortcuts import redirect,reverse


def checklogin(fun):
    def check(request,*args):
        # un=request.session.get('username')
        # if un:
        #     return fun(request,*args)
        # else:
        #     return redirect(reverse('vote:login'))
        if request.user and request.user.is_authenticated:
            return fun(request,*args)
        else:
            return redirect(reverse('vote:login'))

    return check