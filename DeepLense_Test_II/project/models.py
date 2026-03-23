from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional
from datetime import datetime

class SimulationRequest(BaseModel):
    """Parameters for a gravitational lensing simulation."""

    sim_profile: Literal["model_i", "model_ii"] = Field(
        default="model_i",
        description=(
            "model_i: 150x150, Gaussian PSF, Sersic source (DeepLense Model_I). "
            "model_ii: 64x64 Euclid-style, magnitude Sersic source (DeepLense Model_II)."
        ),
    )
    substructure_type: Literal["no_sub", "cdm", "axion"] = Field(description="Type of dark matter substructure")
    num_images: int = Field(default=5, ge=1, le=100, description="Number of images to generate")
    halo_mass: float = Field(default=1e12, description="Main halo mass in solar masses")
    z_halo: float = Field(default=0.5, ge=0.1, le=2.0, description="Redshift of the lens (dark matter halo)")
    z_gal: float = Field(default=1.0, ge=0.1, le=5.0, description="Redshift of the source galaxy")
    axion_mass: Optional[float] = Field(default=None, description="Axion particle mass in eV (required for axion/vortex)")

    @model_validator(mode='after')
    def validate_physics(self):
        if self.z_gal <= self.z_halo:
            raise ValueError(f"z_gal ({self.z_gal}) must be > z_halo ({self.z_halo})")
        
        if self.substructure_type == 'axion' and self.axion_mass is None:
            raise ValueError("axion_mass is required for axion substructure")
        
        return self
    
class SimulationMetadata(BaseModel):
    """Metadata for a completed simulation."""
    sim_profile: str
    substructure_type: str
    num_images: int
    halo_mass: float
    z_halo: float
    z_gal: float
    image_shape: tuple
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class SimulationResult(BaseModel):
    """Result of a simulation run."""
    image_paths: list[str]
    metadata: SimulationMetadata

    class Config:
        arbitrary_types_allowed=True
