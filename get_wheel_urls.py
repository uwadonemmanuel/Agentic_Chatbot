#!/usr/bin/env python3
"""Get direct download URLs for missing packages from PyPI"""

import json
import urllib.request
import ssl

# Create SSL context that doesn't verify (for getting URLs only)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

packages = {
    'numpy': '2.3.4',
    'faiss-cpu': '1.12.0',
    'pandas': '2.3.3',
    'pyarrow': '21.0.0',  # Required by streamlit
    'streamlit': None,  # Will get latest
    'tavily-python': None,  # Will get latest
    'langchain-community': None,  # Will get latest
}

def get_wheel_url(package_name, version=None):
    """Get the wheel URL for a package from PyPI"""
    try:
        if version:
            url = f"https://pypi.org/pypi/{package_name}/{version}/json"
        else:
            url = f"https://pypi.org/pypi/{package_name}/json"
        
        print(f"Fetching info for {package_name}...")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        # Find the right wheel file for Python 3.13 on macOS x86_64
        wheels = []
        for file_info in data.get('urls', []):
            if file_info.get('packagetype') == 'bdist_wheel':
                filename = file_info.get('filename', '')
                if 'cp313' in filename and 'macosx' in filename and 'x86_64' in filename:
                    wheels.append({
                        'filename': filename,
                        'url': file_info.get('url'),
                        'size': file_info.get('size', 0)
                    })
        
        if wheels:
            # Return the first match (usually there's only one)
            wheel = wheels[0]
            size_mb = wheel['size'] / (1024 * 1024)
            return {
                'package': package_name,
                'filename': wheel['filename'],
                'url': wheel['url'],
                'size_mb': f"{size_mb:.1f} MB"
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching {package_name}: {e}")
        return None

print("=" * 70)
print("PYPI WHEEL DOWNLOAD URLs")
print("=" * 70)
print()

results = []
for pkg, version in packages.items():
    result = get_wheel_url(pkg, version)
    if result:
        results.append(result)
    print()

print("\n" + "=" * 70)
print("DOWNLOAD INSTRUCTIONS")
print("=" * 70)
print("\n1. Download these files in your browser (right-click, Save As):\n")
for r in results:
    print(f"   {r['filename']} ({r['size_mb']})")
    print(f"   URL: {r['url']}")
    print()

print("\n2. Save all files to: downloads/")
print("\n3. Run: ./install_from_local.sh")
print("\n" + "=" * 70)

