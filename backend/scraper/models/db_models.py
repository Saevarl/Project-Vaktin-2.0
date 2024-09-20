import datetime
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class GPUModel(Base):
    __tablename__ = 'gpu_models'

    id = Column(Integer, primary_key=True)
    model = Column(String(100), nullable=False)
    brand = Column(String(50), nullable=True)
    series = Column(String(50), nullable=True)
    vram = Column(String(20), nullable=True)
    benchmark_score = Column(Integer, nullable=True)

    # One-to-many relationship with GPUs
    gpus = relationship("GPU", back_populates="model")

    def __repr__(self):
        return f"<GPUModel(model={self.model}, manufacturer={self.manufacturer}, brand={self.brand}, series={self.series}, vram={self.vram}, benchmark_score={self.benchmark_score})>"

class GPU(Base):
    __tablename__ = 'gpus'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    manufacturer = Column(String(50), nullable=False)
    link = Column(String(255), nullable=True)
    model_id = Column(Integer, ForeignKey('gpu_models.id'), nullable=False)

    # Many-to-one relationship with GPUModel
    model = relationship("GPUModel", back_populates="gpus")
    # One-to-many relationship with Prices
    prices = relationship("Price", back_populates="gpu")

    def __repr__(self):
        return f"<GPU(name={self.name}, link={self.link})>"

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