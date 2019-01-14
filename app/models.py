# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(80), nullable=False)

    # @property
    # def serialize(self):
    #     return {
    #         'category_name': self.category_name,
    #         'id': self.id
    #     }


class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    team_name = Column(String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    team_details = Column(String(256))

    # @property
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'item_name': self.item_name,
    #         'category_id': self.category_id,
    #         'team_details': self.details
    #     }

#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     email = Column(String(250), nullable=False)
#     picture = Column(String(250))


engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
