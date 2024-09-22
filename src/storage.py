from typing import List

import sqlalchemy
from sqlalchemy import select, func
from sqlalchemy import create_engine, Integer, String, Boolean, ForeignKey, Table, Column, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Session
import argparse

from src import reporting_pb2


class Base(DeclarativeBase):
    pass


# note (from documentation
# for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
spaceship_officer = Table(
    "spaceship_officer",
    Base.metadata,
    Column("spaceship_id", ForeignKey("spaceship.id"), primary_key=True),
    Column("officer_id", ForeignKey("officer.id"), primary_key=True)
)


class Officer(Base):
    __tablename__ = "officer"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    rank: Mapped[str] = mapped_column(String(50))

    __table_args__ = (UniqueConstraint('first_name', 'last_name', 'rank', name='_officer_unique'),)

    def __repr__(self) -> str:
        return f"Officer(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, rank={self.rank})"


class Spaceship(Base):
    __tablename__ = "spaceship"

    id: Mapped[int] = mapped_column(primary_key=True)
    alignment: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    class_: Mapped[str] = mapped_column(String(50))
    length: Mapped[float] = mapped_column(Integer())
    crew_size: Mapped[int] = mapped_column(Integer())
    armed: Mapped[bool] = mapped_column(Boolean())
    officers: Mapped[List[Officer]] = relationship(secondary=spaceship_officer)

    def __repr__(self) -> str:
        return f"Spaceship(id={self.id}, name={self.name}, length={self.length}, crew_size={self.crew_size}, armed={self.armed}, officers={self.officers})"


url = sqlalchemy.engine.url.URL.create(drivername="",
                                       username="", password="",
                                       database="", host="localhost", port=5432)

engine = create_engine(url, echo=False)
Base.metadata.create_all(engine)


def get_officer(officer_dict) -> Officer:
    with Session(engine) as session:
        stmt = select(Officer).where(
            (Officer.first_name == officer_dict.get("first_name")) &
            (Officer.last_name == officer_dict.get("last_name")) &
            (Officer.rank == officer_dict.get("rank"))
        )

        if result := session.scalars(stmt).first():
            print("Officer found in database")
            print(result)
            return result
        else:
            return Officer(
                first_name=officer_dict.get("first_name"),
                last_name=officer_dict.get("last_name"),
                rank=officer_dict.get("rank")
            )


def grpc_to_orm(spaceship_dict) -> Spaceship:
    return Spaceship(
        alignment=spaceship_dict.get("alignment"),
        name=spaceship_dict.get("name"),
        class_=spaceship_dict.get("class"),
        length=spaceship_dict.get("length"),
        crew_size=spaceship_dict.get("crew_size"),
        armed=spaceship_dict.get("armed"),
        # check traitors
        officers=[get_officer(officer) for officer in spaceship_dict.get("officers")]
    )


def save_ship(grpc_spaceship: reporting_pb2.Spaceship) -> None:
    try:
        with Session(engine) as session:
            orm_spaceship: Spaceship = grpc_to_orm(grpc_spaceship)
            print(orm_spaceship)
            session.add(orm_spaceship)
            session.commit()
    except Exception as e:
        print("Error while saving spaceship")
        print(e)


def find_traitors():
    stmt = (select(Officer)
            .join(spaceship_officer, Officer.id == spaceship_officer.c.officer_id)
            .join(Spaceship, Spaceship.id == spaceship_officer.c.spaceship_id)
            .group_by(Officer.id)
            .having(func.count(func.distinct(Spaceship.alignment)) > 1)
    )
    with Session(engine) as session:
        result = session.scalars(stmt).all()
        for officer in result:
            print(officer)