from setuptools import find_packages, setup


setup(
    name="bounded-mdl-residue-test",
    version="0.2.0",
    description="Deterministic multi-agent MDL communication analysis framework",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
)
