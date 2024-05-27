#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""

        if 'password' in kwargs:
            kwargs['password'] = self.hash_pass(kwargs['password'])
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Password getter."""
        return self._password

    @password.setter
    def password(self, value):
        """Password setter."""
        self._password = self.hash_pass(value)

    def hash_pass(self, password):
        """Hashes a password using md5."""
        return md5(password.encode()).hexdigest()

    def to_dict(self):
        """Overrides the base_model to_dict."""
        new_dict = super().to_dict()
        if models.storage_t == 'db' and 'password' in new_dict:
            new_dict.pop("password", None)
        return new_dict
