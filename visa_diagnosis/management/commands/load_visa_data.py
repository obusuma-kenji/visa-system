"""
初期データ投入用カスタムコマンド
python manage.py load_visa_data
"""
from django.core.management.base import BaseCommand
from visa_diagnosis.models import (
    VisaCategory, VisaRequirement, IndustryVisaMapping, DocumentTemplate
)


class Command(BaseCommand):
    help = '在留資格の初期データを投入します'
    
    def handle(self, *args, **options):
        self.stdout.write('初期データの投入を開始します...')
        
        # 既存データのクリア
        self.stdout.write('既存データをクリアしています...')
        DocumentTemplate.objects.all().delete()
        IndustryVisaMapping.objects.all().delete()
        VisaRequirement.objects.all().delete()
        VisaCategory.objects.all().delete()
        
        # 在留資格の作成
        self.stdout.write('在留資格を作成しています...')
        self._create_visa_categories()
        
        # 要件の作成
        self.stdout.write('要件を作成しています...')
        self._create_requirements()
        
        # 業種マッピングの作成
        self.stdout.write('業種マッピングを作成しています...')
        self._create_industry_mappings()
        
        # 必要書類の作成
        self.stdout.write('必要書類を作成しています...')
        self._create_documents()
        
        self.stdout.write(self.style.SUCCESS('初期データの投入が完了しました！'))
    
    def _create_visa_categories(self):
        """在留資格の作成"""
        categories = [
            {
                'code': 'engineer_specialist',
                'name_ja': '技術・人文知識・国際業務',
                'name_en': 'Engineer/Specialist in Humanities/International Services',
                'category_type': 'work',
                'description': '理学、工学、人文科学、社会科学の分野に属する技術・知識を要する業務、外国の文化に基盤を有する思考・感受性を必要とする業務に従事する活動',
                'priority': 1,
            },
            {
                'code': 'specified_skilled_worker_1',
                'name_ja': '特定技能1号',
                'name_en': 'Specified Skilled Worker (i)',
                'category_type': 'specified',
                'description': '特定産業分野（14分野）において、相当程度の知識または経験を必要とする技能を要する業務に従事する活動',
                'priority': 2,
            },
            {
                'code': 'specified_skilled_worker_2',
                'name_ja': '特定技能2号',
                'name_en': 'Specified Skilled Worker (ii)',
                'category_type': 'specified',
                'description': '特定産業分野において、熟練した技能を要する業務に従事する活動',
                'priority': 3,
            },
            {
                'code': 'highly_skilled_professional',
                'name_ja': '高度専門職',
                'name_en': 'Highly Skilled Professional',
                'category_type': 'work',
                'description': 'ポイント制により、高度な専門的知識や技術を有する外国人の活動',
                'priority': 4,
            },
            {
                'code': 'skilled_labor',
                'name_ja': '技能',
                'name_en': 'Skilled Labor',
                'category_type': 'work',
                'description': '産業上の特殊な分野に属する熟練した技能を要する業務に従事する活動',
                'priority': 5,
            },
            {
                'code': 'intra_company_transferee',
                'name_ja': '企業内転勤',
                'name_en': 'Intra-company Transferee',
                'category_type': 'work',
                'description': '外国の事業所からの期間を定めた転勤により、日本の事業所において技術・知識を要する業務または国際業務に従事する活動',
                'priority': 6,
            },
        ]
        
        for cat_data in categories:
            VisaCategory.objects.create(**cat_data)
    
    def _create_requirements(self):
        """要件の作成"""
        
        # 技術・人文知識・国際業務
        engineer = VisaCategory.objects.get(code='engineer_specialist')
        VisaRequirement.objects.create(
            visa_category=engineer,
            requirement_type='education',
            condition='大学卒業以上、または関連分野の専攻（理工系、人文科学、社会科学など）',
            is_mandatory=True,
            alternative_condition='実務経験10年以上で代替可能（専門学校卒の場合は3年以上）',
            alternative_ok=True,
            display_order=1
        )
        VisaRequirement.objects.create(
            visa_category=engineer,
            requirement_type='salary',
            condition='日本人が従事する場合に受ける報酬と同等額以上',
            is_mandatory=True,
            display_order=2
        )
        VisaRequirement.objects.create(
            visa_category=engineer,
            requirement_type='other',
            condition='単純労働でないこと（専門的・技術的な業務内容）',
            is_mandatory=True,
            display_order=3
        )
        
        # 特定技能1号
        tokutei1 = VisaCategory.objects.get(code='specified_skilled_worker_1')
        VisaRequirement.objects.create(
            visa_category=tokutei1,
            requirement_type='qualification',
            condition='特定産業分野の技能評価試験に合格',
            is_mandatory=True,
            alternative_condition='技能実習2号を良好に修了',
            alternative_ok=True,
            display_order=1
        )
        VisaRequirement.objects.create(
            visa_category=tokutei1,
            requirement_type='qualification',
            condition='日本語能力試験N4以上または国際交流基金日本語基礎テストに合格',
            is_mandatory=True,
            display_order=2
        )
        VisaRequirement.objects.create(
            visa_category=tokutei1,
            requirement_type='other',
            condition='特定産業分野での就労（介護、ビルクリーニング、素形材産業、産業機械製造業、電気・電子情報関連産業、建設、造船・舶用工業、自動車整備、航空、宿泊、農業、漁業、飲食料品製造業、外食業）',
            is_mandatory=True,
            display_order=3
        )
        
        # 特定技能2号
        tokutei2 = VisaCategory.objects.get(code='specified_skilled_worker_2')
        VisaRequirement.objects.create(
            visa_category=tokutei2,
            requirement_type='qualification',
            condition='特定産業分野の技能評価試験（2号レベル）に合格',
            is_mandatory=True,
            display_order=1
        )
        VisaRequirement.objects.create(
            visa_category=tokutei2,
            requirement_type='other',
            condition='特定産業分野での就労（建設、造船・舶用工業）※2024年時点',
            is_mandatory=True,
            display_order=2
        )
        
        # 高度専門職
        highly_skilled = VisaCategory.objects.get(code='highly_skilled_professional')
        VisaRequirement.objects.create(
            visa_category=highly_skilled,
            requirement_type='other',
            condition='ポイント計算で70点以上（学歴、職歴、年収、年齢等で算出）',
            is_mandatory=True,
            display_order=1
        )
        VisaRequirement.objects.create(
            visa_category=highly_skilled,
            requirement_type='education',
            condition='修士号以上が有利（ポイント加算）',
            is_mandatory=False,
            display_order=2
        )
        VisaRequirement.objects.create(
            visa_category=highly_skilled,
            requirement_type='salary',
            condition='年収300万円以上（ポイント加算の基準）',
            is_mandatory=True,
            display_order=3
        )
        
        # 技能
        skilled = VisaCategory.objects.get(code='skilled_labor')
        VisaRequirement.objects.create(
            visa_category=skilled,
            requirement_type='experience',
            condition='該当分野での実務経験10年以上',
            is_mandatory=True,
            display_order=1
        )
        VisaRequirement.objects.create(
            visa_category=skilled,
            requirement_type='other',
            condition='特殊な技能（調理師、建築技術者、外国特有製品製造・修理など）',
            is_mandatory=True,
            display_order=2
        )
        
        # 企業内転勤
        transfer = VisaCategory.objects.get(code='intra_company_transferee')
        VisaRequirement.objects.create(
            visa_category=transfer,
            requirement_type='experience',
            condition='転勤直前に外国の事業所で1年以上継続して勤務',
            is_mandatory=True,
            display_order=1
        )
        VisaRequirement.objects.create(
            visa_category=transfer,
            requirement_type='other',
            condition='技術・知識を要する業務または国際業務に従事',
            is_mandatory=True,
            display_order=2
        )
    
    def _create_industry_mappings(self):
        """業種マッピングの作成"""
        engineer = VisaCategory.objects.get(code='engineer_specialist')
        tokutei1 = VisaCategory.objects.get(code='specified_skilled_worker_1')
        skilled = VisaCategory.objects.get(code='skilled_labor')
        
        mappings = [
            # IT関連
            {'industry': 'IT・ソフトウェア', 'job': 'システムエンジニア', 'visa': engineer, 'score': 95},
            {'industry': 'IT・ソフトウェア', 'job': 'プログラマー', 'visa': engineer, 'score': 90},
            {'industry': 'IT・ソフトウェア', 'job': 'Webデザイナー', 'visa': engineer, 'score': 80},
            
            # 製造業
            {'industry': '製造業', 'job': '製造技術者', 'visa': engineer, 'score': 85},
            {'industry': '製造業', 'job': '製造ライン作業', 'visa': tokutei1, 'score': 90, 'notes': '特定技能「製造3分野」'},
            {'industry': '製造業', 'job': '品質管理', 'visa': engineer, 'score': 80},
            
            # 商社・貿易
            {'industry': '商社・貿易', 'job': '海外営業', 'visa': engineer, 'score': 90, 'notes': '国際業務として該当'},
            {'industry': '商社・貿易', 'job': '貿易事務', 'visa': engineer, 'score': 85},
            
            # 飲食業
            {'industry': '飲食業', 'job': '調理師', 'visa': tokutei1, 'score': 85, 'notes': '特定技能「外食業」'},
            {'industry': '飲食業', 'job': '外国料理専門調理師', 'visa': skilled, 'score': 90, 'notes': '10年以上の経験が必要'},
            
            # 建設業
            {'industry': '建設業', 'job': '建築技術者', 'visa': engineer, 'score': 85},
            {'industry': '建設業', 'job': '建設作業員', 'visa': tokutei1, 'score': 90, 'notes': '特定技能「建設」'},
            
            # 介護
            {'industry': '介護', 'job': '介護職員', 'visa': tokutei1, 'score': 95, 'notes': '特定技能「介護」'},
            
            # 宿泊業
            {'industry': '宿泊業', 'job': 'フロント業務', 'visa': tokutei1, 'score': 85, 'notes': '特定技能「宿泊」'},
            
            # 農業
            {'industry': '農業', 'job': '農業作業員', 'visa': tokutei1, 'score': 90, 'notes': '特定技能「農業」'},
            
            # 通訳・翻訳
            {'industry': 'サービス業', 'job': '通訳', 'visa': engineer, 'score': 95, 'notes': '国際業務として該当'},
            {'industry': 'サービス業', 'job': '翻訳', 'visa': engineer, 'score': 90, 'notes': '国際業務として該当'},
        ]
        
        for mapping in mappings:
            IndustryVisaMapping.objects.create(
                industry=mapping['industry'],
                job_category=mapping['job'],
                visa_category=mapping['visa'],
                match_score=mapping['score'],
                notes=mapping.get('notes', '')
            )
    
    def _create_documents(self):
        """必要書類の作成"""
        engineer = VisaCategory.objects.get(code='engineer_specialist')
        tokutei1 = VisaCategory.objects.get(code='specified_skilled_worker_1')
        
        # 技術・人文知識・国際業務の必要書類
        doc_list_engineer = [
            ('在留資格認定証明書交付申請書', '所定の様式に記入', True),
            ('写真（4cm×3cm）', '申請前3か月以内に撮影されたもの', True),
            ('返信用封筒', '404円分の切手を貼付', True),
            ('卒業証明書', '最終学歴の卒業証明書（原本）', True),
            ('成績証明書', '大学等の成績証明書', True),
            ('雇用契約書または採用内定通知書', '業務内容、報酬額が明記されたもの', True),
            ('会社の登記事項証明書', '発行後3か月以内のもの', True),
            ('会社案内パンフレット', '事業内容が分かるもの', False),
            ('直近年度の決算文書', '貸借対照表、損益計算書等', True),
        ]
        
        for idx, (name, desc, mandatory) in enumerate(doc_list_engineer, 1):
            DocumentTemplate.objects.create(
                visa_category=engineer,
                document_name=name,
                description=desc,
                is_mandatory=mandatory,
                display_order=idx
            )
        
        # 特定技能1号の必要書類
        doc_list_tokutei = [
            ('在留資格認定証明書交付申請書', '特定技能用の様式', True),
            ('写真（4cm×3cm）', '申請前3か月以内に撮影されたもの', True),
            ('特定技能評価試験の合格証明書', 'または技能実習2号修了証明書', True),
            ('日本語能力を証する書類', 'N4以上の合格証明書', True),
            ('特定技能雇用契約書', '所定の様式に記入', True),
            ('支援計画書', '登録支援機関が作成する場合もあり', True),
            ('会社の登記事項証明書', '発行後3か月以内のもの', True),
        ]
        
        for idx, (name, desc, mandatory) in enumerate(doc_list_tokutei, 1):
            DocumentTemplate.objects.create(
                visa_category=tokutei1,
                document_name=name,
                description=desc,
                is_mandatory=mandatory,
                display_order=idx
            )
