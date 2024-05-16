# grab_package_versions.py

import subprocess
import sys

# Method to fetch package versions
def fetch_package_versions(packages):
    package_versions = {}
    for package in packages:
        try:
            # Use pip show command to get package information
            result = subprocess.run([sys.executable, '-m', 'pip', 'show', package], capture_output=True, text=True)
            output = result.stdout
            # Parse output to extract version
            version = next(line.split(': ')[1].strip() for line in output.split('\n') if line.startswith('Version: '))
            package_versions[package] = version
        except Exception as e:
            package_versions[package] = "Not installed"
    return package_versions

# List of packages you want to get versions for
packages_to_check = ['requests', 'beautifulsoup4', 'tk']

# Fetch versions for the specified packages
package_versions = fetch_package_versions(packages_to_check)

# Write package versions to a file
with open('python_package_versions.txt', 'w') as file:
    for package, version in package_versions.items():
        file.write(f"{package}: {version}\n")

print("Package versions have been written to package_versions.txt")
