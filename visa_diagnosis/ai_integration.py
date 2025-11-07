"""
AI統合モジュール - Claude APIを使用した高度な判定
"""
import json
from typing import Dict, Any, Optional


class VisaAIAnalyzer:
    """
    Claude APIを使用した在留資格診断の高度化
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: Anthropic APIキー(Noneの場合はAI機能なしで動作)
        """
        self.api_key = api_key
        self.client = None  # ← 最初に必ず定義
        
        if api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                print("警告: anthropicパッケージがインストールされていません")
                self.client = None
            except Exception as e:
                print(f"警告: Claude APIの初期化に失敗しました: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """AI機能が利用可能かチェック"""
        return self.client is not None
    
    def analyze_major_relevance(self, major: str, job_field: str, job_description: str = "") -> Dict[str, Any]:
        """
        専攻と職種の関連性をAIで分析
        
        Args:
            major: 専攻（例: 情報工学）
            job_field: 職種（例: システムエンジニア）
            job_description: 業務内容（オプション）
        
        Returns:
            {
                'score': int (0-100),
                'level': str (高い/中程度/低い),
                'reason': str,
                'recommendation': str
            }
        """
        if not self.is_available():
            return {
                'score': 50,
                'level': '不明',
                'reason': 'AI機能が無効です（手動確認が必要）',
                'recommendation': '専攻と職種の関連性を手動で確認してください'
            }
        
        try:
            job_info = f"\n職務内容: {job_description}" if job_description else ""
            
            prompt = f"""あなたは日本の在留資格審査の専門家です。
以下の専攻と職種の関連性を評価してください。

専攻: {major}
職種: {job_field}{job_info}

評価基準:
- 直接関連（90-100点）: 専攻の知識が直接的に業務に活かせる
- 関連あり（70-89点）: 専攻の一部の知識が業務に活かせる
- やや関連（50-69点）: 間接的に役立つ知識がある
- 関連性低（0-49点）: ほとんど関係がない

以下のJSON形式で回答してください:
{{
    "score": <0-100の整数>,
    "level": "<高い/中程度/低い>",
    "reason": "<関連性の理由を1-2文で>",
    "recommendation": "<在留資格申請に関するアドバイス>"
}}"""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # レスポンスのパース
            response_text = message.content[0].text
            result = json.loads(response_text)
            
            return result
            
        except Exception as e:
            print(f"AI分析エラー: {e}")
            return {
                'score': 50,
                'level': '不明',
                'reason': f'AI分析中にエラーが発生しました: {str(e)}',
                'recommendation': '手動での確認を推奨します'
            }
    
    def analyze_job_description(self, job_description: str, visa_type: str = "技術・人文知識・国際業務") -> Dict[str, Any]:
        """
        業務内容を分析し、単純労働でないかを判定
        
        Args:
            job_description: 業務内容の説明
            visa_type: 対象の在留資格
        
        Returns:
            {
                'is_suitable': bool,
                'professional_score': int (0-100),
                'concerns': list,
                'strengths': list,
                'recommendations': list
            }
        """
        if not self.is_available():
            return {
                'is_suitable': None,
                'professional_score': 50,
                'concerns': ['AI機能が無効です'],
                'strengths': [],
                'recommendations': ['手動で業務内容を確認してください']
            }
        
        try:
            prompt = f"""あなたは日本の在留資格審査の専門家です。
以下の業務内容が在留資格「{visa_type}」に該当するか分析してください。

業務内容:
{job_description}

この在留資格の要件:
- 大学等で学んだ専門的な知識や技術が必要な業務
- 単純労働でないこと
- 判断、企画、設計などの知的業務

以下のJSON形式で回答してください:
{{
    "is_suitable": <true/false>,
    "professional_score": <0-100の整数>,
    "concerns": [<懸念点のリスト>],
    "strengths": [<強みのリスト>],
    "recommendations": [<改善提案のリスト>]
}}"""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            result = json.loads(response_text)
            
            return result
            
        except Exception as e:
            print(f"AI分析エラー: {e}")
            return {
                'is_suitable': None,
                'professional_score': 50,
                'concerns': [f'AI分析中にエラーが発生: {str(e)}'],
                'strengths': [],
                'recommendations': ['手動での確認を推奨します']
            }
    
    def generate_improvement_suggestions(self, applicant_data: Dict[str, Any], diagnosis_result: Dict[str, Any]) -> str:
        """
        診断結果に基づいて改善提案を生成
        
        Args:
            applicant_data: 申請者情報
            diagnosis_result: 診断結果
        
        Returns:
            改善提案のテキスト
        """
        if not self.is_available():
            return "AI機能が無効のため、改善提案を生成できません。"
        
        try:
            # 不足要件を抽出
            missing_items = []
            if diagnosis_result.get('top_recommendations'):
                top = diagnosis_result['top_recommendations'][0]
                missing_items = top.get('missing_items', [])
            
            if not missing_items:
                return "現在の条件で申請可能です。特に改善が必要な点はありません。"
            
            prompt = f"""あなたは在留資格申請の専門コンサルタントです。

申請者情報:
- 学歴: {applicant_data.get('education', {}).get('degree', '未記入')}
- 専攻: {applicant_data.get('education', {}).get('major', '未記入')}
- 経験年数: {sum([exp.get('years', 0) for exp in applicant_data.get('experience', [])])}年
- 職種: {applicant_data.get('job_details', {}).get('position', '未記入')}
- 報酬: {applicant_data.get('salary', 0)}円

不足している要件:
{json.dumps(missing_items, ensure_ascii=False, indent=2)}

これらの不足要件を満たすための具体的で実行可能な改善提案を3-5個、箇条書きで提案してください。
各提案は「・」で始めてください。"""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"AI分析エラー: {e}")
            return f"改善提案の生成中にエラーが発生しました: {str(e)}"


# 簡易的なテスト用関数
def test_ai_integration(api_key: str):
    """AI統合のテスト"""
    analyzer = VisaAIAnalyzer(api_key)
    
    if not analyzer.is_available():
        print("❌ AI機能が利用できません")
        return
    
    print("✅ AI機能が利用可能です")
    
    # テスト1: 専攻と職種の関連性
    print("\n【テスト1】専攻と職種の関連性分析")
    result = analyzer.analyze_major_relevance("情報工学", "システムエンジニア")
    print(f"スコア: {result['score']}点")
    print(f"レベル: {result['level']}")
    print(f"理由: {result['reason']}")
    
    # テスト2: 業務内容の分析
    print("\n【テスト2】業務内容の分析")
    job_desc = "顧客の要望をヒアリングし、Webシステムの設計・開発を行う。要件定義から実装、テストまで担当。"
    result = analyzer.analyze_job_description(job_desc)
    print(f"適合: {result['is_suitable']}")
    print(f"専門性スコア: {result['professional_score']}点")
    print(f"強み: {', '.join(result['strengths'][:2])}")
    
    print("\n✅ テスト完了")


if __name__ == "__main__":
    # テスト実行
    import sys
    if len(sys.argv) > 1:
        test_ai_integration(sys.argv[1])
    else:
        print("使用方法: python ai_integration.py YOUR_API_KEY")
