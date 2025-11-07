# 🚀 Render.com デプロイガイド

このガイドに従って、在留資格診断システムをインターネット上に公開します。

---

## 📋 事前準備

### 必要なもの
- ✅ GitHubアカウント（無料）
- ✅ Render.comアカウント（無料）
- ✅ Claude APIキー

---

## Step 1: GitHubにアップロード

### 1-1. GitHubアカウント作成

1. https://github.com/ にアクセス
2. 「Sign up」をクリック
3. メールアドレスを入力して登録

### 1-2. 新しいリポジトリを作成

1. GitHubにログイン
2. 右上の「+」→「New repository」
3. Repository name: `visa-diagnosis-system`
4. Public（公開）を選択
5. 「Create repository」をクリック

### 1-3. コードをアップロード

#### 方法A: GitHub Desktop使用（簡単・推奨）

1. https://desktop.github.com/ から GitHub Desktop をダウンロード
2. インストールして起動
3. GitHubアカウントでログイン
4. 「File」→「Add local repository」
5. `C:\Users\owner\foreign_worker_visa_system` を選択
6. 「Publish repository」をクリック

#### 方法B: コマンドライン使用

```cmd
cd C:\Users\owner\foreign_worker_visa_system

# Gitの初期化
git init

# ファイルを追加
git add .

# コミット
git commit -m "Initial commit"

# GitHubに接続
git remote add origin https://github.com/あなたのユーザー名/visa-diagnosis-system.git

# アップロード
git branch -M main
git push -u origin main
```

---

## Step 2: Render.comでデプロイ

### 2-1. Render.comアカウント作成

1. https://render.com/ にアクセス
2. 「Get Started」をクリック
3. GitHubアカウントで登録（Sign up with GitHub）

### 2-2. 新しいWebサービスを作成

1. ダッシュボードで「New +」→「Web Service」をクリック
2. 「Connect a repository」で作成したGitHubリポジトリを選択
3. 以下の設定を入力：

```
Name: visa-diagnosis-system
Region: Singapore (最も近いリージョン)
Branch: main
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn visa_system.wsgi:application
Instance Type: Free
```

### 2-3. 環境変数の設定

「Environment」セクションで以下を追加：

```
ANTHROPIC_API_KEY = sk-ant-api03-あなたのAPIキー
PYTHON_VERSION = 3.12.0
DEBUG = False
ALLOWED_HOSTS = .onrender.com
```

### 2-4. デプロイ実行

1. 「Create Web Service」をクリック
2. 自動的にビルドとデプロイが開始されます
3. 5-10分待ちます

---

## Step 3: 動作確認

### 3-1. URLにアクセス

デプロイ完了後、以下のようなURLが発行されます：

```
https://visa-diagnosis-system.onrender.com
```

### 3-2. 管理者アカウントの作成

Render.comのダッシュボードで：

1. 「Shell」タブをクリック
2. 以下のコマンドを実行：

```bash
python manage.py createsuperuser
```

3. ユーザー名、メール、パスワードを入力

### 3-3. 診断テスト

公開されたURLで診断を実行してテスト：

```
https://visa-diagnosis-system.onrender.com/diagnosis-form/
```

---

## 📊 料金について

### 無料プラン
- ✅ 完全無料
- ✅ 十分な性能
- ⚠️ 15分間アクセスがないとスリープ（初回アクセス時に30秒ほど待つ）

### 有料プラン（$7/月）
- ✅ スリープなし
- ✅ より高速
- ✅ カスタムドメイン可能

最初は無料プランで十分です！

---

## 🔒 セキュリティ注意事項

### ⚠️ 重要：APIキーの保護

- ✅ GitHubに`.env`ファイルはアップロードしない
- ✅ APIキーは環境変数で設定
- ✅ settings.pyにAPIキーを直接書かない

### .gitignore ファイルの確認

以下のファイルがGitにアップロードされないようにする：

```
*.pyc
__pycache__/
db.sqlite3
.env
staticfiles/
```

---

## 🎯 デプロイ後のチェックリスト

- [ ] トップページが表示される
- [ ] 診断フォームが動作する
- [ ] AI分析が表示される
- [ ] 在留資格一覧が表示される
- [ ] 管理画面にログインできる

---

## 🆘 トラブルシューティング

### ビルドエラーが出る場合

1. Render.comのログを確認
2. Python バージョンを確認
3. requirements.txt を確認

### AI機能が動作しない場合

1. 環境変数 `ANTHROPIC_API_KEY` が設定されているか確認
2. APIキーが正しいか確認
3. API残高があるか確認

### データベースがリセットされる場合

Render.comの無料プランでは、デプロイごとにデータベースがリセットされます。
有料プランで外部データベース（PostgreSQL）を使用すると解決します。

---

## 📱 カスタムドメインの設定（オプション）

独自ドメイン（例：visa.example.jp）を使いたい場合：

1. Render.comの有料プラン（$7/月）にアップグレード
2. ドメインを取得（お名前.com等）
3. Render.comでカスタムドメインを設定

---

## 🎊 完了！

これでシステムがインターネット上に公開されました！

URLを共有するだけで、誰でもどこからでもアクセスできます：

```
https://visa-diagnosis-system.onrender.com
```

---

## 📞 サポート

問題が発生した場合は、以下を確認：
- Render.comのログ
- GitHubのコミット履歴
- 環境変数の設定

それでも解決しない場合は、エラーメッセージをコピーして質問してください！
