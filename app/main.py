from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import douyin
from app.services.playwright_service import playwright_service

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    logger.info("正在启动抖音长截图服务...")
    await playwright_service.initialize()
    yield
    # 关闭时清理
    logger.info("正在关闭抖音长截图服务...")
    await playwright_service.close()

app = FastAPI(
    title="抖音长截图服务",
    description="提供抖音视频长截图功能的API服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(douyin.router)

@app.get("/")
async def root():
    return {"message": "抖音长截图服务运行中"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
