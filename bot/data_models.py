from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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
