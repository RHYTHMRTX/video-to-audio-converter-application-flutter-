# Sonic Extract

Sonic Extract is a video-to-audio converter project. It has a Flutter user interface and a Python server that uses FFmpeg to extract the audio track from a video.

This repository is a learning project and a starting point for a larger application. It is not currently a single self-contained app that can be sent to a friend and run without installing anything. The Flutter client and Python conversion server are separate pieces.

## What the project contains

```text
CPP+python/
|-- api.py                 Python web API used by Flutter
|-- backend.py             Older standalone Tkinter desktop version
|-- requirements.txt       Python server dependencies
|-- flutter_app/
|   |-- lib/main.dart      Flutter application interface
|   |-- pubspec.yaml       Flutter package configuration
|   |-- README.md           Flutter-specific notes
|-- README.md              This guide
```

### `api.py`

This is the Python backend for the Flutter app. It creates a FastAPI web server with one endpoint:

```text
POST /convert
```

The endpoint receives a video file and a requested format (`mp3` or `wav`). It then:

1. Saves the upload in a temporary folder.
2. Runs the FFmpeg command-line program.
3. Returns the converted audio file to Flutter.
4. Deletes the temporary files after the response is sent.

### `backend.py`

This is the original desktop application. It uses Tkinter for its interface and MoviePy for conversion. It runs independently and does not communicate with Flutter or `api.py`.

For the newer project, use `api.py` instead. Keep `backend.py` as an example or older desktop version.

### `flutter_app/lib/main.dart`

This is the cross-platform frontend. It lets a user:

- Pick a video file.
- Choose MP3 or WAV output.
- Enter the Python server address.
- Upload the video to the API.
- Save the returned audio in the app's documents folder.

The same Flutter code can target Windows and Android, although each platform needs its own build tools.

## How the pieces communicate

```text
User
  |
  v
Flutter app
  |  POST /convert with a multipart video upload
  v
FastAPI server (`api.py`)
  |
  v
FFmpeg
  |
  v
MP3 or WAV returned to Flutter
```

The default server address in the Flutter app is:

```text
http://127.0.0.1:8000
```

That address means "this same computer." It works when the Flutter app and Python API both run on the same PC.

For an Android phone connected to the same Wi-Fi network as the PC, replace it in the Flutter settings with the PC's local IPv4 address, for example:

```text
http://192.168.1.5:8000
```

The PC firewall may need to allow incoming connections on port `8000`.

## Running the Python API

A Python virtual environment is already present locally, but it should not be uploaded to GitHub. To create a fresh one:

```powershell
cd "C:\path\to\CPP+python"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

FFmpeg must also be installed and available on the system `PATH`. Check it with:

```powershell
ffmpeg -version
```

Start the API:

```powershell
python -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Leave this terminal open while the Flutter app is using the converter.

You can visit this address in a browser to see the automatically generated API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Flutter frontend

Install Flutter and the platform tools first. From the `flutter_app` folder:

```powershell
flutter pub get
flutter run -d windows
```

If Flutter is managed by Puro, use:

```powershell
puro flutter pub get
puro flutter run -d windows
```

Windows development requires Visual Studio with the **Desktop development with C++** workload, including the Windows SDK and CMake tools.

For Android development, install Android Studio, an Android SDK, and either an emulator or a USB-connected Android phone with USB debugging enabled. Then run:

```powershell
flutter devices
flutter run
```

## Building files to share

Build a Windows release with:

```powershell
flutter build windows
```

The output is placed under:

```text
flutter_app/build/windows/x64/runner/Release/
```

An Android APK can be built with:

```powershell
flutter build apk --release
```

The APK is placed under:

```text
flutter_app/build/app/outputs/flutter-apk/
```

Important: these builds only package the Flutter frontend. The Python API and FFmpeg still need to run somewhere. For friends to use the app, choose one of these designs:

- Run the API on your own PC and have friends connect to it over the internet. This needs deployment, authentication, and security work.
- Host the API on a server and put that server URL in the app.
- Rewrite the conversion layer to run locally inside each platform app. This is more difficult, especially on Android, because FFmpeg must be bundled separately for each platform.

## Uploading to GitHub

Do not upload these items:

```text
.venv/
__pycache__/
*.pyc
flutter_app/build/
flutter_app/.dart_tool/
```

Also check the source for personal usernames, private file paths, API keys, or test videos before making the repository public.

A useful root `.gitignore` is:

```gitignore
.venv/
__pycache__/
*.pyc
flutter_app/build/
flutter_app/.dart_tool/
flutter_app/.idea/
flutter_app/.flutter-plugins
flutter_app/.flutter-plugins-dependencies
flutter_app/.packages
```

## Known limitations and next improvements

- The API currently allows all origins and has no authentication. That is acceptable for local learning, but unsafe for a public internet deployment.
- Conversion is synchronous, so large videos can take a while and do not report detailed progress.
- The Flutter app stores the output file but does not yet provide a system share or save-as dialog on every platform.
- The Python API depends on FFmpeg being installed separately.
- The old MoviePy/Tkinter app and the new FastAPI/Flutter app duplicate conversion concepts. A future cleanup could move shared conversion logic into one Python module.
- The Flutter client currently keeps the entire upload and response in memory, which should be changed to streaming for very large files.

## A simple mental model

Think of Flutter as the remote control and `api.py` as the machine doing the work. Flutter shows buttons and chooses files. The API receives the file. FFmpeg performs the actual video-to-audio conversion. The API sends the result back, and Flutter saves it.

A developer familiar with Flutter should begin with `flutter_app/lib/main.dart`. A developer familiar with Python web servers should begin with `api.py` and `requirements.txt`.
