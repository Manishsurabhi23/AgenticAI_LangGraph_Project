from configparser import ConfigParser
import os

class Config:
    def __init__(self):
        self.config = ConfigParser()
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(base_dir, 'uiconfigfile.ini')
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Config file not found at: {config_file}")
            self.config.read(config_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file error: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")

    def get_page_title(self):
        try:
            return self.config['DEFAULT'].get('PAGE_TITLE', 'LangGraph : Build Stateful Agentic AI graph')
        except Exception as e:
            raise RuntimeError(f"Error reading PAGE_TITLE from config: {e}")

    def get_llm_options(self):
        try:
            value = self.config['DEFAULT'].get('LLM_OPTIONS', '')
            if not value:
                raise ValueError("LLM_OPTIONS is missing or empty in config file")
            return value.split(',')
        except ValueError as e:
            raise ValueError(f"Configuration error: {e}")
        except Exception as e:
            raise RuntimeError(f"Error reading LLM_OPTIONS from config: {e}")

    def get_usecase_options(self):
        try:
            value = self.config['DEFAULT'].get('USECASE_OPTIONS', '')
            if not value:
                raise ValueError("USECASE_OPTIONS is missing or empty in config file")
            return value.split(',')
        except ValueError as e:
            raise ValueError(f"Configuration error: {e}")
        except Exception as e:
            raise RuntimeError(f"Error reading USECASE_OPTIONS from config: {e}")

    def get_groq_model_options(self):
        try:
            value = self.config['DEFAULT'].get('GROQ_MODEL_OPTIONS', '')
            if not value:
                raise ValueError("GROQ_MODEL_OPTIONS is missing or empty in config file")
            return value.split(',')
        except ValueError as e:
            raise ValueError(f"Configuration error: {e}")
        except Exception as e:
            raise RuntimeError(f"Error reading GROQ_MODEL_OPTIONS from config: {e}")