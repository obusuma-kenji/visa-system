"""
在留資格診断エンジン
"""
import re
from typing import Dict, List, Any
from django.conf import settings
from .models import VisaCategory, VisaRequirement, IndustryVisaMapping, DocumentTemplate
from .ai_integration import VisaAIAnalyzer


class VisaDiagnosisEngine:
    """在留資格診断エンジン"""
    
    def __init__(self):
        """初期化"""
        self.visa_categories = VisaCategory.objects.filter(is_active=True)
        
        # AI機能の初期化
        self.ai_analyzer = None
        if settings.ENABLE_AI_FEATURES and settings.ANTHROPIC_API_KEY:
            self.ai_analyzer = VisaAIAnalyzer(settings.ANTHROPIC_API_KEY)
            if self.ai_analyzer.is_available():
                print("✅ AI機能が有効化されました")
            else:
                print("⚠️ AI機能の初期化に失敗しました")
        else:
            print("ℹ️ AI機能は無効です（settings.pyで有効化できます）")
    
    def diagnose(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        診断のメイン処理
        
        Args:
            applicant_data: 申請者情報
                - nationality: 国籍
                - education: 学歴情報 {degree, major, university}
                - experience: 実務経験 [{years, field, position}]
                - qualifications: 保有資格リスト
                - job_details: 職務情報 {industry, position, duties}
                - salary: 月額報酬
                - company_info: 企業情報
        
        Returns:
            診断結果の辞書
        """
        results = []
        
        # 業種・職種からの候補抽出
        initial_candidates = self._get_candidates_by_job(applicant_data.get('job_details', {}))
        
        # 各在留資格について適合度を計算
        for visa in self.visa_categories:
            # 初期候補に含まれない場合はスキップ（効率化）
            if initial_candidates and visa.id not in initial_candidates:
                continue
            
            score = self._calculate_match_score(visa, applicant_data)
            
            if score['total_score'] > 0:
                results.append({
                    'visa_category': {
                        'id': visa.id,
                        'code': visa.code,
                        'name_ja': visa.name_ja,
                        'name_en': visa.name_en,
                        'description': visa.description,
                    },
                    'match_score': score['total_score'],
                    'requirements_status': score['details'],
                    'missing_items': score['missing'],
                    'recommendation_level': self._get_recommendation_level(score['total_score']),
                    'approval_probability': self._estimate_approval_probability(score['total_score'], score['missing']),
                    'required_documents': self._get_required_documents(visa),
                })
        
        # スコアでソート
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        # AI機能による追加分析
        ai_analysis = self._perform_ai_analysis(applicant_data, results)
        
        return {
            'diagnosis_id': self._generate_diagnosis_id(),
            'applicant_summary': self._create_applicant_summary(applicant_data),
            'top_recommendations': results[:3],
            'all_options': results,
            'analysis_summary': self._generate_summary(results, applicant_data),
            'next_steps': self._generate_next_steps(results),
            'ai_analysis': ai_analysis,  # AI分析結果を追加
        }
    
    def _get_candidates_by_job(self, job_details: Dict[str, Any]) -> List[int]:
        """業種・職種から候補となる在留資格を抽出"""
        if not job_details:
            return []
        
        industry = job_details.get('industry', '')
        position = job_details.get('position', '')
        
        if not industry and not position:
            return []
        
        # マッピングテーブルから検索
        mappings = IndustryVisaMapping.objects.filter(
            industry__icontains=industry
        ) | IndustryVisaMapping.objects.filter(
            job_category__icontains=position
        )
        
        return [m.visa_category_id for m in mappings.distinct()]
    
    def _calculate_match_score(self, visa: VisaCategory, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """各在留資格の適合度スコア計算"""
        score = 0
        max_score = 0
        details = []
        missing = []
        
        requirements = visa.requirements.all()
        
        if not requirements.exists():
            # 要件が設定されていない場合は中程度のスコア
            return {
                'total_score': 50,
                'details': [{'requirement': '要件未設定', 'status': '要確認', 'type': 'other'}],
                'missing': ['要件情報の確認が必要']
            }
        
        for req in requirements:
            weight = 20 if req.is_mandatory else 10
            max_score += weight
            
            check_result = self._check_requirement(req, applicant_data)
            
            if check_result['met']:
                score += weight
                details.append({
                    'requirement': req.condition,
                    'status': '✓ 充足',
                    'type': req.get_requirement_type_display(),
                    'detail': check_result.get('reason', '')
                })
            else:
                status = '✗ 不足' if req.is_mandatory else '△ 推奨'
                details.append({
                    'requirement': req.condition,
                    'status': status,
                    'type': req.get_requirement_type_display(),
                    'detail': check_result.get('reason', '')
                })
                if req.is_mandatory:
                    missing.append({
                        'requirement': req.condition,
                        'alternative': req.alternative_condition if req.alternative_ok else None
                    })
        
        return {
            'total_score': int((score / max_score * 100) if max_score > 0 else 0),
            'details': details,
            'missing': missing
        }
    
    def _check_requirement(self, requirement: VisaRequirement, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """個別要件のチェック"""
        req_type = requirement.requirement_type
        
        if req_type == 'education':
            return self._check_education(requirement, applicant_data.get('education', {}))
        elif req_type == 'experience':
            return self._check_experience(requirement, applicant_data.get('experience', []))
        elif req_type == 'salary':
            return self._check_salary(requirement, applicant_data.get('salary', 0))
        elif req_type == 'qualification':
            return self._check_qualifications(requirement, applicant_data.get('qualifications', []))
        elif req_type == 'company':
            return self._check_company(requirement, applicant_data.get('company_info', {}))
        else:
            return {'met': None, 'reason': '手動確認が必要'}
    
    def _check_education(self, requirement: VisaRequirement, education_data: Dict[str, Any]) -> Dict[str, Any]:
        """学歴要件チェック（AI統合版）"""
        condition = requirement.condition.lower()
        degree = education_data.get('degree', '').lower()
        major = education_data.get('major', '')
        
        # 大学卒業以上
        if '大学' in condition or '学士' in condition:
            valid_degrees = ['学士', '修士', '博士', 'bachelor', 'master', 'phd', 'doctor']
            if any(d in degree for d in valid_degrees):
                return {'met': True, 'reason': f'学歴: {education_data.get("degree", "")}'}
        
        # 専門学校
        if '専門学校' in condition:
            if '専門' in degree or 'diploma' in degree or '専修' in degree:
                return {'met': True, 'reason': f'学歴: {education_data.get("degree", "")}'}
        
        # 関連専攻（AI機能があれば使用）
        if '関連' in condition or '専攻' in condition:
            if major:
                # AI機能が有効な場合は詳細分析
                if self.ai_analyzer and self.ai_analyzer.is_available():
                    # 後で職種との関連性をチェックする際に使用
                    return {'met': True, 'reason': f'専攻: {major}（AI分析で関連性を判定）'}
                else:
                    return {'met': True, 'reason': f'専攻: {major}（関連性は要確認）'}
        
        return {'met': False, 'reason': f'現在の学歴: {education_data.get("degree", "未記入")}'}
    
    def _check_experience(self, requirement: VisaRequirement, experience_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """実務経験要件チェック"""
        total_years = sum([exp.get('years', 0) for exp in experience_data])
        condition = requirement.condition
        
        # 正規表現で年数を抽出
        years_match = re.search(r'(\d+)年', condition)
        if years_match:
            required_years = int(years_match.group(1))
            if total_years >= required_years:
                return {'met': True, 'reason': f'実務経験: {total_years}年'}
            else:
                return {'met': False, 'reason': f'実務経験: {total_years}年（{required_years}年必要）'}
        
        return {'met': None, 'reason': '実務経験の確認が必要'}
    
    def _check_salary(self, requirement: VisaRequirement, salary: int) -> Dict[str, Any]:
        """報酬要件チェック"""
        condition = requirement.condition
        
        # 日本人と同等以上
        if '日本人と同等' in condition or '同等以上' in condition:
            # 業種・職種別の最低ラインを設定（簡易版）
            min_salary = 220000  # 最低基準
            if salary >= min_salary:
                return {'met': True, 'reason': f'月額報酬: ¥{salary:,}'}
            else:
                return {'met': False, 'reason': f'月額報酬: ¥{salary:,}（低い可能性あり）'}
        
        # 金額指定がある場合
        amount_match = re.search(r'(\d+)万円', condition)
        if amount_match:
            required_amount = int(amount_match.group(1)) * 10000
            if salary >= required_amount:
                return {'met': True, 'reason': f'月額報酬: ¥{salary:,}'}
            else:
                return {'met': False, 'reason': f'月額報酬: ¥{salary:,}（¥{required_amount:,}必要）'}
        
        return {'met': True, 'reason': '報酬要件の詳細確認が必要'}
    
    def _check_qualifications(self, requirement: VisaRequirement, qualifications: List[str]) -> Dict[str, Any]:
        """資格要件チェック"""
        condition = requirement.condition
        
        # 日本語能力試験
        if 'N4' in condition or 'JLPT' in condition:
            jlpt_found = any('N4' in q or 'N3' in q or 'N2' in q or 'N1' in q for q in qualifications)
            if jlpt_found:
                return {'met': True, 'reason': f'保有資格に日本語能力試験あり'}
            else:
                return {'met': False, 'reason': '日本語能力試験N4以上が必要'}
        
        # 特定技能評価試験
        if '特定技能' in condition and '評価試験' in condition:
            tokutei_found = any('特定技能' in q or '評価試験' in q for q in qualifications)
            if tokutei_found:
                return {'met': True, 'reason': '特定技能評価試験合格'}
            else:
                return {'met': False, 'reason': '特定技能評価試験の合格が必要'}
        
        # その他の資格
        if qualifications:
            return {'met': True, 'reason': f'保有資格あり（要確認）'}
        
        return {'met': False, 'reason': '必要資格なし'}
    
    def _check_company(self, requirement: VisaRequirement, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """企業要件チェック"""
        # 簡易版：企業情報があればOK
        if company_info:
            return {'met': True, 'reason': '企業情報確認済み'}
        return {'met': None, 'reason': '企業情報の確認が必要'}
    
    def _get_recommendation_level(self, score: int) -> str:
        """推奨レベルの判定"""
        if score >= 80:
            return '◎ 強く推奨'
        elif score >= 60:
            return '○ 推奨'
        elif score >= 40:
            return '△ 条件付き可能'
        else:
            return '✗ 困難'
    
    def _estimate_approval_probability(self, score: int, missing_items: List[Dict]) -> str:
        """許可見込みの推定"""
        if missing_items:
            mandatory_missing = any(item for item in missing_items if not item.get('alternative'))
            if mandatory_missing:
                return '低い（必須要件不足）'
        
        if score >= 80:
            return '高い（80%以上）'
        elif score >= 60:
            return '中程度（50-70%）'
        else:
            return '要検討（50%未満）'
    
    def _get_required_documents(self, visa: VisaCategory) -> List[Dict[str, str]]:
        """必要書類リストの取得"""
        documents = visa.documents.filter(is_mandatory=True).order_by('display_order')
        return [
            {
                'name': doc.document_name,
                'description': doc.description,
                'url': doc.url
            }
            for doc in documents
        ]
    
    def _create_applicant_summary(self, applicant_data: Dict[str, Any]) -> Dict[str, str]:
        """申請者サマリーの作成"""
        education = applicant_data.get('education', {})
        experience = applicant_data.get('experience', [])
        job_details = applicant_data.get('job_details', {})
        
        return {
            'nationality': applicant_data.get('nationality', '未記入'),
            'education': f"{education.get('degree', '')}（{education.get('major', '')}専攻）" if education else '未記入',
            'experience_years': sum([exp.get('years', 0) for exp in experience]),
            'target_job': f"{job_details.get('industry', '')} - {job_details.get('position', '')}" if job_details else '未記入',
        }
    
    def _generate_summary(self, results: List[Dict], applicant_data: Dict[str, Any]) -> str:
        """診断サマリーの生成"""
        if not results:
            return '申請者の情報では、該当する在留資格が見つかりませんでした。詳細をご確認ください。'
        
        top = results[0]
        visa_name = top['visa_category']['name_ja']
        score = top['match_score']
        level = top['recommendation_level']
        
        summary = f"{visa_name}での申請を推奨します（適合度{score}点、{level}）。"
        
        if top['missing_items']:
            summary += f" ただし、{len(top['missing_items'])}項目の要件が不足しています。"
        else:
            summary += " 全ての必須要件を満たしています。"
        
        return summary
    
    def _generate_next_steps(self, results: List[Dict]) -> List[str]:
        """次のステップの生成"""
        if not results:
            return ['申請者情報の再確認をお願いします。']
        
        top = results[0]
        steps = []
        
        # 書類準備
        if top['required_documents']:
            steps.append(f"必要書類の準備（{len(top['required_documents'])}種類）")
        
        # 不足要件への対応
        if top['missing_items']:
            steps.append('不足要件への対応検討')
        
        # 申請書類作成
        steps.append('在留資格認定証明書交付申請書の作成')
        
        # 専門家への相談
        if top['match_score'] < 70:
            steps.append('社会保険労務士・行政書士への相談を推奨')
        
        return steps
    
    def _generate_diagnosis_id(self) -> str:
        """診断IDの生成"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = random.randint(1000, 9999)
        return f"DIAG-{timestamp}-{random_suffix}"
    
    def _perform_ai_analysis(self, applicant_data: Dict[str, Any], results: List[Dict]) -> Dict[str, Any]:
        """AI機能による追加分析"""
        if not self.ai_analyzer or not self.ai_analyzer.is_available():
            return {
                'enabled': False,
                'message': 'AI機能は現在無効です。settings.pyでANTHROPIC_API_KEYを設定してください。'
            }
        
        try:
            education = applicant_data.get('education', {})
            job_details = applicant_data.get('job_details', {})
            
            major = education.get('major', '')
            position = job_details.get('position', '')
            duties = job_details.get('duties', '')
            
            analysis = {
                'enabled': True,
                'major_relevance': None,
                'job_suitability': None,
                'improvement_suggestions': None
            }
            
            # 専攻と職種の関連性分析
            if major and position:
                analysis['major_relevance'] = self.ai_analyzer.analyze_major_relevance(
                    major, position, duties
                )
            
            # 業務内容の分析
            if duties and results:
                top_visa = results[0]['visa_category']['name_ja']
                analysis['job_suitability'] = self.ai_analyzer.analyze_job_description(
                    duties, top_visa
                )
            
            # 改善提案の生成
            if results:
                diagnosis_result = {
                    'top_recommendations': results[:3]
                }
                analysis['improvement_suggestions'] = self.ai_analyzer.generate_improvement_suggestions(
                    applicant_data, diagnosis_result
                )
            
            return analysis
            
        except Exception as e:
            print(f"AI分析エラー: {e}")
            return {
                'enabled': True,
                'error': str(e),
                'message': 'AI分析中にエラーが発生しました'
            }
