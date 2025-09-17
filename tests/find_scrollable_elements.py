#!/usr/bin/env python3
"""
查找页面中可滚动的元素
"""
import asyncio
import logging
import sys
sys.path.append('.')
from simple_douyin_test import DouyinScreenshot

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def find_scrollable_elements():
    """查找页面中所有可滚动的元素"""
    douyin_url = "https://v.douyin.com/Zdo3P7Zv51o/"
    
    logger.info("=" * 60)
    logger.info("查找可滚动元素")
    logger.info("=" * 60)
    
    screenshot_service = DouyinScreenshot()
    
    try:
        # 启动浏览器
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
            logger.info("页面访问成功，开始查找可滚动元素...")
            
            # 等待页面完全加载
            await asyncio.sleep(5)
            
            # 查找所有可滚动的元素
            scrollable_elements = await screenshot_service.page.evaluate("""
                () => {
                    const elements = [];
                    const allElements = document.querySelectorAll('*');
                    
                    for (let elem of allElements) {
                        const style = window.getComputedStyle(elem);
                        const overflowY = style.overflowY;
                        const overflowX = style.overflowX;
                        
                        // 检查是否可滚动
                        if ((overflowY === 'scroll' || overflowY === 'auto' || overflowX === 'scroll' || overflowX === 'auto') ||
                            elem.scrollHeight > elem.clientHeight || 
                            elem.scrollWidth > elem.clientWidth) {
                            
                            elements.push({
                                tagName: elem.tagName,
                                className: elem.className,
                                id: elem.id,
                                scrollHeight: elem.scrollHeight,
                                clientHeight: elem.clientHeight,
                                scrollWidth: elem.scrollWidth,
                                clientWidth: elem.clientWidth,
                                scrollTop: elem.scrollTop,
                                scrollLeft: elem.scrollLeft,
                                overflowY: overflowY,
                                overflowX: overflowX,
                                hasScrollbar: elem.scrollHeight > elem.clientHeight,
                                canScrollVertically: elem.scrollHeight > elem.clientHeight,
                                canScrollHorizontally: elem.scrollWidth > elem.clientWidth
                            });
                        }
                    }
                    
                    return elements;
                }
            """)
            
            logger.info(f"发现 {len(scrollable_elements)} 个可滚动元素:")
            for i, elem in enumerate(scrollable_elements):
                logger.info(f"\n元素 {i+1}:")
                for key, value in elem.items():
                    logger.info(f"  {key}: {value}")
            
            # 尝试监听页面的滚动事件
            logger.info("\n监听页面滚动事件...")
            await screenshot_service.page.evaluate("""
                () => {
                    window.scrollEvents = [];
                    
                    // 监听window滚动
                    window.addEventListener('scroll', () => {
                        window.scrollEvents.push({
                            type: 'window',
                            scrollY: window.pageYOffset,
                            timestamp: Date.now()
                        });
                    });
                    
                    // 监听所有元素的滚动
                    document.querySelectorAll('*').forEach(elem => {
                        elem.addEventListener('scroll', (e) => {
                            window.scrollEvents.push({
                                type: 'element',
                                tagName: e.target.tagName,
                                className: e.target.className,
                                scrollTop: e.target.scrollTop,
                                timestamp: Date.now()
                            });
                        });
                    });
                }
            """)
            
            # 模拟用户滚动操作
            logger.info("模拟不同方式的滚动...")
            
            # 尝试点击页面然后滚动
            await screenshot_service.page.click('body')
            await asyncio.sleep(0.5)
            
            # 尝试鼠标滚轮在不同位置
            for y in [100, 200, 400, 600]:
                await screenshot_service.page.mouse.wheel(0, y)
                await asyncio.sleep(0.5)
            
            # 检查是否有滚动事件
            scroll_events = await screenshot_service.page.evaluate("window.scrollEvents")
            logger.info(f"\n捕获到 {len(scroll_events)} 个滚动事件:")
            for event in scroll_events:
                logger.info(f"  {event}")
            
            # 尝试查找特定的滚动容器
            logger.info("\n查找常见的滚动容器...")
            containers = await screenshot_service.page.evaluate("""
                () => {
                    const selectors = [
                        '.main-content', '.content', '.container', '.scroll-view',
                        '.list-container', '.page-content', '[data-scroll]',
                        'main', 'section', 'article', '.wrapper'
                    ];
                    
                    const containers = [];
                    
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(elem => {
                            if (elem.scrollHeight > elem.clientHeight) {
                                containers.push({
                                    selector: selector,
                                    tagName: elem.tagName,
                                    className: elem.className,
                                    scrollHeight: elem.scrollHeight,
                                    clientHeight: elem.clientHeight
                                });
                            }
                        });
                    });
                    
                    return containers;
                }
            """)
            
            if containers:
                logger.info("发现潜在的滚动容器:")
                for container in containers:
                    logger.info(f"  {container}")
            else:
                logger.info("未发现潜在的滚动容器")
            
            # 等待观察
            logger.info("\n等待15秒供你手动测试滚动...")
            await asyncio.sleep(15)
        
        else:
            logger.error(f"页面访问失败: {result.get('error')}")
    
    finally:
        await screenshot_service.close()

async def main():
    """主函数"""
    await find_scrollable_elements()

if __name__ == "__main__":
    asyncio.run(main())
