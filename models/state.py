#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities_states = relationship('City', backref='state',
                                 cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """returns the list of City instances with state_id equals
        to the current State.id
        """
        return [city for city in models.storage.all(City).values()
                if city.state_id == self.id]
