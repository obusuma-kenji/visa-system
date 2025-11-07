# 📦 インストール手順

## 🎯 3ステップで完了！

### Step 1: ファイルのダウンロード

**ZIPファイルをダウンロード:**
Claude の画面から `foreign_worker_visa_system.zip` をダウンロードしてください。

### Step 2: 解凍

ダウンロードしたZIPファイルを解凍します。

```
Windows: 右クリック → 「すべて展開」
Mac: ダブルクリック
```

### Step 3: セットアップ実行

解凍したフォルダ内で、OSに応じてセットアップスクリプトを実行します。

#### 🪟 Windowsの場合

1. `foreign_worker_visa_system` フォルダを開く
2. `setup.bat` をダブルクリック
3. 完了を待つ（1-2分）

#### 🍎 Mac/Linuxの場合

1. ターミナルを開く
2. 以下を実行:

```bash
cd /path/to/foreign_worker_visa_system
bash setup.sh
```

---

## ✅ 起動方法

セットアップが完了したら：

### Windowsの場合
```cmd
python manage.py runserver
```

### Mac/Linuxの場合
```bash
python3 manage.py runserver
```

### ブラウザでアクセス
```
http://127.0.0.1:8000/
```

---

## 🔑 ログイン情報

**管理画面:** http://127.0.0.1:8000/admin/

- **ユーザー名:** `admin`
- **パスワード:** `admin123`

---

## 📝 必要な環境

- **Python:** 3.8以上
- **OS:** Windows 10/11, macOS, Linux

### Pythonのインストール確認

```bash
# Windowsの場合
python --version

# Mac/Linuxの場合
python3 --version
```

3.8以上のバージョンが表示されればOKです。

### Pythonがインストールされていない場合

**Windows:**
1. https://www.python.org/downloads/ にアクセス
2. 「Download Python」をクリック
3. インストーラーを実行
4. ⚠️ **重要:** 「Add Python to PATH」にチェックを入れる

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 🔧 トラブルシューティング

### エラー: `python: command not found`

**解決方法:**
- Windowsの場合: `python` の代わりに `py` を使う
- Mac/Linuxの場合: `python` の代わりに `python3` を使う

### エラー: `pip: command not found`

**解決方法:**
```bash
# Windowsの場合
python -m pip install Django

# Mac/Linuxの場合
python3 -m pip install Django
```

### ポートが使用中

**解決方法:**
別のポートで起動する
```bash
python manage.py runserver 8001
```

### それでも動かない場合

`TROUBLESHOOTING.md` を確認してください。

---

## 📂 フォルダ構成

```
foreign_worker_visa_system/
├── setup.bat              ← Windowsセットアップ
├── setup.sh               ← Mac/Linuxセットアップ
├── manage.py              ← Django管理コマンド
├── README.md              ← 詳細ドキュメント
├── QUICKSTART.md          ← クイックスタート
├── TROUBLESHOOTING.md     ← トラブルシューティング
├── ROADMAP.md             ← 開発ロードマップ
├── visa_system/           ← プロジェクト設定
└── visa_diagnosis/        ← メインアプリ
    ├── models.py          ← データモデル
    ├── logic.py           ← 診断ロジック
    ├── views.py           ← ビュー
    └── templates/         ← HTMLテンプレート
```

---

## 🎉 インストール完了後

1. **トップページにアクセス**
   http://127.0.0.1:8000/

2. **診断を試す**
   - 「診断を開始する」をクリック
   - サンプルデータを入力
   - 結果を確認

3. **管理画面を確認**
   - http://127.0.0.1:8000/admin/ にアクセス
   - admin / admin123 でログイン
   - データの確認・編集

---

## 📞 サポート

問題が発生した場合:
1. `TROUBLESHOOTING.md` を確認
2. エラーメッセージをコピー
3. 以下の情報を集める:
   - OS
   - Pythonバージョン
   - エラーメッセージ全文

---

**Happy Coding! 🚀**
