import threading

#اگر نیاز داشتیم داخل مدل و ریکوست داشته باشیم از میدل ویر استفاده میکنیم
#این امکان را بما میدهد که بتونم توسط گت ریپانس وروودی به  کمک ترد ریکویست را برگردانم
class RequestMiddleware:
    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local
        
        
    def __call__(self, request):
        self.thread_local.current_request = request
        response = self.get_response(request)
        return response
    
    
    