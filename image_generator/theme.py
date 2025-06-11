from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class Theme:
    name: str
    background_color: Tuple[int, int, int, int]
    background_gradient: bool
    gradient_colors: Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]
    text_shadow: bool
    border_style: str  # 'solid', 'glow', 'double'
    border_color: Tuple[int, int, int]
    overlay_opacity: float

class ThemeManager:
    def __init__(self):
        self.themes = {
            'default': Theme(
                name='default',
                background_color=(0, 0, 0, 0),
                background_gradient=False,
                gradient_colors=None,
                text_shadow=False,
                border_style='solid',
                border_color=(255, 255, 255),
                overlay_opacity=0.0
            ),
            'minimal': Theme(
                name='minimal',
                background_color=(245, 245, 245, 255),
                background_gradient=False,
                gradient_colors=None,
                text_shadow=False,
                border_style='solid',
                border_color=(200, 200, 200),
                overlay_opacity=0.0
            ),
            'gradient': Theme(
                name='gradient',
                background_color=(0, 0, 0, 0),
                background_gradient=True,
                gradient_colors=((88, 101, 242), (237, 66, 69)),  # Discord 색상
                text_shadow=True,
                border_style='glow',
                border_color=(255, 255, 255),
                overlay_opacity=0.2
            ),
            'dark': Theme(
                name='dark',
                background_color=(35, 39, 42, 255),
                background_gradient=False,
                gradient_colors=None,
                text_shadow=True,
                border_style='double',
                border_color=(255, 255, 255),
                overlay_opacity=0.0
            ),
            'colorful': Theme(
                name='colorful',
                background_color=(0, 0, 0, 0),
                background_gradient=True,
                gradient_colors=((255, 0, 150), (0, 150, 255)),
                text_shadow=True,
                border_style='glow',
                border_color=(255, 255, 255),
                overlay_opacity=0.3
            ),
            'gaming': Theme(
                name='gaming',
                background_color=(20, 20, 20, 255),
                background_gradient=True,
                gradient_colors=((138, 43, 226), (0, 255, 127)),
                text_shadow=True,
                border_style='glow',
                border_color=(0, 255, 0),
                overlay_opacity=0.4
            ),
            'cute': Theme(
                name='cute',
                background_color=(255, 240, 245, 255),
                background_gradient=True,
                gradient_colors=((255, 182, 193), (255, 192, 203)),
                text_shadow=False,
                border_style='double',
                border_color=(255, 105, 180),
                overlay_opacity=0.1
            )
        }
    
    def get_theme(self, theme_name: str) -> Theme:
        """테마 이름으로 테마 객체 반환"""
        return self.themes.get(theme_name, self.themes['default'])
    
    def get_available_themes(self) -> list:
        """사용 가능한 테마 목록 반환"""
        return list(self.themes.keys())
