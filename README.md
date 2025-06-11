# 🎨 Python Welcome Image Service

> 새로운 디스코드 멤버를 반갑게 맞이하는 멋진 환영 이미지 카드를 만들어봐요! 🥳

![image](https://github.com/user-attachments/assets/88f780d0-998e-4890-b701-71f395b31cb7)


## 📜 프로젝트 소개
Python으로 구현된 gRPC 기반 서비스예요.  
사용자가 디스코드 서버에 들어오면 프로필 사진, 텍스트, 테마를 조합해 환영 이미지를 생성해주고, 백엔드에서 처리해요.

## 🚀 주요 기능
- 7가지 테마 지원: Default, Minimal, Gradient, Dark, Colorful, Gaming, Cute  
- 유니코드·이모지·특수문자 완벽 렌더링  
- 텍스트 커스터마이징(취소선·색상·접미사)  
- 배경 이미지 URL 지원 및 그라데이션 오버레이  
- gRPC로 빠르고 안정적인 통신

## 🛠️ 기술 스택
- Python 3.11  
- gRPC (`grpcio`, `grpcio-tools`)  
- Pillow (RAQM)  
- FontTools  
- Docker & Docker Compose  

---

## 🏁 빠른 시작

### 1) 로컬 개발
```bash
# 클론 & 이동
git clone https://github.com/your-username/python-welcome-service.git
cd python-welcome-service

# 실행 권한 부여
chmod +x setup.sh generate_proto.sh

# 개발 환경 설정 (venv 생성, 패키지 설치, proto 컴파일)
./setup.sh

# 가상환경 활성화
source venv/bin/activate

# 서버 실행
python image_generator/server.py
```

### 2) Proto 재컴파일
```bash
./generate_proto.sh
```

### 3) Docker로 실행
```bash
docker compose -f ../docker-compose.yaml up -d python-welcome-service
docker compose -f ../docker-compose.yaml logs -f python-welcome-service
docker compose -f ../docker-compose.yaml down python-welcome-service
```

---

## 💡 프로젝트 구조
```
python-welcome-service/
├── image_generator/       # 핵심 로직 (서버·생성기·폰트·렌더러·테마 등)
├── proto/                 # .proto 정의 파일
├── compile_protos.py      # proto 자동 컴파일 스크립트
├── setup.sh               # 로컬 개발 환경 설정 스크립트
├── generate_proto.sh      # proto 재컴파일 스크립트
├── requirements.txt       # Python 의존성 목록
├── Dockerfile             # 컨테이너 이미지 빌드 설정
└── README.md              # 프로젝트 안내
```

---

## 🤝 기여하기
1. Fork & Clone  
2. `feature/YourFeature` 브랜치 생성  
3. 코드 작성 & 커밋 (`git commit -m "Add awesome feature"`)  
4. Push & Pull Request  
- PEP8 스타일 준수  
- 주요 기능엔 테스트 추가  
- 문서 업데이트 잊지 않기

---

## 📄 라이센스
이 프로젝트는 MIT 라이센스를 따릅니다.  
자유롭게 사용·수정·배포하세요! ❤️

---

> 궁금한 점이나 버그는 언제든 이슈로 알려주세요!  
> 여러분의 디스코드 서버에 따뜻한 환영을 선사하길 바라요! 🌈  
