# CHEATDETECTION - Online Exam Cheating Detection App

A Streamlit-based web application that detects cheating behavior during online exams using computer vision, gaze tracking, facial recognition, and deep learning models.

## 📌 Features

- **User Authentication**: Supports participant and supervisor login with role-based access.
- **Proctoring System**: Automatically monitors test-takers during exams using webcam feed.
- **Cheating Detection**:
  - Detects head turns and eye movement.
  - Captures screenshots on suspicious behavior.
  - Records time, type of behavior, and visual evidence.
- **Supervisor Dashboard**:
  - View detailed cheating reports.
  - Analyze participant behavior with interactive visualizations.
  - Download logs and screenshots for documentation.
- **Clean Interface**: Built using Streamlit and AgGrid for a responsive and interactive UI.

## 🛠️ Technologies Used

- **Frontend/UI**: Streamlit, Plotly, st-aggrid
- **Computer Vision**: OpenCV, dlib
- **Machine Learning/AI**: TensorFlow / Keras
- **Facial Analysis**: Gaze tracking, facial landmarks, and object detection

## 📂 Folder Structure

```
├── Cascades/               # Haarcascade XML files
├── dataset/                # Dataset for face detection
├── gaze_tracking/          # Gaze tracking logic
├── models/                 # Pre-trained models
├── trainer/                # Face training logic
├── img/                    # Screenshot outputs
├── main.py                 # Streamlit app launcher
├── facemain.py             # Main logic for camera + detection
├── facerecognition.py      # Face recognition functions
├── facetraining.py         # Face model trainer
├── objectdetection.py      # Eye/mouth detection
├── requirements.txt
└── README.md
```

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/alexandertiopan1212/Streamlit_App_Cheat_Detection.git
   cd Streamlit_App_Cheat_Detection
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure your system has:
   - Webcam access
   - Python 3.7+
   - Compatible environment (Windows preferred for dlib .whl)

4. Run the app:
   ```bash
   streamlit run main.py
   ```

## 👥 Default Login Accounts

| Username  | Password | Role      |
|-----------|----------|-----------|
| raff      | 123      | Student   |
| Dyah      | 123      | Student   |
| Yusuf     | 123      | Student   |
| Pengawas  | 123      | Supervisor|

## 📊 Example Output

- Real-time detection of face movements and gaze direction
- Report table with screenshots and timestamps of suspicious behavior
