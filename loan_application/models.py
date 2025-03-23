from django.db import models
from django.conf import settings
from accounts.models import CustomUser, FarmerProfile, FinancialInstitutionProfile
from credit_score.models import CreditScore
from gis_data.models import Farmland

class LoanProduct(models.Model):
    """Different loan products offered by financial institutions."""
    name = models.CharField(max_length=100)
    financial_institution = models.ForeignKey(FinancialInstitutionProfile, on_delete=models.CASCADE, related_name='loan_products')
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in percentage")
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Processing fee in percentage")
    tenure_min = models.PositiveIntegerField(help_text="Minimum tenure in months")
    tenure_max = models.PositiveIntegerField(help_text="Maximum tenure in months")
    min_credit_score = models.PositiveIntegerField(default=0, help_text="Minimum credit score required")
    purpose = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.financial_institution.institution_name}"

class LoanApplication(models.Model):
    """Model for loan applications."""
    LOAN_TYPES = (
        ('crop_loan', 'Crop Loan'),
        ('equipment_loan', 'Farm Equipment Loan'),
        ('development_loan', 'Farm Development Loan'),
        ('livestock_loan', 'Livestock Loan'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    )
    
    # Foreign keys
    farmer = models.ForeignKey('accounts.FarmerProfile', on_delete=models.CASCADE, related_name='loan_applications')
    farmland = models.ForeignKey('gis_data.Farmland', on_delete=models.SET_NULL, blank=True, null=True, related_name='loan_applications')
    
    # Basic info
    application_number = models.CharField(max_length=20, unique=True)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    term = models.IntegerField(help_text="Loan term in months")
    purpose = models.TextField()
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_loan_type_display()} - ₹{self.amount_requested} ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-created_at']

class LoanAgreement(models.Model):
    """Loan agreements for approved applications."""
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='loan_agreement')
    agreement_number = models.CharField(max_length=20, unique=True)
    amount_approved = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure = models.PositiveIntegerField(help_text="Tenure in months")
    disbursement_date = models.DateField()
    maturity_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_payable = models.DecimalField(max_digits=12, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    signed_document = models.FileField(upload_to='loan_agreements/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Loan Agreement #{self.agreement_number}"

class RepaymentSchedule(models.Model):
    """Repayment schedule for loans."""
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partially_paid', 'Partially Paid'),
        ('waived', 'Waived'),
    )
    
    loan_agreement = models.ForeignKey(LoanAgreement, on_delete=models.CASCADE, related_name='repayment_schedule')
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Installment #{self.installment_number} for Loan #{self.loan_agreement.agreement_number}"
    
    class Meta:
        ordering = ['installment_number']

class Payment(models.Model):
    """Payment records for loan repayments."""
    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('check', 'Check'),
        ('other', 'Other'),
    )
    
    repayment = models.ForeignKey(RepaymentSchedule, on_delete=models.CASCADE, related_name='payments')
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    received_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_payments',
        limit_choices_to={'user_type': 'financial_institution'}
    )
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of ₹{self.payment_amount} for {self.repayment.loan_agreement.loan_application.farmer.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Update repayment status based on payment
        repayment = self.repayment
        total_paid = Payment.objects.filter(repayment=repayment).aggregate(models.Sum('payment_amount'))['payment_amount__sum'] or 0
        repayment.amount_paid = total_paid
        
        if total_paid >= repayment.total_amount:
            repayment.status = 'paid'
            repayment.payment_date = self.payment_date
        elif total_paid > 0:
            repayment.status = 'partially_paid'
        
        repayment.save()
    
    class Meta:
        ordering = ['-payment_date']
