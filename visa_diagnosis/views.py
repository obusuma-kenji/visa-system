from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from .models import VisaCategory, DiagnosisSession
from .logic import VisaDiagnosisEngine


def index(request):
    """トップページ"""
    return render(request, 'visa_diagnosis/index.html')


def visa_list(request):
    """在留資格一覧"""
    visas = VisaCategory.objects.filter(is_active=True).order_by('priority')
    return render(request, 'visa_diagnosis/visa_list.html', {'visas': visas})


@csrf_exempt
@require_http_methods(["POST"])
def diagnose(request):
    """診断API"""
    try:
        # リクエストボディからデータ取得
        data = json.loads(request.body)
        
        # 診断エンジンの実行
        engine = VisaDiagnosisEngine()
        result = engine.diagnose(data)
        
        # セッションの保存
        session_id = str(uuid.uuid4())
        DiagnosisSession.objects.create(
            session_id=session_id,
            status='completed',
            applicant_data=data,
            diagnosis_result=result
        )
        
        result['session_id'] = session_id
        
        return JsonResponse(result, json_dumps_params={'ensure_ascii': False})
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'message': '診断処理中にエラーが発生しました'
        }, status=500)


def diagnosis_form(request):
    """診断フォーム"""
    return render(request, 'visa_diagnosis/diagnosis_form.html')


@csrf_exempt
@require_http_methods(["POST"])
def submit_diagnosis(request):
    """診断フォームの送信処理"""
    try:
        # フォームデータの取得
        applicant_data = {
            'nationality': request.POST.get('nationality', ''),
            'education': {
                'degree': request.POST.get('degree', ''),
                'major': request.POST.get('major', ''),
                'university': request.POST.get('university', ''),
            },
            'experience': [
                {
                    'years': int(request.POST.get('experience_years', 0)),
                    'field': request.POST.get('experience_field', ''),
                }
            ] if request.POST.get('experience_years') else [],
            'qualifications': [q.strip() for q in request.POST.get('qualifications', '').split(',') if q.strip()],
            'job_details': {
                'industry': request.POST.get('industry', ''),
                'position': request.POST.get('position', ''),
                'duties': request.POST.get('duties', ''),
            },
            'salary': int(request.POST.get('salary', 0)) if request.POST.get('salary') else 0,
            'company_info': {
                'name': request.POST.get('company_name', ''),
            }
        }
        
        # 診断実行
        engine = VisaDiagnosisEngine()
        result = engine.diagnose(applicant_data)
        
        # セッション保存
        session_id = str(uuid.uuid4())
        DiagnosisSession.objects.create(
            session_id=session_id,
            status='completed',
            applicant_data=applicant_data,
            diagnosis_result=result
        )
        
        return render(request, 'visa_diagnosis/result.html', {
            'result': result,
            'session_id': session_id
        })
        
    except Exception as e:
        return render(request, 'visa_diagnosis/error.html', {
            'error_message': f'診断処理中にエラーが発生しました: {str(e)}'
        })
