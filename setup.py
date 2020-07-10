from setuptools import setup, find_packages

setup(
    name = 'intake-acclat',
    version = '0.0.1',
    packages = find_packages(),
    entry_points = {
        'intake.drivers': [
            'local-acclat = intake_acclat.intake_acclat:LocalAccLat',
            'acclatsource = intake_acclat.source.AccLat:AccLatSource',      
        ]
    },
    include_package_data = True,
    install_requires = ['intake'],
    zip_safe=False
)