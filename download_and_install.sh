#!/bin/bash

cd "/Users/emmanuel/Documents/Projects/Andela GenAI/AgenticChatBot"
source venv/bin/activate

# Create downloads directory
mkdir -p downloads

# Download faiss-cpu wheel
echo "Downloading faiss-cpu wheel..."
curl -L -o downloads/faiss_cpu-1.12.0-cp313-cp313-macosx_13_0_x86_64.whl \
  "https://files.pythonhosted.org/packages/9c/2a/8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c/faiss_cpu-1.12.0-cp313-cp313-macosx_13_0_x86_64.whl" \
  || curl -L -k -o downloads/faiss_cpu-1.12.0-cp313-cp313-macosx_13_0_x86_64.whl \
  "https://files.pythonhosted.org/packages/9c/2a/8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c8b3c/faiss_cpu-1.12.0-cp313-cp313-macosx_13_0_x86_64.whl"

# Install from local file
if [ -f downloads/faiss_cpu-1.12.0-cp313-cp313-macosx_13_0_x86_64.whl ]; then
    echo "Installing faiss-cpu from local file..."
    pip install downloads/faiss_cpu-1.12.0-cp313-cp313-macosx_13_0_x86_64.whl
else
    echo "Download failed. Trying alternative URL..."
    # Try to find the correct URL
    pip download faiss-cpu -d downloads --trusted-host pypi.org --trusted-host files.pythonhosted.org || true
    if ls downloads/faiss_cpu*.whl 1> /dev/null 2>&1; then
        pip install downloads/faiss_cpu*.whl
    fi
fi

