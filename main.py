from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4

app = FastAPI()

# post model

class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


posts = []


def search_post(id: str):
    post_lambda = filter(lambda post: post.id == id, posts)
    try:
        return list(post_lambda)[0]
    except:
        return {'error': 'User not found'}


@app.get('/')
def read_root():
    return {'welcome': 'Welcome to my REST_API'}


@app.get('/posts')
def get_posts():
    return posts


@app.get('/posts/{post_id}')
def get_post(post_id: str):
    return search_post(post_id)


@app.post('/posts')
def save_posts(post: Post):
    post.id = str(uuid4())
    posts.append(post)
    return post


@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post.id == post_id:
            del posts[index]  # <---- Manera 1 de eliminar por indice
            # posts.pop(index) # <---- Manera 2 de eliminar por indice
            return {'message': 'Usuario eliminado con exito'}
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='No se ha podido eliminar el usuario')


@app.put('/posts')
def update_post(updatedPost: Post):
    found = False
    for index, post in enumerate(posts):
        if post.id == updatedPost.id:
            posts[index] = updatedPost
            found = True
            return {'message': 'Usuario modificado con exito'}, updatedPost
    if not found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Usuario no encontrado')

