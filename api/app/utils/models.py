from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from utils.database import Base

class UserType(Base):
    __tablename__ = "user_type"
    __table_args__ = {'schema': 'pharmaguide'}

    id = Column(Integer, primary_key=True, index=True)
    user_type = Column(String(32), nullable=False)
    users = relationship("User", back_populates="user_type")


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'schema': 'pharmaguide'}

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(25))
    email = Column(String(52))
    type = Column(Integer, ForeignKey("pharmaguide.user_type.id"))
    user_type = relationship("UserType", back_populates="users")

    pharmacy = relationship("Pharmacy", back_populates="user")


class Pharmacy(Base):
    __tablename__ = "pharmacy"
    __table_args__ = { 'schema' : 'pharmaguide' }

    pharmacy_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100))
    lat = Column(DECIMAL)
    lng = Column(DECIMAL)
    contact = Column(String(50))
    owner = Column(Integer, ForeignKey('pharmaguide.user.user_id'))

    images = relationship("PharmacyImage", back_populates="pharmacy")
    user = relationship("User", back_populates="pharmacy")


class PharmacyImage(Base):
    __tablename__ = "pharmacy_image"
    __table_args__ = { 'schema' : 'pharmaguide' }

    name = Column(String(44), primary_key=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmaguide.pharmacy.pharmacy_id'))

    pharmacy = relationship("Pharmacy", back_populates="images")
    

class Category(Base):
    __tablename__ = 'category_name'
    __table_args__ = { 'schema' : 'pharmaguide' }

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = { 'schema' : 'pharmaguide' }

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), nullable=False)
    code = Column(String(12), nullable=False)
    description = Column(String(200))


class ProductCategory(Base):
    __tablename__ = 'product_category'
    __table_args__ = { 'schema' : 'pharmaguide' }

    product_id = Column(Integer, ForeignKey('pharmaguide.product.product_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('pharmaguide.category_name.category_id'), primary_key=True)


class ProductImage(Base):
    __tablename__ = 'product_image'
    __table_args__ = { 'schema' : 'pharmaguide' }

    name = Column(String(44), primary_key=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmaguide.product.product_id'))


class Inventory(Base):
    __tablename__ = 'inventory'
    __table_args__ = { 'schema' : 'pharmaguide' }

    product_id = Column(Integer, ForeignKey('pharmaguide.product.product_id'), primary_key=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmaguide.pharmacy.pharmacy_id'), primary_key=True)
    price = Column(DECIMAL, nullable=False)
    stock = Column(Integer)


class Advertisement(Base):
    __tablename__ = 'advertisement'
    __table_args__ = { 'schema' : 'pharmaguide' }

    advertisement_id = Column(Integer, nullable=False, primary_key=True, index=True)
    advertisement_title = Column(String(25), nullable=False)
    advertisement_description = Column(String(50), nullable=False)
    advertisement_image = Column(String(50), nullable=False)
    owner = Column(Integer, ForeignKey('pharmaguide.user.user_id'))
