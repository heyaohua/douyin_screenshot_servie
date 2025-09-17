#!/usr/bin/env python3
"""
使用Firefox的Playwright测试
"""
import asyncio
import logging
import os
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_with_firefox():
    """使用Firefox测试"""
    douyin_url = "https://v.douyin.com/CCFAA7m56G8/"
    
    logger.info("开始使用Firefox测试...")
    
    try:
        async with async_playwright() as p:
            logger.info("Playwright启动成功")
            
            # 使用Firefox浏览器
            browser = await p.firefox.launch(headless=False)
            logger.info("Firefox浏览器启动成功")
            
            # 创建页面
            page = await browser.new_page()
            logger.info("页面创建成功")
            
            # 先访问一个简单的页面测试
            logger.info("正在访问测试页面...")
            await page.goto("https://httpbin.org/get", timeout=30000)
            logger.info("测试页面加载成功")
            
            # 获取页面标题
            title = await page.title()
            logger.info(f"测试页面标题: {title}")
            
            # 现在尝试访问抖音链接
            logger.info(f"正在访问抖音链接: {douyin_url}")
            
            # 设置User-Agent模拟移动设备
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
            })
            
            response = await page.goto(douyin_url, timeout=30000)
            logger.info(f"抖音页面响应状态码: {response.status}")
            
            # 等待页面加载
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # 获取页面信息
            douyin_title = await page.title()
            current_url = page.url
            
            logger.info(f"抖音页面标题: {douyin_title}")
            logger.info(f"当前URL: {current_url}")
            
            # 暂停观察页面
            logger.info("暂停5秒观察页面...")
            await asyncio.sleep(5)
            
            # 尝试截图
            screenshots_dir = "../screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = f"{screenshots_dir}/douyin_firefox_screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"截图已保存到: {screenshot_path}")
            
            # 关闭浏览器
            await browser.close()
            logger.info("Firefox浏览器已关闭")
            
            return {
                "success": True,
                "browser": "Firefox",
                "original_url": douyin_url,
                "current_url": current_url,
                "title": douyin_title,
                "status_code": response.status,
                "screenshot_path": screenshot_path
            }
            
    except Exception as e:
        logger.error(f"Firefox测试失败: {e}")
        return {
            "success": False,
            "browser": "Firefox",
            "error": str(e)
        }

async def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始使用Firefox测试抖音链接")
    logger.info("=" * 50)
    
    result = await test_with_firefox()
    
    logger.info("=" * 50)
    logger.info("测试结果:")
    for key, value in result.items():
        logger.info(f"{key}: {value}")
    logger.info("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
