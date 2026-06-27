from django.shortcuts import redirect
from django.contrib.auth import logout
class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        # logout処理
        if request.path == "/logout/":
            return redirect('/login/')
        # loginページにアクセスしたときに有効なセッションが存在する場合はsessionを削除してログインページを表示させる。
        elif request.path == "/login/":
            if request.user.is_authenticated:  
                logout(request)
        return self.get_response(request)