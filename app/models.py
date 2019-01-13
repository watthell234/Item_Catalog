# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Categories():
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(80), nullable=False)


class Items():
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    description = Column(String(80))


engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
