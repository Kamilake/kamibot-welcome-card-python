import os
import subprocess
import sys
from pathlib import Path
from typing import List

class ProtoCompiler:
    def __init__(self, proto_dir: str = "proto", output_dir: str = "."):
        self.proto_dir = Path(proto_dir)
        self.output_dir = Path(output_dir)
        
    def find_proto_files(self) -> List[Path]:
        """재귀적으로 모든 .proto 파일을 찾습니다."""
        if not self.proto_dir.exists():
            print(f"Warning: Proto directory '{self.proto_dir}' not found")
            return []
        return list(self.proto_dir.rglob("*.proto"))
    
    def compile_protos(self):
        """프로토 파일을 컴파일합니다."""
        proto_files = self.find_proto_files()
        
        if not proto_files:
            print(f"No proto files found in {self.proto_dir}")
            return
        
        print(f"Found {len(proto_files)} proto files")
        
        # protoc 명령 구성
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{self.proto_dir}",
            f"--python_out={self.output_dir}",
            f"--grpc_python_out={self.output_dir}"
        ]
        
        # 모든 프로토 파일 추가
        for proto_file in proto_files:
            cmd.append(str(proto_file))
            print(f"Compiling: {proto_file}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error compiling protos: {result.stderr}")
                sys.exit(1)
            else:
                print("Proto compilation successful")
        except Exception as e:
            print(f"Failed to compile protos: {e}")
            sys.exit(1)


if __name__ == "__main__":
    print("=" * 50)
    print("Proto 파일 컴파일 시작")
    print(f"Python 버전: {sys.version}")
    print("=" * 50)
    
    compiler = ProtoCompiler()
    compiler.compile_protos()
    print("\n✅ Proto compilation completed!")
