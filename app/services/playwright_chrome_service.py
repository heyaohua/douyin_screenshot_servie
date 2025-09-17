"""
Playwright Chrome服务模块 - 用于处理网页截图和操作（Chrome版本）
"""
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from typing import Optional, Dict, Any, List
import asyncio
import logging
import os
from datetime import datetime
from PIL import Image
from app.core.config import settings

logger = logging.getLogger(__name__)

class PlaywrightChromeService:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        
    async def initialize(self):
        """初始化Playwright Chrome浏览器"""
        try:
            playwright = await async_playwright().start()
            # 使用系统Chrome浏览器 - 反检测配置
            self.browser = await playwright.chromium.launch(
                headless=False,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # 使用系统Chrome
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--incognito',  # 隐私模式
                    '--disable-blink-features=AutomationControlled',  # 隐藏自动化特征
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-field-trial-config',
                    '--disable-background-networking',
                    '--disable-sync',
                    '--metrics-recording-only',
                    '--no-first-run',
                    '--safebrowsing-disable-auto-update',
                    '--disable-client-side-phishing-detection',
                    '--disable-component-extensions-with-background-pages',
                    '--disable-default-apps',
                    '--mute-audio',
                    '--no-default-browser-check',
                    '--autoplay-policy=user-gesture-required',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection'
                ]
            )
            
            # 创建移动端浏览器上下文，模拟iPhone设备
            self.context = await self.browser.new_context(
                # iPhone 12 Pro 的视口
                viewport={'width': 390, 'height': 844},
                # 最新的iOS Safari User-Agent
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                # 设备像素比
                device_scale_factor=3,
                # Chrome支持的触摸配置
                has_touch=True,
                # 语言设置
                locale='zh-CN',
                # 时区
                timezone_id='Asia/Shanghai'
            )
            
            # 设置额外的HTTP头，模拟真实移动请求
            await self.context.set_extra_http_headers({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            })
            
            logger.info("Playwright Chrome浏览器初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"初始化Chrome浏览器失败: {e}")
            return False
    
    async def close(self):
        """关闭浏览器"""
        try:
            if self.context:
                await self.context.close()
                logger.info("Chrome浏览器上下文已关闭")
            if self.browser:
                await self.browser.close()
                logger.info("Chrome浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭Chrome浏览器时出错: {e}")
    
    async def open_douyin_url(self, url: str) -> Dict[str, Any]:
        """
        打开抖音链接并获取页面信息
        
        Args:
            url: 抖音视频链接
            
        Returns:
            包含页面信息的字典
        """
        if not self.context:
            raise Exception("浏览器未初始化，请先调用initialize方法")
        
        try:
            page = await self.context.new_page()
            
            # 模拟移动端特有的JavaScript API + 反检测
            await page.add_init_script("""
                // 反检测：隐藏自动化特征
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // 反检测：删除自动化相关属性
                delete window.navigator.webdriver;
                delete window.chrome.runtime.onConnect;
                delete window.chrome.runtime.onMessage;
                
                // 反检测：模拟真实用户行为
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
                
                // 模拟触摸事件支持
                Object.defineProperty(navigator, 'maxTouchPoints', {
                    get: () => 5
                });
                
                // 模拟移动端屏幕方向
                Object.defineProperty(screen, 'orientation', {
                    get: () => ({
                        angle: 0,
                        type: 'portrait-primary'
                    })
                });
                
                // 模拟移动端连接信息
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        downlink: 10,
                        rtt: 100
                    })
                });
                
                // 反检测：模拟真实的鼠标和键盘事件
                const originalAddEventListener = EventTarget.prototype.addEventListener;
                EventTarget.prototype.addEventListener = function(type, listener, options) {
                    if (type === 'mousedown' || type === 'mouseup' || type === 'mousemove') {
                        // 模拟真实用户行为
                        setTimeout(() => {
                            originalAddEventListener.call(this, type, listener, options);
                        }, Math.random() * 100);
                    } else {
                        originalAddEventListener.call(this, type, listener, options);
                    }
                };
                
                // 设置移动端视口元标签
                const viewport = document.createElement('meta');
                viewport.name = 'viewport';
                viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(viewport);
            """)
            
            # 设置超时时间
            page.set_default_timeout(settings.screenshot_timeout * 1000)
            
            logger.info(f"正在打开链接: {url}")
            
            # 打开页面
            response = await page.goto(url, wait_until='networkidle')
            
            # 等待页面加载完成
            await page.wait_for_load_state('networkidle')
            
            # 获取页面基本信息
            title = await page.title()
            current_url = page.url
            
            page_info = {
                "success": True,
                "original_url": url,
                "current_url": current_url,
                "title": title,
                "status_code": response.status
            }
            
            logger.info(f"页面加载成功: {title}")
            
            # 暂时不关闭页面，保持打开状态以便后续操作
            
            return page_info
            
        except Exception as e:
            logger.error(f"打开链接失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_url": url
            }
    
    async def take_screenshot(self, page: Page, full_page: bool = True) -> bytes:
        """
        截图页面
        
        Args:
            page: 页面对象
            full_page: 是否全页截图
            
        Returns:
            截图的字节数据
        """
        try:
            return await page.screenshot(full_page=full_page)
        except Exception as e:
            logger.error(f"截图失败: {e}")
            raise
    
    async def take_long_screenshot(self, url: str, output_dir: str = "screenshots") -> Dict[str, Any]:
        """
        对抖音页面进行长截图
        
        Args:
            url: 抖音页面URL
            output_dir: 输出目录
            
        Returns:
            长截图结果信息
        """
        if not self.context:
            raise Exception("浏览器未初始化，请先调用initialize方法")
        
        try:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 创建页面
            page = await self.context.new_page()
            
            # 添加移动端模拟脚本
            await page.add_init_script("""
                // 模拟触摸事件支持
                Object.defineProperty(navigator, 'maxTouchPoints', {
                    get: () => 5
                });
                
                // 模拟移动端屏幕方向
                Object.defineProperty(screen, 'orientation', {
                    get: () => ({
                        angle: 0,
                        type: 'portrait-primary'
                    })
                });
                
                // 模拟移动端连接信息
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        downlink: 10,
                        rtt: 100
                    })
                });
                
                // 设置移动端视口元标签
                const viewport = document.createElement('meta');
                viewport.name = 'viewport';
                viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(viewport);
            """)
            
            # 设置超时时间
            page.set_default_timeout(settings.screenshot_timeout * 1000)
            
            logger.info(f"正在访问长截图URL: {url}")
            
            # 打开页面
            response = await page.goto(url, wait_until='networkidle')
            await page.wait_for_load_state('networkidle')
            
            # 等待页面完全加载，包括动态内容（与成功脚本保持一致）
            await asyncio.sleep(3)
            
            # 尝试滚动触发懒加载 - 使用多种方式，针对正确的滚动容器
            logger.info("尝试触发懒加载...")
            
            # 方法1: 使用JavaScript滚动容器
            await page.evaluate("""
                () => {
                    const scrollContainer = document.querySelector('.detail-container__body') || 
                                          document.querySelector('#container') ||
                                          document.body;
                    scrollContainer.scrollTop = scrollContainer.scrollHeight;
                    if (scrollContainer === document.body) {
                        window.scrollTo(0, document.body.scrollHeight);
                    }
                }
            """)
            await asyncio.sleep(1)
            
            # 方法2: 使用键盘事件
            await page.keyboard.press("End")
            await asyncio.sleep(1)
            
            # 回到顶部
            await page.evaluate("""
                () => {
                    const scrollContainer = document.querySelector('.detail-container__body') || 
                                          document.querySelector('#container') ||
                                          document.body;
                    scrollContainer.scrollTop = 0;
                    if (scrollContainer === document.body) {
                        window.scrollTo(0, 0);
                    }
                }
            """)
            await page.keyboard.press("Home")
            await asyncio.sleep(1)
            
            # 查找主要的滚动容器并获取页面尺寸
            viewport_size = await page.evaluate("""
                () => {
                    // 查找主要的滚动容器
                    const scrollContainer = document.querySelector('.detail-container__body') || 
                                          document.querySelector('#container') ||
                                          document.body;
                    
                    const body = document.body;
                    const html = document.documentElement;
                    
                    return {
                        width: window.innerWidth,
                        height: window.innerHeight,
                        scrollHeight: scrollContainer.scrollHeight,
                        clientHeight: scrollContainer.clientHeight,
                        scrollTop: scrollContainer.scrollTop,
                        bodyScrollHeight: body.scrollHeight,
                        documentScrollHeight: html.scrollHeight,
                        devicePixelRatio: window.devicePixelRatio || 1,
                        containerSelector: scrollContainer.className || scrollContainer.tagName,
                        hasScrollContainer: scrollContainer !== body
                    };
                }
            """)
            
            viewport_height = viewport_size['height']
            scroll_height = viewport_size['scrollHeight']
            client_height = viewport_size['clientHeight']
            device_pixel_ratio = viewport_size['devicePixelRatio']
            has_scroll_container = viewport_size['hasScrollContainer']
            container_selector = viewport_size['containerSelector']
            
            logger.info(f"页面信息: 视口高度={viewport_height}, 容器高度={client_height}, 总滚动高度={scroll_height}")
            logger.info(f"滚动容器: {container_selector}, 是否为内部容器={has_scroll_container}")
            logger.info(f"body高度={viewport_size['bodyScrollHeight']}, document高度={viewport_size['documentScrollHeight']}, 像素比={device_pixel_ratio}")
            
            # 检查是否需要滚动
            if scroll_height <= viewport_height:
                logger.info("页面无需滚动，执行单次截图")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(output_dir, f"douyin_screenshot_{timestamp}.png")
                await page.screenshot(path=output_path)
                
                await page.close()
                return {
                    "success": True,
                    "output_path": output_path,
                    "screenshot_count": 1,
                    "total_height": client_height,
                    "file_size": os.path.getsize(output_path) if os.path.exists(output_path) else 0
                }
            
            # 回到滚动容器顶部 - 使用多种方法确保滚动到顶部
            logger.info("回到滚动容器顶部")
            await page.evaluate("""
                () => {
                    const scrollContainer = document.querySelector('.detail-container__body') || 
                                          document.querySelector('#container') ||
                                          document.body;
                    scrollContainer.scrollTop = 0;
                    if (scrollContainer === document.body) {
                        window.scrollTo({top: 0, behavior: 'smooth'});
                    }
                }
            """)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Home")
            await asyncio.sleep(0.5)
            # 确认回到顶部
            scroll_position = await page.evaluate("""
                () => {
                    const scrollContainer = document.querySelector('.detail-container__body') || 
                                          document.querySelector('#container') ||
                                          document.body;
                    return scrollContainer.scrollTop;
                }
            """)
            logger.info(f"当前滚动容器位置: {scroll_position}")
            
            # 长截图参数（最优配置）
            scroll_step = 500  # 滚动距离
            crop_bottom_pixels = 300  # 底部裁剪像素
            
            logger.info(f"开始长截图: 滚动步长={scroll_step}px, 底部裁剪={crop_bottom_pixels}px")
            
            # 执行长截图
            screenshots = []
            current_scroll = 0
            screenshot_index = 0
            max_scroll_height = scroll_height
            
            while current_scroll < max_scroll_height:
                logger.info(f"截图第 {screenshot_index + 1} 部分，当前滚动位置: {current_scroll}")
                
                # 等待页面稳定
                await asyncio.sleep(0.8)
                
                # 截图当前视窗
                temp_screenshot_path = os.path.join(output_dir, f"debug_screenshot_{screenshot_index:02d}_scroll_{current_scroll}.png")
                await page.screenshot(path=temp_screenshot_path)
                screenshots.append(temp_screenshot_path)
                logger.info(f"保存截图: {temp_screenshot_path}")
                
                # 计算下一次滚动位置
                next_scroll = current_scroll + scroll_step
                
                # 滚动到下一个位置 - 使用容器滚动
                if next_scroll >= max_scroll_height:
                    # 滚动到底部
                    logger.info("滚动到容器底部")
                    await page.evaluate("""
                        () => {
                            const scrollContainer = document.querySelector('.detail-container__body') || 
                                                  document.querySelector('#container') ||
                                                  document.body;
                            scrollContainer.scrollTop = scrollContainer.scrollHeight;
                            if (scrollContainer === document.body) {
                                window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
                            }
                        }
                    """)
                    await asyncio.sleep(0.5)
                    await page.keyboard.press("End")
                    current_scroll = max_scroll_height
                else:
                    # 滚动到指定位置
                    logger.info(f"滚动容器到位置: {next_scroll}")
                    await page.evaluate(f"""
                        () => {{
                            const scrollContainer = document.querySelector('.detail-container__body') || 
                                                  document.querySelector('#container') ||
                                                  document.body;
                            scrollContainer.scrollTop = {next_scroll};
                            if (scrollContainer === document.body) {{
                                window.scrollTo({{top: {next_scroll}, behavior: 'smooth'}});
                            }}
                        }}
                    """)
                    await asyncio.sleep(0.5)
                    # 使用鼠标滚轮辅助滚动
                    await page.mouse.wheel(0, scroll_step // 2)
                    current_scroll = next_scroll
                
                # 等待滚动完成和内容加载
                await asyncio.sleep(1)
                
                # 检查实际滚动位置
                actual_scroll = await page.evaluate("""
                    () => {
                        const scrollContainer = document.querySelector('.detail-container__body') || 
                                              document.querySelector('#container') ||
                                              document.body;
                        return scrollContainer.scrollTop;
                    }
                """)
                logger.info(f"期望滚动位置: {current_scroll}, 实际滚动位置: {actual_scroll}")
                
                # 如果滚动位置差异很大，说明页面可能有特殊的滚动行为
                if abs(actual_scroll - current_scroll) > 50:
                    logger.info(f"滚动位置差异较大，调整当前位置记录")
                    current_scroll = actual_scroll
                
                # 如果连续两次实际滚动位置相同，说明到达底部或无法继续滚动
                if screenshot_index > 0 and actual_scroll > 0:
                    # 检查是否到达底部
                    container_info = await page.evaluate("""
                        () => {
                            const scrollContainer = document.querySelector('.detail-container__body') || 
                                                  document.querySelector('#container') ||
                                                  document.body;
                            return {
                                scrollTop: scrollContainer.scrollTop,
                                scrollHeight: scrollContainer.scrollHeight,
                                clientHeight: scrollContainer.clientHeight,
                                isAtBottom: scrollContainer.scrollTop + scrollContainer.clientHeight >= scrollContainer.scrollHeight - 10
                            };
                        }
                    """)
                    
                    if container_info['isAtBottom']:
                        logger.info("已到达容器底部")
                        break
                
                screenshot_index += 1
                
                # 防止无限循环
                if screenshot_index >= 20:
                    logger.warning("达到最大截图数量限制")
                    break
            
            logger.info(f"总共截取了 {len(screenshots)} 张图片，开始拼接...")
            
            # 生成最终输出路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"douyin_long_screenshot_chrome_{timestamp}.png")
            
            # 拼接图片
            if len(screenshots) == 1:
                # 只有一张图片，直接重命名
                os.rename(screenshots[0], output_path)
                total_height = Image.open(output_path).height
            else:
                # 拼接多张图片
                total_height = await self._stitch_screenshots(screenshots, output_path, crop_bottom_pixels)
            
            # 保留调试截图，不删除临时文件
            logger.info("调试截图已保存，可以逐张检查:")
            for i, temp_file in enumerate(screenshots):
                if os.path.exists(temp_file):
                    logger.info(f"  截图 {i+1}: {temp_file}")
            
            await page.close()
            
            return {
                "success": True,
                "output_path": output_path,
                "screenshot_count": len(screenshots),
                "total_height": total_height,
                "file_size": os.path.getsize(output_path) if os.path.exists(output_path) else 0,
                "original_url": url,
                "current_url": page.url,
                "title": await page.title() if not page.is_closed() else ""
            }
            
        except Exception as e:
            logger.error(f"长截图失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_url": url
            }
    
    async def _stitch_screenshots(self, screenshot_paths: List[str], output_path: str, crop_bottom_pixels: int = 300) -> int:
        """
        拼接多张截图
        
        Args:
            screenshot_paths: 截图文件路径列表
            output_path: 输出文件路径
            crop_bottom_pixels: 底部裁剪像素数
            
        Returns:
            拼接后的总高度
        """
        try:
            logger.info(f"拼接 {len(screenshot_paths)} 张图片，底部裁剪: {crop_bottom_pixels}px...")
            
            # 打开所有图片
            images = []
            for path in screenshot_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    images.append(img)
            
            if not images:
                raise Exception("没有有效的图片可以拼接")
            
            # 计算拼接后的尺寸
            total_width = images[0].width
            if len(images) == 1:
                total_height = images[0].height
            else:
                # 前面的图片去掉底部crop_bottom_pixels，最后一张图片完整保留
                total_height = sum(img.height - crop_bottom_pixels for img in images[:-1]) + images[-1].height
            
            logger.info(f"拼接图片尺寸: {total_width} x {total_height}")
            
            # 创建新的图片
            result_image = Image.new('RGB', (total_width, total_height))
            
            # 拼接图片
            y_offset = 0
            for i, img in enumerate(images):
                if i == len(images) - 1:
                    # 最后一张图片完整保留
                    result_image.paste(img, (0, y_offset))
                    y_offset += img.height
                else:
                    # 前面的图片去掉底部区域
                    if img.height > crop_bottom_pixels:
                        cropped_img = img.crop((0, 0, img.width, img.height - crop_bottom_pixels))
                        result_image.paste(cropped_img, (0, y_offset))
                        y_offset += cropped_img.height
                        cropped_img.close()
                    else:
                        logger.warning(f"图片 {i+1} 高度({img.height})小于裁剪区域({crop_bottom_pixels})，跳过")
                
                img.close()
            
            # 保存拼接后的图片
            result_image.save(output_path, 'PNG', quality=95)
            result_image.close()
            
            logger.info("图片拼接完成")
            return total_height
            
        except Exception as e:
            logger.error(f"图片拼接失败: {e}")
            raise

# 创建全局Chrome服务实例
playwright_chrome_service = PlaywrightChromeService()
