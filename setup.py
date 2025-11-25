from setuptools import find_packages, setup
import os

# Define the project name and version
PROJECT_NAME = 'Home_Price_Prediction_AI'
VERSION = '0.0.1'
AUTHOR = 'Your Name'
EMAIL = 'your.email@example.com'

# Helper function to read dependencies from requirements.txt
def get_requirements(file_path: str) -> list[str]:
    '''
    Reads the list of packages required for the project from the requirements.txt file.
    It removes newline characters and the editable install marker (-e .).
    '''
    requirements = []
    
    # Check if the file exists before attempting to read
    if not os.path.exists(file_path):
        print(f"Warning: requirements file not found at {file_path}")
        return requirements

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        
        # Clean up the list
        requirements = [req.replace("\n", "") for req in requirements]
        
        # Remove the editable install flag if present
        if '-e .' in requirements:
            requirements.remove('-e .')
            
    return requirements

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description='End-to-end ML project for unbiased home price prediction.',
    packages=find_packages(), # CRUCIAL: This automatically finds the 'house_price_prediction' folder
    long_description="Refer to the README for project details.",
    # This line is essential for automated dependency installation
    install_requires=get_requirements('requirements.txt') 
)