from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import unicodedata

@dataclass
class CharacterAdjustment:
    """개별 문자 또는 문자 범위에 대한 조정 값"""
    scale: float = 1.0  # 크기 배율 (1.0 = 100%)
    offset_x: float = 0.0  # X축 오프셋 (픽셀)
    offset_y: float = 0.0  # Y축 오프셋 (픽셀)
    
    def apply_to_size(self, size: int) -> int:
        """폰트 크기에 스케일 적용"""
        return int(size * self.scale)
    
    def apply_to_position(self, x: int, y: int, font_size: int) -> Tuple[int, int]:
        """위치에 오프셋 적용 (폰트 크기에 비례)"""
        adjusted_x = int(x + self.offset_x * font_size / 100)
        adjusted_y = int(y + self.offset_y * font_size / 100)
        return adjusted_x, adjusted_y

class CharacterAdjustmentRules:
    """문자별 조정 규칙 관리"""
    
    def __init__(self):
        # 개별 문자 조정 규칙
        self.char_rules: Dict[str, CharacterAdjustment] = {}
        
        # 유니코드 범위별 조정 규칙
        self.range_rules: Dict[Tuple[int, int], CharacterAdjustment] = {}
        
        # 유니코드 카테고리별 조정 규칙
        self.category_rules: Dict[str, CharacterAdjustment] = {}
        
        # 기본 규칙 설정
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """기본 조정 규칙 설정"""
        
        # Mathematical Bold Italic 대문자 (U+1D468 ~ U+1D481)
        self.range_rules[(0x1D468, 0x1D481)] = CharacterAdjustment(
            scale=1.18,      # 10% 크기 증가
            offset_y=8.0   # 20% 아래로 이동
        )
        
        # Mathematical Bold Italic 소문자 (U+1D482 ~ U+1D49B)
        self.range_rules[(0x1D482, 0x1D49B)] = CharacterAdjustment(
            scale=1.14,     # 5% 크기 증가
            offset_y=8.0   # 15% 아래로 이동
        )
        
        # # Mathematical Script 대문자 (U+1D49C ~ U+1D4B5)
        # self.range_rules[(0x1D49C, 0x1D4B5)] = CharacterAdjustment(
        #     scale=1.08,     # 8% 크기 증가
        #     offset_y=18.0   # 18% 아래로 이동
        # )
        
        # # Mathematical Bold Script 대문자 (U+1D4D0 ~ U+1D4E9)
        # self.range_rules[(0x1D4D0, 0x1D4E9)] = CharacterAdjustment(
        #     scale=1.1,      # 10% 크기 증가
        #     offset_y=20.0   # 20% 아래로 이동
        # )
        
        # Mathematical Fraktur 대문자 (U+1D504 ~ U+1D51D)
        self.range_rules[(0x1D504, 0x1D51D)] = CharacterAdjustment(
            scale=1.10,     # 12% 크기 증가
            offset_y=0.0   # 22% 아래로 이동
        )

        # Mathematical Fraktur 소문자 (U+1D51E ~ U+1D537)
        self.range_rules[(0x1D51E, 0x1D537)] = CharacterAdjustment(
            scale=1.10,     # 8% 크기 증가
            offset_y=0.0   # 18% 아래로 이동
        )
        
        # # Mathematical Double-Struck 대문자 (U+1D538 ~ U+1D550)
        # self.range_rules[(0x1D538, 0x1D550)] = CharacterAdjustment(
        #     scale=1.05,     # 5% 크기 증가
        #     offset_y=10.0   # 10% 아래로 이동
        # )
        
        # # Mathematical Sans-Serif Bold Italic (U+1D63C ~ U+1D66F)
        # self.range_rules[(0x1D63C, 0x1D66F)] = CharacterAdjustment(
        #     scale=1.08,     # 8% 크기 증가
        #     offset_y=15.0   # 15% 아래로 이동
        # )
        
        # # Superscript 숫자 (U+2070 ~ U+2079)
        # self.range_rules[(0x2070, 0x2079)] = CharacterAdjustment(
        #     scale=0.8,      # 20% 크기 감소
        #     offset_y=-30.0  # 30% 위로 이동
        # )
        
        # # Subscript 숫자 (U+2080 ~ U+2089)
        # self.range_rules[(0x2080, 0x2089)] = CharacterAdjustment(
        #     scale=0.8,      # 20% 크기 감소
        #     offset_y=25.0   # 25% 아래로 이동
        # )
        
        # # 원문자 (U+2460 ~ U+24FF)
        # self.range_rules[(0x2460, 0x24FF)] = CharacterAdjustment(
        #     scale=1.1,      # 10% 크기 증가
        #     offset_y=5.0    # 5% 아래로 이동
        # )
        
        # # 전각 문자 (U+FF00 ~ U+FFEF)
        # self.range_rules[(0xFF00, 0xFFEF)] = CharacterAdjustment(
        #     scale=0.95,     # 5% 크기 감소
        #     offset_y=2.0    # 2% 아래로 이동
        # )
        
        # # 특정 이모지 조정 (예시)
        # # 얼굴 이모지
        # self.range_rules[(0x1F600, 0x1F64F)] = CharacterAdjustment(
        #     scale=1.15,     # 15% 크기 증가
        #     offset_y=8.0    # 8% 아래로 이동
        # )
        
        # # 손 이모지
        # self.range_rules[(0x1F90D, 0x1F9CF)] = CharacterAdjustment(
        #     scale=1.12,     # 12% 크기 증가
        #     offset_y=10.0   # 10% 아래로 이동
        # )
        
        # # 개별 문자 조정 예시
        # self.char_rules['™'] = CharacterAdjustment(
        #     scale=0.85,     # 15% 크기 감소
        #     offset_y=-25.0  # 25% 위로 이동
        # )
        
        # self.char_rules['®'] = CharacterAdjustment(
        #     scale=0.85,     # 15% 크기 감소
        #     offset_y=-25.0  # 25% 위로 이동
        # )
        
        # self.char_rules['©'] = CharacterAdjustment(
        #     scale=0.9,      # 10% 크기 감소
        #     offset_y=-5.0   # 5% 위로 이동
        # )
    
    def add_char_rule(self, char: str, adjustment: CharacterAdjustment):
        """개별 문자에 대한 조정 규칙 추가"""
        self.char_rules[char] = adjustment
    
    def add_range_rule(self, start: int, end: int, adjustment: CharacterAdjustment):
        """유니코드 범위에 대한 조정 규칙 추가"""
        self.range_rules[(start, end)] = adjustment
    
    def add_category_rule(self, category: str, adjustment: CharacterAdjustment):
        """유니코드 카테고리에 대한 조정 규칙 추가"""
        self.category_rules[category] = adjustment
    
    def get_adjustment(self, char: str) -> Optional[CharacterAdjustment]:
        """문자에 대한 조정 값 가져오기"""
        
        # 1. 개별 문자 규칙 확인
        if char in self.char_rules:
            return self.char_rules[char]
        
        # 2. 유니코드 범위 규칙 확인
        char_code = ord(char)
        for (start, end), adjustment in self.range_rules.items():
            if start <= char_code <= end:
                return adjustment
        
        # 3. 유니코드 카테고리 규칙 확인
        try:
            category = unicodedata.category(char)
            if category in self.category_rules:
                return self.category_rules[category]
        except:
            pass
        
        # 조정이 필요 없는 경우
        return None
    
    def merge_adjustments(self, adj1: CharacterAdjustment, adj2: CharacterAdjustment) -> CharacterAdjustment:
        """두 조정 값을 병합"""
        return CharacterAdjustment(
            scale=adj1.scale * adj2.scale,
            offset_x=adj1.offset_x + adj2.offset_x,
            offset_y=adj1.offset_y + adj2.offset_y
        )
