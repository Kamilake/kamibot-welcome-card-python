import unicodedata
from typing import Tuple, List, Optional
from PIL import ImageDraw, ImageFont
from font_manager import FontManager
from character_adjustment import CharacterAdjustmentRules, CharacterAdjustment
from theme import Theme
import grapheme

class TextSegment:
    """텍스트 세그먼트 - 동일한 폰트로 렌더링할 수 있는 텍스트 덩어리"""
    def __init__(self, text: str, font: ImageFont.FreeTypeFont, is_fallback: bool = False, adjustment: Optional[CharacterAdjustment] = None):
        self.text = text
        self.font = font
        self.is_fallback = is_fallback
        self.adjustment = adjustment or CharacterAdjustment()

class TextRenderer:
    def __init__(self, font_manager: FontManager):
        self.font_manager = font_manager
        self.adjustment_rules = CharacterAdjustmentRules()
    
    def normalize_text(self, text: str) -> str:
        """텍스트 정규화 및 제어 문자 처리"""
        if not text:
            return text
        
        text = text.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='replace')
        
        cleaned = []
        for char in text:
            category = unicodedata.category(char)
            
            if category == 'Cc':
                if char in '\t\n\r':
                    cleaned.append(' ')
            elif category in ['Cs', 'Co']:
                continue
            elif ord(char) in [0x200B, 0x200C, 0x200D, 0xFEFF]:
                # ZWJ(U+200D)는 이모지 시퀀스에 필요하므로 제거하지 않음
                if ord(char) != 0x200D:
                    continue
                else:
                    cleaned.append(char)
            else:
                cleaned.append(char)
        
        return ''.join(cleaned)
    
    def segment_text_by_font_support(self, text: str, font_size: int, preferred_font_name: str = None) -> List[TextSegment]:
        """텍스트를 폰트 지원 여부에 따라 세그먼트로 분할"""
        if not text:
            return []
        
        text = self.normalize_text(text)
        segments = []
        
        # 그래핌 클러스터로 분할
        grapheme_clusters = list(grapheme.graphemes(text))
        
        i = 0
        while i < len(grapheme_clusters):
            cluster = grapheme_clusters[i]
            
            # 첫 번째 문자의 조정 규칙 가져오기
            adjustment = self.adjustment_rules.get_adjustment(cluster[0]) if cluster else None
            adjusted_font_size = adjustment.apply_to_size(font_size) if adjustment else font_size
            
            # 현재 클러스터에 적합한 폰트 찾기
            if preferred_font_name and preferred_font_name in self.font_manager.available_fonts:
                # 선호 폰트가 모든 문자를 지원하는지 확인
                if all(self.font_manager.font_supports_character(preferred_font_name, char) for char in cluster):
                    try:
                        path_info = self.font_manager.available_fonts[preferred_font_name]
                        if isinstance(path_info, tuple):
                            font_path, font_index = path_info
                            current_font = ImageFont.truetype(font_path, adjusted_font_size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                        else:
                            current_font = ImageFont.truetype(path_info, adjusted_font_size, layout_engine=ImageFont.Layout.RAQM)
                        current_font_name = preferred_font_name
                        is_fallback = False
                    except:
                        current_font = None
                        current_font_name = None
                else:
                    current_font = None
                    current_font_name = None
            else:
                current_font = None
                current_font_name = None
            
            # 선호 폰트가 없거나 지원하지 않으면 폴백
            if not current_font:
                # 우선순위에 따라 폰트 찾기
                for font_name in self.font_manager.font_priority:
                    if font_name in self.font_manager.available_fonts:
                        if all(self.font_manager.font_supports_character(font_name, char) for char in cluster):
                            try:
                                path_info = self.font_manager.available_fonts[font_name]
                                if isinstance(path_info, tuple):
                                    font_path, font_index = path_info
                                    current_font = ImageFont.truetype(font_path, adjusted_font_size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                                else:
                                    current_font = ImageFont.truetype(path_info, adjusted_font_size, layout_engine=ImageFont.Layout.RAQM)
                                current_font_name = font_name
                                is_fallback = True
                                break
                            except:
                                continue
            
            if not current_font:
                # 폴백도 실패하면 기본 폰트 사용
                current_font = self.font_manager.get_font(adjusted_font_size)
                current_font_name = 'default'
                is_fallback = True
            
            # 같은 폰트와 같은 조정 규칙을 사용할 수 있는 연속된 클러스터들을 묶기
            segment_text = cluster
            j = i + 1
            
            while j < len(grapheme_clusters):
                next_cluster = grapheme_clusters[j]
                next_adjustment = self.adjustment_rules.get_adjustment(next_cluster[0]) if next_cluster else None
                
                # 다음 클러스터도 같은 폰트로 지원 가능하고 같은 조정 규칙을 가지는지 확인
                same_adjustment = (
                    (adjustment is None and next_adjustment is None) or
                    (adjustment and next_adjustment and 
                     adjustment.scale == next_adjustment.scale and
                     adjustment.offset_x == next_adjustment.offset_x and
                     adjustment.offset_y == next_adjustment.offset_y)
                )
                
                if current_font_name and same_adjustment and all(self.font_manager.font_supports_character(current_font_name, char) for char in next_cluster):
                    segment_text += next_cluster
                    j += 1
                else:
                    break
            
            segments.append(TextSegment(segment_text, current_font, is_fallback, adjustment))
            i = j
        
        return segments
    
    def render_mixed_text(self, draw: ImageDraw, text: str, x: int, y: int, 
                         default_color: Tuple[int, int, int], font_size: int, 
                         shadow: bool = False, shadow_offset: int = 2,
                         preferred_font_name: str = None) -> int:
        """혼합된 유니코드 텍스트 렌더링 - 세그먼트 기반"""
        if not text:
            return 0
        
        segments = self.segment_text_by_font_support(text, font_size, preferred_font_name)
        current_x = x
        
        # 베이스라인 계산을 위한 참조 폰트
        ref_font = self.font_manager.get_font(font_size)
        ref_bbox = ref_font.getbbox("Ay")
        ref_baseline = ref_bbox[3]
        
        for segment in segments:
            if segment.text:
                # 조정된 위치 계산
                adjusted_x, adjusted_y = segment.adjustment.apply_to_position(current_x, y, font_size)
                
                # 세그먼트의 베이스라인 조정
                seg_bbox = segment.font.getbbox("Ay")
                seg_baseline = seg_bbox[3]
                baseline_diff = ref_baseline - seg_baseline
                final_y = adjusted_y + baseline_diff
                
                # 세그먼트 전체를 한 번에 렌더링
                if shadow:
                    draw.text((adjusted_x + shadow_offset, final_y + shadow_offset), 
                             segment.text, fill=(0, 0, 0, 128), font=segment.font)
                
                # 폴백 폰트의 경우 약간 다른 색상 사용 (선택적)
                color = default_color if not segment.is_fallback else default_color
                draw.text((adjusted_x, final_y), segment.text, fill=color, font=segment.font)
                
                # 세그먼트 너비 계산
                bbox = segment.font.getbbox(segment.text)
                segment_width = bbox[2] - bbox[0]
                current_x += segment_width
        
        return current_x - x
    
    def get_mixed_text_width(self, text: str, font_size: int, preferred_font_name: str = None) -> int:
        """혼합된 유니코드 텍스트의 너비 계산 - 세그먼트 기반"""
        if not text:
            return 0
        
        segments = self.segment_text_by_font_support(text, font_size, preferred_font_name)
        total_width = 0
        
        for segment in segments:
            if segment.text:
                bbox = segment.font.getbbox(segment.text)
                total_width += bbox[2] - bbox[0]
        
        return total_width
    
    def get_text_bottom_offset(self, font: ImageFont.FreeTypeFont, text: str = "Ay") -> int:
        """텍스트의 하단 오프셋 계산"""
        bbox = font.getbbox(text)
        return bbox[3]
