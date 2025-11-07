from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class VisaCategory(models.Model):
    """在留資格カテゴリ"""
    
    CATEGORY_TYPES = [
        ('work', '就労'),
        ('activity', '身分・地位'),
        ('specified', '特定活動'),
    ]
    
    code = models.CharField('資格コード', max_length=50, unique=True)
    name_ja = models.CharField('資格名（日本語）', max_length=100)
    name_en = models.CharField('資格名（英語）', max_length=100, blank=True)
    category_type = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_TYPES)
    description = models.TextField('説明', blank=True)
    priority = models.IntegerField('優先順位', default=0)
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        db_table = 'visa_categories'
        verbose_name = '在留資格'
        verbose_name_plural = '在留資格一覧'
        ordering = ['priority', 'code']
    
    def __str__(self):
        return f"{self.name_ja} ({self.code})"


class VisaRequirement(models.Model):
    """在留資格要件"""
    
    REQUIREMENT_TYPES = [
        ('education', '学歴'),
        ('experience', '実務経験'),
        ('qualification', '資格'),
        ('salary', '報酬'),
        ('company', '企業要件'),
        ('other', 'その他'),
    ]
    
    visa_category = models.ForeignKey(
        VisaCategory, 
        on_delete=models.CASCADE,
        related_name='requirements',
        verbose_name='在留資格'
    )
    requirement_type = models.CharField('要件種別', max_length=30, choices=REQUIREMENT_TYPES)
    condition = models.TextField('要件内容')
    is_mandatory = models.BooleanField('必須', default=True)
    alternative_condition = models.TextField('代替条件', blank=True)
    alternative_ok = models.BooleanField('代替可能', default=False)
    display_order = models.IntegerField('表示順', default=0)
    
    class Meta:
        db_table = 'visa_requirements'
        verbose_name = '在留資格要件'
        verbose_name_plural = '在留資格要件一覧'
        ordering = ['visa_category', 'display_order', 'requirement_type']
    
    def __str__(self):
        return f"{self.visa_category.code} - {self.get_requirement_type_display()}: {self.condition[:50]}"


class IndustryVisaMapping(models.Model):
    """業種・職種と在留資格のマッピング"""
    
    industry = models.CharField('業種', max_length=100)
    job_category = models.CharField('職種', max_length=100)
    visa_category = models.ForeignKey(
        VisaCategory,
        on_delete=models.CASCADE,
        related_name='industry_mappings',
        verbose_name='在留資格'
    )
    match_score = models.IntegerField(
        '適合度',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='0-100の範囲で適合度を入力'
    )
    notes = models.TextField('備考', blank=True)
    
    class Meta:
        db_table = 'industry_visa_mapping'
        verbose_name = '業種職種マッピング'
        verbose_name_plural = '業種職種マッピング一覧'
        ordering = ['-match_score']
    
    def __str__(self):
        return f"{self.industry} - {self.job_category} → {self.visa_category.code} ({self.match_score}点)"


class DiagnosisSession(models.Model):
    """診断セッション"""
    
    STATUS_CHOICES = [
        ('in_progress', '進行中'),
        ('completed', '完了'),
        ('abandoned', '中断'),
    ]
    
    session_id = models.CharField('セッションID', max_length=100, unique=True)
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='in_progress')
    applicant_data = models.JSONField('申請者情報', default=dict)
    diagnosis_result = models.JSONField('診断結果', default=dict, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        db_table = 'diagnosis_sessions'
        verbose_name = '診断セッション'
        verbose_name_plural = '診断セッション一覧'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"診断 {self.session_id} ({self.get_status_display()})"


class DocumentTemplate(models.Model):
    """必要書類テンプレート"""
    
    visa_category = models.ForeignKey(
        VisaCategory,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='在留資格'
    )
    document_name = models.CharField('書類名', max_length=200)
    description = models.TextField('説明', blank=True)
    is_mandatory = models.BooleanField('必須', default=True)
    url = models.URLField('参考URL', blank=True)
    display_order = models.IntegerField('表示順', default=0)
    
    class Meta:
        db_table = 'document_templates'
        verbose_name = '必要書類テンプレート'
        verbose_name_plural = '必要書類テンプレート一覧'
        ordering = ['visa_category', 'display_order']
    
    def __str__(self):
        return f"{self.visa_category.code} - {self.document_name}"
