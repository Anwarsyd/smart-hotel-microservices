from fastapi import Request
import logging
import time

logger = logging.getLogger("api_gateway")

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} completed in {process_time:.2f}s")
    return response
