@echo off
chcp 65001 >nul
echo ========================================
echo 外国人雇用在留資格診断システム
echo セットアップスクリプト (Windows用)
echo ========================================
echo.

echo [1/5] Djangoのインストール...
pip install Django
if %errorlevel% neq 0 (
    echo エラー: Djangoのインストールに失敗しました
    pause
    exit /b 1
)

echo.
echo [2/5] データベースのマイグレーション...
python manage.py migrate
if %errorlevel% neq 0 (
    echo エラー: マイグレーションに失敗しました
    pause
    exit /b 1
)

echo.
echo [3/5] 初期データの投入...
python manage.py load_visa_data
if %errorlevel% neq 0 (
    echo エラー: 初期データの投入に失敗しました
    pause
    exit /b 1
)

echo.
echo [4/5] 管理者ユーザーの作成...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123'); print('管理者ユーザーを作成しました')"
if %errorlevel% neq 0 (
    echo 警告: 管理者ユーザーの作成に失敗しました（既に存在している可能性があります）
)

echo.
echo [5/5] セットアップ完了チェック...
python manage.py check
if %errorlevel% neq 0 (
    echo エラー: システムチェックに失敗しました
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ セットアップ完了！
echo ========================================
echo.
echo 次のコマンドでサーバーを起動してください:
echo     python manage.py runserver
echo.
echo ブラウザで以下にアクセス:
echo     http://127.0.0.1:8000/
echo.
echo 管理画面:
echo     http://127.0.0.1:8000/admin/
echo     ユーザー名: admin
echo     パスワード: admin123
echo.
pause
