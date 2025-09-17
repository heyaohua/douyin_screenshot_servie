#!/usr/bin/env python3
"""
本地测试脚本 - 验证Playwright能否正常打开抖音链接
"""
import asyncio
import logging
import os
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_douyin_link():
    """测试打开抖音链接"""
    douyin_url = "https://v.douyin.com/CCFAA7m56G8/"
    
    logger.info("开始启动Playwright浏览器...")
    
    try:
        async with async_playwright() as p:
            # 启动浏览器 - 使用更简单的参数
            browser = await p.chromium.launch(
                headless=True,  # 先用headless模式测试
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            )
            
            logger.info("浏览器启动成功")
            
            # 创建浏览器上下文，模拟移动设备
            context = await browser.new_context(
                viewport={'width': 375, 'height': 812},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
            )
            
            # 创建新页面
            page = await context.new_page()
            
            logger.info(f"正在打开抖音链接: {douyin_url}")
            
            # 打开页面
            response = await page.goto(douyin_url, wait_until='networkidle', timeout=30000)
            
            logger.info(f"页面响应状态码: {response.status}")
            
            # 等待页面加载完成
            await page.wait_for_load_state('networkidle')
            
            # 获取页面信息
            title = await page.title()
            current_url = page.url
            
            logger.info(f"页面标题: {title}")
            logger.info(f"当前URL: {current_url}")
            
            # 暂停5秒让我们观察页面
            logger.info("暂停5秒，观察页面加载情况...")
            await asyncio.sleep(5)
            
            # 尝试截图
            screenshots_dir = "../screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = f"{screenshots_dir}/test_screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"截图已保存到: {screenshot_path}")
            
            # 关闭浏览器
            await browser.close()
            logger.info("浏览器已关闭")
            
            return {
                "success": True,
                "original_url": douyin_url,
                "current_url": current_url,
                "title": title,
                "status_code": response.status,
                "screenshot_path": screenshot_path
            }
            
    except Exception as e:
        logger.error(f"测试失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

async def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始测试Playwright打开抖音链接")
    logger.info("=" * 50)
    
    result = await test_douyin_link()
    
    logger.info("=" * 50)
    logger.info("测试结果:")
    for key, value in result.items():
        logger.info(f"{key}: {value}")
    logger.info("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
