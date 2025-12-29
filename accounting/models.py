from django.db import models
from krd.models import Loan
from users.models import User, Filial

class AccountedLoan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan,on_delete=models.CASCADE)
    filial = models.ForeignKey(Filial,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)