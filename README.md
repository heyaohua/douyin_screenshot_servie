# 抖音长截图服务

一个基于FastAPI和Playwright的抖音长截图服务，支持Firefox和Chrome两种浏览器，具备反检测能力。

## 功能特性

- 🚀 **双浏览器支持**: Firefox和Chrome两种浏览器选择
- 📱 **移动端模拟**: 完美模拟iPhone设备访问
- 🛡️ **反检测机制**: 绕过抖音的自动化检测和验证码
- 📸 **长截图功能**: 自动滚动并拼接完整页面截图
- 🔧 **调试模式**: 保存中间截图便于调试
- 🌐 **API接口**: 提供RESTful API和直接服务调用

## 项目结构

```
douyin_screenshot_service/
├── app/
│   ├── api/           # FastAPI路由
│   ├── core/          # 配置管理
│   ├── models/        # 数据模型
│   ├── services/      # 核心服务
│   │   ├── playwright_service.py      # Firefox服务
│   │   └── playwright_chrome_service.py  # Chrome服务
│   └── main.py        # 主应用
├── tests/             # 测试脚本
├── screenshots/       # 截图输出目录
├── requirements.txt   # 依赖包
└── run.py            # 启动脚本
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器

```bash
playwright install firefox
playwright install chromium
```

### 3. 启动服务

```bash
python run.py
```

### 4. 使用API

```bash
# 长截图接口
curl -X POST "http://localhost:8000/douyin/long-screenshot" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://v.douyin.com/your-video-url/"}'

# 测试接口
curl -X POST "http://localhost:8000/douyin/test-long-screenshot"
```

## 直接使用服务

```python
import asyncio
from app.services.playwright_service import playwright_service
from app.services.playwright_chrome_service import playwright_chrome_service

async def main():
    # Firefox版本
    await playwright_service.initialize()
    result = await playwright_service.take_long_screenshot(
        url="https://v.douyin.com/your-url/",
        output_dir="screenshots"
    )
    await playwright_service.close()
    
    # Chrome版本
    await playwright_chrome_service.initialize()
    result = await playwright_chrome_service.take_long_screenshot(
        url="https://v.douyin.com/your-url/",
        output_dir="screenshots"
    )
    await playwright_chrome_service.close()

asyncio.run(main())
```

## 测试脚本

```bash
# 测试Firefox版本
python tests/test_service.py

# 测试Chrome版本
python tests/test_chrome_service.py
```

## 配置说明

### 环境变量

创建 `.env` 文件：

```env
HEADLESS=False
SCREENSHOT_TIMEOUT=30
```

### 浏览器配置

- **Firefox**: 使用Playwright内置Firefox，稳定可靠
- **Chrome**: 使用系统Chrome浏览器，反检测能力强

## 技术特点

### 反检测机制

- 隐藏自动化特征 (`navigator.webdriver`)
- 模拟真实用户行为
- 使用隐私模式和无痕浏览
- 随机化事件触发时间

### 移动端模拟

- iPhone 12 Pro视口 (390x844)
- 设备像素比 3x
- 触摸事件支持
- 移动端User-Agent

### 长截图算法

- 智能滚动容器检测
- 动态内容懒加载触发
- 精确的图片拼接和裁剪
- 可配置的滚动步长和裁剪像素

## 输出结果

```json
{
  "success": true,
  "output_path": "screenshots/douyin_long_screenshot_20250917_091724.png",
  "screenshot_count": 8,
  "total_height": 18156,
  "file_size": 5652480,
  "original_url": "https://v.douyin.com/your-url/",
  "current_url": "https://haohuo.jinritemai.com/...",
  "title": "页面标题"
}
```

## 注意事项

1. **Chrome兼容性**: 在macOS上建议使用系统Chrome而非Playwright内置版本
2. **网络环境**: 确保网络稳定，避免页面加载超时
3. **资源占用**: 长截图会占用较多内存和存储空间
4. **调试模式**: 开启调试模式会保存中间截图，注意清理

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！