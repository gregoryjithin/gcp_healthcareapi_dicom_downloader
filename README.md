# DICOM Downloader

This project provides a graphical user interface (GUI) for downloading DICOM files from a Google Cloud Healthcare API. The GUI allows users to specify the service account JSON path, DICOM store URL, study ID, and output folder path. The download progress is displayed using a progress bar, and log messages are shown in a text widget.

## Features

- Browse and select the service account JSON file.
- Enter the DICOM store URL.
- Enter the study ID.
- Browse and select the output folder path.
- Display download progress using a progress bar.
- Log messages in a text widget.

## Requirements

- Python 3.x
- `requests` library
- `google-auth` library
- `tkinter` library (usually included with Python)
- `pyinstaller` library (for creating executables)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/dicom_downloader.git
    cd dicom_downloader
    ```

2. Install the required libraries:

    ```sh
    pip install requests google-auth pyinstaller
    ```

## Usage

1. Run the [main.py](http://_vscodecontentref_/1) script to start the DICOM Downloader GUI:

    ```sh
    python main.py
    ```

2. Use the GUI to:
    - Browse and select the service account JSON file.
    - Enter the DICOM store URL.
    - Enter the study ID.
    - Browse and select the output folder path.
    - Click the "Download DICOM" button to start the download process.

## Creating an Executable with PyInstaller

To create an executable for the DICOM Downloader using PyInstaller, follow these steps:

1. Ensure the [dicom_downloader.spec](http://_vscodecontentref_/2) file is present in the repository.

2. Run PyInstaller with the spec file to create the executable:

    ```sh
    pyinstaller dicom_downloader.spec
    ```

3. The executable will be created in the [dist](http://_vscodecontentref_/3) directory.

## Code Overview

### [main.py](http://_vscodecontentref_/4)

This module provides the main functionality of the DICOM Downloader GUI.

#### Classes

- [DicomDownloaderUI](http://_vscodecontentref_/5): A class to represent the DICOM Downloader UI.
- [Downloader](http://_vscodecontentref_/6): A class to handle the downloading of DICOM files.

#### [DicomDownloaderUI](http://_vscodecontentref_/7)

This class creates the GUI and handles user interactions.

- [__init__(self, root)](http://_vscodecontentref_/8): Initializes the DICOM Downloader UI.
- [browse_file(self, entry)](http://_vscodecontentref_/9): Opens a file dialog to browse for a file and inserts the selected file path into the entry widget.
- [browse_folder(self, entry)](http://_vscodecontentref_/10): Opens a file dialog to browse for a folder and inserts the selected folder path into the entry widget.
- [start_download(self)](http://_vscodecontentref_/11): Starts the download process by creating a [Downloader](http://_vscodecontentref_/12) instance and running it in a separate thread.
- [run_download(self, downloader)](http://_vscodecontentref_/13): Runs the download process and stops the progress bar animation when done.

#### [Downloader](http://_vscodecontentref_/14)

This class handles the downloading of DICOM files.

- [__init__(self, service_account_json_path, datastore_path, progress_bar, log_text)](http://_vscodecontentref_/15): Initializes the Downloader.
- [extract_gcp_info(self, resource_path)](http://_vscodecontentref_/16): Extracts Google Cloud Platform information from the resource path.
- [download(self, study_id, output_folder)](http://_vscodecontentref_/17): Downloads DICOM files for the specified study ID and saves them to the output folder.
- [_get_access_tocken(self)](http://_vscodecontentref_/18): Gets the access token for the Google Cloud Healthcare API.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please contact jtihin.gregory@trenser.com.