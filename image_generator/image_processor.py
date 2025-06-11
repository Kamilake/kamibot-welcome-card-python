import requests
from io import BytesIO
from PIL import Image, ImageDraw
from theme import Theme

class ImageProcessor:
    @staticmethod
    def load_background_image(bg_url: str, width: int, height: int, theme: Theme) -> Image.Image:
        """URL에서 배경 이미지 로드 및 처리"""
        try:
            response = requests.get(bg_url)
            response.raise_for_status()
            bg_image = Image.open(BytesIO(response.content))
            
            if bg_image.mode != 'RGBA':
                bg_image = bg_image.convert('RGBA')
            
            bg_width, bg_height = bg_image.size
            scale = max(width / bg_width, height / bg_height)
            
            new_width = int(bg_width * scale)
            new_height = int(bg_height * scale)
            
            bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            bg_image = bg_image.crop((left, top, left + width, top + height))
            
            if theme.overlay_opacity > 0:
                overlay = Image.new('RGBA', (width, height), (0, 0, 0, int(255 * theme.overlay_opacity)))
                bg_image = Image.alpha_composite(bg_image, overlay)
            
            return bg_image
            
        except Exception as e:
            print(f"배경 이미지 로드 실패: {e}, 기본 배경 사용")
            return ImageProcessor.create_background(width, height, theme)
    
    @staticmethod
    def create_background(width: int, height: int, theme: Theme) -> Image.Image:
        """테마에 따른 배경 생성"""
        background = Image.new('RGBA', (width, height), theme.background_color)
        
        if theme.background_gradient:
            draw = ImageDraw.Draw(background)
            start_color, end_color = theme.gradient_colors
            
            for i in range(height):
                ratio = i / height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                draw.line([(0, i), (width, i)], fill=(r, g, b, 255))
        
        return background
    
    @staticmethod
    def load_profile_image(avatar_url: str) -> Image.Image:
        """URL에서 프로필 이미지 로드"""
        response = requests.get(avatar_url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    
    @staticmethod
    def create_circular_image(image: Image.Image, diameter: int, theme: Theme) -> Image.Image:
        """테마에 따른 원형 프로필 이미지 생성"""
        image = image.resize((diameter, diameter), Image.Resampling.LANCZOS)
        
        border_thickness = 15
        total_diameter = diameter + (border_thickness * 2)
        result = Image.new('RGBA', (total_diameter, total_diameter), (0, 0, 0, 0))
        
        mask = Image.new('L', (diameter, diameter), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, diameter, diameter), fill=255)
        
        output = Image.new('RGBA', (diameter, diameter), (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)
        
        result.paste(output, (border_thickness, border_thickness))
        
        draw = ImageDraw.Draw(result)
        
        if theme.border_style == 'glow':
            for i in range(5):
                alpha = int(255 * (0.3 - i * 0.05))
                color = theme.border_color + (alpha,)
                draw.ellipse((border_thickness - i*2, border_thickness - i*2, 
                             border_thickness + diameter + i*2, border_thickness + diameter + i*2), 
                            outline=color, width=border_thickness + i*2)
        
        elif theme.border_style == 'double':
            draw.ellipse((border_thickness - 5, border_thickness - 5, 
                         border_thickness + diameter + 5, border_thickness + diameter + 5), 
                        outline=theme.border_color, width=5)
        
        draw.ellipse((border_thickness, border_thickness, 
                     border_thickness + diameter, border_thickness + diameter), 
                    outline=theme.border_color, width=border_thickness)
        
        return result
