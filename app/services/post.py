from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status

from app.models.post import ActivityCategoryPost, Post
from app.repository.post import PostRepository
from app.schemas.post import PostCreate, PostSchema, PostUpdate


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def get_posts(self) -> list[PostSchema]:
        """
        Get all posts.
        """
        posts = await self.repository.get_posts()
        return [PostSchema.from_model(post) for post in posts]

    async def get_post(
        self, post_id: UUID, with_user: bool = False, increment_views: bool = False
    ) -> Optional[Post]:
        """
        Get a specific post by ID.
        """
        post = await self.repository.get_post_by_id(post_id, with_user, increment_views)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        return PostSchema.from_model(post)

    async def get_user_posts(self, user_id: UUID) -> list[Post]:
        """
        Get all posts for a specific user.
        """
        posts = await self.repository.get_user_posts(user_id)
        return [PostSchema.from_model(post) for post in posts]

    async def create_post(self, post_data: PostCreate, user_id: UUID) -> Post:
        """
        Create a new post.
        """

        post_activity_categories_ids = post_data.category_ids
        post_data.category_ids = None

        post_data.user_id = user_id
        new_post = Post(
            title=post_data.title,
            description=post_data.description,
            service_price=post_data.service_price,
            service_type=post_data.service_type,
            user_id=user_id,
        )
        await self.repository.save(new_post)

        post_activity_categories = [
            ActivityCategoryPost(
                post_id=new_post.id,
                category_id=category_id,
            )
            for category_id in post_activity_categories_ids
        ]

        new_post_refreshed = await self.repository.get_post_by_id(new_post.id)
        await self.repository.save_many(post_activity_categories)
        return new_post_refreshed

    async def update_post(
        self, post_id: UUID, post_data: PostUpdate, user_id: UUID
    ) -> Post:
        """
        Update a post.
        """
        post = await self.repository.get_post_by_id(post_id)
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post",
            )

        if post_data.category_ids:
            await self.repository.clean_activity_categories(post_id)

            new_activity_categories = [
                ActivityCategoryPost(post_id=post_id, category_id=category_id)
                for category_id in post_data.category_ids
            ]

            await self.repository.save_many(new_activity_categories)
            post_data.category_ids = None

        await self.repository.update(post_id, post_data)
        updated_post = await self.repository.get_post_by_id(post_id)
        return PostSchema.from_model(updated_post)

    async def delete_post(self, post_id: UUID, user_id: UUID) -> bool:
        """
        Delete a post.
        """
        post = await self.get_post(post_id)
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post",
            )

        return await self.repository.delete_post(post_id)
