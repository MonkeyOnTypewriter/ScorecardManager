from django.db import models

from scorecards.models import Scorecard, ScorecardTier

class Retailer(models.Model):
	name=models.CharField(max_length=128)
	def __str__(self):
		return self.name

#Tracking changes to mdr, fee, apr, credit limit, and promo -> do changes apply to all account, or only new originations?

class LineType(models.Model):
	name=models.CharField(max_length=64)
	def __str__(self):
		return self.name


class CreditLine(models.Model):
	name=models.CharField(max_length=64)
	linetype=models.ForeignKey(LineType, on_delete=models.CASCADE)
	limit=models.DecimalField(max_digits=7, decimal_places=2)
	tier=models.CharField(max_length=2)
	
	def __str__(self):
		return self.name
	

class PromoType(models.Model):
	name=models.CharField(max_length=64)
	type = models.CharField(max_length=64)
	description = models.CharField(max_length=128)	
	
	def __str__(self):
		return self.name

class Promo(models.Model):
	name=models.CharField(max_length=64)
	promotype=models.ForeignKey(PromoType, on_delete=models.CASCADE)
	length=models.CharField(max_length=16)
	
	def __str__(self):
		return self.name
	
class FeeType(models.Model):
	name=models.CharField(max_length=64)
	type=models.CharField(max_length=64)
	description=models.CharField(max_length=128)
	
	def __str__(self):
		return self.name

class Fee(models.Model):
	name=models.CharField(max_length=64)
	feetype=models.ForeignKey(FeeType, on_delete=models.CASCADE)
	amount=models.DecimalField(max_digits=5, decimal_places=2)
	
	def __str__(self):
		return self.name
	
class APR(models.Model):
	name=models.CharField(max_length=64)
	rate=models.DecimalField(max_digits=4, decimal_places=4)
	
	def __str__(self):
		return self.name
	
class Discount(models.Model):
	name=models.CharField(max_length=64)
	rate=models.DecimalField(max_digits=4, decimal_places=4)
	
	def __str__(self):
		return self.name
	

class ApplicationProcess(models.Model):
	name=models.CharField(max_length=32)
	
	def __str__(self):
		return self.name
	

class BrandingCode(models.Model):
	name=models.CharField(max_length=128)
	retailer=models.ForeignKey(Retailer, on_delete=models.CASCADE)
	activeproduct=models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='activeproduct')
	   
	def __str__(self):
		return self.name
	

class Product(models.Model):
	STATES= {
		'DAD':"deactivated",
		'ACT':"active",
		'AWP':"awaiting approval",
		'AWA':"awaiting activation",
		'RJT':"rejected"
	}
	name=models.CharField(max_length=128)
	state=models.CharField(max_length=3, choices=STATES)
	scorecard=models.ForeignKey(Scorecard, on_delete=models.CASCADE)
	promotype=models.ForeignKey(PromoType, on_delete=models.CASCADE)
	feetype=models.ForeignKey(FeeType, on_delete=models.CASCADE)
	linetype=models.ForeignKey(LineType, on_delete=models.CASCADE)
	applicationprocess=models.ForeignKey(ApplicationProcess, on_delete=models.CASCADE)
	brandingcode=models.ForeignKey(BrandingCode, on_delete=models.CASCADE)
	creationdate=models.DateField()
	approvaldate=models.DateField(null=True, blank=True)
	activationdate=models.DateField(null=True, blank=True)
	rejectiondate=models.DateField(null=True, blank=True)
	deactivationdate=models.DateField(null=True, blank=True)

	def __str__(self):
		return self.name
	

class Loan(models.Model):
	name=models.CharField(max_length=128)
	scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE)
	scorecardtier = models.ForeignKey(ScorecardTier, on_delete=models.CASCADE)
	creditlimit = models.ForeignKey(CreditLine, on_delete=models.CASCADE)
	promo=models.ForeignKey(Promo, on_delete=models.CASCADE)
	apr=models.ForeignKey(APR, on_delete=models.CASCADE)
	fee=models.ForeignKey(Fee, on_delete=models.CASCADE)
	mdr=models.ForeignKey(Discount, on_delete=models.CASCADE)
	product=models.ForeignKey(Product, on_delete=models.CASCADE)

	class Meta:
		constraints= [
			models.UniqueConstraint(fields=['product', 'scorecardtier'], name='unique_product_scorecardtier')
		]
		   
	def __str__(self):
		return self.name

	


