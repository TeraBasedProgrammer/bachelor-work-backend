from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import auth_wrapper
from app.api.dependencies.services import get_post_service
from app.api.dependencies.user import get_current_user
from app.models.user import User
from app.schemas.post import PostCreate, PostSchema, PostUpdate
from app.services.post import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostSchema])
async def get_all_posts(
    _: Annotated[User, Depends(auth_wrapper)],
    post_service: PostService = Depends(get_post_service),
):
    """
    Get all posts.
    """
    return await post_service.get_posts()


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: UUID,
    increment_views: bool = False,
    post_service: PostService = Depends(get_post_service),
):
    """
    Get a specific post by ID.
    """
    return await post_service.get_post(post_id, increment_views)


@router.get("/user/{user_id}", response_model=list[PostSchema])
async def get_user_posts(
    user_id: str,
    post_service: PostService = Depends(get_post_service),
):
    """
    Get all posts for a specific user.
    """
    return await post_service.get_user_posts(user_id)


@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new post.
    """
    return await post_service.create_post(post_data, current_user.id)


@router.put("/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: UUID,
    post_data: PostUpdate,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    """
    Update a post.
    """
    return await post_service.update_post(post_id, post_data, current_user.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: UUID,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a post.
    """
    await post_service.delete_post(post_id, current_user.id)
