[![Astro Deployment](https://img.shields.io/badge/Deployed%20on-Astro.io-blue)](https://your-astro-deployment-url.com)

# 🚀 Airflow ETL Pipeline with Postgres and API Integration

## 📌 Project Overview
This project demonstrates the creation of an **ETL (Extract, Transform, Load) pipeline** using **Apache Airflow**. The pipeline extracts data from an external API (NASA’s Astronomy Picture of the Day – APOD API), transforms it into a clean format, and loads it into a **Postgres database**. The entire workflow is orchestrated by Airflow, enabling scheduling, monitoring, and managing complex data pipelines.

The setup leverages **Docker** to run Airflow and Postgres as services, ensuring an isolated and reproducible environment. Airflow’s powerful hooks and operators are used to streamline the ETL process efficiently.

---

## 🔑 Key Components

### ⚡ Airflow for Orchestration
- Defines, schedules, and monitors the ETL pipeline.
- Manages task dependencies to ensure sequential and reliable execution.
- Uses a **DAG (Directed Acyclic Graph)** to structure tasks such as data extraction, transformation, and loading.

### 🗄️ Postgres Database
- Stores the extracted and transformed data.
- Runs inside a Docker container for easy management and persistence with volumes.
- Interacts with Airflow via **PostgresHook** and **PostgresOperator**.

### 🌌 NASA API (APOD)
- Provides astronomy picture of the day data including **title, explanation, and image URL**.
- Data is fetched using Airflow’s **SimpleHttpOperator**.

---

## 🎯 Objectives
1. **Extract Data**  
   Fetch astronomy-related metadata from NASA’s APOD API on a scheduled basis (daily).

2. **Transform Data**  
   Clean and process JSON response (e.g., title, explanation, url, date) into a database-ready format.

3. **Load Data into Postgres**  
   Insert transformed data into a PostgreSQL table. If the target table doesn’t exist, it is created automatically as part of the DAG.

---

## 🏗️ Architecture & Workflow
The ETL pipeline is orchestrated in Airflow using a DAG with the following stages:

### 1️⃣ Extract (E)
- Uses **SimpleHttpOperator** to make GET requests to NASA’s APOD API.
- Receives JSON response containing astronomy metadata.

### 2️⃣ Transform (T)
- Processes JSON using Airflow’s **TaskFlow API** (`@task` decorator).
- Extracts and formats required fields: `title`, `explanation`, `url`, `date`.

### 3️⃣ Load (L)
- Loads the cleaned data into **Postgres** using **PostgresHook**.
- Automatically creates the required table if it doesn’t exist.

---

## 📊 High-Level Architecture Diagram
```
          ┌─────────────┐        ┌─────────────┐        ┌───────────────┐
          │   Extract   │  --->  │  Transform  │  --->  │     Load       │
          │ (NASA API)  │        │ (Clean JSON)│        │ (Postgres DB) │
          └─────────────┘        └─────────────┘        └───────────────┘
```

---

## 🛠️ Tech Stack
- **Apache Airflow** – Orchestration & Workflow Management  
- **Python** – Data transformation logic  
- **PostgreSQL** – Persistent Data Storage  
- **Docker** – Containerized environment  
- **NASA APOD API** – Data Source  

---

## 🌟 Deployment
This pipeline can be deployed locally using **Docker Compose** or on cloud platforms like **Astronomer (Astro.io)** for production-ready orchestration.

