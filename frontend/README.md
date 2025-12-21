# Frontend - Sistema Biométrico IA

Interfaz web para el análisis de emociones y microexpresiones faciales.

## Stack Tecnológico

- **React 18** con TypeScript
- **Vite** - Build tool rápido
- **Tailwind CSS** - Estilos utility-first
- **Axios** - Cliente HTTP

## Características

- 🖼️ **Drag & Drop**: Arrastra imágenes o haz click para seleccionar
- 👁️ **Preview**: Vista previa de la imagen antes de analizar
- 😊 **Visualización**: Resultados con emoji, confianza y análisis clínico
- 📱 **Responsive**: Diseño adaptable a móvil y desktop
- ⚡ **Rápido**: Construcción optimizada con Vite

## Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build

# Preview de producción
npm run preview
```

## Uso

1. Asegúrate de que el backend esté corriendo en `http://localhost:8000`
2. Inicia el frontend con `npm run dev`
3. Abre `http://localhost:5173` en tu navegador
4. Sube una imagen con rostro
5. Haz click en "Analizar Emoción"
6. Visualiza los resultados

## Estructura del Proyecto

```
src/
├── components/       # Componentes React
│   ├── ImageUploader.tsx
│   ├── EmotionDisplay.tsx
│   ├── LoadingSpinner.tsx
│   └── ErrorMessage.tsx
├── services/        # Servicios API
│   └── api.ts
├── types/          # Definiciones TypeScript
│   └── index.ts
├── App.tsx         # Componente principal
├── main.tsx        # Punto de entrada
└── index.css       # Estilos globales
```

## Configuración

El frontend está configurado para conectarse al backend en `http://localhost:8000`. Si necesitas cambiar esto, edita `src/services/api.ts`:

```typescript
const API_URL = 'http://tu-backend-url:puerto';
```

## Desarrollo

El proyecto usa TypeScript con modo estricto y ESLint para mantener calidad de código.

## Licencia

Parte del proyecto Sistema Biométrico IA
