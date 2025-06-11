#!/usr/bin/env bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

echo "Proto 파일 컴파일 시작..."

# 새로운 compile_protos.py 사용
python -m proto_compiler

# 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ 컴파일 완료!"
else
    echo "❌ 컴파일 실패!"
    exit 1
fi
