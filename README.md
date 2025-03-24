# Gaia Assistant

Gaia Assistant is a personal assistant application that integrates various functionalities such as note-taking, calendar management, task management, and more. It leverages Google APIs, Firebase, and machine learning models to provide a comprehensive assistant experience.

## Project Structure
Gaia-Assistant/
├── app.py
├── gaia_request_app.py
├── gaia.py
├── gaiaRequests.py
├── __pycache__/
├── aether/
│   ├── db.sqlite3
│   ├── manage.py
│   ├── gaia_api/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── rest_api/
│   │   ├── ...
├── apollo/
│   ├── AI.py
├── eleuthia/
│   ├── drive.py
│   ├── todays_pdf/
│   │   ├── ...
├── ephaestus/
│   ├── summarize_class.py
│   ├── summarizer.py
├── minerva/
│   ├── assets/
│   ├── notesReferences/
│   │   ├── linkToNotes.csv
│   │   ├── notes.py
│   ├── readCalendar/
│   │   ├── app.py
│   │   ├── readCalendar.py
│   ├── todos/
│   │   ├── openTodo.py
│   │   ├── getTodos.py
│   │   ├── todo.py
├── utils/
│   ├── terminalGaia.py
│   ├── test.py

## Features

- **Note Management**: Manage and open notes using the `NoteLink` class in [notes.py](minerva/notesReferences/notes.py).
- **Calendar Management**: Read and manage calendar events using Google Calendar API in [readCalendar.py](minerva/readCalendar/readCalendar.py).
- **Task Management**: Manage tasks using Firebase Firestore in [openTodo.py](minerva/todos/openTodo.py) and [getTodos.py](minerva/todos/getTodos.py).
- **PDF Management**: Download and read PDFs from Google Drive in [drive.py](eleuthia/drive.py).
- **Voice Interaction**: Use speech recognition and text-to-speech for voice interaction in [audio_set.py](utils/audio_set.py).
- **Machine Learning**: Summarize and predict actions using a k-NN model in [summarize_class.py](ephaestus/summarize_class.py).
- **Code Generation**: Generate code snippets using OpenAI in [AI.py](apollo/AI.py).

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/Gaia-Assistant.git
    cd Gaia-Assistant
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up Google APIs**:
    - Place your `credentials.json` and `token.pickle` files in the `eleuthia/` directory.
    - Place your `credentials-calendar.json` and `token.json` files in the `minerva/readCalendar/` directory.

4. **Set up Firebase**:
    - Place your `serviceAccount.json` file in the `minerva/todos/` directory.

## Usage

- **Run the main application**:
    ```sh
    python app.py
    ```

- **Run the Gaia request application**:
    ```sh
    python gaia_request_app.py "your request"
    ```

## Web Page
If you want to use the gaia web page that consent also the usage of vocal command (only on supported browsers), go to "https://gaiaassistant.netlify.app/" and run on "https://127.0.0.1:8000" the aether server. For running the server you need to generate a cert.pem and a key.pem to run the server on https so that the netlify site can get changes.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes to simonebatt51@gmail.com.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.