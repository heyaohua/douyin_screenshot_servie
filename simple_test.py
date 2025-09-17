#!/usr/bin/env python3
"""
简单的Playwright测试 - 验证基础功能
"""
import asyncio
import logging
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def simple_test():
    """简单测试"""
    logger.info("开始简单的Playwright测试...")
    
    try:
        async with async_playwright() as p:
            logger.info("Playwright启动成功")
            
            # 启动浏览器 - 不使用无头模式
            browser = await p.chromium.launch(headless=False)
            logger.info("浏览器启动成功")
            
            # 创建页面
            page = await browser.new_page()
            logger.info("页面创建成功")
            
            # 访问一个简单的页面
            await page.goto("https://httpbin.org/get")
            logger.info("页面加载成功")
            
            # 获取页面标题
            title = await page.title()
            logger.info(f"页面标题: {title}")
            
            # 关闭浏览器
            await browser.close()
            logger.info("浏览器关闭成功")
            
            return {"success": True, "title": title}
            
    except Exception as e:
        logger.error(f"测试失败: {e}")
        return {"success": False, "error": str(e)}

async def main():
    """主函数"""
    result = await simple_test()
    logger.info(f"测试结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())
