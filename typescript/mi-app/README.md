# FitTracker - Sprint 0

Aplicación básica de React y TypeScript para guardar un perfil, registrar ejercicios y ver estadísticas de una rutina semanal.

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
npm test
npm run build
```

El comando `typecheck` ejecuta TypeScript con `--strict`. Las configuraciones también tienen `strict: true`. Las pruebas usan el ejecutor incluido en Node.js.

Para ver la compilación:

```bash
npm run preview
```

## Uso

1. Ingresar nombre, edad y nivel, y pulsar **Guardar perfil**.
2. Agregar cada ejercicio con su día, duración y calorías por minuto.
3. Completar la distancia solamente cuando corresponda.
4. Consultar la lista, el total, el promedio por día entrenado y el resumen comparativo.

El perfil se puede actualizar sin perder la rutina. Todos los datos están en memoria y se borran al recargar la página. No hay backend ni almacenamiento.

## Ejemplo del enunciado

Perfil: María López, 28 años, nivel `Intermedio`.

| Día | Ejercicio | Minutos | Calorías por minuto | Distancia en km |
| --- | --- | --- | --- | --- |
| Lunes | Running | 45 | 10.4 | 5.2 |
| Miércoles | Squats | 30 | 10 | Dejar vacío |
| Viernes | Swimming | 60 | 12 | 9.6 |

Resultados esperados:

- Calorías: Running 468, Squats 300 y Swimming 720.
- Ritmos: Running 8.65 min/km y Swimming 6.25 min/km. Squats no muestra ritmo.
- Total: 1488 calorías.
- Promedio por día entrenado: 496 calorías.
- Mayor duración y más calorías: Swimming, con 60 minutos y 48% del total.
- Porcentajes individuales: 31%, 20% y 48%. Se redondean al entero más cercano y pueden no sumar 100%.

Varios ejercicios en un mismo día cuentan como un solo día entrenado. En caso de empate, el resumen muestra el primer ejercicio registrado. Una rutina vacía muestra cero calorías y ningún ganador.

## Archivos principales

- `src/types.ts`: tipos del usuario, ejercicios y rutina. Los niveles permitidos son `Principiante`, `Intermedio` y `Avanzado`.
- `src/statistics.ts`: cálculos de calorías, ritmo, duración y comparaciones.
- `src/App.tsx`: formularios y resultados.
- `tests/statistics.test.ts`: pruebas de los cálculos.

Solo se incluye el Sprint 0. No se incluyen el catálogo, contratos con interfaces, una capa de validaciones en runtime, API externa, almacenamiento genérico ni dashboard de los siguientes sprints. Los formularios usan restricciones básicas de HTML.
