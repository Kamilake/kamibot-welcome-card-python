############################
# 1) 빌드 스테이지
############################
FROM python:3.11-slim AS builder

# 빌드에 필요한 도구들 설치
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential \
  gcc \
  g++ \
  pkg-config \
  # Pillow RAQM 빌드에 필요한 개발 라이브러리들
  libfreetype6-dev \
  libharfbuzz-dev \
  libfribidi-dev \
  libpng-dev \
  libjpeg-dev \
  libtiff-dev \
  libwebp-dev \
  libraqm-dev \
  libopenjp2-7-dev \
  zlib1g-dev \
  && rm -rf /var/lib/apt/lists/*

# 가상 환경 생성
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# requirements.txt 복사 및 패키지 빌드
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r /tmp/requirements.txt

############################
# 2) 런타임 스테이지
############################
FROM python:3.11-slim AS runtime

# 저장소 추가
RUN set -eux; \
  # 기존 debian.sources 파일의 Components를 수정
  sed -i 's/Components: main$/Components: main contrib non-free non-free-firmware/' /etc/apt/sources.list.d/debian.sources

# 런타임에 필요한 라이브러리들만 설치 (개발 패키지는 제외)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  # 기본 시스템 패키지
  fontconfig \
  curl \
  ca-certificates \
  git \
  # Pillow RAQM 런타임 라이브러리들
  libfreetype6 \
  libharfbuzz0b \
  libfribidi0 \
  libpng16-16 \
  libjpeg62-turbo \
  libtiff6 \
  libwebp7 \
  libraqm0 \
  libopenjp2-7 \
  zlib1g \
  # 한국어 폰트
  fonts-nanum \
  fonts-nanum-coding \
  fonts-nanum-extra \
  # Noto 폰트 (CJK 포함)
  fonts-noto \
  fonts-noto-cjk \
  fonts-noto-cjk-extra \
  fonts-noto-color-emoji \
  fonts-noto-mono \
  fonts-noto-ui-core \
  # 일본어 폰트
  fonts-takao \
  fonts-takao-gothic \
  fonts-takao-mincho \
  # 중국어 폰트
  fonts-wqy-microhei \
  fonts-wqy-zenhei \
  fonts-arphic-ukai \
  fonts-arphic-uming \
  # 서양 폰트 (기본)
  fonts-dejavu \
  fonts-dejavu-core \
  fonts-dejavu-extra \
  fonts-liberation \
  fonts-liberation2 \
  fonts-roboto \
  fonts-roboto-slab \
  fonts-droid-fallback \
  fonts-opensymbol \
  # 웹/시스템 폰트
  fonts-crosextra-carlito \
  fonts-crosextra-caladea \
  # ttf-mscorefonts-installer \
  #     root@399476863ffa:/usr/share/fonts/truetype/msttcorefonts# ls
  # Andale_Mono.ttf         Courier_New.ttf              Impact.ttf                       Trebuchet_MS_Italic.ttf  arialbd.ttf  courbi.ttf    timesbd.ttf   verdanab.ttf
  # Arial.ttf               Courier_New_Bold.ttf         Times_New_Roman.ttf              Verdana.ttf              arialbi.ttf  couri.ttf     timesbi.ttf   verdanai.ttf
  # Arial_Black.ttf         Courier_New_Bold_Italic.ttf  Times_New_Roman_Bold.ttf         Verdana_Bold.ttf         ariali.ttf   georgia.ttf   timesi.ttf    verdanaz.ttf
  # Arial_Bold.ttf          Courier_New_Italic.ttf       Times_New_Roman_Bold_Italic.ttf  Verdana_Bold_Italic.ttf  ariblk.ttf   georgiab.ttf  trebuc.ttf    webdings.ttf
  # Arial_Bold_Italic.ttf   Georgia.ttf                  Times_New_Roman_Italic.ttf       Verdana_Italic.ttf       comic.ttf    georgiai.ttf  trebucbd.ttf
  # Arial_Italic.ttf        Georgia_Bold.ttf             Trebuchet_MS.ttf                 Webdings.ttf             comicbd.ttf  georgiaz.ttf  trebucbi.ttf
  # Comic_Sans_MS.ttf       Georgia_Bold_Italic.ttf      Trebuchet_MS_Bold.ttf            andalemo.ttf             cour.ttf     impact.ttf    trebucit.ttf
  # Comic_Sans_MS_Bold.ttf  Georgia_Italic.ttf           Trebuchet_MS_Bold_Italic.ttf     arial.ttf                courbd.ttf   times.ttf     verdana.ttf
  # 개발자용 폰트
  fonts-firacode \
  fonts-hack \
  fonts-inconsolata \
  # 기타 폰트
  fonts-lato \
  fonts-open-sans \
  fonts-freefont-ttf \
  fonts-font-awesome \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Microsoft Segoe UI 폰트 설치
RUN set -eux; \
  TMPDIR="$(mktemp -d)" && \
  git clone --depth 1 https://github.com/mrbvrz/segoe-ui-linux.git "$TMPDIR"/segoe && \
  mkdir -p /usr/share/fonts/truetype/segoe-ui && \
  find "$TMPDIR"/segoe/font -name '*.ttf' -exec install -m644 {} /usr/share/fonts/truetype/segoe-ui/ \; && \
  rm -rf "$TMPDIR"

# 폰트 캐시 새로고침
RUN fc-cache -fv

# 빌드 스테이지에서 가상 환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . .

ENV IS_DOCKER_ENV=true

EXPOSE 50051

STOPSIGNAL SIGTERM

# exec 형태로 실행하여 PID 1에서 신호를 받을 수 있도록 함
CMD ["python", "-u", "image_generator/server.py"]