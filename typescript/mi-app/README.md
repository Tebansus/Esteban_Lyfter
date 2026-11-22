# FitTracker - Sprint 1

Aplicación básica de React y TypeScript para guardar un perfil y su membresía, registrar ejercicios por categoría y consultar las estadísticas de una rutina semanal. Extiende el Sprint 0.

## Ejecutar

Se necesita Node.js 24 y npm.

Desde la raíz del repositorio:

```bash
cd typescript/mi-app
npm ci
npm run dev
```

Abrir la dirección que indique Vite en la terminal.

## Comprobar el proyecto

```bash
npm run typecheck
npm run lint
npm run build
```

El comando `typecheck` ejecuta TypeScript con `--strict`. Las configuraciones también tienen `strict: true`.

Para ver la compilación:

```bash
npm run preview
```

## Uso

1. Ingresar nombre, edad y nivel de experiencia.
2. Seleccionar el plan de membresía, su fecha de inicio y si está activa. Pulsar **Guardar perfil**.
3. Elegir primero la categoría del ejercicio.
4. Completar el nombre, día, duración y calorías por minuto, junto con los campos de la categoría:
   - Cardio: distancia y zona de frecuencia cardíaca del 1 al 5. El ritmo se calcula con la duración y la distancia.
   - Fuerza: series, repeticiones por serie y peso en kg.
   - Flexibilidad: número de poses.
5. Pulsar **Agregar ejercicio** para actualizar el catálogo y el resumen.

El catálogo muestra la cantidad de ejercicios, minutos y calorías de cada categoría. También conserva el total de calorías, el promedio por día entrenado, los porcentajes y la comparación de duración y calorías del Sprint 0.

El perfil se puede actualizar sin perder la rutina ni cambiar sus identificadores. Todos los datos están en memoria y se borran al recargar la página.

## Ejemplo del enunciado

Perfil: Ana García, 28 años, nivel `Intermedio`, plan `premium`, inicio `2026-11-15`, membresía activa.

| Día | Categoría | Ejercicio | Minutos | Calorías por minuto | Datos de la categoría |
| --- | --- | --- | --- | --- | --- |
| Lunes | Cardio | Running | 45 | 10.4 | 5.2 km, zona 3 |
| Miércoles | Cardio | Cycling | 60 | 9 | 20 km, zona 2 |
| Viernes | Fuerza | Bench Press | 30 | 10 | 4 series, 10 repeticiones, 60 kg |
| Domingo | Flexibilidad | Yoga Flow | 40 | 4 | 12 poses |

Resultados esperados:

- Cardio: 2 ejercicios, 105 minutos y 1008 kcal. Ritmos: Running 8.65 min/km y Cycling 3.00 min/km.
- Fuerza: 1 ejercicio, 30 minutos y 300 kcal.
- Flexibilidad: 1 ejercicio, 40 minutos y 160 kcal.
- Total: 4 ejercicios y 1468 kcal.
- Promedio por día entrenado: 367 kcal.
- Mayor duración y más calorías: Cycling, con 60 minutos y 540 kcal.

Varios ejercicios en un mismo día cuentan como un solo día entrenado. Los porcentajes se redondean al entero más cercano y pueden no sumar 100%. En caso de empate, el resumen muestra el primer ejercicio registrado. Una categoría vacía muestra cero ejercicios, minutos y calorías.

## Archivos principales

- `src/types.ts`: todos los tipos del dominio. `Exercise` une cardio, fuerza y flexibilidad usando `category` para distinguirlos. Cada categoría tiene sus propios campos obligatorios. `User` combina los datos personales y de membresía con una intersección de tipos. Los identificadores de ejercicios, usuarios y rutinas son cadenas generadas con `crypto.randomUUID()`.
- `src/statistics.ts`: cálculos del Sprint 0. El ritmo solo corresponde a cardio.
- `src/catalog.ts`: descripciones y subtotales por categoría.
- `src/App.tsx`: formularios y resultados.

Los niveles permitidos siguen siendo `Principiante`, `Intermedio` y `Avanzado`. Los planes disponibles son `basic` y `premium`.

El alcance llega hasta el Sprint 1. Los contratos con interfaces, las validaciones avanzadas en runtime, la API externa, el almacenamiento genérico y el dashboard quedan para futuros sprints. Los formularios usan restricciones básicas de HTML.
