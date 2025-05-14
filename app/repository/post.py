from typing import Optional, Tuple
from uuid import UUID

from sqlalchemy import Select, asc, delete, desc, func, select
from sqlalchemy.orm import joinedload

from app.models.post import ActivityCategoryPost, Post
from app.repository.base import BaseRepository
from app.schemas.post import PostCreate, PostFilter, PostPagination, PostSort


class PostRepository(BaseRepository):
    model = Post

    async def count(self, query: Select) -> int:
        """
        Count the number of records that match the query.
        """
        count_query = select(func.count()).select_from(query.subquery())
        result = await self.async_session.execute(count_query)
        return result.scalar_one()

    def _apply_filters(self, query: Select, filters: PostFilter):
        """Apply filters to the query."""
        if filters.title:
            query = query.where(Post.title.ilike(f"%{filters.title}%"))
        if filters.description:
            query = query.where(Post.description.ilike(f"%{filters.description}%"))
        if filters.min_price is not None:
            query = query.where(Post.service_price >= filters.min_price)
        if filters.max_price is not None:
            query = query.where(Post.service_price <= filters.max_price)
        if filters.service_type:
            query = query.where(Post.service_type == filters.service_type)
        if filters.user_id:
            query = query.where(Post.user_id == filters.user_id)
        if filters.min_views is not None:
            query = query.where(Post.number_of_views >= filters.min_views)
        if filters.max_views is not None:
            query = query.where(Post.number_of_views <= filters.max_views)
        if filters.created_after:
            query = query.where(Post.created_at >= filters.created_after)
        if filters.created_before:
            query = query.where(Post.created_at <= filters.created_before)
        if filters.category_ids:
            query = query.join(ActivityCategoryPost).where(
                ActivityCategoryPost.category_id.in_(filters.category_ids)
            )
        return query

    def _apply_sorting(self, query, sort: Optional[PostSort]):
        """Apply sorting to the query."""
        if sort:
            field = getattr(Post, sort.field)
            query = query.order_by(desc(field) if sort.order == "desc" else asc(field))
        return query

    def _apply_pagination(self, query, pagination: Optional[PostPagination]):
        """Apply pagination to the query."""
        if pagination:
            offset = (pagination.page - 1) * pagination.per_page
            query = query.offset(offset).limit(pagination.per_page)
        return query

    async def get_posts(
        self,
        filters: Optional[PostFilter] = None,
        sort: Optional[PostSort] = None,
        pagination: Optional[PostPagination] = None,
    ) -> Tuple[list[Post], int]:
        """
        Get posts with filtering, sorting, and pagination.
        Returns a tuple of (posts, total_count).
        """
        # Base query with relationships
        query = select(Post).options(
            joinedload(Post.categories).joinedload(ActivityCategoryPost.category),
            joinedload(Post.user),
        )

        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)

        # Get total count before pagination
        count_query = select(Post)
        if filters:
            count_query = self._apply_filters(count_query, filters)
        total_count = await self.count(count_query)

        # Apply sorting and pagination
        query = self._apply_sorting(query, sort)
        query = self._apply_pagination(query, pagination)

        # Execute query
        posts = await self.get_many(query)
        return posts, total_count

    async def get_post_by_id(
        self, post_id: UUID, with_user: bool = False, increment_views: bool = False
    ) -> Optional[Post]:
        query = select(Post).where(Post.id == post_id)
        query = query.options(
            joinedload(Post.categories).joinedload(ActivityCategoryPost.category)
        )
        if with_user:
            query = query.options(joinedload(Post.user))
        post: Post = await self.get_instance(query)
        if increment_views:
            post.number_of_views += 1
            await self.save(post)

        return post

    async def get_user_posts(
        self,
        user_id: UUID,
    ) -> list[Post]:
        query = (
            select(Post)
            .where(Post.user_id == user_id)
            .options(
                joinedload(Post.categories).joinedload(ActivityCategoryPost.category),
                joinedload(Post.user),
            )
        )

        return await self.get_many(query)

    async def create_post(self, post_data: PostCreate) -> Post:
        post = await self.create(post_data)
        return post

    async def delete_post(self, post_id: UUID) -> bool:
        return await self.delete(post_id)

    async def clean_activity_categories(self, post_id: UUID) -> None:
        await self.async_session.execute(
            delete(ActivityCategoryPost).where(ActivityCategoryPost.post_id == post_id)
        )
        await self.async_session.commit()
        self.async_session.expire_all()
