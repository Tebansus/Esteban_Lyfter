import { useState } from 'react'
import type { FormEvent, JSX } from 'react'
import type { Exercise, ExperienceLevel, RoutineEntry, User, WeekDay } from './types.ts'
import {
  calculateCalories,
  calculateCaloriePercentage,
  calculateDailyAverage,
  calculatePace,
  calculateTotalCalories,
  formatDuration,
  getLongestExercise,
  getMostCaloricExercise,
} from './statistics.ts'
import './App.css'

function App(): JSX.Element {
  // Datos guardados en memoria.
  const [user, setUser] = useState<User | null>(null)
  const hasExercises: boolean = user !== null && user.routine.entries.length > 0
  const totalCalories: number = user === null ? 0 : calculateTotalCalories(user.routine)
  const dailyAverage: number = user === null ? 0 : calculateDailyAverage(user.routine)
  const longest: Exercise | undefined =
    user === null ? undefined : getLongestExercise(user.routine)
  const mostCaloric: Exercise | undefined =
    user === null ? undefined : getMostCaloricExercise(user.routine)

  // Guarda el perfil y mantiene la rutina.
  function saveProfile(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault()
    const data: FormData = new FormData(event.currentTarget)
    const name: string = String(data.get('name')).trim()
    const age: number = Number(data.get('age'))
    const experienceLevel: ExperienceLevel = data.get('experienceLevel') as ExperienceLevel

    if (name === '') {
      return
    }

    setUser({
      name,
      age,
      experienceLevel,
      routine: user?.routine ?? { name: 'Mi rutina semanal', entries: [] },
    })
  }

  // Agrega un ejercicio a la rutina.
  function addExercise(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault()

    if (user === null) {
      return
    }

    const form: HTMLFormElement = event.currentTarget
    const data: FormData = new FormData(form)
    const name: string = String(data.get('exerciseName')).trim()
    const day: WeekDay = data.get('day') as WeekDay
    const distance: string = String(data.get('distanceKm'))
    const exercise: Exercise = {
      name,
      durationMinutes: Number(data.get('durationMinutes')),
      caloriesPerMinute: Number(data.get('caloriesPerMinute')),
    }

    if (name === '') {
      return
    }

    if (distance !== '') {
      exercise.distanceKm = Number(distance)
    }

    setUser({
      ...user,
      routine: {
        ...user.routine,
        entries: [...user.routine.entries, { day, exercise }],
      },
    })
    form.reset()
  }

  return (
    <main>
      <header>
        <h1>FitTracker</h1>
        <p>Registra tu perfil y tus ejercicios de la semana.</p>
        <p>Los datos se borran al recargar la página.</p>
      </header>

      <section>
        <h2>Perfil de usuario</h2>
        <form onSubmit={saveProfile}>
          <label htmlFor="name">Nombre</label>
          <input id="name" name="name" type="text" required />

          <label htmlFor="age">Edad</label>
          <input id="age" name="age" type="number" min="1" step="1" required />

          <label htmlFor="experienceLevel">Nivel de experiencia</label>
          <select id="experienceLevel" name="experienceLevel" defaultValue="Principiante">
            <option value="Principiante">Principiante</option>
            <option value="Intermedio">Intermedio</option>
            <option value="Avanzado">Avanzado</option>
          </select>

          <button type="submit">Guardar perfil</button>
        </form>

        {user !== null && (
          <div aria-live="polite">
            <p><strong>Nombre:</strong> {user.name}</p>
            <p><strong>Edad:</strong> {user.age}</p>
            <p><strong>Nivel:</strong> {user.experienceLevel}</p>
          </div>
        )}
      </section>

      {user === null ? (
        <p>Guarda tu perfil para empezar a registrar ejercicios.</p>
      ) : (
        <>
          <section>
            <h2>Registrar ejercicio</h2>
            <form onSubmit={addExercise}>
              <label htmlFor="exerciseName">Nombre del ejercicio</label>
              <input id="exerciseName" name="exerciseName" type="text" required />

              <label htmlFor="day">Día de la semana</label>
              <select id="day" name="day" defaultValue="Lunes">
                <option>Lunes</option>
                <option>Martes</option>
                <option>Miércoles</option>
                <option>Jueves</option>
                <option>Viernes</option>
                <option>Sábado</option>
                <option>Domingo</option>
              </select>

              <label htmlFor="durationMinutes">Duración (minutos)</label>
              <input id="durationMinutes" name="durationMinutes" type="number" min="1" step="1" required />

              <label htmlFor="caloriesPerMinute">Calorías por minuto</label>
              <input id="caloriesPerMinute" name="caloriesPerMinute" type="number" min="0" step="0.01" required />

              <label htmlFor="distanceKm">Distancia (km, opcional)</label>
              <input id="distanceKm" name="distanceKm" type="number" min="0.01" step="0.01" />

              <button type="submit">Agregar ejercicio</button>
            </form>
          </section>

          <section>
            <h2>Ejercicios registrados</h2>
            <p>{user.routine.name}</p>
            {!hasExercises ? (
              <p>Todavía no hay ejercicios registrados.</p>
            ) : (
              <ul className="exercise-list">
                {user.routine.entries.map((entry: RoutineEntry, index: number): JSX.Element => {
                  const pace: number | undefined = calculatePace(entry.exercise)

                  return (
                    <li key={index}>
                      <strong>{entry.exercise.name}</strong> — {entry.day}
                      <p>
                        {formatDuration(entry.exercise.durationMinutes)}
                        {pace !== undefined && ` | Ritmo: ${pace.toFixed(2)} min/km`}
                        {' | '}{calculateCalories(entry.exercise).toFixed(2)} cal
                        {' | '}{calculateCaloriePercentage(entry.exercise, totalCalories)}% del total
                      </p>
                    </li>
                  )
                })}
              </ul>
            )}
            <p><strong>Total:</strong> {totalCalories.toFixed(2)} cal</p>
            <p><strong>Promedio por día entrenado:</strong> {dailyAverage.toFixed(2)} cal</p>
          </section>

          <section aria-live="polite">
            <h2>Resumen comparativo</h2>
            {!hasExercises && <p>Agrega un ejercicio para ver el resumen.</p>}
            {longest !== undefined && (
              <p>
                <strong>Mayor duración:</strong> {longest.name} ({longest.durationMinutes} min,
                {' '}{calculateCaloriePercentage(longest, totalCalories)}% del total de calorías)
              </p>
            )}
            {mostCaloric !== undefined && (
              <p>
                <strong>Más calorías:</strong> {mostCaloric.name} ({calculateCalories(mostCaloric).toFixed(2)} cal,
                {' '}{calculateCaloriePercentage(mostCaloric, totalCalories)}% del total)
              </p>
            )}
          </section>
        </>
      )}
    </main>
  )
}

export default App
