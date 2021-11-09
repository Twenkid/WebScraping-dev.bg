from datetime import datetime

from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey, UnicodeText,
)
from sqlalchemy.dialects.mysql.base import LONGTEXT

from . import Base


class Website(Base):
    __tablename__ = 'websites'

    id = Column(
        Integer,
        primary_key=True
    )
    url = Column(
        Text(),
        nullable=False
    )
    data = Column(
        LONGTEXT(),
        nullable=False,
    )
    created = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    last_updated = Column(
        DateTime,
        nullable=False
    )


class Category(Base):
    __tablename__ = 'categories'

    id = Column(
        Integer,
        primary_key=True
    )
    website_id = Column(
        Integer,
        ForeignKey('websites.id')
    )
    category_name = Column(
        Text(),
        nullable=False,
    )
    category_url = Column(
        Text(),
        nullable=False,
    )


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(
        Integer,
        primary_key=True
    )
    category_id = Column(
        Integer,
        ForeignKey('categories.id')
    )
    job_name = Column(
        Text(),
        nullable=False,
    )
    job_url = Column(
        Text(),
        nullable=False,
    )


class JobListing(Base):
    __tablename__ = 'job_listings'

    id = Column(
        Integer,
        primary_key=True
    )
    job_id = Column(
        Integer,
        ForeignKey('jobs.id')
    )
    listing_name = Column(
        Text(),
        nullable=False,
    )
    listing_url = Column(
        Text(),
        nullable=False,
    )
    listing_data = Column(
        Text(),
        nullable=False
    )
