import os
from typing import Dict, List, Optional, Set
from PIL import ImageFont
from fontTools.ttLib import TTFont
import unicodedata

class FontManager:
    def __init__(self):
        # 시스템에 설치된 다양한 폰트 경로 (TTC 파일의 경우 인덱스 포함)
        self.font_paths = {
            # 한국어 폰트 (나눔)
            'nanum_square': '/usr/share/fonts/truetype/nanum/NanumSquareB.ttf',
            'nanum_gothic': '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            'nanum_gothic_bold': '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
            'nanum_myeongjo': '/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf',
            'nanum_myeongjo_bold': '/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf',
            'nanum_coding': '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf',
            
            # Noto 폰트 (CJK) - TTC 파일이므로 폰트 인덱스 필요
            'noto_sans_kr': ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 0),
            'noto_sans_kr_bold': ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 0),
            'noto_serif_kr': ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 0),
            'noto_serif_kr_bold': ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc', 0),
            'noto_mono': '/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf',
            'noto_sans': '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
            'noto_sans_bold': '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf',

            # 이모지, 특수 문자 지원 폰트
            'noto_emoji': '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
            'noto_emoji_regular': '/usr/share/fonts/truetype/noto/NotoEmoji-Regular.ttf',
            
            # Segoe UI 폰트 패밀리 (Windows 기본 폰트)
            'segoe_ui': '/usr/share/fonts/truetype/segoe-ui/segoeui.ttf',
            'segoe_ui_bold': '/usr/share/fonts/truetype/segoe-ui/segoeuib.ttf',
            'segoe_ui_italic': '/usr/share/fonts/truetype/segoe-ui/segoeuii.ttf',
            'segoe_ui_bold_italic': '/usr/share/fonts/truetype/segoe-ui/segoeuiz.ttf',
            'segoe_ui_light': '/usr/share/fonts/truetype/segoe-ui/segoeuil.ttf',
            'segoe_ui_semibold': '/usr/share/fonts/truetype/segoe-ui/seguisb.ttf',
            'segoe_ui_black': '/usr/share/fonts/truetype/segoe-ui/seguibl.ttf',
            'segoe_ui_emoji': '/usr/share/fonts/truetype/segoe-ui/seguiemj.ttf',
            'segoe_ui_historic': '/usr/share/fonts/truetype/segoe-ui/seguihis.ttf',
            'segoe_ui_symbol': '/usr/share/fonts/truetype/segoe-ui/seguisym.ttf',
            
            # 일본어 폰트
            'takao_gothic': '/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf',
            'takao_mincho': '/usr/share/fonts/truetype/takao-mincho/TakaoMincho.ttf',
            'takao_pgothic': '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf',
            'takao_pmincho': '/usr/share/fonts/truetype/takao-mincho/TakaoPMincho.ttf',
            
            # 중국어 폰트 - TTC 파일
            'wqy_microhei': ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 0),
            'wqy_zenhei': ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 0),
            'arphic_ukai': ('/usr/share/fonts/truetype/arphic/ukai.ttc', 0),
            'arphic_uming': ('/usr/share/fonts/truetype/arphic/uming.ttc', 0),
            
            # 서양 폰트 (기본)
            'dejavu_sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            'dejavu_sans_bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            'dejavu_serif': '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
            'dejavu_serif_bold': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
            'dejavu_mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
            'dejavu_mono_bold': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
            
            # Liberation 폰트
            'liberation_sans': '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            'liberation_sans_bold': '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            'liberation_serif': '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
            'liberation_serif_bold': '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
            'liberation_mono': '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            'liberation_mono_bold': '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',
            'liberation2_sans': '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
            'liberation2_serif': '/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf',
            'liberation2_mono': '/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf',
            
            # Roboto 폰트 패밀리
            'roboto': '/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Regular.ttf',
            'roboto_bold': '/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Bold.ttf',
            'roboto_slab': '/usr/share/fonts/truetype/roboto-slab/RobotoSlab-Regular.ttf',
            'roboto_slab_bold': '/usr/share/fonts/truetype/roboto-slab/RobotoSlab-Bold.ttf',
            
            # Droid 폰트
            'droid_fallback': '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            
            # 웹/시스템 폰트 (Carlito = Calibri 대체, Caladea = Cambria 대체)
            'carlito': '/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf',
            'carlito_bold': '/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf',
            'caladea': '/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf',
            'caladea_bold': '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf',
            
            # 기타 웹 폰트
            'open_sans': '/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf',
            'open_sans_bold': '/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf',
            'lato': '/usr/share/fonts/truetype/lato/Lato-Regular.ttf',
            'lato_bold': '/usr/share/fonts/truetype/lato/Lato-Bold.ttf',
            
            # 개발자용 폰트
            'fira_code': '/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf',
            'fira_code_bold': '/usr/share/fonts/truetype/firacode/FiraCode-Bold.ttf',
            'jetbrains_mono': '/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf',
            'jetbrains_mono_bold': '/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf',
            'hack': '/usr/share/fonts/truetype/hack/Hack-Regular.ttf',
            'hack_bold': '/usr/share/fonts/truetype/hack/Hack-Bold.ttf',
            'inconsolata': '/usr/share/fonts/truetype/inconsolata/Inconsolata-Regular.ttf',
            'cascadia_code': '/usr/share/fonts/truetype/cascadia-code/CascadiaCode.ttf',
            
            # FreeFonts
            'freefont_sans': '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
            'freefont_sans_bold': '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
            'freefont_serif': '/usr/share/fonts/truetype/freefont/FreeSerif.ttf',
            'freefont_serif_bold': '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf',
            'freefont_mono': '/usr/share/fonts/truetype/freefont/FreeMono.ttf',
            'freefont_mono_bold': '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',

            # FontAwesome (아이콘 폰트)
            'font_awesome': '/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf',
            
            # OpenSymbol
            'opensymbol': '/usr/share/fonts/truetype/opensymbol/opens___.ttf'
        }
        
        # 사용 가능한 폰트 확인
        self.available_fonts = {}
        for name, path_info in self.font_paths.items():
            if isinstance(path_info, tuple):
                path, font_index = path_info
            else:
                path = path_info
                font_index = None
                
            if os.path.exists(path):
                self.available_fonts[name] = (path, font_index) if font_index is not None else path
                print(f"폰트 발견: {name} -> {path}" + (f" (인덱스: {font_index})" if font_index is not None else ""))
        
        # 통합된 폰트 우선순위 목록 (높은 우선순위부터) - Noto 폰트 패밀리 우선순위 상승
        self.font_priority = [
            'noto_sans_kr_bold',    # 1순위: Noto Sans 한국어 볼드
            'noto_sans_kr',         # 2순위: Noto Sans 한국어
            'noto_serif_kr_bold',   # 3순위: Noto Serif 한국어 볼드
            'noto_serif_kr',        # 4순위: Noto Serif 한국어
            'noto_sans_bold',       # 5순위: Noto Sans 볼드
            'noto_sans',            # 6순위: Noto Sans
            'noto_emoji',           # 7순위: Noto 이모지 컬러
            'noto_emoji_regular',   # 8순위: Noto 이모지 일반
            'noto_mono',            # 9순위: Noto Mono
            'segoe_ui_bold',        # 10순위: Segoe UI 볼드
            'segoe_ui',             # 11순위: Segoe UI
            'segoe_ui_semibold',    # 12순위: Segoe UI 세미볼드
            'segoe_ui_emoji',       # 13순위: Segoe UI 이모지
            'segoe_ui_symbol',      # 14순위: Segoe UI 심볼
            'nanum_square',         # 15순위: 나눔스퀘어
            'nanum_gothic_bold',    # 16순위: 나눔고딕 볼드
            'nanum_gothic',         # 17순위: 나눔고딕
            'segoe_ui_light',       # 18순위: Segoe UI 라이트
            'segoe_ui_italic',      # 19순위: Segoe UI 이탤릭
            'segoe_ui_bold_italic', # 20순위: Segoe UI 볼드 이탤릭
            'segoe_ui_black',       # 21순위: Segoe UI 블랙
            'segoe_ui_historic',    # 22순위: Segoe UI 히스토릭
            'carlito_bold',         # 23순위: Carlito 볼드 (Calibri 대체)
            'carlito',              # 24순위: Carlito (Calibri 대체)
            'caladea_bold',         # 25순위: Caladea 볼드 (Cambria 대체)
            'caladea',              # 26순위: Caladea (Cambria 대체)
            'dejavu_sans_bold',     # 27순위: DejaVu Sans 볼드
            'dejavu_sans',          # 28순위: DejaVu Sans
            'roboto_bold',          # 29순위: Roboto 볼드
            'roboto',               # 30순위: Roboto
            'liberation_sans_bold', # 31순위: Liberation Sans 볼드
            'liberation_sans',      # 32순위: Liberation Sans
            'open_sans_bold',       # 33순위: Open Sans 볼드
            'open_sans',            # 34순위: Open Sans
            'lato_bold',            # 35순위: Lato 볼드
            'lato',                 # 36순위: Lato
            'takao_gothic',         # 37순위: 일본어 고딕
            'takao_pgothic',        # 38순위: 일본어 P고딕
            'wqy_microhei',         # 39순위: 중국어 폰트
            'wqy_zenhei',           # 40순위: 중국어 젠헤이
            'arphic_ukai',          # 41순위: 중국어 우카이
            'arphic_uming',         # 42순위: 중국어 우밍
            'roboto_slab_bold',     # 43순위: Roboto Slab 볼드
            'roboto_slab',          # 44순위: Roboto Slab
            'liberation2_sans',     # 45순위: Liberation2 Sans
            'dejavu_serif_bold',    # 46순위: DejaVu Serif 볼드
            'dejavu_serif',         # 47순위: DejaVu Serif
            'liberation_serif_bold', # 48순위: Liberation Serif 볼드
            'liberation_serif',     # 49순위: Liberation Serif
            'freefont_sans_bold',   # 50순위: FreeSans 볼드
            'freefont_sans',        # 51순위: FreeSans
            'droid_fallback',       # 52순위: Droid Fallback
            'takao_mincho',         # 53순위: 일본어 명조
            'takao_pmincho',        # 54순위: 일본어 P명조
            'fira_code_bold',       # 55순위: FiraCode 볼드
            'fira_code',            # 56순위: FiraCode
            'jetbrains_mono_bold',  # 57순위: JetBrains Mono 볼드
            'jetbrains_mono',       # 58순위: JetBrains Mono
            'hack_bold',            # 59순위: Hack 볼드
            'hack',                 # 60순위: Hack
            'dejavu_mono_bold',     # 61순위: DejaVu Mono 볼드
            'dejavu_mono',          # 62순위: DejaVu Mono
            'liberation_mono_bold', # 63순위: Liberation Mono 볼드
            'liberation_mono',      # 64순위: Liberation Mono
            'liberation2_mono',     # 65순위: Liberation2 Mono
            'freefont_mono_bold',   # 66순위: FreeMono 볼드
            'freefont_mono',        # 67순위: FreeMono
            'inconsolata',          # 68순위: Inconsolata
            'cascadia_code',        # 69순위: Cascadia Code
            'nanum_myeongjo_bold',  # 70순위: 나눔명조 볼드
            'nanum_myeongjo',       # 71순위: 나눔명조
            'nanum_coding',         # 72순위: 나눔고딕코딩
            'freefont_serif_bold',  # 73순위: FreeSerif 볼드
            'freefont_serif',       # 74순위: FreeSerif
            'liberation2_serif',    # 75순위: Liberation2 Serif
            'opensymbol',           # 76순위: OpenSymbol
            'font_awesome'          # 77순위: FontAwesome
        ]
        
        # 폰트 'cmap' 테이블 캐시
        self.font_cmap_cache = {}
        # 지원되지 않는 문자들을 추적
        self.unsupported_characters = set()
        # 지원되는 문자들과 사용된 폰트를 추적
        self.supported_characters = {}  # {char: font_name}
        self._load_font_cmaps()
        
        print(f"총 {len(self.available_fonts)}개의 폰트가 사용 가능합니다.")
        print(f"폰트 우선순위 목록에 {len(self.font_priority)}개 폰트가 등록되어 있습니다.")
    
    def add_font(self, font_name: str, font_path: str, font_index: Optional[int] = None, priority_position: int = 0):
        """새 폰트를 시스템에 추가"""
        path_info = (font_path, font_index) if font_index is not None else font_path
        
        if os.path.exists(font_path):
            self.font_paths[font_name] = path_info
            self.available_fonts[font_name] = path_info
            
            # 우선순위 목록에 추가
            if font_name not in self.font_priority:
                if 0 <= priority_position <= len(self.font_priority):
                    self.font_priority.insert(priority_position, font_name)
                else:
                    self.font_priority.append(font_name)
            
            # cmap 로드
            try:
                self._load_single_font_cmap(font_name, path_info)
                print(f"폰트 추가됨: {font_name} -> {font_path} (우선순위: {self.font_priority.index(font_name) + 1})")
                return True
            except Exception as e:
                print(f"폰트 cmap 로드 실패: {font_name} - {e}")
                return False
        else:
            print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
            return False
    
    def remove_font(self, font_name: str):
        """폰트를 시스템에서 제거"""
        if font_name in self.available_fonts:
            del self.available_fonts[font_name]
            
        if font_name in self.font_paths:
            del self.font_paths[font_name]
            
        if font_name in self.font_priority:
            self.font_priority.remove(font_name)
            
        if font_name in self.font_cmap_cache:
            del self.font_cmap_cache[font_name]
            
        print(f"폰트 제거됨: {font_name}")
    
    def set_font_priority(self, font_name: str, priority_position: int):
        """폰트의 우선순위 변경"""
        if font_name in self.font_priority:
            self.font_priority.remove(font_name)
        
        if 0 <= priority_position <= len(self.font_priority):
            self.font_priority.insert(priority_position, font_name)
        else:
            self.font_priority.append(font_name)
        
        print(f"폰트 우선순위 변경: {font_name} -> {self.font_priority.index(font_name) + 1}순위")
    
    def get_font_priority_list(self) -> List[str]:
        """현재 폰트 우선순위 목록 반환"""
        return self.font_priority.copy()
    
    def print_font_priority(self):
        """폰트 우선순위 목록 출력"""
        print("\n=== 폰트 우선순위 목록 ===")
        for i, font_name in enumerate(self.font_priority, 1):
            available = "✓" if font_name in self.available_fonts else "✗"
            print(f"{i:2d}. {available} {font_name}")
        print("========================\n")
    
    def _load_single_font_cmap(self, font_name: str, path_info):
        """단일 폰트의 cmap 테이블 로드"""
        try:
            if isinstance(path_info, tuple):
                font_path, font_index = path_info
                tt_font = TTFont(font_path, fontNumber=font_index)
            else:
                font_path = path_info
                tt_font = TTFont(font_path)
            
            if 'cmap' in tt_font:
                char_map = {}
                for table in tt_font['cmap'].tables:
                    if hasattr(table, 'cmap'):
                        char_map.update(table.cmap)
                
                self.font_cmap_cache[font_name] = char_map
                print(f"폰트 {font_name}: {len(char_map)}개 문자 지원")
            else:
                self.font_cmap_cache[font_name] = {}
                
            tt_font.close()
        except Exception as e:
            print(f"폰트 {font_name} cmap 로드 실패: {e}")
            self.font_cmap_cache[font_name] = {}
    
    def _load_font_cmaps(self):
        """모든 사용 가능한 폰트의 cmap 테이블을 미리 로드"""
        for font_name, path_info in self.available_fonts.items():
            self._load_single_font_cmap(font_name, path_info)
    
    def font_supports_character(self, font_name: str, char: str) -> bool:
        """fontTools cmap 테이블을 사용하여 폰트가 특정 문자를 지원하는지 확인"""
        if font_name not in self.font_cmap_cache:
            return False
        
        char_code = ord(char)
        is_supported = char_code in self.font_cmap_cache[font_name]
        
        if is_supported:
            # 지원되는 문자 추적 (첫 번째로 찾은 폰트 기록)
            if char not in self.supported_characters:
                self.supported_characters[char] = font_name
        else:
            # 지원되지 않는 문자 추적
            self.unsupported_characters.add(char)
        
        return is_supported
    
    def font_supports_cluster(self, font_name: str, cluster: str) -> bool:
        """폰트가 그래핌 클러스터의 모든 문자를 지원하는지 확인"""
        if font_name not in self.font_cmap_cache:
            return False
        
        # 클러스터의 모든 문자가 지원되어야 함
        for char in cluster:
            if not self.font_supports_character(font_name, char):
                return False
        
        return True
    
    def get_font_for_character(self, char: str, size: int) -> Optional[ImageFont.FreeTypeFont]:
        """특정 문자에 대해 지원하는 폰트 찾기 (우선순위 기준)"""
        # 우선순위대로 폰트 시도
        for font_name in self.font_priority:
            if font_name in self.available_fonts and self.font_supports_character(font_name, char):
                try:
                    path_info = self.available_fonts[font_name]
                    if isinstance(path_info, tuple):
                        font_path, font_index = path_info
                        return ImageFont.truetype(font_path, size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                    else:
                        return ImageFont.truetype(path_info, size, layout_engine=ImageFont.Layout.RAQM)
                except Exception:
                    continue
        
        # 우선순위 목록에 없는 나머지 폰트들도 시도
        for font_name in self.available_fonts:
            if font_name not in self.font_priority and self.font_supports_character(font_name, char):
                try:
                    path_info = self.available_fonts[font_name]
                    if isinstance(path_info, tuple):
                        font_path, font_index = path_info
                        return ImageFont.truetype(font_path, size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                    else:
                        return ImageFont.truetype(path_info, size, layout_engine=ImageFont.Layout.RAQM)
                except Exception:
                    continue
        
        return None
    
    def get_font_for_cluster(self, cluster: str, size: int, preferred_font_name: str = None) -> Optional[ImageFont.FreeTypeFont]:
        """그래핌 클러스터에 대해 지원하는 폰트 찾기"""
        # 선호 폰트 먼저 시도
        if preferred_font_name and preferred_font_name in self.available_fonts:
            if self.font_supports_cluster(preferred_font_name, cluster):
                try:
                    path_info = self.available_fonts[preferred_font_name]
                    if isinstance(path_info, tuple):
                        font_path, font_index = path_info
                        return ImageFont.truetype(font_path, size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                    else:
                        return ImageFont.truetype(path_info, size, layout_engine=ImageFont.Layout.RAQM)
                except Exception:
                    pass
        
        # 우선순위대로 폰트 시도
        for font_name in self.font_priority:
            if font_name in self.available_fonts and self.font_supports_cluster(font_name, cluster):
                try:
                    path_info = self.available_fonts[font_name]
                    if isinstance(path_info, tuple):
                        font_path, font_index = path_info
                        return ImageFont.truetype(font_path, size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                    else:
                        return ImageFont.truetype(path_info, size, layout_engine=ImageFont.Layout.RAQM)
                except Exception:
                    continue
        
        return None
    
    def get_unsupported_characters_report(self) -> str:
        """지원되지 않는 문자들의 리포트 생성"""
        if not self.unsupported_characters:
            return "모든 문자가 지원됩니다."
        
        report = f"지원되지 않는 문자 {len(self.unsupported_characters)}개:\n"
        for char in sorted(self.unsupported_characters):
            char_code = ord(char)
            char_name = ""
            try:
                char_name = unicodedata.name(char, "")
            except:
                pass
            
            report += f"  - '{char}' (U+{char_code:04X}) {char_name}\n"
        
        return report
    
    def get_supported_characters_report(self) -> str:
        """지원되는 문자들의 리포트 생성"""
        if not self.supported_characters:
            return "지원되는 문자가 없습니다."
        
        # 폰트별로 그룹화
        font_groups = {}
        for char, font_name in self.supported_characters.items():
            if font_name not in font_groups:
                font_groups[font_name] = []
            font_groups[font_name].append(char)
        
        report = f"지원되는 문자 {len(self.supported_characters)}개 (폰트별 분류):\n\n"
        
        # 우선순위 순으로 정렬
        sorted_fonts = []
        for font_name in self.font_priority:
            if font_name in font_groups:
                sorted_fonts.append(font_name)
        
        # 우선순위에 없는 폰트들 추가
        for font_name in font_groups:
            if font_name not in sorted_fonts:
                sorted_fonts.append(font_name)
        
        for font_name in sorted_fonts:
            chars = font_groups[font_name]
            report += f"📝 {font_name} ({len(chars)}개 문자):\n"
            
            # 문자를 유니코드 순으로 정렬
            sorted_chars = sorted(chars, key=ord)
            
            # 문자들을 카테고리별로 분류
            categories = {}
            for char in sorted_chars:
                try:
                    category = unicodedata.category(char)
                    category_name = self._get_category_name(category)
                    if category_name not in categories:
                        categories[category_name] = []
                    categories[category_name].append(char)
                except:
                    if "기타" not in categories:
                        categories["기타"] = []
                    categories["기타"].append(char)
            
            # 카테고리별로 출력
            for category_name, category_chars in categories.items():
                report += f"  [{category_name}] "
                char_list = []
                for char in category_chars[:20]:  # 최대 20개까지만 표시
                    char_code = ord(char)
                    char_name = ""
                    try:
                        char_name = unicodedata.name(char, "")
                    except:
                        pass
                    
                    char_display = f"'{char}'"
                    if char_name:
                        char_display += f"({char_name[:20]}...)" if len(char_name) > 20 else f"({char_name})"
                    char_display += f"[U+{char_code:04X}]"
                    char_list.append(char_display)
                
                if len(category_chars) > 20:
                    char_list.append(f"... 외 {len(category_chars) - 20}개")
                
                report += ", ".join(char_list) + "\n"
            
            report += "\n"
        
        return report
    
    def _get_category_name(self, category: str) -> str:
        """유니코드 카테고리 코드를 한국어 이름으로 변환"""
        category_names = {
            'Lu': '대문자',
            'Ll': '소문자', 
            'Lt': '제목문자',
            'Lm': '수식문자',
            'Lo': '기타문자',
            'Mn': '결합문자(간격없음)',
            'Mc': '결합문자(간격있음)',
            'Me': '결합문자(둘러싸임)',
            'Nd': '십진수',
            'Nl': '문자수',
            'No': '기타수',
            'Pc': '연결구두점',
            'Pd': '대시구두점',
            'Ps': '시작구두점',
            'Pe': '끝구두점',
            'Pi': '시작인용부호',
            'Pf': '끝인용부호',
            'Po': '기타구두점',
            'Sm': '수학기호',
            'Sc': '통화기호',
            'Sk': '수식기호',
            'So': '기타기호',
            'Zs': '공백',
            'Zl': '줄구분자',
            'Zp': '단락구분자',
            'Cc': '제어문자',
            'Cf': '서식문자',
            'Cs': '대용문자',
            'Co': '사용자정의',
            'Cn': '할당안됨'
        }
        return category_names.get(category, f"알수없음({category})")
    
    def get_font_usage_statistics(self) -> str:
        """폰트 사용 통계 리포트 생성"""
        if not self.supported_characters:
            return "폰트 사용 통계가 없습니다."
        
        # 폰트별 사용 횟수 계산
        font_usage = {}
        for font_name in self.supported_characters.values():
            font_usage[font_name] = font_usage.get(font_name, 0) + 1
        
        # 사용 횟수 순으로 정렬
        sorted_usage = sorted(font_usage.items(), key=lambda x: x[1], reverse=True)
        
        report = f"폰트 사용 통계 (총 {len(self.supported_characters)}개 문자):\n\n"
        
        for i, (font_name, count) in enumerate(sorted_usage, 1):
            percentage = (count / len(self.supported_characters)) * 100
            priority = "순위권 밖"
            if font_name in self.font_priority:
                priority = f"{self.font_priority.index(font_name) + 1}순위"
            
            report += f"{i:2d}. {font_name:<20} {count:3d}개 ({percentage:5.1f}%) - {priority}\n"
        
        return report
    
    def clear_character_tracking(self):
        """문자 추적 정보 초기화"""
        self.supported_characters.clear()
        self.unsupported_characters.clear()

    def get_font(self, size: int, font_type: str = 'default') -> ImageFont.FreeTypeFont:
        """폰트 객체 반환 - 폴백 지원 (font_type 파라미터는 호환성을 위해 유지)"""
        # 우선순위대로 폰트 시도
        for font_name in self.font_priority:
            if font_name in self.available_fonts:
                try:
                    path_info = self.available_fonts[font_name]
                    if isinstance(path_info, tuple):
                        font_path, font_index = path_info
                        return ImageFont.truetype(font_path, size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                    else:
                        return ImageFont.truetype(path_info, size, layout_engine=ImageFont.Layout.RAQM)
                except Exception:
                    continue
        
        # 우선순위 목록에 없는 폰트들도 시도
        for font_name in self.available_fonts:
            if font_name not in self.font_priority:
                try:
                    path_info = self.available_fonts[font_name]
                    if isinstance(path_info, tuple):
                        font_path, font_index = path_info
                        return ImageFont.truetype(font_path, size, index=font_index, layout_engine=ImageFont.Layout.RAQM)
                    else:
                        return ImageFont.truetype(path_info, size, layout_engine=ImageFont.Layout.RAQM)
                except Exception:
                    continue
        
        raise RuntimeError("사용 가능한 폰트가 없습니다.")
