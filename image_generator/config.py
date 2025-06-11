import os
from dataclasses import dataclass

@dataclass
class Config:
    # gRPC 서버 설정
    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50051
    
    # 환경 설정
    is_docker: bool = os.environ.get('IS_DOCKER_ENV', 'false').lower() == 'true'
    
    # 프로토 설정
    proto_dir: str = "proto"  # 실제 디렉토리명에 맞춤
    proto_output_dir: str = "."  # 현재 디렉토리에 생성
    
    @property
    def grpc_server_address(self) -> str:
        return f"{self.grpc_host}:{self.grpc_port}"

# 싱글톤 인스턴스
config = Config()
