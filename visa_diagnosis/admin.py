from django.contrib import admin
from .models import (
    VisaCategory, VisaRequirement, IndustryVisaMapping, 
    DiagnosisSession, DocumentTemplate
)


@admin.register(VisaCategory)
class VisaCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name_ja', 'category_type', 'priority', 'is_active']
    list_filter = ['category_type', 'is_active']
    search_fields = ['code', 'name_ja', 'name_en']
    ordering = ['priority', 'code']


@admin.register(VisaRequirement)
class VisaRequirementAdmin(admin.ModelAdmin):
    list_display = ['visa_category', 'requirement_type', 'condition', 'is_mandatory', 'alternative_ok']
    list_filter = ['visa_category', 'requirement_type', 'is_mandatory']
    search_fields = ['condition']


@admin.register(IndustryVisaMapping)
class IndustryVisaMappingAdmin(admin.ModelAdmin):
    list_display = ['industry', 'job_category', 'visa_category', 'match_score']
    list_filter = ['visa_category', 'industry']
    search_fields = ['industry', 'job_category']
    ordering = ['-match_score']


@admin.register(DiagnosisSession)
class DiagnosisSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['session_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ['visa_category', 'document_name', 'is_mandatory', 'display_order']
    list_filter = ['visa_category', 'is_mandatory']
    search_fields = ['document_name', 'description']
    ordering = ['visa_category', 'display_order']
