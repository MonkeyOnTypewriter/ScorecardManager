from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.db import transaction
from .forms import ProductForm, LoanForm, RetailerOptionsForm
from .models import Product, Loan, Fee, ScorecardTier, CreditLine, Promo, BrandingCode, Scorecard
from datetime import datetime
# Create your views here.

def list_brandingcode_products(request, brandingcode_id):
    product_list=Product.objects.filter(brandingcode_id=brandingcode_id)
    return render(request, 'product_list.html', {'product_list':product_list})

def product_detail(request, product_id):
    product=Product.objects.get(pk=product_id)
    loans=Loan.objects.filter(product_id=product_id).order_by('name')
    return render(request, 'product_detail.html', {'product':product, 'loans':loans})


def product_detail_options(request, product_id):
    if request.method == 'POST':
        if 'activate_product' in request.POST:
            product=Product.objects.get(id=product_id)
            brandingcode=BrandingCode.objects.get(id=product.brandingcode_id)
            try:
                oldproduct=Product.objects.get(id=brandingcode.activeproduct_id)
                oldproduct.state='DAD'
                oldproduct.save()
            except Exception as e:
                pass
            brandingcode.activeproduct=product
            product.state='ACT'
            brandingcode.save()
            product.save()

    product=Product.objects.get(pk=product_id)
    loans=Loan.objects.filter(product_id=product_id).order_by('name')
    product_detail_html=render_to_string('product_detail.html', {'product':product, 'loans':loans})
    return render(request, 'product_detail_options.html', {'product_id':product_id, 'product_detail_html':product_detail_html})


def retailer_options(request):
    if request.method == 'POST':

        brandingcode_id = request.POST['brandingcode']
        brandingcode = BrandingCode.objects.get(id=brandingcode_id)

        product_detail_url=''
        if brandingcode.activeproduct is not None:
            product_id = brandingcode.activeproduct.id
            product_detail_url = reverse('product_detail', kwargs={'product_id':product_id})


        form=RetailerOptionsForm(request.POST)
        if form.is_valid():

            if 'create_product' in request.POST:
                
                brandingcode_id = request.POST['brandingcode']
                iframe_url=reverse('product_form', kwargs={'brandingcode_id':brandingcode_id})

                return render(request, 'retailer_options.html', {'form':form, 'iframe_url':iframe_url, 'product_detail_url':product_detail_url})
            
            elif 'all_products' in request.POST:
                brandingcode_id = request.POST['brandingcode']
                iframe_url=reverse('list_brandingcode_products', kwargs={'brandingcode_id':brandingcode_id})

                return render(request, 'retailer_options.html', {'form':form, 'iframe_url':iframe_url, 'product_detail_url':product_detail_url})
    
    form=RetailerOptionsForm()
    return render(request, 'retailer_options.html', {'form':form})

def filter_brandingcodes(request):

    retailer_id = request.GET.get('retailer_id')

    brandingcodes = BrandingCode.objects.filter(retailer_id=retailer_id).order_by('name')

    brandingcode_choices = [{'id': brandingcode.id, 'name': brandingcode.name} for brandingcode in brandingcodes]
    
    return JsonResponse({'brandingcodes': brandingcode_choices})


def product_creation_success(request):
    return render(request, 'product_creation_success.html')

def product_form(request, brandingcode_id):
    if request.method == 'POST':
        
        try:
            qdict = request.POST
            productname=qdict['name']
            applicationprocess_id=qdict['applicationprocess']
            scorecard_id = qdict['scorecard']
            linetype_id =qdict['linetype']
            promotype_id =qdict['promotype']
            feetype_id=qdict['feetype']
            scorecardtier_ids=qdict.getlist('scorecardtier')
            creditlimit_ids=qdict.getlist('creditlimit')
            apr_ids=qdict.getlist('apr')
            mdr_ids=qdict.getlist('mdr')
            promo_ids=qdict.getlist('promo')
            fee_ids=qdict.getlist('fee')
            
            productdata={
                'name':productname,
                'applicationprocess':applicationprocess_id,
                'scorecard':scorecard_id,
                'linetype':linetype_id,
                'promotype':promotype_id,
                'feetype':feetype_id,
            }
            productform=ProductForm(productdata)
            if productform.is_valid():
                product=productform.save(commit=False)
                product.brandingcode=BrandingCode.objects.get(pk=brandingcode_id)
                product.state='AWP'
                product.creationdate=datetime.today()
                product.save()
                product_id=product.id
            for n in range(len(scorecardtier_ids)):
                print('loan ' + f'{n}')
                loandata={
                    'scorecardtier':scorecardtier_ids[n],
                    'creditlimit':creditlimit_ids[n],
                    'apr':apr_ids[n],
                    'mdr':mdr_ids[n],
                    'promo':promo_ids[n],
                    'fee':fee_ids[n]
                }
                print(loandata)
                loanform=LoanForm(loandata)
                if loanform.is_valid():
                    loan=loanform.save(commit=False)
                    loan.name= f"{product.name}, tier {ScorecardTier.objects.get(pk=scorecardtier_ids[n]).tier}"
                    loan.scorecard=Scorecard.objects.get(pk=scorecard_id)
                    loan.product=Product.objects.get(pk=product_id)
                    loan.save()
                else:
                    raise Exception('loan input error')
            return redirect('product_creation_success')
        except Exception as e:
            print(f'Error: {e}')
            form = ProductForm()
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


def get_loan_forms(request):
    scorecard_id = request.GET.get('scorecard_id')
    scorecardtiers = ScorecardTier.objects.filter(scorecard_id=scorecard_id)
    initial_data = [{'scorecardtier': scorecardtier.id} for scorecardtier in scorecardtiers]

    loan_forms=[]
    for data in initial_data:
        form = LoanForm(data)
        loan_forms.append(form)
    html = render_to_string('loan_forms.html', {'loan_forms':loan_forms})
    return JsonResponse({'html':html})


def filter_creditlines(request):

    scorecardtier_id = request.GET.get('scorecardtier_id')
    linetype_id = request.GET.get('linetype_id')

    creditlines = CreditLine.objects.filter(linetype_id=linetype_id).filter(tier=ScorecardTier.objects.get(pk=scorecardtier_id).tier).order_by('name')

    creditline_choices = [{'id': creditline.id, 'name': creditline.name} for creditline in creditlines]

    return JsonResponse({'creditlines': creditline_choices})


def filter_promos(request):
    promotype_id = request.GET.get('promotype_id')

    promos = Promo.objects.filter(promotype_id=promotype_id).order_by('name')

    promo_choices = [{'id': promo.id, 'name': promo.name} for promo in promos]

    return JsonResponse({'promos': promo_choices})

def filter_fees(request):
    feetype_id = request.GET.get('feetype_id')

    fees = Fee.objects.filter(feetype_id=feetype_id).order_by('name')

    fee_choices = [{'id': fee.id, 'name': fee.name} for fee in fees]

    return JsonResponse({'fees': fee_choices})


