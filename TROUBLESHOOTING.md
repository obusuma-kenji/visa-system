# 🔧 トラブルシューティングガイド

## よくあるエラーと解決方法

### 1. `ModuleNotFoundError: No module named 'django'`

**原因**: Djangoがインストールされていない

**解決方法**:
```bash
pip install Django --break-system-packages
```

---

### 2. `Port 8000 is already in use`

**原因**: ポート8000が既に使用されている

**解決方法**:
```bash
# 別のポートで起動
python manage.py runserver 8001

# または、既存のプロセスを停止
# Windowsの場合
netstat -ano | findstr :8000
taskkill /PID <プロセスID> /F

# Mac/Linuxの場合
lsof -ti:8000 | xargs kill -9
```

---

### 3. `OperationalError: no such table`

**原因**: データベースが初期化されていない

**解決方法**:
```bash
# データベースを作り直す
python manage.py migrate
python manage.py load_visa_data
```

---

### 4. `ImportError: cannot import name 'VisaDiagnosisEngine'`

**原因**: ファイルパスの問題

**解決方法**:
```bash
# 正しいディレクトリにいるか確認
pwd
# foreign_worker_visa_system が含まれていることを確認

# 正しいディレクトリに移動
cd /path/to/foreign_worker_visa_system
```

---

### 5. ページが表示されない（404 Not Found）

**原因**: URLの間違い

**解決方法**:
```
正しいURL:
✓ http://127.0.0.1:8000/
✓ http://127.0.0.1:8000/diagnosis-form/
✓ http://127.0.0.1:8000/admin/

間違ったURL:
✗ http://localhost:8000/visa_diagnosis/
✗ http://127.0.0.1:8000/home/
```

---

### 6. 管理画面にログインできない

**原因**: パスワードが設定されていない、または間違い

**解決方法**:
```bash
# パスワードをリセット
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='admin')
u.set_password('admin123')
u.save()
print('パスワードをリセットしました')
"
```

---

### 7. `UnicodeDecodeError`

**原因**: ファイルのエンコーディング問題

**解決方法**:
Windowsの場合、環境変数を設定:
```bash
set PYTHONIOENCODING=utf-8
python manage.py runserver
```

---

### 8. `Permission denied`

**原因**: ファイルの権限問題

**解決方法**:
```bash
# Mac/Linux
chmod +x manage.py

# または管理者権限で実行
sudo python manage.py runserver
```

---

### 9. 診断結果が表示されない

**原因**: 初期データが投入されていない

**解決方法**:
```bash
# データを確認
python manage.py shell -c "
from visa_diagnosis.models import VisaCategory
print(f'在留資格数: {VisaCategory.objects.count()}')
"

# 0件の場合は初期データを投入
python manage.py load_visa_data
```

---

### 10. `CSRF verification failed`

**原因**: CSRF トークンの問題

**解決方法**:
ブラウザのキャッシュをクリアするか、シークレットモードで試す

---

## 完全リセット手順

すべてが動かない場合、データベースをリセット:

```bash
# 1. データベース削除
rm db.sqlite3

# 2. マイグレーションファイル削除（初期以外）
rm visa_diagnosis/migrations/0*.py
# ただし __init__.py は削除しない

# 3. データベース再作成
python manage.py makemigrations
python manage.py migrate

# 4. 初期データ投入
python manage.py load_visa_data

# 5. 管理者作成
python manage.py createsuperuser
# または
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"
```

---

## デバッグモード

詳細なエラー情報を見るには:

```bash
# settings.py で確認
DEBUG = True  # これがTrueになっているか確認
```

エラーの詳細ログを見る:
```bash
python manage.py runserver --verbosity 3
```

---

## システム要件チェック

```bash
# Pythonバージョン確認（3.8以上必要）
python --version

# Djangoバージョン確認
python -m django --version

# インストール済みパッケージ確認
pip list | grep Django
```

---

## それでも解決しない場合

以下の情報を集めてください:

1. **エラーメッセージ全文**（スクリーンショット）
2. **実行したコマンド**
3. **OS とPythonバージョン**
4. **以下のコマンドの結果**:

```bash
python --version
python -m django --version
pwd
ls -la
python manage.py check
```

これらの情報があれば、より具体的な解決策を提案できます。
