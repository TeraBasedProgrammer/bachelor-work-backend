from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from app.models.post import ActivityCategoryPost, Post
from app.repository.base import BaseRepository
from app.schemas.post import PostCreate


class PostRepository(BaseRepository):
    model = Post

    async def get_posts(self) -> list[Post]:
        return await self.get_many(
            select(Post).options(
                joinedload(Post.categories).joinedload(ActivityCategoryPost.category)
            )
        )

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
        self, user_id: UUID, with_user: bool = False
    ) -> list[Post]:
        query = (
            select(Post)
            .where(Post.user_id == user_id)
            .options(
                joinedload(Post.categories).joinedload(ActivityCategoryPost.category)
            )
        )
        if with_user:
            query = query.options(joinedload(Post.user))
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
