import numpy as np
import os
from datetime import datetime
from models import SimulationRequest, SimulationResult, SimulationMetadata

class LensingSimulator:
    """Wraps DeepLenseSim to run simulations from validated requests."""
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir

    def simulate(self, request: SimulationRequest) -> SimulationResult:
        """Run simulation based on a validated SimulationRequest."""
        from deeplense.lens import DeepLens

        os.makedirs(self.output_dir, exist_ok=True)

        # Log parameters for debugging
        print(f"[SIM] Parameters received:")
        print(f"  sim_profile = {request.sim_profile}")
        print(f"  substructure_type = {request.substructure_type}")
        print(f"  num_images = {request.num_images}")
        print(f"  halo_mass = {request.halo_mass:.2e}")
        print(f"  z_halo = {request.z_halo}")
        print(f"  z_gal = {request.z_gal}")
        print(f"  axion_mass = {request.axion_mass}")

        image_paths = []

        for i in range(request.num_images):
            dl = DeepLens(
                z_halo=request.z_halo,
                z_gal=request.z_gal,
                axion_mass=request.axion_mass
            )
            dl.make_single_halo(request.halo_mass)

            if request.substructure_type == "no_sub":
                dl.make_no_sub()
            elif request.substructure_type == "cdm":
                dl.make_old_cdm()
            elif request.substructure_type == "axion":
                dl.make_vortex(vort_mass=1e10)

            if request.sim_profile == "model_i":
                dl.make_source_light()
                dl.simple_sim()
            elif request.sim_profile == "model_ii":
                dl.set_instrument("euclid")
                dl.make_source_light_mag()
                dl.simple_sim_2()
            else:
                raise ValueError(f"Unknown sim_profile: {request.sim_profile}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{request.sim_profile}_{request.substructure_type}_{timestamp}_{i}.npy"
            path = os.path.join(self.output_dir, filename)
            np.save(path, dl.image_real)
            image_paths.append(path)

        metadata = SimulationMetadata(
            sim_profile=request.sim_profile,
            substructure_type=request.substructure_type,
            num_images=request.num_images,
            halo_mass=request.halo_mass,
            z_halo=request.z_halo,
            z_gal=request.z_gal,
            image_shape=dl.image_real.shape,
        )

        return SimulationResult(image_paths=image_paths, metadata=metadata)
