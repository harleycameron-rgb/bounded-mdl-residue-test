from setuptools import find_packages, setup


setup(
    name="bounded-mdl-residue-test",
    version="0.2.0",
    description="Deterministic multi-agent MDL communication analysis framework",
    packages=find_packages(include=["REFERENCE_IMPLEMENTATION", "REFERENCE_IMPLEMENTATION.*", "multi_agent", "multi_agent.*", "analysis", "analysis.*", "tests", "tests.*"]),
    include_package_data=True,
)
