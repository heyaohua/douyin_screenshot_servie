"""
抖音相关的数据模型
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class DouyinUrlRequest(BaseModel):
    """抖音链接请求模型"""
    url: HttpUrl
    
class DouyinPageResponse(BaseModel):
    """抖音页面响应模型"""
    original_url: str
    current_url: Optional[str] = None
    title: Optional[str] = None
    status_code: Optional[int] = None
    viewport: Optional[Dict[str, int]] = None
    success: bool
    error: Optional[str] = None
    
class ScreenshotRequest(BaseModel):
    """截图请求模型"""
    url: HttpUrl
    full_page: bool = True
    
class ScreenshotResponse(BaseModel):
    """截图响应模型"""
    success: bool
    message: str
    screenshot_path: Optional[str] = None
    error: Optional[str] = None
