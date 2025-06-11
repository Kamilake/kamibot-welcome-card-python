from PIL import Image, ImageDraw
from io import BytesIO
from typing import Tuple, Optional

from theme import ThemeManager
from font_manager import FontManager
from text_renderer import TextRenderer
from image_processor import ImageProcessor
from character_adjustment import CharacterAdjustment

class WelcomeImageGenerator:
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.font_manager = FontManager()
        self.text_renderer = TextRenderer(self.font_manager)
        self.image_processor = ImageProcessor()
        
        # 추가 문자 조정 규칙 설정 (필요시)
        self._setup_custom_adjustments()
    
    def _setup_custom_adjustments(self):
        """커스텀 문자 조정 규칙 설정"""
        # 예시: 특정 문자에 대한 추가 조정
        # self.text_renderer.adjustment_rules.add_char_rule(
        #     '𝑬', 
        #     CharacterAdjustment(scale=1.1, offset_y=20.0)
        # )
        pass

    def generate_welcome_image(
        self,
        title_text: str,
        subtitle_text: str,
        avatar_url: str,
        bg_url: Optional[str],
        header_text: str,
        footer_text: str,
        strikeout: bool,
        username_color_hex: str,
        suffix_text: str,
        theme_name: str = 'default'
    ) -> bytes:
        try:
            # 문자 추적 초기화 (새로운 이미지 생성시마다)
            self.font_manager.clear_character_tracking()
            
            theme = self.theme_manager.get_theme(theme_name)
            
            width = 2880
            height = 1094
            
            if bg_url:
                background = self.image_processor.load_background_image(bg_url, width, height, theme)
            else:
                background = self.image_processor.create_background(width, height, theme)
                
            draw = ImageDraw.Draw(background)
            
            profile_image = self.image_processor.load_profile_image(avatar_url)
            
            profile_diameter = 480
            profile_image = self.image_processor.create_circular_image(profile_image, profile_diameter, theme)
            
            # 레이아웃 계산
            header_y = int(height * 0.08)
            profile_title_y = int(height * 0.4)
            subtitle_y = int(height * 0.7)
            footer_y = int(height * 0.85)
            
            profile_x = 0
            profile_y = profile_title_y - profile_diameter // 2
            
            background.paste(profile_image, (profile_x, profile_y), profile_image)
            
            username_color = self._parse_color(username_color_hex)
            
            if header_text:
                self._draw_header_text(draw, header_text, width // 2, header_y, theme)
            
            title_x = profile_x + profile_diameter + 60
            title_y = profile_title_y - 170
            actual_title_font_size = self._draw_title(draw, title_text, title_x, title_y, username_color, strikeout, theme, suffix_text)
            
            suffix_end_x = title_x
            if suffix_text:
                title_width = self.text_renderer.get_mixed_text_width(title_text, actual_title_font_size)
                suffix_x = title_x + title_width + 20
                suffix_width = self.text_renderer.get_mixed_text_width(suffix_text, 100)
                suffix_end_x = suffix_x + suffix_width
                self._draw_suffix(draw, suffix_text, suffix_x, title_y, actual_title_font_size, theme)
            else:
                suffix_end_x = title_x + self.text_renderer.get_mixed_text_width(title_text, actual_title_font_size)
            
            if subtitle_text:
                content_start_x = profile_x
                content_end_x = suffix_end_x
                content_center_x = (content_start_x + content_end_x) // 2
                self._draw_subtitle(draw, subtitle_text, content_center_x, subtitle_y, theme)
            
            if footer_text:
                self._draw_footer_text(draw, footer_text, width // 2, footer_y, theme)
            
            img_byte_array = BytesIO()
            background.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)
            
            # 폰트 지원 리포트 출력
            self._print_font_reports()
            
            return img_byte_array.getvalue()
            
        except Exception as e:
            print(f"이미지 생성 중 오류 발생: {str(e)}")
            raise
    
    def _print_font_reports(self):
        """폰트 관련 리포트들을 출력"""
        print("\n" + "="*60)
        print("🔍 폰트 사용 분석 리포트")
        print("="*60)
        
        # 1. 폰트 사용 통계
        usage_report = self.font_manager.get_font_usage_statistics()
        if "폰트 사용 통계가 없습니다." not in usage_report:
            print("\n📊 폰트 사용 통계:")
            print("-" * 40)
            print(usage_report)
        
        # 2. 지원되지 않는 문자 리포트
        unsupported_report = self.font_manager.get_unsupported_characters_report()
        if "모든 문자가 지원됩니다." not in unsupported_report:
            print("\n❌ 지원되지 않는 문자:")
            print("-" * 40)
            print(unsupported_report)
        
        # 3. 지원되는 문자 리포트 (디버깅용)
        supported_report = self.font_manager.get_supported_characters_report()
        if "지원되는 문자가 없습니다." not in supported_report:
            print("\n✅ 지원되는 문자 (상세):")
            print("-" * 40)
            print(supported_report)
        
        print("="*60)

    def _parse_color(self, color_hex: str) -> Tuple[int, int, int]:
        """16진수 색상 코드를 RGB 튜플로 변환"""
        if not color_hex:
            return (255, 255, 255)
        
        color_hex = color_hex.lstrip('#')
        return tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    
    def _draw_title(self, draw: ImageDraw, text: str, x: int, y: int, 
                    color: Tuple[int, int, int], strikeout: bool, theme, suffix_text: str = "") -> int:
        """타이틀 텍스트 그리기"""
        font_size = 260
        suffix_font_size = 100
        
        max_width = 2880 - x - 100
        
        # 타이틀과 접미사의 전체 너비 계산
        while font_size > 50:
            title_width = self.text_renderer.get_mixed_text_width(text, font_size)
            suffix_width = 0
            if suffix_text:
                suffix_width = self.text_renderer.get_mixed_text_width(suffix_text, suffix_font_size) + 10  # 20은 타이틀과 접미사 사이 간격
            
            total_width = title_width + suffix_width
            
            if total_width <= max_width:
                break
            
            font_size -= 1
        
        actual_width = self.text_renderer.render_mixed_text(
            draw, text, x, y, color, font_size, 
            shadow=theme.text_shadow, shadow_offset=3
        )
        
        if strikeout:
            line_y = y + (font_size // 1.2)
            draw.line((x, line_y, x + actual_width, line_y), 
                     fill=(255, 255, 255) if color == (255, 255, 255) else (192, 192, 192), 
                     width=25)
        
        return font_size
    
    def _draw_subtitle(self, draw: ImageDraw, text: str, x: int, y: int, theme):
        """서브타이틀 텍스트 그리기"""
        font_size = 105
        text_width = self.text_renderer.get_mixed_text_width(text, font_size)
        
        self.text_renderer.render_mixed_text(
            draw, text, x - text_width // 2, y, (230, 230, 230), font_size,
            shadow=theme.text_shadow, shadow_offset=2
        )
    
    def _draw_header_text(self, draw: ImageDraw, text: str, x: int, y: int, theme):
        """헤더 텍스트 그리기"""
        font_size = 80
        text_width = self.text_renderer.get_mixed_text_width(text, font_size)
        
        self.text_renderer.render_mixed_text(
            draw, text, x - text_width // 2, y, (230, 230, 230), font_size,
            shadow=theme.text_shadow, shadow_offset=2
        )
    
    def _draw_footer_text(self, draw: ImageDraw, text: str, x: int, y: int, theme):
        """푸터 텍스트 그리기"""
        font_size = 70
        text_width = self.text_renderer.get_mixed_text_width(text, font_size)
        
        self.text_renderer.render_mixed_text(
            draw, text, x - text_width // 2, y, (230, 230, 230), font_size,
            shadow=theme.text_shadow, shadow_offset=2
        )
    
    def _draw_suffix(self, draw: ImageDraw, text: str, x: int, y: int, title_font_size: int, theme):
        """접미사 텍스트 그리기"""
        suffix_font_size = 100
        
        title_font = self.font_manager.get_font(title_font_size, 'korean')
        suffix_font = self.font_manager.get_font(suffix_font_size, 'korean')
        
        title_bottom = self.text_renderer.get_text_bottom_offset(title_font)
        suffix_bottom = self.text_renderer.get_text_bottom_offset(suffix_font)
        
        bottom_diff = title_bottom - suffix_bottom
        adjusted_y = y + bottom_diff - 15
        
        self.text_renderer.render_mixed_text(
            draw, text, x, adjusted_y, (230, 230, 230), suffix_font_size,
            shadow=theme.text_shadow, shadow_offset=2
        )
