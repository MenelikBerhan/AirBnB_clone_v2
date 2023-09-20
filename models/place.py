#!/usr/bin/env python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id', ondelete='cascade'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id', ondelete='cascade'),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan')
        amenities = relationship(
            'Amenity', secondary=place_amenity,
            back_populates='place_amenities', viewonly=False)
    else:
        @property
        def reviews(self):
            """returns the list of `Review` instances with `place_id` equals
            to the current Place.id"""
            from models import storage
            from models.review import Review
            return [review for review in storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """returns the list of 'Amenity' instances
            based on the attribute"""
            from models import storage
            from models.amenity import Amenity
            return [amenity for amenity in storage.all(Amenity).values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, amenity=None):
            from models.amenity import Amenity
            """Appends amenity ids to the attribute"""
            if type(amenity) is Amenity and amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)
