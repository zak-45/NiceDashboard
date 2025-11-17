# NiceDashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A dashboard built with [NiceGUI](https://nicegui.io/) to visualize real-time data and statistics from [WLEDVideoSync](https://github.com/dev-suda/WLED-Video-Sync).

## ✨ Features

- **Real-time Monitoring**: Watch key metrics from WLEDVideoSync as they happen.
- **Dynamic Charts**: Visualize performance with smooth, live-updating charts for:
  - LED Color Average
  - Frames Per Second (FPS)
  - System Latency
- **Modern UI**: Clean and intuitive interface powered by NiceGUI.
- **Dark Mode**: Toggle between light and dark themes for your viewing comfort.

## 📸 Screenshots

![Dashboard Light Mode](https://github.com/user-attachments/assets/6cfdf651-581a-4241-9143-46451f50d5c8)
*Dashboard in light mode*

---

![Dashboard Dark Mode](https://github.com/user-attachments/assets/6c9f8d4a-38a0-435f-9d18-b0ea4278eae5)
*Dashboard in dark mode*

---

![Chart Detail](https://github.com/user-attachments/assets/73928f6b-d82d-45f4-9ae4-ed11542734a0)
*Detailed view of the performance charts*

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

- Python 3.8+
- Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/NiceDashboard.git
    cd NiceDashboard
    ```

2.  **Create and activate a virtual environment (recommended):**
    *   On Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Usage

Once the dependencies are installed, you can run the dashboard:

```sh
python main.py
```

The application will be available at `http://localhost:8080` in your web browser.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.
