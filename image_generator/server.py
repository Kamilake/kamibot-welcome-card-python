import grpc
from concurrent import futures
import time
import logging
import signal
import sys
import threading
from welcome_image_generator import WelcomeImageGenerator
from config import config

# 프로토 파일 컴파일 확인
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proto_compiler import ProtoCompiler
compiler = ProtoCompiler()
compiler.compile_protos()

# 생성된 proto 파일들을 import
try:
    import welcome_image_service_pb2
    import welcome_image_service_pb2_grpc
except ImportError:
    print("Proto 파일이 컴파일되지 않았습니다.")
    raise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WelcomeImageServiceServicer(welcome_image_service_pb2_grpc.WelcomeImageServiceServicer):
    def __init__(self):
        self.image_generator = WelcomeImageGenerator()
        logger.info("WelcomeImageService 초기화 완료")
    
    def GenerateWelcomeImage(self, request, context):
        try:
            logger.info(f"이미지 생성 요청 받음: {request.title_text} (테마: {request.theme})")
            
            # 테마 매핑
            theme_map = {
                welcome_image_service_pb2.THEME_DEFAULT: 'default',
                welcome_image_service_pb2.THEME_MINIMAL: 'minimal',
                welcome_image_service_pb2.THEME_GRADIENT: 'gradient',
                welcome_image_service_pb2.THEME_DARK: 'dark',
                welcome_image_service_pb2.THEME_COLORFUL: 'colorful',
                welcome_image_service_pb2.THEME_GAMING: 'gaming',
                welcome_image_service_pb2.THEME_CUTE: 'cute',
            }
            
            theme_name = theme_map.get(request.theme, 'default')
            
            # 이미지 생성
            image_data = self.image_generator.generate_welcome_image(
                title_text=request.title_text,
                subtitle_text=request.subtitle_text,
                avatar_url=request.avatar_url,
                bg_url=request.bg_url if request.bg_url else None,
                header_text=request.header_text,
                footer_text=request.footer_text,
                strikeout=request.strikeout,
                username_color_hex=request.username_color_hex,
                suffix_text=request.suffix_text,
                theme_name=theme_name
            )
            
            logger.info(f"이미지 생성 성공: {len(image_data)} bytes")
            
            return welcome_image_service_pb2.GenerateWelcomeImageResponse(
                image_data=image_data,
                success=True,
                error_message=""
            )
            
        except Exception as e:
            logger.error(f"이미지 생성 실패: {str(e)}", exc_info=True)
            return welcome_image_service_pb2.GenerateWelcomeImageResponse(
                image_data=b"",
                success=False,
                error_message=str(e)
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    welcome_image_service_pb2_grpc.add_WelcomeImageServiceServicer_to_server(
        WelcomeImageServiceServicer(), server
    )
    
    # 설정에서 포트 가져오기
    server.add_insecure_port(f'[::]:{config.grpc_port}')
    server.start()
    logger.info(f"gRPC 서버가 포트 {config.grpc_port}에서 시작되었습니다.")
    
    # Graceful shutdown을 위한 이벤트
    shutdown_event = threading.Event()
    
    def signal_handler(signum, frame):
        logger.info(f"종료 신호 {signum} 수신, 서버를 종료합니다...")
        shutdown_event.set()
    
    # 신호 핸들러 등록
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # 종료 신호까지 대기
        shutdown_event.wait()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt 수신")
    finally:
        logger.info("서버 종료 중...")
        server.stop(grace=5)  # 5초 grace period
        logger.info("서버가 종료되었습니다.")

if __name__ == '__main__':
    serve()
