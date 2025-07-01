---
page_type: sample
languages:
  - python
name: Python quickstart for Azure AI Search
products:
  - azure
  - azure-cognitive-search
description: |
  Learn how to create, load, and query an Azure AI Search index using Python.
urlFragment: python-quickstart
---

# Python quickstart for Azure AI Search

![Flask sample MIT license badge](https://img.shields.io/badge/license-MIT-green.svg)

Demonstrates using Python and the Azure SDK for Python to create an Azure AI Search index, load it with documents, and execute a few queries. The index is modeled on a subset of the Hotels dataset, reduced for readability and comprehension. Index definition and documents are included in the code.

This sample is a Jupyter Python3 .ipynb file to perform the actions against the Azure AI Search service.

## Prerequisites

* Visual Studio Code with the Python extension (or equivalent tool), with Python 3.10 or later

* [azure-search-documents package](https://pypi.org/project/azure-search-documents/) from the Azure SDK for Python

## Set up the sample

1. Clone or download this sample repository.

1. Extract contents if the download is a zip file. Make sure the files are read-write.

1. Install the required dependencies:
   ```bash
   pip install azure-search-documents python-dotenv
   ```

## Configure your environment

1. **Option 1: Use the setup script (Recommended)**
   ```bash
   cd Quickstart
   python setup_environment.py
   ```
   This will create a `.env` file from `sample.env` and guide you through the configuration.

1. **Option 2: Manual setup**
   - Copy `sample.env` to `.env`
   - Edit `.env` with your actual Azure Search service details:
     - `SEARCH-ENDPOINT`: Your Azure Search service endpoint (e.g., `https://your-service-name.search.windows.net`)
     - `SEARCH-API-KEY`: Your Azure Search service admin API key

## Run the sample

1. Open the `azure-search-quickstart.ipynb` file in Visual Studio Code or Jupyter.

1. Run each cell in sequence. The notebook will automatically load your environment variables from the `.env` file.

## Troubleshooting

If you encounter connection errors:
- Verify your Azure Search service is running
- Check that your endpoint URL is correct (should end with `.search.windows.net`)
- Ensure your API key is valid and has admin permissions
- Run `python setup_environment.py` to validate your configuration

## Next steps

You can learn more about Azure AI Search on the [official documentation site](https://learn.microsoft.com/azure/search).
