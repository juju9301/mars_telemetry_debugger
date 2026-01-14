from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TelemetryPacket(BaseModel):
    'Represents a single telemetry packet from the Mars rover'

    timestamp: datetime = Field(
        ..., description='Earth UTC timestamp when the packet was generated or received'
    )
    sol: int = Field(
        ..., ge=0, description='Martial solar day since landing'
    )
    battery_level: float = Field(
        ..., ge=0.0, le=100.0, description='Battery level percentage' 
    )
    wheel_torque: List[float] = Field(
        ...,
        min_items=4,
        max_items=6,
        description='Torque values for each wheel in Nm' 

    )
    temperature_internal: float = Field(
        ..., description='Internal rover temperature, in degrees Celcius'
    )

    temperature_external: float = Field(
        ..., description='External environment temperature, in degrees Celcius'
    )
    radiation_level: float = Field(
        ..., ge=0.0, description='Radiation level'
    )

    gps_lat: float = Field(
        ..., ge=-90.0, le=90.0, description='Latitude on Mars in degrees'
    )
    gps_lon: float = Field(
        ..., ge=-180.0, le=180.0, description='Longitude on Mars in degrees'
    )

    error_flags: List[Literal['OK', 'WARN', 'ERROR']] = Field(
        default_factory=lambda:['OK'],
        description='List of error states for this packet.'
    )

    note: Optional[str] = Field(
        default=None,
        description='Optional human-readable note'
    )
