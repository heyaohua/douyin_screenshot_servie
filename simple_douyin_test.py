#!/usr/bin/env python3
"""
简化的抖音截图脚本 - 基于成功的Firefox测试
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

class DouyinScreenshot:
    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
    
    async def start_browser(self, headless=False):
        """启动浏览器"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.firefox.launch(headless=headless)
            logger.info("Firefox浏览器启动成功")
            return True
        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            return False
    
    async def create_mobile_context(self):
        """创建移动端浏览器上下文"""
        try:
            # 创建移动端设备上下文（Firefox兼容配置）
            self.context = await self.browser.new_context(
                # iPhone 12 Pro 的视口
                viewport={'width': 390, 'height': 844},
                # 最新的iOS Safari User-Agent
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                # 设备像素比
                device_scale_factor=3,
                # Firefox支持的触摸配置
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
            
            logger.info("移动端浏览器上下文创建成功")
            return True
        except Exception as e:
            logger.error(f"创建移动端上下文失败: {e}")
            return False
    
    async def create_page(self):
        """创建页面"""
        try:
            # 使用移动端上下文创建页面
            self.page = await self.context.new_page()
            
            # 模拟移动端特有的JavaScript API
            await self.page.add_init_script("""
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
            
            logger.info("移动端页面创建成功")
            return True
        except Exception as e:
            logger.error(f"创建页面失败: {e}")
            return False
    
    async def visit_douyin_url(self, url, timeout=30):
        """访问抖音链接"""
        try:
            logger.info(f"正在访问: {url}")
            response = await self.page.goto(url, timeout=timeout*1000, wait_until='networkidle')
            logger.info(f"页面响应状态码: {response.status}")
            
            # 等待页面完全加载
            await self.page.wait_for_load_state('networkidle', timeout=10000)
            
            # 获取页面信息
            title = await self.page.title()
            current_url = self.page.url
            
            result = {
                "success": True,
                "original_url": url,
                "current_url": current_url,
                "title": title,
                "status_code": response.status
            }
            
            logger.info(f"页面加载成功: {title}")
            logger.info(f"重定向到: {current_url}")
            
            return result
            
        except Exception as e:
            logger.error(f"访问页面失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def take_long_screenshot(self, output_path=None):
        """长截图 - 滚动页面并拼接多个截图"""
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # 确保screenshots目录存在
                screenshots_dir = "../screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                output_path = f"{screenshots_dir}/douyin_long_screenshot_{timestamp}.png"
            
            logger.info("开始长截图...")
            
            # 等待页面完全加载，包括动态内容
            logger.info("等待页面动态内容加载...")
            await asyncio.sleep(2)
            
            # 尝试滚动触发懒加载 - 使用多种方式，针对正确的滚动容器
            logger.info("尝试触发懒加载...")
            
            # 方法1: 使用JavaScript滚动容器
            await self.page.evaluate("""
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
            await self.page.keyboard.press("End")
            await asyncio.sleep(1)
            
            # 方法3: 使用鼠标滚轮
            await self.page.mouse.wheel(0, 1000)
            await asyncio.sleep(1)
            
            # 回到顶部
            await self.page.evaluate("""
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
            await self.page.keyboard.press("Home")
            await asyncio.sleep(1)
            
            # 查找主要的滚动容器并获取页面尺寸
            viewport_size = await self.page.evaluate("""
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
            
            # 如果页面不需要滚动，但我们仍然尝试滚动模式以确保捕获动态内容
            if scroll_height <= viewport_height:
                logger.info("页面看起来无需滚动，但仍尝试滚动模式以捕获动态内容")
                # 可以选择直接截图或强制使用滚动模式
                # await self.page.screenshot(path=output_path, full_page=True)
                # return output_path
            
            # 滚动截图
            screenshots = []
            current_scroll = 0
            screenshot_index = 0
            
            # 回到滚动容器顶部 - 使用多种方法确保滚动到顶部
            logger.info("回到滚动容器顶部")
            await self.page.evaluate("""
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
            await self.page.keyboard.press("Home")
            await asyncio.sleep(0.5)
            # 确认回到顶部
            scroll_position = await self.page.evaluate("""
                () => {
                    const scrollContainer = document.querySelector('.detail-container__body') || 
                                          document.querySelector('#container') ||
                                          document.body;
                    return scrollContainer.scrollTop;
                }
            """)
            logger.info(f"当前滚动容器位置: {scroll_position}")
            
            # 使用固定的滚动策略
            actual_scroll_step = 1000  # 固定滚动距离1000px（最优配置）
            crop_bottom_pixels = 300  # 裁剪底部300px（除了最后一张图片）
            max_scroll_height = scroll_height  # 保持原来的最大滚动高度
            
            logger.info(f"滚动策略: 容器高度={client_height}, 滚动步长={actual_scroll_step}, 底部裁剪={crop_bottom_pixels}px")
            
            while current_scroll < max_scroll_height:
                logger.info(f"截图第 {screenshot_index + 1} 部分，当前滚动位置: {current_scroll}")
                
                # 等待页面稳定
                await asyncio.sleep(0.8)
                
                # 截图当前视窗
                temp_screenshot_path = f"{screenshots_dir}/debug_screenshot_{screenshot_index:02d}_scroll_{current_scroll}.png"
                await self.page.screenshot(path=temp_screenshot_path)
                screenshots.append(temp_screenshot_path)
                logger.info(f"保存截图: {temp_screenshot_path}")
                
                # 计算下一次滚动位置 - 使用实际的滚动步长
                next_scroll = current_scroll + actual_scroll_step
                
                # 滚动到下一个位置 - 使用容器滚动
                if next_scroll >= max_scroll_height:
                    # 滚动到底部
                    logger.info("滚动到容器底部")
                    await self.page.evaluate("""
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
                    await self.page.keyboard.press("End")
                    current_scroll = max_scroll_height
                else:
                    # 滚动到指定位置
                    logger.info(f"滚动容器到位置: {next_scroll}")
                    await self.page.evaluate(f"""
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
                    await self.page.mouse.wheel(0, actual_scroll_step // 2)
                    current_scroll = next_scroll
                
                # 等待滚动完成和内容加载
                await asyncio.sleep(1)
                
                # 检查实际滚动位置
                actual_scroll = await self.page.evaluate("""
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
                    container_info = await self.page.evaluate("""
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
                
                # 防止无限循环，最多截取20张图片
                if screenshot_index >= 20:
                    logger.warning("达到最大截图数量限制")
                    break
            
            logger.info(f"总共截取了 {len(screenshots)} 张图片，开始拼接...")
            
            # 拼接图片
            if len(screenshots) == 1:
                # 只有一张图片，直接重命名
                os.rename(screenshots[0], output_path)
            else:
                # 拼接多张图片
                await self.stitch_screenshots(screenshots, output_path, crop_bottom_pixels)
            
            # 保留调试截图，不删除临时文件
            logger.info("调试截图已保存，可以逐张检查:")
            for i, temp_file in enumerate(screenshots):
                if os.path.exists(temp_file):
                    logger.info(f"  截图 {i+1}: {temp_file}")
            # 注释掉删除逻辑，保留调试截图
            # for temp_file in screenshots:
            #     if os.path.exists(temp_file):
            #         os.remove(temp_file)
            
            # 获取文件信息
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"长截图已保存到: {output_path}")
                logger.info(f"文件大小: {file_size} bytes")
            
            return output_path
            
        except Exception as e:
            logger.error(f"长截图失败: {e}")
            return None
    
    async def stitch_screenshots(self, screenshot_paths, output_path, crop_bottom_pixels=90):
        """拼接多张截图，裁剪前面图片的底部区域"""
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
            
            logger.info(f"拼接图片尺寸: {total_width} x {total_height} (原始总高度: {sum(img.height for img in images)})")
            
            # 创建新的图片
            result_image = Image.new('RGB', (total_width, total_height))
            
            # 拼接图片
            y_offset = 0
            for i, img in enumerate(images):
                if i == len(images) - 1:
                    # 最后一张图片完整保留
                    result_image.paste(img, (0, y_offset))
                    y_offset += img.height
                    logger.info(f"图片 {i+1}: 最后一张，完整粘贴，高度: {img.height}")
                else:
                    # 前面的图片去掉底部区域
                    if img.height > crop_bottom_pixels:
                        cropped_img = img.crop((0, 0, img.width, img.height - crop_bottom_pixels))
                        result_image.paste(cropped_img, (0, y_offset))
                        y_offset += cropped_img.height
                        logger.info(f"图片 {i+1}: 去掉底部{crop_bottom_pixels}px，粘贴高度: {cropped_img.height}")
                        cropped_img.close()
                    else:
                        logger.warning(f"图片 {i+1} 高度({img.height})小于裁剪区域({crop_bottom_pixels})，跳过")
            
            # 保存拼接后的图片
            result_image.save(output_path, 'PNG', quality=95)
            logger.info("图片拼接完成")
            
            # 关闭所有图片对象
            for img in images:
                img.close()
            result_image.close()
            
        except Exception as e:
            logger.error(f"图片拼接失败: {e}")
            raise
    
    async def take_screenshot(self, output_path=None, full_page=True):
        """普通截图（兼容旧版本）"""
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # 确保screenshots目录存在
                screenshots_dir = "../screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                output_path = f"{screenshots_dir}/douyin_screenshot_{timestamp}.png"
            
            await self.page.screenshot(path=output_path, full_page=full_page)
            logger.info(f"截图已保存到: {output_path}")
            
            # 获取文件信息
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"截图文件大小: {file_size} bytes")
            
            return output_path
            
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    async def close(self):
        """关闭浏览器"""
        try:
            if self.context:
                await self.context.close()
                logger.info("浏览器上下文已关闭")
            if self.browser:
                await self.browser.close()
                logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")

async def main():
    """主函数"""
    douyin_url = "https://v.douyin.com/Zdo3P7Zv51o/"
    
    logger.info("=" * 60)
    logger.info("开始抖音长截图服务测试")
    logger.info("=" * 60)
    
    screenshot_service = DouyinScreenshot()
    
    try:
        # 启动浏览器（设置为False可以看到浏览器界面）
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
            logger.info("页面访问成功，开始长截图...")
            
            # 等待一下让页面内容完全加载
            await asyncio.sleep(3)
            
            # 长截图
            screenshot_path = await screenshot_service.take_long_screenshot()
            
            if screenshot_path:
                logger.info("=" * 60)
                logger.info("长截图测试完成！")
                logger.info(f"原始链接: {result['original_url']}")
                logger.info(f"重定向链接: {result['current_url']}")
                logger.info(f"页面标题: {result.get('title', '无标题')}")
                logger.info(f"长截图文件: {screenshot_path}")
                logger.info("=" * 60)
            else:
                logger.error("长截图失败")
        else:
            logger.error(f"页面访问失败: {result.get('error')}")
    
    finally:
        await screenshot_service.close()

if __name__ == "__main__":
    asyncio.run(main())
