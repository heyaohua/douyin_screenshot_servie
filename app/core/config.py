from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用基础配置
    app_name: str = "抖音长截图服务"
    debug: bool = False
    version: str = "1.0.0"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 截图配置
    screenshot_timeout: int = 30
    max_screenshot_height: int = 20000
    screenshot_quality: int = 95
    
    # 文件存储配置
    upload_dir: str = "./uploads"
    static_dir: str = "./static"
    
    # Chrome配置
    chrome_driver_path: Optional[str] = None
    headless: bool = True
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 全局设置实例
settings = Settings()
