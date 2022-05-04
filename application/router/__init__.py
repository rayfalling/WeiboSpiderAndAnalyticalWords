from .user import user_router
from .admin import admin_router
from .search import search_router
from .detail import detail_router
from .word_cloud import word_cloud_router
from .user_activity import user_activity_router

__all__ = (
    "user_router", "admin_router", "search_router", "detail_router", "word_cloud_router", "user_activity_router",
)
