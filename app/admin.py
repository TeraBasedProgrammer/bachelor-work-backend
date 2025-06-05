from sqladmin import ModelView

from app.models.chat import ChatConversation, ChatMessage
from app.models.invoice import LessonInvoice
from app.models.payment import Transaction
from app.models.post import ActivityCategoryPost, Post
from app.models.user import (
    ActivityCategory,
    ActivityCategoryUser,
    User,
    UserVerification,
)


class UserAdmin(ModelView, model=User):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class UserVerificationAdmin(ModelView, model=UserVerification):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ActivityCategoryAdmin(ModelView, model=ActivityCategory):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ActivityCategoryUserAdmin(ModelView, model=ActivityCategoryUser):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ChatConversationAdmin(ModelView, model=ChatConversation):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ChatMessageAdmin(ModelView, model=ChatMessage):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class PostAdmin(ModelView, model=Post):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ActivityCategoryPostAdmin(ModelView, model=ActivityCategoryPost):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class TransactionAdmin(ModelView, model=Transaction):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class InvoiceAdmin(ModelView, model=LessonInvoice):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
