import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from sqladmin import Admin

from app.admin import (
    ActivityCategoryAdmin,
    ActivityCategoryUserAdmin,
    ChatConversationAdmin,
    ChatMessageAdmin,
    PostAdmin,
    TransactionAdmin,
    UserAdmin,
    UserVerificationAdmin,
)
from app.api.endpoints import router
from app.config.logs.log_config import LOGGING_CONFIG
from app.config.settings.base import settings
from app.core.database import engine

# Set up logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(title="Mentorship App")

# Admin
admin = Admin(app=app, engine=engine)
admin.add_view(UserAdmin)
admin.add_view(UserVerificationAdmin)
admin.add_view(ActivityCategoryAdmin)
admin.add_view(ActivityCategoryUserAdmin)
admin.add_view(ChatConversationAdmin)
admin.add_view(ChatMessageAdmin)
admin.add_view(PostAdmin)
admin.add_view(TransactionAdmin)

app.include_router(router)

# Enable pagination in the app
add_pagination(app)
disable_installed_extensions_check()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)
