from django import forms
from .models import Product, Loan, CreditLine, ScorecardTier,Promo, Fee, Retailer, BrandingCode








class RetailerOptionsForm(forms.Form):
    retailer=forms.ModelChoiceField(queryset=Retailer.objects.all())
    brandingcode=forms.ModelChoiceField(queryset=BrandingCode.objects.all())



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','applicationprocess','scorecard', 'linetype', 'promotype', 'feetype']






class LoanForm(forms.ModelForm):

    scorecardtier = forms.ModelChoiceField(queryset=ScorecardTier.objects.all())
    creditlimit = forms.ModelChoiceField(queryset=CreditLine.objects.all())
    promo = forms.ModelChoiceField(queryset=Promo.objects.all())
    fee = forms.ModelChoiceField(queryset=Fee.objects.all())


    class Meta:
        model = Loan
        fields = ['scorecardtier', 'creditlimit','apr', 'mdr', 'promo','fee']





        
