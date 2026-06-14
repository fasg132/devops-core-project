# DevOps Core Infrastructure Project

![CI DevOps Pipeline](https://github.com/fasg132/devops-core-project/actions/workflows/main.yml/badge.badge.svg)

A production-ready infrastructure blueprint demonstrating modern DevOps, CI/CD, and SecDevOps practices. The project orchestrates a Python Flask web application, an Nginx reverse proxy, and a PostgreSQL database using Docker Compose, fully covered by automated linting and security checks.

---

## 🏗️ Architecture Overview

The system architecture minimizes the attack surface by isolating the backend components inside a private virtual network.



* **Nginx (Gateway):** Acts as a Reverse Proxy listening on public port `80`. It handles incoming traffic and forwards it to the backend.
* **Flask App (Web):** Internal backend application hidden from the public internet (exposed only internally on port `5000`).
* **PostgreSQL (Database):** Isolated database service accessible only by the Flask application container.

---

## 🚀 Features & Automation

* **Reverse Proxying:** Nginx acts as a secure entry point, shielding the Flask application.
* **Database Backups:** Automated `backup.sh` script to dump, compress, and archive database states.
* **Self-Healing Monitoring:** A lightweight `monitor.sh` script that polls the application and automatically triggers a container recovery flow if the site is down.
* **CI/CD Pipeline:** Fully automated GitHub Actions workflow executing code linting (`ShellCheck`) and staging Docker build verification on every push.

---

## 🛠️ How to Run Locally

### Prerequisites
* Docker & Docker Desktop installed and running.
* Git.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/fasg132/devops-core-project.git](https://github.com/fasg132/devops-core-project.git)
   cd devops-core-project
