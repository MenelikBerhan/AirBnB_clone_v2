#!/usr/bin/env python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Serves as the blueprint for future amenities"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
        "Place", secondary=place_amenity, back_populates="amenities")
