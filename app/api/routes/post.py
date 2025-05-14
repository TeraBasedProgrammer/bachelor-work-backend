from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth import auth_wrapper
from app.api.dependencies.services import get_post_service
from app.api.dependencies.user import get_current_user
from app.models.user import User
from app.schemas.post import (
    PaginatedResponse,
    PostCreate,
    PostFilter,
    PostPagination,
    PostSchema,
    PostSort,
    PostUpdate,
)
from app.services.post import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PaginatedResponse)
async def get_all_posts(
    _: Annotated[User, Depends(auth_wrapper)],
    post_service: PostService = Depends(get_post_service),
    # Filter parameters
    title: Optional[str] = Query(
        None, description="Filter by title (case-insensitive)"
    ),
    description: Optional[str] = Query(
        None, description="Filter by description (case-insensitive)"
    ),
    min_price: Optional[float] = Query(None, description="Minimum service price"),
    max_price: Optional[float] = Query(None, description="Maximum service price"),
    service_type: Optional[str] = Query(None, description="Service type (S or P)"),
    category_ids: Optional[list[UUID]] = Query(
        None, description="Filter by category IDs"
    ),
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    min_views: Optional[int] = Query(None, description="Minimum number of views"),
    max_views: Optional[int] = Query(None, description="Maximum number of views"),
    created_after: Optional[datetime] = Query(
        None, description="Filter posts created after this date"
    ),
    created_before: Optional[datetime] = Query(
        None, description="Filter posts created before this date"
    ),
    # Sort parameters
    sort_field: Optional[str] = Query(
        "created_at",
        description="Field to sort by (title, service_price, number_of_views, created_at)",
    ),
    sort_order: Optional[str] = Query(
        "desc",
        description="Sort order (asc or desc)",
    ),
    # Pagination parameters
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
):
    """
    Get all posts with filtering, sorting, and pagination.
    """
    # Build filter
    filters = PostFilter(
        title=title,
        description=description,
        min_price=min_price,
        max_price=max_price,
        service_type=service_type,
        category_ids=category_ids,
        user_id=user_id,
        min_views=min_views,
        max_views=max_views,
        created_after=created_after,
        created_before=created_before,
    )

    # Build sort
    sort = PostSort(
        field=sort_field,
        order=sort_order,
    )

    # Build pagination
    pagination = PostPagination(
        page=page,
        per_page=per_page,
    )

    # Get posts
    posts, total_count = await post_service.get_posts(filters, sort, pagination)

    # Calculate total pages
    total_pages = (total_count + per_page - 1) // per_page

    return PaginatedResponse(
        items=posts,
        total=total_count,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: UUID,
    increment_views: bool = False,
    post_service: PostService = Depends(get_post_service),
):
    """
    Get a specific post by ID.
    """
    return await post_service.get_post(
        post_id, with_user=True, increment_views=increment_views
    )


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
