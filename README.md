# 外国人雇用 在留資格診断システム

## 概要

このシステムは、外国人を雇用する企業が最適な在留資格を診断できるWebアプリケーションです。
社会保険労務士の専門知識に基づいた診断ロジックで、高精度な判定が可能です。

## 主な機能

### ✅ 実装済み機能

1. **在留資格診断エンジン**
   - 学歴、実務経験、職務内容から最適な在留資格を自動判定
   - 複数候補をスコアリング（0-100点）
   - 要件の充足状況を詳細表示

2. **主要在留資格対応**
   - 技術・人文知識・国際業務
   - 特定技能1号・2号
   - 高度専門職
   - 技能
   - 企業内転勤

3. **業種別マッピング**
   - IT、製造、商社、飲食、建設、介護、宿泊、農業など
   - 18種類の業種・職種パターン登録済み

4. **必要書類リスト**
   - 在留資格ごとの必要書類を自動表示
   - 必須・推奨の区分表示

5. **管理画面**
   - 在留資格、要件、業種マッピングの管理
   - 診断履歴の確認

## 技術スタック

- **Backend**: Python 3.x, Django 5.2
- **Database**: SQLite3（開発用）
- **Frontend**: HTML, CSS（ピュアJavaScript）

## セットアップ手順

### 1. 前提条件

- Python 3.8以上
- pip

### 2. インストール

```bash
# リポジトリのクローン（またはZIPダウンロード）
cd foreign_worker_visa_system

# Djangoのインストール
pip install Django --break-system-packages

# データベース初期化
python manage.py migrate

# 初期データ投入
python manage.py load_visa_data

# 管理者ユーザー作成（既に作成済みの場合はスキップ）
# ユーザー名: admin
# パスワード: admin123
```

### 3. 実行

```bash
# 開発サーバー起動
python manage.py runserver

# ブラウザでアクセス
# http://127.0.0.1:8000/
```

## 使い方

### 一般ユーザー向け

1. トップページから「診断を開始する」をクリック
2. フォームに外国人材の情報を入力
3. 「診断する」ボタンをクリック
4. 診断結果を確認

### 管理者向け

1. http://127.0.0.1:8000/admin/ にアクセス
2. ユーザー名: `admin` / パスワード: `admin123` でログイン
3. 在留資格、要件、マッピングデータを管理

## プロジェクト構造

```
foreign_worker_visa_system/
├── manage.py
├── visa_system/              # プロジェクト設定
│   ├── settings.py
│   └── urls.py
└── visa_diagnosis/           # メインアプリ
    ├── models.py             # データモデル
    ├── logic.py              # 診断ロジック
    ├── views.py              # ビュー
    ├── admin.py              # 管理画面
    ├── templates/            # HTMLテンプレート
    └── management/
        └── commands/
            └── load_visa_data.py  # 初期データ投入
```

## データモデル

### VisaCategory（在留資格）
- 在留資格の基本情報（名称、説明、優先度）

### VisaRequirement（要件）
- 各在留資格の要件（学歴、経験、報酬など）

### IndustryVisaMapping（業種マッピング）
- 業種・職種と在留資格の関連付け

### DiagnosisSession（診断セッション）
- 診断履歴の保存

### DocumentTemplate（必要書類）
- 在留資格ごとの必要書類リスト

## API仕様（将来実装）

### POST /diagnose/

診断APIエンドポイント（現在はフォーム経由のみ）

**リクエストボディ:**
```json
{
  "nationality": "ベトナム",
  "education": {
    "degree": "学士",
    "major": "情報工学",
    "university": "○○大学"
  },
  "experience": [
    {
      "years": 3,
      "field": "ソフトウェア開発"
    }
  ],
  "job_details": {
    "industry": "IT・ソフトウェア",
    "position": "システムエンジニア",
    "duties": "Webシステムの開発"
  },
  "salary": 280000,
  "qualifications": ["日本語能力試験N2"]
}
```

**レスポンス:**
```json
{
  "diagnosis_id": "DIAG-20250916-1234",
  "top_recommendations": [
    {
      "visa_category": {
        "name_ja": "技術・人文知識・国際業務",
        "code": "engineer_specialist"
      },
      "match_score": 85,
      "recommendation_level": "○ 推奨",
      "requirements_status": [...],
      "required_documents": [...]
    }
  ]
}
```

## カスタマイズ方法

### 新しい在留資格の追加

1. 管理画面で「在留資格」を追加
2. 「在留資格要件」を追加
3. 「業種職種マッピング」を追加（必要に応じて）
4. 「必要書類テンプレート」を追加

### 診断ロジックの調整

`visa_diagnosis/logic.py` の `VisaDiagnosisEngine` クラスを編集

## 今後の拡張案

### 短期（1-2ヶ月）
- [ ] AI統合（Claude API / OpenAI API）
- [ ] 専攻と職種の関連性AI判定
- [ ] 業務内容の単純労働判定

### 中期（3-6ヶ月）
- [ ] チャットボット形式のUI
- [ ] 多言語対応（英語、ベトナム語、中国語）
- [ ] PDF出力機能（診断結果レポート）
- [ ] ポイント計算機能（高度専門職）

### 長期（6ヶ月以上）
- [ ] 申請書類の自動作成
- [ ] 入管申請進捗管理
- [ ] 社労士向けSaaSモデル化
- [ ] スマートフォンアプリ

## ライセンス

MIT License

## 開発者情報

- 社会保険労務士監修
- 2025年9月開発

## サポート

問題が発生した場合は、以下を確認してください：

1. Pythonのバージョンが3.8以上か
2. Djangoが正しくインストールされているか
3. データベースが正しく初期化されているか
4. 初期データが投入されているか

## セキュリティ注意事項

**本番環境にデプロイする前に必ず以下を実施してください:**

1. `SECRET_KEY` の変更（settings.py）
2. `DEBUG = False` に設定
3. `ALLOWED_HOSTS` の設定
4. PostgreSQL等の本番用DBへの変更
5. 管理者パスワードの変更
6. HTTPS/SSLの有効化

---

**重要**: このシステムは診断支援ツールであり、最終的な在留資格の判定は専門家（社会保険労務士、行政書士）にご相談ください。
