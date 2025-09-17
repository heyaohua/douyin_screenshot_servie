"""
抖音相关的API路由
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
from app.models.douyin import DouyinUrlRequest, DouyinPageResponse
from app.services.playwright_service import playwright_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/douyin", tags=["抖音"])

@router.post("/open", response_model=DouyinPageResponse)
async def open_douyin_url(request: DouyinUrlRequest):
    """
    打开抖音链接并获取页面信息
    
    Args:
        request: 包含抖音链接的请求对象
        
    Returns:
        页面信息
    """
    try:
        # 确保浏览器已初始化
        if not playwright_service.browser:
            await playwright_service.initialize()
        
        # 打开抖音链接
        result = await playwright_service.open_douyin_url(str(request.url))
        
        if result.get("success"):
            return DouyinPageResponse(**result)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"打开链接失败: {result.get('error', '未知错误')}"
            )
            
    except Exception as e:
        logger.error(f"处理抖音链接时出错: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )

@router.get("/test")
async def test_douyin_link():
    """
    测试打开指定的抖音链接
    """
    test_url = "https://v.douyin.com/CCFAA7m56G8/"
    
    try:
        # 确保浏览器已初始化
        if not playwright_service.browser:
            init_result = await playwright_service.initialize()
            if not init_result:
                raise HTTPException(
                    status_code=500,
                    detail="浏览器初始化失败"
                )
        
        # 打开测试链接
        result = await playwright_service.open_douyin_url(test_url)
        
        return {
            "message": "测试完成",
            "test_url": test_url,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"测试抖音链接时出错: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"测试失败: {str(e)}"
        )

@router.post("/long-screenshot")
async def take_long_screenshot(request: DouyinUrlRequest):
    """
    对抖音页面进行长截图
    
    Args:
        request: 包含抖音链接的请求对象
        
    Returns:
        长截图结果信息
    """
    try:
        # 确保浏览器已初始化
        if not playwright_service.browser:
            init_result = await playwright_service.initialize()
            if not init_result:
                raise HTTPException(
                    status_code=500,
                    detail="浏览器初始化失败"
                )
        
        # 执行长截图
        result = await playwright_service.take_long_screenshot(str(request.url))
        
        if result.get("success"):
            return {
                "message": "长截图完成",
                "data": result
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"长截图失败: {result.get('error', '未知错误')}"
            )
            
    except Exception as e:
        logger.error(f"长截图时出错: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )

@router.post("/test-long-screenshot")
async def test_long_screenshot():
    """
    测试长截图功能
    """
    test_url = "https://v.douyin.com/Zdo3P7Zv51o/"
    
    try:
        # 确保浏览器已初始化
        if not playwright_service.browser:
            init_result = await playwright_service.initialize()
            if not init_result:
                raise HTTPException(
                    status_code=500,
                    detail="浏览器初始化失败"
                )
        
        # 执行长截图
        result = await playwright_service.take_long_screenshot(test_url)
        
        return {
            "message": "测试长截图完成",
            "test_url": test_url,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"测试长截图时出错: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"测试失败: {str(e)}"
        )

@router.post("/close-browser")
async def close_browser():
    """关闭浏览器"""
    try:
        await playwright_service.close()
        return {"message": "浏览器已关闭"}
    except Exception as e:
        logger.error(f"关闭浏览器时出错: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"关闭浏览器失败: {str(e)}"
        )
