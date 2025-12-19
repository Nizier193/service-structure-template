import time
import uuid
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from core.logger import set_request_id

logger = logging.getLogger(__name__)


class TracingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.service_name = "backend-api"
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = self.generate_request_id()
        
        request.state.request_id = request_id
        set_request_id(request_id)
        
        self.log_request_start(
            request=request,
            request_id=request_id
        )
        
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time

        response = self.add_tracing_headers(
            response=response,
            request_id=request_id,
            duration=duration
        )
        self.log_request_end(
            request=request,
            response=response,
            request_id=request_id,
            duration=duration
        )
        
        return response
    
    def generate_request_id(self) -> str:
        unique_id = str(uuid.uuid4())
        return unique_id
    
    def log_request_start(self, request: Request, request_id: str):
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        logger.info(
            f"→ START {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_host": client_host,
                "user_agent": user_agent,
                "service": self.service_name
            }
        )
    
    def log_request_end(
        self,
        request: Request,
        response: Response,
        request_id: str,
        duration: float
    ):
        status_code = response.status_code
        
        log_level = self.get_log_level(status_code)
        
        logger.log(
            log_level,
            f"← END {request.method} {request.url.path} | "
            f"Status: {status_code} | Duration: {duration:.3f}s",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration": duration,
                "service": self.service_name
            }
        )
    
    def add_tracing_headers(
        self,
        response: Response,
        request_id: str,
        duration: float
    ) -> Response:
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration:.3f}"
        response.headers["X-Service-Name"] = self.service_name
        
        return response
    
    def get_log_level(self, status_code: int) -> int:
        if status_code >= 500:
            return logging.ERROR
        elif status_code >= 400:
            return logging.WARNING
        else:
            return logging.INFO

