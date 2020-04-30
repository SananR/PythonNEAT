import setuptools

#pypi-AgENdGVzdC5weXBpLm9yZwIkMzdiN2Y3MzAtZGZjNC00ODk0LTk3ZTYtN2U0NTU2YjM2NzgzAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiAW5WQhlug-vlYTMHpuFRmzNFjsifNGaJ0QowuQqvYg2w

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonneat-SananR", # Replace with your own username
    version="2.3.8",
    author="Sanan Rao",
    author_email="raosanan@gmail.com",
    description="An implementation for NEAT (Neuroevolution of Augmenting Topologies) By Stanley O. Brian",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SananR/PythonNEAT.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)