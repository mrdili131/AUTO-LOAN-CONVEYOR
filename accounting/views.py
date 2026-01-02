from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from krd.models import Loan, Product, PaymentMonth
from django.http.response import JsonResponse
from .models import AccountedLoan
from django.utils.decorators import method_decorator
from krd.utils import role_required
from datetime import date
import calendar
from django.db.models import Sum


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
    
@method_decorator(role_required('accountant'),name="dispatch")
class PaymentView(LoginRequiredMixin,View):
    def get(self,request):
        query = request.GET.get("q")
        try:
            element = AccountedLoan.objects.get(loan__contract_id=query)
            loan = Loan.objects.get(id=element.loan.id)
            return render(request,'accounting/payment.html',{"loan":loan,"q":query})
        except AccountedLoan.DoesNotExist:
            return render(request,'accounting/payment.html',{"q":query})        
    
@role_required('accountant')
def document(request,id,doct):
    loan = Loan.objects.get(id=id)
    if (doct and doct == "accounting_cheque"):
        return render(request,'accounting/accounting_cheque.html',{"loan":loan})
    

@login_required
def done(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')

        if(loan_id):
            loan = Loan.objects.get(id=loan_id)
            product = Product.objects.get(id=loan.product.id)
            product.quantity-=1
            product.save()
            loan.status = "done"
            loan.save()
            AccountedLoan( # Accountant is approving
                user=request.user,
                loan = loan,
                filial = request.user.filial
            ).save()
            for exists in PaymentMonth.objects.filter(loan=loan):
                exists.delete()
            for i in range(1,loan.term+1): # Creates monthly payment objects
                month = loan.start_date.month + i
                year = loan.start_date.year + (month-1)//12
                month = (month-1)%12+1
                last_day = calendar.monthrange(year,month)[1]
                day = min(loan.payday,last_day)
                payment_date = date(year,month,day)
                PaymentMonth(
                    loan=loan,
                    month=i,
                    payment=loan.payment,
                    payment_date = payment_date
                ).save()
            return JsonResponse({"status":True,"msg":"Kredit rasmiylashtirildi!"})
        
@role_required('accountant')
def pay(request,id,amount):
    loan = Loan.objects.get(id=id)
    loan.pay(amount)
    return JsonResponse({"status":True})