# MedVi — An AI-Powered Handwritten Clinical Record Digitization

MedVi is an AI-driven desktop application designed to digitize handwritten healthcare notes using real-time image capture, optical character recognition (OCR) via the Gemini Vision API, and a local SQLite database for report storage. It is developed with edge deployment in mind (e.g., Raspberry Pi 5 with GPIO support) and can be operated either via GUI or tactile input like button triggers.
This is the MedVi codebase with integrated OCR, UI and database functionalities
---

## 🧠 Core Features

* Capture or upload handwritten clinical note images.
* Extract clean transcriptions using Google's Gemini multimodal model.
* Store patient ID, phone number, timestamp, image, and extracted text into a local SQLite database.
* Preview captured/uploaded image and extracted content.
* Download the generated report for offline usage.
* Physical button support via GPIO (e.g., Raspberry Pi).

---

## 🛠️ Technologies Used

| Component        | Technology                              |
| ---------------- | --------------------------------------- |
| UI               | Tkinter                                 |
| Image Processing | OpenCV, PIL (Pillow)                    |
| OCR Engine       | Google Gemini Vision API (generativeai) |
| Database         | SQLite3                                 |
| GPIO Integration | gpiozero                                |
| Multithreading   | threading + signal.pause()              |

---

## 🚀 Installation & Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/medvi-digitization.git
   cd medvi-digitization
   ```

2. Install required dependencies:

   ```bash
   pip install pillow opencv-python google-generativeai gpiozero
   ```

3. Configure your Gemini API key:
   Replace the placeholder in the script:

   ```python
   genai.configure(api_key="YOUR_GEMINI_API_KEY")
   ```

4. (Optional) Enable GPIO if running on Raspberry Pi:
   Ensure you have pin 17 connected to a tactile button.

---

## 💡 How It Works

* Upon launching the application, a login screen prompts for a patient ID and phone number.
* Users can:

  * Capture an image from a connected webcam.
  * Upload a scanned/captured image.
  * Trigger capture using a GPIO-connected button.
* The image is sent to Gemini for transcription with the prompt:

  > "Extract only the handwritten text in this image with no explanation or preamble."
* The extracted text is displayed and optionally stored in the SQLite database.
* All reports are timestamped and persist locally for future reference.

---

## 🧪 Sample Flow

1. Start the application (python script).
2. Enter Patient ID and Phone Number.
3. Capture/upload handwritten image.
4. Click "Generate Report" to run OCR.
5. Click "Save" to store it or "Download" to save a copy.

---

## 🖥️ Running on Raspberry Pi

Ensure your Pi has:

* GPIO pin 17 configured for physical button input.
* Python 3 and all required libraries installed.
* OpenCV configured for camera access.

GPIO-based capture allows healthcare workers to snap a report image using a button press instead of interacting with the GUI—ideal for gloves-on environments.

---

## 🧷 Security & Privacy

* No patient data is transmitted outside the device except the image during Gemini API calls.
* For sensitive use cases, consider on-device OCR models like fine-tuned Tesseract or deploy Gemini via a proxy server with added access control.

---

## 📁 Database Schema

SQLite Table: reports

| Column          | Type    | Description                     |
| --------------- | ------- | ------------------------------- |
| id              | INTEGER | Auto-incrementing primary key   |
| patient\_id     | TEXT    | Identifier for the patient      |
| phone\_number   | TEXT    | Contact number                  |
| timestamp       | TEXT    | Date & time of image capture    |
| image\_path     | TEXT    | Path to stored image            |
| extracted\_text | TEXT    | Transcribed text from the image |

---

## 📎 To Do

* [ ] Add PDF export for reports.
* [ ] Deploy as a .exe or .deb package.
* [ ] Replace Gemini API with local fallback using Tesseract or LLaVA.

---

## 📜 License

This project is released under the MIT License.

---


