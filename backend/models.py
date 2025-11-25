from typing import Optional
import datetime

from sqlalchemy import Float, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Food(Base):
    __tablename__ = 'Food'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Consumption: Mapped[list['Consumption']] = relationship('Consumption', back_populates='food')
    Nutritional_values: Mapped[list['NutritionalValues']] = relationship('NutritionalValues', back_populates='food')


class Meal(Base):
    __tablename__ = 'Meal'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    water_intake: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Consumption: Mapped[list['Consumption']] = relationship('Consumption', back_populates='meal')


class Patient(Base):
    __tablename__ = 'Patient'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(255))
    daily_caloric_intake: Mapped[Optional[int]] = mapped_column(Integer)
    physical_activity_level: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    BMI: Mapped[list['BMI']] = relationship('BMI', back_populates='patient')
    Disease: Mapped[list['Disease']] = relationship('Disease', back_populates='patient')


class BMI(Base):
    __tablename__ = 'BMI'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['Patient.id'], ondelete='CASCADE', name='bmi_ibfk_1'),
        Index('patient_id', 'patient_id')
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    score: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    patient: Mapped['Patient'] = relationship('Patient', back_populates='BMI')


class Consumption(Base):
    __tablename__ = 'Consumption'
    __table_args__ = (
        ForeignKeyConstraint(['food_id'], ['Food.id'], ondelete='CASCADE', name='consumption_ibfk_2'),
        ForeignKeyConstraint(['meal_id'], ['Meal.id'], ondelete='CASCADE', name='consumption_ibfk_1'),
        Index('food_id', 'food_id'),
        Index('meal_id', 'meal_id')
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    meal_id: Mapped[str] = mapped_column(String(36), nullable=False)
    food_id: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    food: Mapped['Food'] = relationship('Food', back_populates='Consumption')
    meal: Mapped['Meal'] = relationship('Meal', back_populates='Consumption')


class Disease(Base):
    __tablename__ = 'Disease'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['Patient.id'], ondelete='CASCADE', name='disease_ibfk_1'),
        Index('patient_id', 'patient_id')
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    patient: Mapped['Patient'] = relationship('Patient', back_populates='Disease')


class NutritionalValues(Base):
    __tablename__ = 'Nutritional_values'
    __table_args__ = (
        ForeignKeyConstraint(['food_id'], ['Food.id'], ondelete='CASCADE', name='nutritional_values_ibfk_1'),
        Index('food_id', 'food_id')
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    food_id: Mapped[str] = mapped_column(String(36), nullable=False)
    calories: Mapped[Optional[float]] = mapped_column(Float)
    protein: Mapped[Optional[float]] = mapped_column(Float)
    carbohydrates: Mapped[Optional[float]] = mapped_column(Float)
    fat: Mapped[Optional[float]] = mapped_column(Float)
    fiber: Mapped[Optional[float]] = mapped_column(Float)
    sugars: Mapped[Optional[float]] = mapped_column(Float)
    sodium: Mapped[Optional[float]] = mapped_column(Float)
    cholesterol: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    food: Mapped['Food'] = relationship('Food', back_populates='Nutritional_values')
