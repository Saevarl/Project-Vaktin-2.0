import datetime
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class GPU(Base):
    __tablename__ = 'gpus'

    id = Column(Integer, primary_key=True)
    model = Column(String(100), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    brand = Column(String(50), nullable=True)
    series = Column(String(50), nullable=True)
    vram = Column(String(20), nullable=True)
    link = Column(String(255), nullable=True)

    # One-to-many relationship with Prices
    prices = relationship("Price", back_populates="gpu")

    def __repr__(self):
        return f"<GPU(name={self.name}, model={self.model}, manufacturer={self.manufacturer}, brand={self.brand}, series={self.series}, vram={self.vram})>"

class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    website_url = Column(String(255), nullable=True)
    logo_url = Column(String(255), nullable=True)

    # One-to-many relationship with Prices
    prices = relationship("Price", back_populates="store")

    def __repr__(self):
        return f"<Store(name={self.name}, website_url={self.website_url})>"


class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    gpu_id = Column(Integer, ForeignKey('gpus.id'), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    price = Column(DECIMAL(10, 3), nullable=False)
    date_checked = Column(Date, nullable=False, default=datetime.datetime.now)

    # Relationships
    gpu = relationship("GPU", back_populates="prices")
    store = relationship("Store", back_populates="prices")

    def __repr__(self):
        return f"<Price(gpu_id={self.gpu_id}, store_id={self.store_id}, price={self.price}, date_checked={self.date_checked})>"
