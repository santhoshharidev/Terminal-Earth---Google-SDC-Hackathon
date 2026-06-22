
# 🌍 Terminal Earth

Terminal Earth is an AI-powered Logistics Intelligence System that transforms a simple command-line interface into a complete logistics planning and decision-support platform.

By combining AI reasoning, route visualization, automated reporting, and sustainability analysis, Terminal Earth helps users make informed transportation and supply-chain decisions through natural language interactions.

---

## 🚀 Features

### 📦 Logistics Planning

* Natural language shipment planning
* Source and destination route analysis
* Budget and delivery deadline consideration
* Multi-modal transport comparison

### 🤖 AI-Powered Analysis

* Transportation recommendations using Gemini API
* Cost estimation and risk assessment
* Delivery time analysis
* Intelligent logistics decision support

### 🗺️ Route Visualization

* Automatic Google Maps integration
* Route analysis from source to destination
* Interactive route exploration

### 📊 Automated Dashboard Generation

* Google Sheets dashboard creation
* Shipment summary reports
* Transport comparison tables
* Analytics-ready data organization

### 📈 Dynamic Analytics

* Cost comparison visualization
* Transport performance tracking
* Dashboard-based decision support

### ⚡ Optimization Engine

* Alternative transportation suggestions
* Cost-saving recommendations
* Delivery-time optimization insights
* AI-generated logistics improvements

### 🌱 Carbon Footprint Analysis

* Transportation emission estimates
* Sustainability-focused recommendations
* Environment-friendly route suggestions

### 🕒 Shipment History

* Command history tracking
* Context-aware follow-up analysis
* Historical shipment reference system

---

## 🏗️ System Architecture

```text
User Command
      │
      ▼
Terminal Earth (CLI)
      │
      ▼
Gemini API
      │
      ▼
Logistics Analysis Engine
      │
 ┌────┴────┐
 ▼         ▼
Google    Google
Maps      Sheets
(Route)   (Dashboard)
      │
      ▼
Optimization & Carbon Analysis
```

---

## 🛠️ Tech Stack

* Python
* Gemini API
* Google Maps
* Google Sheets API
* Google Service Accounts
* GSpread
* JSON
* Tabulate
* Dotenv

---

## 📸 Project Workflow

1. User enters shipment details in natural language.
2. Gemini analyzes logistics requirements.
3. Transportation options are compared.
4. Route is visualized using Google Maps.
5. Dashboard is generated in Google Sheets.
6. Optimization suggestions are provided.
7. Carbon emissions are estimated.
8. Shipment history is stored for future analysis.

---

## 📂 Project Structure

```text
TerminalEarth/
│
├── terminal.py
├── dashboard_writer.py
├── history.json
├── credentials.json
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/TerminalEarth.git
cd TerminalEarth
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### Add Google Service Account Credentials

Place your Google Service Account JSON file inside the project directory:

```text
credentials.json
```

### Run Application

```bash
python terminal.py
```

---

## 🎯 Example Commands

```bash
move 1000kg of goods from Chennai to Delhi
```

```bash
optimize
```

```bash
carbon
```

```bash
history
```

```bash
clear history
```

---

## 🎥 Demo

A complete project demonstration video is available in this repository with the name "Terminal Earth Demonstration.mp4".

---

## 🔮 Future Enhancements

* Real-time logistics provider integration
* Live transportation pricing
* Advanced route optimization
* Carbon analytics dashboard
* Multi-shipment planning
* Web-based visualization portal

---

## 👨‍💻 Author

**Santhosh Hari I**

B.Tech Computer Science & Engineering
AI & Software Development Enthusiast

If you found this project interesting, feel free to star the repository and connect with me.
