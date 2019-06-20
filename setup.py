"""
Setup
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sap_explainable_ai',
    version='0.0.1',
    packages=setuptools.find_packages(include=['xai*']),
    author="SAP",
    url="https://github.wdf.sap.corp/ML-Leonardo/Explainable_AI",
    description="Explainable AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'xai': 'xai'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Explainable AI',
        'Topic :: Software Development :: XAI'
    ]
)