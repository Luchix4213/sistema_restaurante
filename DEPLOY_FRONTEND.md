# 🚀 Guía de Despliegue en Vercel (Frontend)

¡Ya casi terminamos! El backend está listo, ahora falta la parte visual (Frontend) y conectarla.

Usaremos **Vercel**, que es la mejor plataforma para este tipo de proyectos.

## 1. Crear cuenta en Vercel
1.  Ve a [vercel.com/signup](https://vercel.com/signup).
2.  Regístrate seleccionando "Continue with GitHub".

## 2. Importar el Proyecto
1.  En tu dashboard de Vercel, haz clic en **"Add New..."** -> **"Project"**.
2.  Verás una lista de tus repositorios de GitHub. Busca `sistema-restaurante` y dale al botón **"Import"**.

## 3. Configurar el Proyecto (MUY IMPORTANTE)
Verás una pantalla llamada "Configure Project".

1.  **Framework Preset**: Déjalo en `Vite`.
2.  **Root Directory**:
    *   Haz clic en "Edit".
    *   Selecciona la carpeta `frontend`.
    *   (Esto es crucial porque tu código frontend no está en la raíz, sino dentro de esa carpeta).

3.  **Environment Variables**:
    *   Haz clic para expandir la sección.
    *   Añade la siguiente variable para conectar con tu backend de Render:

| Name | Value |
| :--- | :--- |
| `VITE_API_BASE_URL` | `https://backend-restaurante-qzq7.onrender.com/api/v1` |

**(Nota: Asegúrate de que el Value incluya `/api/v1` al final, tal como está arriba).**

## 4. Desplegar
1.  Haz clic en **"Deploy"**.
2.  Espera unos segundos (verás una pantalla de construcción).
3.  Si todo sale bien, verás una pantalla de felicitaciones con confeti 🎉.

## 5. ¡Prueba final!
1.  Haz clic en la imagen de tu proyecto o en el botón "Visit".
2.  Intenta iniciar sesión con las credenciales de demo:
    *   **Usuario**: `admin@gastrosmart.ai`
    *   **Contraseña**: `admin123`
    *   *(O las credenciales de la parrillada si usaste ese seed)*

¡Si logras entrar y ver el dashboard, tu sistema está 100% en línea! 🚀
