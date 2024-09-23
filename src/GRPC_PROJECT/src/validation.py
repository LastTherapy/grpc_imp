from pydantic import BaseModel, Field, ValidationError,field_validator, model_validator
from typing import Optional, List

class Officer(BaseModel):
    first_name: str
    last_name: str
    rank: str


class Spaceship(BaseModel):
    class_: str = Field(alias="class")
    alignment: str
    name: str
    length: float = Field(..., gt=0)
    crew_size: int = Field(..., gt=0)
    armed: bool
    officers: Optional[List[Officer]] = []

    @field_validator('length')
    def validate_length(cls, v, info):

        ship_type = info.data.get("class_")
        ship_length = {
            "CORVETTE": (80, 250),
            "FRIGATE": (300, 600),
            "CRUISER": (500, 1000),
            "DESTROYER": (800, 2000),
            "CARRIER": (1000, 4000),
            "DREADNOUGHT": (5000, 20000)
        }
        if ship_type in ship_length:
            min_length, max_length = ship_length[ship_type]
            if min_length <= v <= max_length:
                return v
            else:
                raise ValidationError
        else:
            raise ValidationError

    @field_validator('crew_size')
    def validate_crew(cls, v, info):
        ship_type = info.data.get("class_")
        ship_length = {
            "CORVETTE": (4, 10),
            "FRIGATE": (10, 15),
            "CRUISER": (15, 30),
            "DESTROYER": (50, 80),
            "CARRIER": (120, 250),
            "DREADNOUGHT": (300, 500)
        }
        if ship_type in ship_length:
            min_length, max_length = ship_length[ship_type]
            if min_length <= v <= max_length:
                return v
            else:
                raise ValidationError
        else:
            raise ValidationError
    # #
    @field_validator('armed')
    def validate_armed(cls, v, info):
        ship_type = info.data.get("class_")
        ship_length = {
            "CORVETTE": True,
            "FRIGATE": True,
            "CRUISER": True,
            "DESTROYER": True,
            "CARRIER": False,
            "DREADNOUGHT": True
        }
        if ship_length[ship_type] == v:
            return v
        else:
            raise ValidationError

    # # # # alignment
    @field_validator('alignment')
    def validation_enemy(cls, v, info):
        ship_type = info.data.get("class_")
        ship_length = {
            "CORVETTE": True,
            "FRIGATE": False,
            "CRUISER": True,
            "DESTROYER": False,
            "CARRIER": True,
            "DREADNOUGHT": True
        }
        if v == "ENEMY":
            if ship_type not in ship_length:
                raise ValidationError(f"Unknown ship type: {ship_type}")
            if not ship_length[ship_type]:
                raise ValidationError(f"Ship type {ship_type} cannot have alignment 'ENEMY'")
        return v

    @field_validator('name')
    def validation_ship_name(cls, v, info):
        alignment_type: str = info.data.get("alignment")
        if alignment_type == "ALLY" and v == "Unknown":
            raise ValidationError
        else:
            return v

if __name__ == "__main__":
    spaceship_dict = {
        "class": "CORVETTE",
        "alignment": "ENEMY",
        "name": "Dark Shadow",
        "length": 200.0,
        "crew_size": 8,
        "armed": True,
        "officers": []
    }

    ship = Spaceship(**spaceship_dict)
    print(ship)