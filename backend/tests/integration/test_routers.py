# backend/tests/unit/test_routers.py
import pytest
from fastapi import FastAPI, APIRouter


class TestRouters:
    """Tests for API routers."""
    
    def test_router_creation(self):
        """Test creating a router."""
        router = APIRouter()
        assert router is not None
        assert isinstance(router, APIRouter)
    
    def test_router_add_route(self):
        """Test adding route to router."""
        router = APIRouter()
        
        @router.get("/test")
        async def test_endpoint():
            return {"message": "test"}
        
        assert len(router.routes) == 1
        assert router.routes[0].path == "/test"
        assert router.routes[0].methods == {"GET"}
    
    def test_router_add_post_route(self):
        """Test adding POST route to router."""
        router = APIRouter()
        
        @router.post("/moods")
        async def create_mood():
            return {"status": "created"}
        
        assert len(router.routes) == 1
        assert router.routes[0].path == "/moods"
        assert "POST" in router.routes[0].methods
    
    def test_app_creation(self):
        """Test creating FastAPI app."""
        app = FastAPI()
        assert app is not None
        assert isinstance(app, FastAPI)
    
    def test_app_add_router(self):
        """Test adding router to app."""
        app = FastAPI()
        router = APIRouter()
        
        @router.get("/test")
        async def test():
            return {"test": True}
        
        app.include_router(router, prefix="/api/v1")
        
        # Проверяем, что маршрут добавлен
        routes = [route.path for route in app.routes]
        assert any("/api/v1/test" in route for route in routes)
    
    def test_router_with_tags(self):
        """Test router with tags."""
        router = APIRouter(tags=["moods"])
        
        @router.get("/")
        async def get_moods():
            return []
        
        assert router.tags == ["moods"]
    
    def test_router_responses(self):
        """Test router with response model."""
        router = APIRouter()
        
        @router.get("/health", status_code=200)
        async def health_check():
            return {"status": "ok"}
        
        assert router.routes[0].status_code == 200