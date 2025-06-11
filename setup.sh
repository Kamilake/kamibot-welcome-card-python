#!/bin/bash

echo "Python Welcome Service 로컬 개발 환경 설정"
echo "========================================"

# 가상환경 생성
if [ ! -d "venv" ]; then
    echo "1. Python 가상환경 생성 중..."
    python3 -m venv venv
else
    echo "1. 가상환경이 이미 존재합니다."
fi

# 가상환경 활성화
echo "2. 가상환경 활성화..."
source venv/bin/activate

# 의존성 설치
echo "3. 의존성 패키지 설치 중..."
pip install -r requirements.txt

# Proto 파일 컴파일 (새로운 스크립트 사용)
echo "4. Proto 파일 컴파일 중..."
python compile_protos.py

echo ""
echo "✅ 설정 완료!"
echo ""
echo "다음 명령으로 가상환경을 활성화하세요:"
echo "  source venv/bin/activate"
echo ""
echo "Proto 파일을 다시 컴파일하려면:"
echo "  ./generate_proto.sh"
echo ""
echo "서버 실행:"
echo "  python image_generator/server.py"
