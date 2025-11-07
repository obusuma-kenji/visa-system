# 🚀 Render.com 5分クイックスタート

最短ルートでインターネット公開する方法です。

---

## ✅ 必要なもの（3つだけ）

1. GitHubアカウント（無料）
2. Render.comアカウント（無料）
3. Claude APIキー

---

## 📝 5ステップで公開

### Step 1: GitHubにアップロード（2分）

#### 簡単な方法（推奨）

1. https://github.com/new にアクセス
2. Repository name: `visa-system`
3. Public を選択
4. 「Create repository」をクリック
5. 「uploading an existing file」をクリック
6. `foreign_worker_visa_system` フォルダの中身を**すべて**ドラッグ＆ドロップ
7. 「Commit changes」をクリック

---

### Step 2: Render.comに登録（1分）

1. https://render.com/ にアクセス
2. 「Get Started」→「Sign up with GitHub」
3. GitHubでログイン → 認証

---

### Step 3: Webサービス作成（2分）

1. 「New +」→「Web Service」
2. GitHubリポジトリ `visa-system` を選択
3. **以下をそのままコピペ：**

```
Name: visa-system
Runtime: Python 3
Build Command: chmod +x build.sh && ./build.sh
Start Command: gunicorn visa_system.wsgi:application
```

4. 「Free」プランを選択
5. **「Create Web Service」はまだクリックしない！**

---

### Step 4: 環境変数設定（1分）

「Environment」セクションで「Add Environment Variable」を3回クリックして追加：

```
Key: ANTHROPIC_API_KEY
Value: sk-ant-api03-あなたのAPIキー

Key: PYTHON_VERSION
Value: 3.12.0

Key: ALLOWED_HOSTS
Value: .onrender.com
```

---

### Step 5: デプロイ実行（5-10分）

1. **「Create Web Service」をクリック**
2. ビルドログを見ながら待つ（5-10分）
3. 「Live」になったら完成！🎉

---

## 🌐 公開URL

デプロイ完了後、このようなURLでアクセスできます：

```
https://visa-system-xxxx.onrender.com
```

---

## ⚙️ 管理者アカウント作成

1. Render.comダッシュボードの「Shell」タブをクリック
2. 以下を入力：

```bash
python manage.py createsuperuser
```

3. ユーザー名・パスワードを設定

---

## 🎯 動作確認

以下のURLで確認：

```
トップページ:     https://あなたのURL.onrender.com/
診断フォーム:     https://あなたのURL.onrender.com/diagnosis-form/
管理画面:        https://あなたのURL.onrender.com/admin/
```

---

## 💡 重要な注意点

### 無料プランの特徴
- ✅ 完全無料
- ⚠️ 15分間アクセスがないとスリープ
  - 初回アクセス時に30秒ほど待つ
  - その後は高速

### スリープを避けたい場合
- 有料プラン（$7/月）にアップグレード
- 常時稼働、高速、カスタムドメイン可能

---

## 🆘 エラーが出たら

### ビルドエラー
→ Render.comのログを確認
→ `build.sh` の実行権限を確認

### AI機能が動作しない
→ 環境変数 `ANTHROPIC_API_KEY` を確認
→ APIキーが正しいか確認

### データベースがリセットされる
→ 正常です（無料プランの仕様）
→ 有料プランで外部データベースを使用すると解決

---

## 🎊 完了！

URLを共有するだけで、誰でもアクセスできます！

```
https://visa-system-xxxx.onrender.com
```

---

詳細は `DEPLOY_RENDER.md` を参照してください。
