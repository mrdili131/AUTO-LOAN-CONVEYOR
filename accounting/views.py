from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from krd.models import Loan
from django.http.response import JsonResponse
from .models import AccountedLoan
from django.utils.decorators import method_decorator
from krd.utils import role_required

@method_decorator(role_required('accountant'),name="dispatch")
class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        loans = Loan.objects.filter(filial=request.user.filial,status="approved")
        return render(request,'accounting/index.html',{"loans":loans})
    
@method_decorator(role_required('accountant'),name="dispatch")
class HistoryView(LoginRequiredMixin,View):
    def get(self,request):
        loans = AccountedLoan.objects.filter(filial=request.user.filial)
        return render(request,'accounting/history.html',{"loans":loans})
    

@login_required
def done(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')

        if(loan_id):
            loan = Loan.objects.get(id=loan_id)
            loan.status = "done"
            loan.save()
            AccountedLoan(
                user=request.user,
                loan = loan,
                filial = request.user.filial
            ).save()
            return JsonResponse({"status":True,"msg":"Mijozni buxgalteriyaga jo'nating!"})