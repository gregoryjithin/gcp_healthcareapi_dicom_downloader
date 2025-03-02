"""
DICOM Downloader

This module provides a graphical user interface (GUI) for downloading DICOM files from a Google Cloud Healthcare API.
The GUI allows users to specify the service account JSON path, DICOM store URL, study ID, and output folder path.
The download progress is displayed using a progress bar, and log messages are shown in a text widget.

Classes:
    DicomDownloaderUI: A class to represent the DICOM Downloader UI.
    Downloader: A class to handle the downloading of DICOM files.

Usage:
    Run this module as a script to start the DICOM Downloader GUI.
"""

import os
import re
import threading
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

class DicomDownloaderUI:
    """
    A class to represent the DICOM Downloader UI.

    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        service_account_entry (tk.Entry): Entry widget for the service account JSON path.
        dicom_store_url_entry (tk.Entry): Entry widget for the DICOM store URL.
        study_id_entry (tk.Entry): Entry widget for the study ID.
        output_folder_entry (tk.Entry): Entry widget for the output folder path.
        progress (ttk.Progressbar): Progress bar widget to show download progress.
        log_text (tk.Text): Text widget to log messages.
    """

    def __init__(self, root):
        """
        Initialize the DICOM Downloader UI.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("DICOM Downloader")

        tk.Label(root, text="Service Account JSON Path").grid(row=0, column=0)
        self.service_account_entry = tk.Entry(root, width=50)
        self.service_account_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=lambda: self.browse_file(self.service_account_entry)).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(root, text="DICOM Store URL").grid(row=1, column=0)
        self.dicom_store_url_entry = tk.Entry(root, width=50)
        self.dicom_store_url_entry.grid(row=1, column=1)

        tk.Label(root, text="Study ID").grid(row=2, column=0)
        self.study_id_entry = tk.Entry(root, width=50)
        self.study_id_entry.grid(row=2, column=1)

        tk.Label(root, text="Output Folder Path").grid(row=3, column=0)
        self.output_folder_entry = tk.Entry(root, width=50)
        self.output_folder_entry.grid(row=3, column=1)
        tk.Button(root, text="Browse", command=lambda: self.browse_folder(self.output_folder_entry)).grid(row=3, column=2)

        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, pady=10)
        self.progress["value"] = 0  # Initialize progress to 0

        tk.Button(root, text="Download DICOM", command=self.start_download).grid(row=5, column=1, pady=10)

        self.log_text = tk.Text(root, height=10, width=70)
        self.log_text.grid(row=6, column=0, columnspan=3, pady=10)

        tk.Label(root, text="© jtihin.gregory@trenser.com").grid(row=7, column=0, columnspan=3, pady=10)

    def browse_file(self, entry):
        """
        Open a file dialog to browse for a file and insert the selected file path into the entry widget.

        Args:
            entry (tk.Entry): The entry widget to insert the file path into.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def browse_folder(self, entry):
        """
        Open a file dialog to browse for a folder and insert the selected folder path into the entry widget.

        Args:
            entry (tk.Entry): The entry widget to insert the folder path into.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def start_download(self):
        """
        Start the download process by creating a Downloader instance and running it in a separate thread.
        """
        self.progress.start()  # Start the progress bar animation
        downloader = Downloader(self.service_account_entry.get(), self.dicom_store_url_entry.get(), self.progress, self.log_text)
        download_thread = threading.Thread(target=self.run_download, args=(downloader,))
        download_thread.start()

    def run_download(self, downloader):
        """
        Run the download process and stop the progress bar animation when done.

        Args:
            downloader (Downloader): The Downloader instance to run.
        """
        downloader.download(self.study_id_entry.get(), self.output_folder_entry.get())
        self.progress.stop()  # Stop the progress bar animation

class Downloader:
    """
    A class to represent the Downloader.

    Attributes:
        credentials (Credentials): The credentials for the Google Cloud Healthcare API.
        progress_bar (ttk.Progressbar): The progress bar widget to update during the download.
        log_text (tk.Text): The text widget to log messages.
        project_id (str): The Google Cloud project ID.
        location (str): The Google Cloud location.
        dataset (str): The Google Cloud dataset.
        datastore (str): The Google Cloud datastore.
        base_url (str): The base URL for the Google Cloud Healthcare API.
    """

    def __init__(self, service_account_json_path, datastore_path, progress_bar, log_text):
        """
        Initialize the Downloader.

        Args:
            service_account_json_path (str): The path to the service account JSON file.
            datastore_path (str): The DICOM store URL.
            progress_bar (ttk.Progressbar): The progress bar widget to update during the download.
            log_text (tk.Text): The text widget to log messages.
        """
        self.credentials = Credentials.from_service_account_file(
            service_account_json_path,
            scopes=["https://www.googleapis.com/auth/cloud-healthcare"]
        )
        self.extract_gcp_info(datastore_path)
        self.progress_bar = progress_bar
        self.log_text = log_text

    def extract_gcp_info(self, resource_path: str):
        """
        Extract Google Cloud Platform information from the resource path.

        Args:
            resource_path (str): The resource path containing project, location, dataset, and datastore information.
        """
        resource_path = resource_path.strip()
        pattern = (r"projects/(?P<project_id>[^/]+)/locations/(?P<location>[^/]+)/"
                   r"datasets/(?P<dataset>[^/]+)/dicomStores/(?P<datastore>[^/]+)")
        
        match = re.match(pattern, resource_path)
        if match:
            self.project_id = match.group("project_id")
            self.location = match.group("location")
            self.dataset = match.group("dataset")
            self.datastore = match.group("datastore")
            self.base_url = (
                f"https://healthcare.googleapis.com/v1/projects/"
                f"{self.project_id}/"
                f"locations/{self.location}/"
                f"datasets/{self.dataset}/"
                f"dicomStores/{self.datastore}"
            )
    
    def download(self, study_id, output_folder):
        """
        Download DICOM files for the specified study ID and save them to the output folder.

        Args:
            study_id (str): The study ID to download DICOM files for.
            output_folder (str): The folder to save the downloaded DICOM files to.
        """
        try:
            access_token = self._get_access_tocken()
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            study_url = f"{self.base_url}/dicomWeb/studies/{str(study_id).strip()}/series"

            series_response = requests.get(study_url, headers=headers, timeout=1000)
            series_response.raise_for_status()
            series_json = series_response.json()
            print(str(series_json))
            series_list = series_response.json()
            
            study_folder = os.path.join(output_folder, str(study_id).strip())
            os.makedirs(study_folder, exist_ok=True)
            
            total_series = len(series_list)
            self.progress_bar["maximum"] = total_series
            
            for i, series in enumerate(series_list):
                series_id = series["0020000E"]["Value"][0]
                series_folder = os.path.join(study_folder, series_id)
                os.makedirs(series_folder, exist_ok=True)
                
                series_url = f"{study_url}/{series_id}/instances"
                instances_response = requests.get(series_url, headers=headers, timeout=1000)
                instances_response.raise_for_status()
                instances_list = instances_response.json()
                count = 0
                for instance in instances_list:
                    count += 1
                    sop_instance_uid = instance["00080018"]["Value"][0]
                    instance_url = f"{series_url}/{sop_instance_uid}"
                    instance_headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/dicom; transfer-syntax=*"
                    }
                    instance_response = requests.get(instance_url, headers=instance_headers, timeout=1000)
                    instance_response.raise_for_status()
                    if instance_response.status_code == 200:
                        file_name = f'{sop_instance_uid}.dcm'
                        output_file_path = os.path.join(series_folder, file_name)
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                        with open(output_file_path, "wb") as file:
                            file.write(instance_response.content)
                        log_message = f"{count}: {sop_instance_uid}\n"
                        self.log_text.insert(tk.END, log_message)
                        self.log_text.see(tk.END)
                        print(f"DICOM file downloaded successfully: {output_file_path}")
                    else:
                        raise requests.exceptions.HTTPError(
                            f"Failed to download DICOM file. Status code: "
                            f"{instance_response.status_code}"
                        )
                    
                    dicom_file = os.path.join(series_folder, f"{sop_instance_uid}.dcm")
                    with open(dicom_file, "wb") as f:
                        f.write(instance_response.content)
                
                self.progress_bar["value"] = i + 1
                self.progress_bar.update_idletasks()

            messagebox.showinfo("Success", "DICOM download completed successfully!")
        except (requests.exceptions.RequestException, OSError) as e:
            messagebox.showerror("Download Failed", str(e))
        
    def _get_access_tocken(self):
        """
        Get the access token for the Google Cloud Healthcare API.

        Returns:
            str: The access token.
        """
        auth_request = Request()
        self.credentials.refresh(auth_request)
        access_token = self.credentials.token
        return access_token

if __name__ == "__main__":
    root = tk.Tk()
    app = DicomDownloaderUI(root)
    root.mainloop()