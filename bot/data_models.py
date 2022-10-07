from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

# API DATA MODELS
class Locations(BaseModel):
    ENUS:str = Field(default=None, alias='EN-US')
    DEDE:str = Field(default=None,alias='DE-DE')
    FRFR:str = Field(default=None,alias='FR-FR')
    RURU:str = Field(default=None,alias='RU-RU')
    PLPL:str = Field(default=None,alias='PL-PL')
    ESES:str = Field(default=None,alias='ES-ES')
    PTBR:str = Field(default=None,alias='PT-BR')
    ITIT:str = Field(default=None,alias='IT-IT')
    ZHCN:str = Field(default=None,alias='ZH-CN')
    KOKR:str = Field(default=None,alias='KO-KR')
    JAJP:str = Field(default=None,alias='JA-JP')

    class Config:
        allow_population_by_field_name = True

class Item(BaseModel):
    LocalizationNameVariable: str
    LocalizationDescriptionVariable: str
    LocalizedNames: Optional[Locations] = None
    LocalizedDescriptions: Optional[Locations] = None
    Index: int
    UniqueName: str
    score: Optional[float] = None

class Price(BaseModel):
    item_id: str
    city: str
    quality: int
    sell_price_min: int
    sell_price_min_date: datetime
    sell_price_max: int
    sell_price_max_date: datetime
    buy_price_min: int
    buy_price_min_date: datetime
    buy_price_max: int
    buy_price_max_date: datetime

class Guild(BaseModel):
    Id: str
    Name: str

class Player(BaseModel):
    Id: str
    Name: str

# DATABASE DATA MODELS
Base = declarative_base()

class Servers(Base):
    __tablename__ = "servers"
    server_id = Column(Integer, primary_key=True)
    server_name = Column(String)
    owner_id = Column(Integer)
    owner_name = Column(String)
    permissions = relationship("Permited", backref=backref("servers"))

class Roles(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String)

class Permited(Base):
    __tablename__ = "permited"
    member_id = Column(Integer, primary_key=True)
    member_name = Column(String)
    server_id = Column(Integer, ForeignKey("servers.server_id"))
    role_id = Column(Integer, ForeignKey("roles.role_id"))

class AlbionGuilds(Base):
    __tablename__ = "albion_guilds"
    guild_id = Column(String, primary_key=True)
    guild_name = Column(String)
    server_id = Column(Integer, ForeignKey("servers.server_id"))

# class Members(Base):
#     __tablename__ = "members"
#     member_id = Column(Integer, primary_key=True)
#     # member_name = Column(String)
#     # member_nick = Column(String)
#     server_id = Column(Integer, ForeignKey("servers.server_id"))
#     role_id = Column(Integer, ForeignKey("roles.role_id"))

# class Guilds(Base):
#     __tablename__ = "guilds"
#     guild_id = Column(String, primary_key=True)
#     guild_name = Column(String)
#     server_id = Column(Integer, ForeignKey("servers.server_id"))
    # players = relationship("Players", backref=backref("guilds"))

# class Players(Base):
#     __tablename__ = "players"
#     player_id = Column(String, primary_key=True)
#     player_name = Column(String)
#     guild_id = Column(String, ForeignKey("guilds.guild_id"))
#     taxes = relationship("Taxes", backref=backref("players"))

# class Taxes(Base):
#     __tablename__ = "taxes"
#     tax_id = Column(Integer, primary_key=True)
#     player_id = Column(String, ForeignKey("players.player_id"))
#     silver = Column(Integer)
#     ref = Column(Date)