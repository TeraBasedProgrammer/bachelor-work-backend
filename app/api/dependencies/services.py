from fastapi import Depends

from app.api.dependencies.repository import get_repository
from app.repository.activity_category import ActivityCategoryRepository
from app.repository.post import PostRepository
from app.repository.user import UserRepository
from app.repository.user_verification import UserVerificationRepository
from app.services.activity_category import ActivityCategoryService
from app.services.billing import BillingService
from app.services.post import PostService
from app.services.user import UserService
from app.services.user_verification import UserVerificationService


def get_user_service(
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> UserService:
    service = UserService(user_repository)
    return service


def get_activity_category_service(
    activity_category_repository: ActivityCategoryRepository = Depends(
        get_repository(ActivityCategoryRepository)
    ),
) -> ActivityCategoryService:
    service = ActivityCategoryService(activity_category_repository)
    return service


def get_billing_service(
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> BillingService:
    service = BillingService(user_repository)
    return service


def get_verification_service(
    verification_repository: UserVerificationRepository = Depends(
        get_repository(UserVerificationRepository)
    ),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> UserVerificationService:
    service = UserVerificationService(verification_repository, user_repository)
    return service


def get_post_service(
    post_repository: PostRepository = Depends(get_repository(PostRepository)),
) -> PostService:
    service = PostService(post_repository)
    return service
