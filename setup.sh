#!/bin/bash

echo "========================================"
echo "外国人雇用在留資格診断システム"
echo "セットアップスクリプト (Mac/Linux用)"
echo "========================================"
echo ""

echo "[1/5] Djangoのインストール..."
pip3 install Django --break-system-packages || pip3 install Django
if [ $? -ne 0 ]; then
    echo "エラー: Djangoのインストールに失敗しました"
    exit 1
fi

echo ""
echo "[2/5] データベースのマイグレーション..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "エラー: マイグレーションに失敗しました"
    exit 1
fi

echo ""
echo "[3/5] 初期データの投入..."
python3 manage.py load_visa_data
if [ $? -ne 0 ]; then
    echo "エラー: 初期データの投入に失敗しました"
    exit 1
fi

echo ""
echo "[4/5] 管理者ユーザーの作成..."
python3 manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
print('管理者ユーザーを作成しました')
EOF

echo ""
echo "[5/5] セットアップ完了チェック..."
python3 manage.py check
if [ $? -ne 0 ]; then
    echo "エラー: システムチェックに失敗しました"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ セットアップ完了！"
echo "========================================"
echo ""
echo "次のコマンドでサーバーを起動してください:"
echo "    python3 manage.py runserver"
echo ""
echo "ブラウザで以下にアクセス:"
echo "    http://127.0.0.1:8000/"
echo ""
echo "管理画面:"
echo "    http://127.0.0.1:8000/admin/"
echo "    ユーザー名: admin"
echo "    パスワード: admin123"
echo ""
