from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.http.response import JsonResponse
import json
from datetime import datetime

class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
    
class KonveyerView(View):
    def get(self,request,id):
        loan = Loan.objects.get(id=id)
        products = Product.objects.filter(filial=request.user.filial,is_available=True)
        if loan.product_price and loan.rate and loan.product.price:
            loan.amount = (loan.product_price/100*loan.rate)+loan.product_price
            loan.save()
        return render(request,'konveyer.html',{"loan":loan,"products":products})
def create_request(request):
    newloan = Loan(
        user = request.user,
        filial = request.user.filial
    )
    newloan.save()
    return redirect('konveyer',id=newloan.id)

def save_data(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("data"))
        id = request.POST.get("id")
        if data and id:
            loan = Loan.objects.get(id=id)
            product = Product.objects.get(id=int(data["product"]))
            loan.amount = float(data["amount"])
            loan.product = product
            loan.product_price = product.price
            loan.rate = int(data["loan_rate"])
            loan.monthly_income = int(data["monthly_income"])
            loan.monthly_spending = int(data["monthly_spending"])
            loan.scoring = int(data["scoring"])
            loan.work_type = data["work_type"]
            loan.end_date = datetime.strptime(data["loan_end_date"], "%Y-%m-%d").date()
            loan.save()
            return JsonResponse({"status":True})
    
def add_client(request):
    if request.method == "POST":
        passport_pinfl = request.POST.get("pinfl")
        id = request.POST.get("id")
        loan = Loan.objects.get(id=id)
        try:
            client = Client.objects.get(passport_pinfl=passport_pinfl)
            loan.client = client
            loan.save()
            return JsonResponse({"status":True,"msg":"Mijoz topildi !"})
        except Client.DoesNotExist:
            loan.client = None
            return JsonResponse({"status":False, "msg":"Mijoz topilmadi"})
        