import os
import yaml
from gpterm.enums import ThemeMode, VoiceStop, GptModel


class Config:
    DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/gpterm/config.yaml")
    DEFAULT_IMAGE_STORE_PATH = "/var/tmp/gpterm/generated_images"

    def __init__(self, file_path):
        self.file_path = file_path
        self.color_theme = ThemeMode.dark
        self.use_code_format = False  # toggle this to set code formatting on/off
        self.display_advanced = False
        self.use_voice = True
        self.voice_name = 'Karen'
        self.voice_over = False
        self.voice_stop = VoiceStop.period
        self.image_size = 256
        self.image_view = True
        self.image_store = Config.DEFAULT_IMAGE_STORE_PATH
        self.model = GptModel.davinci
        self.temperature = 0.75

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path) as fp:
                    loaded_cfg = yaml.safe_load(fp)
                if loaded_cfg:
                    if 'color_theme' in loaded_cfg:
                        self.color_theme = ThemeMode[loaded_cfg['color_theme']]
                    self.use_code_format = loaded_cfg.get('use_code_format', self.use_code_format)
                    self.display_advanced = loaded_cfg.get('display_advanced', self.display_advanced)
                    self.use_voice = loaded_cfg.get('use_voice', self.use_voice)
                    self.voice_name = loaded_cfg.get('voice_name', self.voice_name)
                    self.voice_over = loaded_cfg.get('voice_over', self.voice_over)
                    if 'voice_stop' in loaded_cfg:
                        self.voice_stop = VoiceStop[loaded_cfg['voice_stop']]
                    self.image_size = loaded_cfg.get('image_size', self.image_size)
                    self.image_view = loaded_cfg.get('image_view', self.image_view)
                    self.image_store = loaded_cfg.get('image_store', self.image_store)
                    if 'model' in loaded_cfg:
                        self.model = GptModel[loaded_cfg['model']]
                    self.temperature = loaded_cfg.get('temperature', self.temperature)
            except Exception as e:
                print(f"Error loading {self.file_path}: {e}")

    def save(self):
        yaml_dict = {'color_theme': self.color_theme.name,
                     'use_code_format': self.use_code_format,
                     'display_advanced': self.display_advanced,
                     'use_voice': self.use_voice,
                     'voice_name': self.voice_name,
                     'voice_over': self.voice_over,
                     'voice_stop': self.voice_stop.name,
                     'image_size': self.image_size,
                     'image_view': self.image_view,
                     'image_store': self.image_store,
                     'model': self.model.name,
                     'temperature': self.temperature,
                     }

        cfg_folder = os.path.dirname(self.file_path)
        if not os.path.exists(cfg_folder):
            os.makedirs(cfg_folder)
        with open(self.file_path, 'w') as fp:
            yaml.safe_dump(yaml_dict, fp, default_flow_style=False)
