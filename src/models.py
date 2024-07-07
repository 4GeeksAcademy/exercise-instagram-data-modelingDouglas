import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    correo = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

    posts = relationship('Post', backref='usuario', lazy=True)
    comentarios = relationship('Comentario', backref='usuario', lazy=True)
    likes = relationship('Like', backref='usuario', lazy=True)
    following = relationship('Follower', foreign_keys='Follower.seguidor_id', backref='seguidor', lazy=True)
    followers = relationship('Follower', foreign_keys='Follower.seguido_id', backref='seguido', lazy=True)

class Comentario(Base):
    __tablename__ = 'comentario'

    id_comentario = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    texto = Column(String(250), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    caption = Column(String)
    image_url = Column(String(250), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

    comentarios = relationship('Comentario', backref='post', lazy=True)
    likes = relationship('Like', backref='post', lazy=True)

    def to_dict(self):
        return {}

class Follower(Base):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)
    seguidor_id = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    seguido_id = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
