from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from user.models import User


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        users = User.objects.filter(user_name=username)
        if users.exists():
            user = users.first()
            if user.user_password == password:
                return JsonResponse({
                    'errno': 0,
                    'msg': "登录成功",
                    'user_id': user.user_id,
                    'username': user.user_name
                })
            else:
                return JsonResponse({'errno': 100003, 'msg': "密码错误"})
        else:
            return JsonResponse({'errno': 100004, 'msg': "用户不存在"})
    else:
        return JsonResponse({'errno': 200001, 'msg': "请求方式错误"})
