# YtbVideoDownloaderGUI
This code provides a simple yet functional YouTube video and playlist downloader with a user-friendly interface, real-time progress tracking, and the ability to cancel downloads.

NOTE: This code provides a graphical user interface (GUI) for downloading YouTube videos or playlists using the `yt_dlp` library. Below is a brief description of the code

### Global Variables and Configurations:
- **`cancel_download_flag`:** A global variable used to signal when to cancel the ongoing download.
- **`config_path`:** Defines the absolute path for a configuration file (`config.json`), which stores the last selected download directory.

### Directory Management Functions:
- **`load_last_directory`:** Reads the configuration file (`config.json`) to load the last selected download directory. If the file is not found, the current working directory is returned.
- **`save_last_directory`:** Saves the last selected download directory to `config.json`.

### Download Management Functions:
- **`update_progress`:** Updates the progress bar on the GUI as the download progresses, showing the percentage of completion.
- **`update_stats`:** Displays real-time download statistics, such as progress, speed, and estimated time remaining. This function also checks if the download has been cancelled by the user.
- **`is_video_already_downloaded`:** Verifies whether the video has already been downloaded in the specified destination folder by checking the file's existence using the video's title and extension.
- **`download_video`:** Downloads a single video from YouTube using the specified URL and stores it in the chosen destination folder. It handles errors and checks if the user has requested to cancel the download.
- **`download_playlist`:** Downloads an entire playlist from YouTube using the provided URL. It operates similarly to `download_video`, but processes multiple videos as part of the playlist.

### Threading and Control Functions:
- **`start_video_download`:** Initializes the video download process in a separate thread to keep the GUI responsive during the download. It also checks if the video has already been downloaded before starting the download.
- **`start_playlist_download`:** Starts the playlist download in a separate thread. Unlike videos, it does not check if the entire playlist has already been downloaded since playlists can have new content over time.
- **`cancel_download`:** Sets the `cancel_download_flag` to `True`, which will interrupt the download when detected by `update_stats`.

### GUI Setup and Interaction:
- **`choose_folder`:** Opens a file dialog to allow the user to select the folder where downloads will be saved.
- **GUI Components:** The GUI is created using `Tkinter` and `ttkthemes`, with labels, buttons, a progress bar, and dynamic statistics to guide the user through selecting a folder, entering a URL, and downloading videos or playlists.
- **Icon and Theme:** The window icon is set using `iconphoto()` with a `.png` image, and the GUI theme is customized with the `scidgreen` theme and a custom background color.
