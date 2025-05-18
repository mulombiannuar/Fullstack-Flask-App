from application import db
from application.models.post import Post
from sqlalchemy.exc import SQLAlchemyError
from slugify import slugify

class PostService:
    
    @staticmethod
    def generate_post_slug(title):
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        # Check if slug already exists
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug
    
    
    @staticmethod
    def get_all_posts():
        try:
            return Post.query.order_by(Post.created_at.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error geting posts: {str(e)}")
            return None
        
    
    
    @staticmethod
    def get_posts_by_user_id(user_id):
        try:
            return Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error geting user posts: {str(e)}")
            return None
    
    
    
    @staticmethod
    def create_post(data):
       
        try:
            post = Post(
                title=data['title'],
                content=data['content'],
                post_image=data['post_image'],
                slug=PostService.generate_post_slug(data['title'])
            )
            db.session.add(post)
            db.session.commit()
            return post
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating post: {str(e)}")
      
            return None
        
    @staticmethod
    def get_post_by_id(post_id):
        try:
            return Post.query.get(post_id)
        except SQLAlchemyError as e:
            print(f"Error fetching post: {str(e)}")
            return None
        
        
        
    @staticmethod
    def update_post(post_id, data):
        try:
            post = Post.query.get(post_id)
            if not post:
                return None

            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            post.post_image = data.get('post_image', post.post_image)
            post.slug = PostService.generate_post_slug(data['title'])

            db.session.commit()
            return post
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating post: {str(e)}")
            return None


    @staticmethod
    def delete_post(post_id):
        try:
            post = Post.query.get(post_id)
            if not post:
                return False
            
            db.session.delete(post)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting post: {str(e)}")
            return False
        
        
        
    

    