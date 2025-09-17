#!/usr/bin/env python3
"""
测试Chrome版本的长截图服务
"""
import asyncio
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.playwright_chrome_service import PlaywrightChromeService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_chrome_long_screenshot_service():
    """测试Chrome版本的长截图服务"""
    
    logger.info("=" * 60)
    logger.info("开始测试Chrome版本长截图服务")
    logger.info("=" * 60)
    
    # 创建Chrome服务实例
    chrome_service = PlaywrightChromeService()
    
    try:
        # 初始化浏览器
        logger.info("正在初始化Chrome浏览器...")
        if not await chrome_service.initialize():
            logger.error("Chrome浏览器初始化失败")
            return
        
        logger.info("Chrome浏览器初始化成功")
        
        # 测试URL
        test_url = "https://v.douyin.com/Zdo3P7Zv51o/"
        logger.info(f"测试URL: {test_url}")
        
        # 执行长截图
        logger.info("开始执行Chrome长截图...")
        result = await chrome_service.take_long_screenshot(
            url=test_url,
            output_dir="screenshots"
        )
        
        # 输出结果
        logger.info("=" * 60)
        logger.info("Chrome长截图完成！结果信息:")
        logger.info("=" * 60)
        
        if result.get("success"):
            logger.info(f"✅ 成功: {result['success']}")
            logger.info(f"📁 输出路径: {result['output_path']}")
            logger.info(f"📊 截图数量: {result['screenshot_count']}")
            logger.info(f"📏 总高度: {result['total_height']}px")
            logger.info(f"💾 文件大小: {result['file_size'] / 1024 / 1024:.2f}MB")
            
            if result.get('original_url'):
                logger.info(f"🔗 原始URL: {result['original_url']}")
            if result.get('current_url'):
                logger.info(f"🔗 当前URL: {result['current_url']}")
            if result.get('title'):
                logger.info(f"📄 页面标题: {result['title']}")
        else:
            logger.error(f"❌ 失败: {result.get('error', '未知错误')}")
            
    except Exception as e:
        logger.error(f"测试过程中出现异常: {e}")
        
    finally:
        # 关闭浏览器
        logger.info("正在关闭Chrome浏览器...")
        await chrome_service.close()
        logger.info("Chrome浏览器已关闭")
        
        logger.info("=" * 60)
        logger.info("Chrome测试完成！")
        logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_chrome_long_screenshot_service())
