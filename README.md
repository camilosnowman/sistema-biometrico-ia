# Sistema Biométrico IA / AI Biometric System

**Current Version**: 1.1.0 (Stable - Full Integration)

---

## 🇪🇸 Español

### Descripción
Este proyecto es un núcleo de inteligencia artificial diseñado para el **análisis de emociones y microexpresiones** utilizando modelos de lenguaje multimodales (Llama 3.2 Vision). Actualmente cuenta con un backend funcional capaz de recibir imágenes y devolver un razonamiento psicológico estruturado.

### Stack Tecnológico
*   **Lenguaje**: Python 3.12 (Estable).
*   **Framework**: FastAPI.
*   **Inteligencia Artificial**: Llama 3.2 Vision (11B).
*   **Inferencia**: Ollama (Local).
*   **Intercambio de Datos**: API REST (JSON).

### Requisitos para Colaboradores
1.  **Python 3.12+**: No usar versiones Alpha/Beta.
2.  **Ollama**: Debe estar instalado y corriendo (`ollama serve`).
3.  **Modelo**: Ejecutar `ollama pull llama3.2-vision`.

### Instalación Rápida
```bash
# 1. Clonar el repo
git clone https://github.com/camilosnowman/sistema-biometrico-ia.git

# 2. Instalar dependencias
pip install -r backend/requirements.txt

# 3. Iniciar Servidor
py -m uvicorn backend.app.main:app --reload
```

### Guía de Contribución (Gitflow)
*   **Rama Principal**: `main` (Producción - No tocar).
*   **Rama de Desarrollo**: `develop` (Código estable actual).
*   **Nuevos Features**:
    *   Si vas a trabajar en el Frontend: Crea la rama `feature/frontend`.
    *   Si vas a trabajar en Video: Crea la rama `feature/video-pipeline`.
*   **Pull Requests**: Siempre deben dirigirse a `develop`.

---

## 🇺🇸 English

### Description
This project is an AI core designed for **emotion and micro-expression analysis** using multimodal language models (Llama 3.2 Vision). It currently features a functional backend capable of processing images and returning structured psychological reasoning.

### Tech Stack
*   **Language**: Python 3.12 (Stable).
*   **Framework**: FastAPI.
*   **Artificial Intelligence**: Llama 3.2 Vision (11B).
*   **Inference**: Ollama (Local).
*   **Data Exchange**: REST API (JSON).

### Collaborator Requirements
1.  **Python 3.12+**: Do not use Alpha/Beta versions.
2.  **Ollama**: Must be installed and running (`ollama serve`).
3.  **Model**: Execute `ollama pull llama3.2-vision`.

### Quick Setup
```bash
# 1. Clone repo
git clone https://github.com/camilosnowman/sistema-biometrico-ia.git

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start Server
py -m uvicorn backend.app.main:app --reload
```

### Contribution Guidelines (Gitflow)
*   **Main Branch**: `main` (Production - Do not touch).
*   **Development Branch**: `develop` (Current stable code).
*   **New Features**:
    *   Working on Frontend? Create branch `feature/frontend`.
    *   Working on Video? Create branch `feature/video-pipeline`.
*   **Pull Requests**: Must always target `develop`.
