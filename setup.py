from setuptools import find_packages, setup

setup(
    name="intake-acclat",
    version="0.0.1",
    py_modules=["intake_acclat"],
    packages=find_packages(),
    entry_points={
        "intake.drivers": [
            "local-acclat = intake_acclat.intake_acclat:LocalAccLat",
            "acclatsource = intake_acclat.source.AccLat:AccLatSource",
        ]
    },
    include_package_data=True,
    install_requires=["intake"],
    zip_safe=False,
)
