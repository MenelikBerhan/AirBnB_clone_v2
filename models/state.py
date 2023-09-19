#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state', order_by='City.id',
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """returns the list of `City` instances with `state_id` equals
            to the current State.id"""
            from models import storage
            from models.city import City
            return [city for city in storage.all(City).values()
                    if city.state_id == self.id]
