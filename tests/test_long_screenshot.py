#!/usr/bin/env python3
"""
长截图功能测试脚本 - 测试不同类型的页面
"""
import asyncio
import logging
import os
from datetime import datetime
from playwright.async_api import async_playwright
from PIL import Image
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从主脚本导入DouyinScreenshot类
import sys
sys.path.append('.')
from simple_douyin_test import DouyinScreenshot

async def test_multiple_urls():
    """测试多个URL的长截图功能"""
    test_urls = [
        "https://v.douyin.com/Zdo3P7Zv51o/",  # 你提供的测试链接
        # 可以添加更多测试链接
    ]
    
    logger.info("=" * 60)
    logger.info("开始多URL长截图测试")
    logger.info("=" * 60)
    
    for i, url in enumerate(test_urls, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"测试第 {i} 个链接: {url}")
        logger.info(f"{'='*60}")
        
        screenshot_service = DouyinScreenshot()
        
        try:
            # 启动浏览器
            if not await screenshot_service.start_browser(headless=False):
                logger.error("浏览器启动失败")
                continue
            
            # 创建移动端上下文
            if not await screenshot_service.create_mobile_context():
                logger.error("移动端上下文创建失败")
                continue
            
            # 创建页面
            if not await screenshot_service.create_page():
                logger.error("页面创建失败")
                continue
            
            # 访问链接
            result = await screenshot_service.visit_douyin_url(url)
            
            if result.get("success"):
                logger.info("页面访问成功，开始长截图...")
                
                # 等待页面完全加载
                await asyncio.sleep(3)
                
                # 生成带索引的截图文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                custom_path = f"../screenshots/test_{i}_{timestamp}_long_screenshot.png"
                
                # 长截图
                screenshot_path = await screenshot_service.take_long_screenshot(custom_path)
                
                if screenshot_path:
                    # 获取文件信息
                    if os.path.exists(screenshot_path):
                        file_size = os.path.getsize(screenshot_path)
                        logger.info(f"✅ 第 {i} 个链接截图成功!")
                        logger.info(f"   原始链接: {result['original_url']}")
                        logger.info(f"   重定向链接: {result['current_url']}")
                        logger.info(f"   截图文件: {screenshot_path}")
                        logger.info(f"   文件大小: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
                else:
                    logger.error(f"❌ 第 {i} 个链接截图失败")
            else:
                logger.error(f"❌ 第 {i} 个链接访问失败: {result.get('error')}")
        
        except Exception as e:
            logger.error(f"❌ 第 {i} 个链接测试出错: {e}")
        
        finally:
            await screenshot_service.close()
            # 等待一下再测试下一个链接
            if i < len(test_urls):
                logger.info("等待3秒后测试下一个链接...")
                await asyncio.sleep(3)
    
    logger.info("\n" + "=" * 60)
    logger.info("所有测试完成！")
    logger.info("=" * 60)

async def main():
    """主函数"""
    await test_multiple_urls()

if __name__ == "__main__":
    asyncio.run(main())
