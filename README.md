<div align="center">

<img src="https://img.shields.io/badge/SwarmRoute-AI-6366f1?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMSAxNEg5VjhoMnY4em00IDBoLTJWOGgydjh6Ii8+PC9zdmc+" alt="SwarmRoute AI" />

# 🐝 SwarmRoute AI

### Adaptive Multi-Agent Logistics Routing Platform

*Transforming supply chain management from reactive planning into proactive, autonomous decision-making.*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-swarmroute--ai.vercel.app-6366f1?style=flat-square)](https://swarmroute-ai.vercel.app/)
[![GitHub](https://img.shields.io/badge/GitHub-mohithgokul%2Fswarmroute--AI-181717?style=flat-square&logo=github)](https://github.com/mohithgokul/swarmroute-AI)
[![TypeScript](https://img.shields.io/badge/TypeScript-77.2%25-3178C6?style=flat-square&logo=typescript)](https://github.com/mohithgokul/swarmroute-AI)
[![Python](https://img.shields.io/badge/Python-17.9%25-3776AB?style=flat-square&logo=python)](https://github.com/mohithgokul/swarmroute-AI)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=flat-square&logo=vercel)](https://swarmroute-ai.vercel.app/)

</div>

---

## 📖 Overview

**SwarmRoute AI** is an intelligent, adaptive logistics platform powered by a coordinated swarm of five specialized AI agents. Instead of relying on static routing rules, SwarmRoute continuously monitors real-world conditions — weather, traffic, geopolitics, and more — to autonomously calculate the safest, fastest, and most cost-efficient shipment routes.

Simply provide your shipment details (source, destination, transport mode, and deadline), and the agent swarm takes over — collaborating in real-time to deliver an optimized, risk-aware routing recommendation.

---

## ✨ Key Features

- 🤖 **Multi-Agent AI Swarm** — Five specialized agents work in parallel to analyze different risk and logistics dimensions simultaneously
- 🌦️ **Real-Time Weather Intelligence** — Live weather data factored into every routing decision
- 🚦 **Dynamic Traffic Analysis** — Up-to-date traffic conditions across transport corridors
- 🌍 **Geopolitical Risk Awareness** — Flags regions with active disruptions, sanctions, or instability
- ⚡ **Proactive Decision-Making** — Shifts logistics from reactive firefighting to autonomous, forward-looking planning
- 🗺️ **Multi-Modal Transport Support** — Road, rail, air, and sea routing capabilities
- 📊 **Comprehensive Risk Reports** — Each agent contributes a scored analysis; results are synthesized into a unified recommendation

---

## 🧠 The Agent Swarm

SwarmRoute deploys **five specialized AI agents** the moment a shipment query is submitted:

| Agent | Role |
|-------|------|
| 🌦️ **Weather Agent** | Analyzes meteorological conditions along the proposed route |
| 🚦 **Traffic Agent** | Evaluates congestion, road closures, and transit delays |
| 🌍 **Geopolitical Agent** | Assesses political risk, border restrictions, and regional conflicts |
| 📦 **Logistics Agent** | Optimizes for cost, transit time, and carrier availability |
| 🔗 **Coordinator Agent** | Synthesizes all agent outputs into a final ranked routing recommendation |

Each agent operates independently and reports its findings; the Coordinator Agent merges these into a single, actionable routing plan.

---

## 🏗️ Architecture

```
swarmroute-AI/
├── backend/          # Python-based agent orchestration & API
│   ├── agents/       # Individual AI agent modules
│   ├── routes/       # FastAPI route handlers
│   └── main.py       # Entry point
├── frontend/         # TypeScript / Next.js UI
│   ├── components/   # React components
│   ├── pages/        # Application pages
│   └── styles/       # CSS styling
└── package-lock.json
```

**Tech Stack:**

| Layer | Technology |
|-------|-----------|
| Frontend | TypeScript, Next.js, React, CSS |
| Backend | Python, FastAPI |
| AI Agents | Multi-agent LLM orchestration |
| Deployment | Vercel |

---

## 🚀 Getting Started

### Prerequisites

- Node.js ≥ 18
- Python ≥ 3.10
- npm or yarn
- An API key for your preferred LLM provider

### 1. Clone the Repository

```bash
git clone https://github.com/mohithgokul/swarmroute-AI.git
cd swarmroute-AI
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```env
LLM_API_KEY=your_api_key_here
# Add any other required environment variables
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Set Up the Frontend

```bash
cd ../frontend
npm install
```

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 💡 How to Use

1. **Enter Shipment Details** — Fill in source location, destination, transport mode, and deadline
2. **Launch the Swarm** — Hit submit to deploy all five AI agents simultaneously
3. **Watch Agents Work** — Each agent streams its analysis in real-time
4. **Get Your Route** — Receive a final optimized, risk-scored routing recommendation
5. **Act on Insights** — Use the detailed breakdown to make informed logistics decisions

---

## 🌐 Live Demo

Try SwarmRoute AI instantly — no setup required:

**[https://swarmroute-ai.vercel.app/](https://swarmroute-ai.vercel.app/)**

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add: your feature description'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code follows existing conventions and includes relevant documentation.

---

## 👥 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/mohithgokul">
        <img src="https://avatars.githubusercontent.com/u/194810209?s=80&v=4" width="60px;" alt="Mohith Gokul"/><br />
        <sub><b>K. Mohith Gokul Reddy</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/KOTHABHASKARABALAJI">
        <img src="https://avatars.githubusercontent.com/u/222498317?s=80&v=4" width="60px;" alt="Kotha Bhaskara Balaji"/><br />
        <sub><b>Kotha Bhaskara Balaji</b></sub>
      </a>
    </td>
  </tr>
</table>

---

## 📄 License

This project is open source. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ by the SwarmRoute AI team

⭐ **Star this repo** if you find it useful — it helps others discover the project!

[![GitHub stars](https://img.shields.io/github/stars/mohithgokul/swarmroute-AI?style=social)](https://github.com/mohithgokul/swarmroute-AI)

</div>
