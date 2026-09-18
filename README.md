<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=3000&pause=1000&color=2ECC71&center=true&vCenter=true&width=700&lines=%F0%9F%8F%94%EF%B8%8F+Landslide+Early+Warning+System;AI%2FML-Powered+Risk+Prediction;Built+for+Northeast+India+%F0%9F%87%AE%F0%9F%87%B3" alt="Typing SVG" />

<br/>

![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,14&height=180&section=header&text=SIH%20Landslide%20Early%20Warning&fontSize=36&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Early%20warning%20today%20saves%20lives%20tomorrow&descAlignY=58&descSize=16)

<p>
  <img src="https://img.shields.io/badge/Model%20Accuracy-93.12%25-2ECC71?style=for-the-badge&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/ROC--AUC-0.9734-27AE60?style=for-the-badge&logo=chartdotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/github/languages/top/subhrajeetshaw008-bit/SIH-Landslide-Early-Warning?style=flat-square&color=blue" />
  <img src="https://img.shields.io/github/last-commit/subhrajeetshaw008-bit/SIH-Landslide-Early-Warning?style=flat-square&color=orange" />
  <img src="https://img.shields.io/github/repo-size/subhrajeetshaw008-bit/SIH-Landslide-Early-Warning?style=flat-square&color=yellow" />
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/license-unspecified-lightgrey?style=flat-square" />
</p>

</div>

---

## 🌍 About the Project

A **machine-learning-driven landslide susceptibility prediction system** built for the hilly, high-risk terrain of **Northeast India**. It fuses **elevation, slope, geolocation, and live weather data** to classify landslide risk in real time — and hands back clear, actionable safety recommendations, not just a probability score.

> ⚠️ Built during **Smart India Hackathon (SIH)** — where minutes of early warning can mean the difference between evacuation and disaster.

<br/>

<div align="center">
<img src="https://raw.githubusercontent.com/subhrajeetshaw008-bit/SIH-Landslide-Early-Warning/main/assets/demo.gif" alt="App demo" width="80%" onerror="this.style.display='none'"/>
</div>

<br/>

## ✨ Current Features

<table align="center">
<tr>
<td align="center" width="200">📍<br/><b>Location Analysis</b><br/><sub>Pinpoint-based risk lookup</sub></td>
<td align="center" width="200">🗺️<br/><b>Interactive Map</b><br/><sub>Visualize risk zones live</sub></td>
<td align="center" width="200">🌦️<br/><b>Live Weather</b><br/><sub>Rainfall & climate signals</sub></td>
<td align="center" width="200">🏔️<br/><b>DEM Elevation</b><br/><sub>Digital elevation modeling</sub></td>
</tr>
<tr>
<td align="center" width="200">⛰️<br/><b>Terrain Slope</b><br/><sub>Gradient risk factor</sub></td>
<td align="center" width="200">🤖<br/><b>ML Prediction</b><br/><sub>Trained classification model</sub></td>
<td align="center" width="200">⚠️<br/><b>Risk Classification</b><br/><sub>Low / Medium / High tiers</sub></td>
<td align="center" width="200">🛡️<br/><b>Safety Guidance</b><br/><sub>Actionable recommendations</sub></td>
</tr>
</table>

<br/>

## 🧠 Baseline ML Model

The current baseline model is trained on four core geospatial features:

| Feature | Description |
|---|---|
| 🌐 Latitude | Geographic coordinate |
| 🌐 Longitude | Geographic coordinate |
| ⛰️ Elevation | From Digital Elevation Model (DEM) |
| 📐 Slope | Computed terrain gradient |

<div align="center">

| Metric | Score |
|:---:|:---:|
| **Accuracy** | `93.12%` |
| **ROC-AUC** | `0.9734` |

![Accuracy](https://progress-bar.xyz/93?title=Accuracy&width=300&color=2ecc71)
![ROC-AUC](https://progress-bar.xyz/97?title=ROC-AUC&width=300&color=3498db)

</div>

<br/>

## 🛠️ Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
</p>

<br/>

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/subhrajeetshaw008-bit/SIH-Landslide-Early-Warning.git
cd SIH-Landslide-Early-Warning

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501` 🎉

<br/>

## 📂 Project Structure

```
SIH-Landslide-Early-Warning/
├── .streamlit/              # Streamlit configuration
├── assets/                  # Static assets (images, icons)
├── chatbot/                 # Conversational safety assistant
├── pages/                   # Multi-page Streamlit app views
├── utils/                   # Helper utilities
├── app.py                   # Main application entry point
├── model.py / ml_model.py   # ML model definitions
├── train_baseline_model.py  # Model training pipeline
├── calculate_slope.py       # Terrain slope computation
├── extract_terrain.py       # DEM terrain extraction
├── weather.py                # Live weather integration
└── requirements.txt          # Python dependencies
```

<br/>

## 🗺️ Roadmap

- [x] Baseline ML model (elevation + slope + geolocation)
- [x] Streamlit interactive dashboard
- [x] Live weather integration
- [ ] Real-time satellite/rainfall alert feed
- [ ] SMS/push notification alerts for at-risk zones
- [ ] Mobile-friendly deployment
- [ ] Expanded training data across more NE India districts

<br/>

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

```bash
# Fork it, then:
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
# Open a Pull Request 🚀
```

<br/>

<div align="center">

### 💬 Get in Touch

<a href="https://github.com/subhrajeetshaw008-bit">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<br/><br/>

⭐ **If this project helped you, consider giving it a star!** ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,14&height=100&section=footer" width="100%"/>

</div>
