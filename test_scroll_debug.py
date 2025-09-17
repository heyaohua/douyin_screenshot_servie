#!/usr/bin/env python3
"""
滚动调试脚本 - 专门测试滚动功能是否正常
"""
import asyncio
import logging
import sys
sys.path.append('.')
from simple_douyin_test import DouyinScreenshot

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_scroll_functionality():
    """测试滚动功能是否正常工作"""
    douyin_url = "https://v.douyin.com/Zdo3P7Zv51o/"
    
    logger.info("=" * 60)
    logger.info("开始滚动功能调试测试")
    logger.info("=" * 60)
    
    screenshot_service = DouyinScreenshot()
    
    try:
        # 启动浏览器（非无头模式，这样可以看到滚动效果）
        if not await screenshot_service.start_browser(headless=False):
            return
        
        # 创建移动端上下文
        if not await screenshot_service.create_mobile_context():
            return
        
        # 创建页面
        if not await screenshot_service.create_page():
            return
        
        # 访问抖音链接
        result = await screenshot_service.visit_douyin_url(douyin_url)
        
        if result.get("success"):
            logger.info("页面访问成功，开始滚动测试...")
            
            # 等待页面完全加载
            await asyncio.sleep(3)
            
            # 获取初始滚动位置
            initial_scroll = await screenshot_service.page.evaluate("window.pageYOffset")
            logger.info(f"初始滚动位置: {initial_scroll}")
            
            # 获取页面高度信息
            page_info = await screenshot_service.page.evaluate("""
                () => {
                    const body = document.body;
                    const html = document.documentElement;
                    return {
                        windowHeight: window.innerHeight,
                        bodyScrollHeight: body.scrollHeight,
                        documentScrollHeight: html.scrollHeight,
                        bodyOffsetHeight: body.offsetHeight,
                        htmlOffsetHeight: html.offsetHeight,
                        scrollY: window.pageYOffset,
                        scrollableHeight: Math.max(body.scrollHeight, html.scrollHeight, body.offsetHeight, html.offsetHeight)
                    };
                }
            """)
            
            logger.info("页面信息:")
            for key, value in page_info.items():
                logger.info(f"  {key}: {value}")
            
            # 测试不同的滚动方法
            scroll_methods = [
                ("JavaScript window.scrollTo", "window.scrollTo(0, 500)"),
                ("JavaScript smooth scroll", "window.scrollTo({top: 500, behavior: 'smooth'})"),
                ("键盘 PageDown", "keyboard:PageDown"),
                ("鼠标滚轮", "wheel:500"),
                ("键盘 End", "keyboard:End"),
            ]
            
            for method_name, method_cmd in scroll_methods:
                logger.info(f"\n--- 测试滚动方法: {method_name} ---")
                
                # 回到顶部
                await screenshot_service.page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.5)
                
                # 获取滚动前位置
                before_scroll = await screenshot_service.page.evaluate("window.pageYOffset")
                logger.info(f"滚动前位置: {before_scroll}")
                
                # 执行滚动
                if method_cmd.startswith("keyboard:"):
                    key = method_cmd.split(":")[1]
                    await screenshot_service.page.keyboard.press(key)
                elif method_cmd.startswith("wheel:"):
                    delta = int(method_cmd.split(":")[1])
                    await screenshot_service.page.mouse.wheel(0, delta)
                else:
                    await screenshot_service.page.evaluate(method_cmd)
                
                # 等待滚动完成
                await asyncio.sleep(1)
                
                # 获取滚动后位置
                after_scroll = await screenshot_service.page.evaluate("window.pageYOffset")
                logger.info(f"滚动后位置: {after_scroll}")
                
                # 检查滚动是否生效
                if after_scroll != before_scroll:
                    logger.info(f"✅ {method_name} 滚动生效! 移动了 {after_scroll - before_scroll} 像素")
                else:
                    logger.info(f"❌ {method_name} 滚动无效")
                
                # 暂停一下让用户观察
                await asyncio.sleep(2)
            
            logger.info("\n" + "=" * 60)
            logger.info("滚动测试完成!")
            logger.info("=" * 60)
            
            # 等待用户观察
            logger.info("等待10秒让你观察最终状态...")
            await asyncio.sleep(10)
        
        else:
            logger.error(f"页面访问失败: {result.get('error')}")
    
    finally:
        await screenshot_service.close()

async def main():
    """主函数"""
    await test_scroll_functionality()

if __name__ == "__main__":
    asyncio.run(main())
