import json

from pydantic_ai import Agent, RunContext
from models import SimulationRequest
from sim_wrapper import LensingSimulator

# The agent
agent = Agent(
    "groq:llama-3.3-70b-versatile",
    system_prompt="""
        You are a gravitational lensing simulation assistant for the DeepLens project.

        You help researchers generate strong gravitational lensing images using DeepLensSim.

        Two simulation pipelines (pick sim_profile explicitly or infer from user):
        - sim_profile "model_i": 150x150 pixels, Gaussian PSF, analytic Sersic source (classic DeepLense Model_I).
        - sim_profile "model_ii": 64x64 Euclid-style survey, magnitude-based Sersic source (DeepLense Model_II).

        Other parameters:
        - substructure_type: "no_sub" (smooth), "cdm" (cold dark matter subhalos), or "axion" (vortex)
        - num_images: 1-100 (default: 5)
        - halo_mass: main lens mass in solar masses (default: 1e12)
        - z_halo: lens redshift 0.1-2.0 (default: 0.5)
        - z_gal: source redshift, must be > z_halo (default: 1.0)
        - axion_mass: required for axion (e.g., 1e-22 eV)

        Human-in-the-loop workflow:
        1) If substructure_type, sim_profile, or axion_mass (when needed) is missing, ASK concise follow-up questions.
        2) Call prepare_simulation_plan to show a JSON plan; ask the user to confirm (e.g. "yes", "proceed").
        3) Only after explicit confirmation, call simulate_lensing with the same parameters.
        - If the user already gave full explicit parameters and said run/execute, you may skip re-asking but still
          briefly restate the plan once before simulate_lensing.
        """,
    output_type=str,
)

simulator = LensingSimulator(output_dir="outputs")

@agent.tool
async def prepare_simulation_plan(
    ctx: RunContext,
    sim_profile: str,
    substructure_type: str,
    num_images: int = 5,
    halo_mass: float = 1e12,
    z_halo: float = 0.5,
    z_gal: float = 1.0,
    axion_mass: float | None = None,
) -> str:
    """Validate parameters and return a JSON plan for user review before running simulate_lensing."""
    try:
        request = SimulationRequest(
            sim_profile=sim_profile,  # type: ignore[arg-type]
            substructure_type=substructure_type,
            num_images=num_images,
            halo_mass=halo_mass,
            z_halo=z_halo,
            z_gal=z_gal,
            axion_mass=axion_mass,
        )
    except ValueError as e:
        return f"Invalid parameters: {e}. Please fix and try again."
    plan = request.model_dump(mode="json")
    return (
        "Proposed simulation (JSON). Ask the user to confirm before calling simulate_lensing.\n"
        + json.dumps(plan, indent=2)
    )


@agent.tool
async def simulate_lensing(
    ctx: RunContext,
    sim_profile: str,
    substructure_type: str,
    num_images: int = 5,
    halo_mass: float = 1e12,  # ensure this default is here
    z_halo: float = 0.5,
    z_gal: float = 1.0,
    axion_mass: float | None = None,
) -> str:
    """Run a gravitational lensing simulation (after user confirmed the plan).

    sim_profile must be "model_i" or "model_ii".

    IMPORTANT parameter constraints:
    - halo_mass: must be between 1e10 and 1e14 solar masses. Default 1e12.
    - z_halo: lens redshift, 0.1-2.0. Default 0.5.
    - z_gal: source redshift, must be > z_halo. Default 1.0.
    - substructure_type: one of "no_sub", "cdm", "axion"
    - If unsure about values, USE THE DEFAULTS.
    """
    try:
        request = SimulationRequest(
            sim_profile=sim_profile,  # type: ignore[arg-type]
            substructure_type=substructure_type,
            num_images=num_images,
            halo_mass=halo_mass,
            z_halo=z_halo,
            z_gal=z_gal,
            axion_mass=axion_mass,
        )
    except ValueError as e:
        return f"Invalid parameters: {e}. Please fix and try again."

    result = simulator.simulate(request)
    structured = result.model_dump(mode="json")
    return (
        f"Simulation complete!\n"
        f"Profile: {result.metadata.sim_profile}\n"
        f"Generated {result.metadata.num_images} images\n"
        f"Type: {result.metadata.substructure_type}\n"
        f"Shape: {result.metadata.image_shape}\n"
        f"Saved to: {', '.join(result.image_paths)}\n\n"
        f"Structured result (JSON):\n{json.dumps(structured, indent=2)}"
    )

@agent.tool
async def list_available_models(ctx: RunContext) -> str:
    """List available simulation configurations."""
    return """
    Available configurations:

    1. Model_I (simple_sim): 150x150 pixles, Gaussian PSF, SNR ~25
        - Source: Sersic light profile
        - Substructure: no_sub, cdm, axion
    
    2. Model_II (simple_sim_2): 64x64 pixles, Euclid instrument
        - Source: Sersic with magnitude
        - Requires: set_instrument('euclid')
    
    Substructure types:
    - no_sub: Smooth mass distribution, no dark matter clumps
    - cdm: Cold dark matter with point-mass subhalos (drawn from mass function)
    - axion: Vortex substructure from ultralight axion dark matter
    """

@agent.tool
async def validate_parameters(
    ctx: RunContext,
    sim_profile: str,
    z_halo: float,
    z_gal: float,
    substructure_type: str,
    axion_mass: float | None = None,
) -> str:
    """Validate simulation parameters before running."""
    issues = []

    if sim_profile not in ["model_i", "model_ii"]:
        issues.append(f"sim_profile must be 'model_i' or 'model_ii', got: {sim_profile}")

    if z_gal <= z_halo:
        issues.append(f"z_gal ({z_gal}) must be > z_halo ({z_halo})")

    if substructure_type not in ["no_sub", "cdm", "axion"]:
        issues.append(f"Invalid substructure type: {substructure_type}")

    if substructure_type == "axion" and axion_mass is None:
        issues.append("axion_mass is required for axion substructure")

    if issues:
        return "Validation failed:\n" + "\n".join(f"- {i}" for i in issues)

    return "All parameters valid"
