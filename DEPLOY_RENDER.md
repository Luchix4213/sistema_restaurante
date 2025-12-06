# 🚀 Guía Completa: De Git a Render

Para poner tu proyecto en línea, primero necesitamos que el código esté en **TU**GitHub, y luego lo conectaremos a Render.

---

## 📅 PARTE 1: Subir el código a tu GitHub

Como clonaste este proyecto de otra persona, actualmente está "conectado" al GitHub de esa persona (o desconectado si borraste el `.git`). Vamos a conectarlo al tuyo.

### 1. Crea un Repositorio Nuevo
1.  Ve a [github.com/new](https://github.com/new).
2.  Nombre del repositorio: `sistema-restaurante` (o lo que gustes).
3.  **Importante**: No marques "Add a README", "Add .gitignore", etc. Déjalo **vacío**.
4.  Dale a "Create repository".

### 2. Conecta tu código local
Abre una terminal en la carpeta de tu proyecto (`sistema_restaurante`) y ejecuta estos comandos uno por uno:

```bash
# 1. Eliminar la conexión con el dueño original
git remote remove origin

# 2. Agregar tu nuevo repositorio (reemplaza TU_USUARIO con tu usuario real de GitHub)
git remote add origin https://github.com/TU_USUARIO/sistema-restaurante.git

# 3. Subir tu código
git branch -M main
git push -u origin main
```

*Si te pide usuario y contraseña: La contraseña es un "Personal Access Token" de GitHub, o usa la ventana de autenticación que salte.*

---

## ☁️ PARTE 2: Desplegar el Backend en Render

Ahora que el código es tuyo, Render puede leerlo.

### 1. Crear el Servicio Web
1.  Ve a [dashboard.render.com](https://dashboard.render.com/) y regístrate.
2.  Haz clic en **"New +"** -> **"Web Service"**.
3.  Selecciona "Build and deploy from a Git repository".
4.  Conecta tu cuenta de GitHub y dale permiso para ver tu nuevo repo `sistema-restaurante`.
5.  Selecciónalo.

### 2. Configurar el Servicio
Llena el formulario con estos datos EXACTOS:

| Campo | Valor |
| :--- | :--- |
| **Name** | `backend-restaurante` (o lo que quieras) |
| **Region** | Oregon (US West) *o la más cercana* |
| **Branch** | `main` |
| **Root Directory** | `backend` (⚠️ MUY IMPORTANTE) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

**Nota**: Al poner `backend` en "Root Directory", Render sabrá que debe buscar el `requirements.txt` ahí.
                        
### 3. Base de Datos (PostgreSQL)
Render ofrece PostgreSQL gratis (por 90 días, luego se borra, ideal para pruebas).

1.  Abre otra pestaña de Render.
2.  **"New +"** -> **"PostgreSQL"**.
3.  Nombre: `db-restaurante`.
4.  Crea la base de datos.
5.  Copia la url **"Internal Database URL"** (empieza con `postgres://...`).

### 4. Variables de Entorno (Environment Variables)
Vuelve a la pestaña de tu **Web Service** (el backend), busca la sección "Environment" y añade:

| Key | Value |
| :--- | :--- |
| `DATABASE_URL` | *Pega la "Internal Database URL" que copiaste* |
| `DATABASE_TYPE` | `postgresql` |
| `PYTHON_VERSION` | `3.11.5` (Obligatorio para que funcione FastAPI) |

### 5. Finalizar
Dale a **"Create Web Service"**. Render empezará a instalar todo.

---

## ✅ Verificación
Cuando termine, verás un enlace arriba a la izquierda (ej: `https://backend-restaurante-xyz.onrender.com`).
Entra a ese enlace y añade `/docs` al final. Si ves la documentación... **¡Felicidades, tu backend está online!**

> **Siguiente paso**: Cúando tengas la URL del backend, avísame para configurar el Frontend.
