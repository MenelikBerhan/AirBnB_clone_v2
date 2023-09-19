#!/usr/bin/env python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Serves as the blueprint for future amenities"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
