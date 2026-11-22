import { useState } from 'react'
import type { ChangeEvent, FormEvent, JSX } from 'react'
import type {
  BaseExercise,
  CategorySummary,
  Exercise,
  ExerciseCategory,
  ExperienceLevel,
  HeartRateZone,
  MembershipData,
  MembershipPlan,
  PersonalData,
  RoutineEntry,
  User,
  WeekDay,
} from './types.ts'
import {
  calculateCalories,
  calculateCaloriePercentage,
  calculateDailyAverage,
  calculateTotalCalories,
  getLongestExercise,
  getMostCaloricExercise,
} from './statistics.ts'
import { describeExercise, getCategorySummary } from './catalog.ts'
import './App.css'

// Nombres de las categorías.
const categories: ExerciseCategory[] = ['cardio', 'strength', 'flexibility']
const categoryNames: Record<ExerciseCategory, string> = {
  cardio: 'Cardio',
  strength: 'Fuerza',
  flexibility: 'Flexibilidad',
}

function App(): JSX.Element {
  // Datos guardados en memoria.
  const [user, setUser] = useState<User | null>(null)
  const [category, setCategory] = useState<ExerciseCategory | ''>('')
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

    const personalData: PersonalData = {
      id: user?.id ?? crypto.randomUUID(),
      name,
      age,
      experienceLevel,
    }
    const membershipData: MembershipData = {
      plan: data.get('plan') as MembershipPlan,
      startDate: String(data.get('startDate')),
      isActive: data.get('isActive') === 'on',
    }

    setUser({
      ...personalData,
      ...membershipData,
      routine: user?.routine ?? {
        id: crypto.randomUUID(),
        name: 'Mi rutina semanal',
        entries: [],
      },
    })
  }

  // Cambia los campos del ejercicio.
  function changeCategory(event: ChangeEvent<HTMLSelectElement>): void {
    setCategory(event.currentTarget.value as ExerciseCategory | '')
  }

  // Agrega un ejercicio a la rutina.
  function addExercise(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault()

    if (user === null || category === '') {
      return
    }

    const form: HTMLFormElement = event.currentTarget
    const data: FormData = new FormData(form)
    const name: string = String(data.get('exerciseName')).trim()
    const day: WeekDay = data.get('day') as WeekDay
    const baseExercise: BaseExercise = {
      id: crypto.randomUUID(),
      name,
      durationMinutes: Number(data.get('durationMinutes')),
      caloriesPerMinute: Number(data.get('caloriesPerMinute')),
    }

    if (name === '') {
      return
    }

    let exercise: Exercise

    switch (category) {
      case 'cardio':
        exercise = {
          ...baseExercise,
          category: 'cardio',
          distanceKm: Number(data.get('distanceKm')),
          heartRateZone: Number(data.get('heartRateZone')) as HeartRateZone,
        }
        break
      case 'strength':
        exercise = {
          ...baseExercise,
          category: 'strength',
          sets: Number(data.get('sets')),
          repetitions: Number(data.get('repetitions')),
          weightKg: Number(data.get('weightKg')),
        }
        break
      case 'flexibility':
        exercise = {
          ...baseExercise,
          category: 'flexibility',
          poses: Number(data.get('poses')),
        }
        break
    }

    setUser({
      ...user,
      routine: {
        ...user.routine,
        entries: [...user.routine.entries, { day, exercise }],
      },
    })
    form.reset()
    setCategory('')
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

          <label htmlFor="plan">Plan de membresía</label>
          <select id="plan" name="plan" defaultValue="basic">
            <option value="basic">Básico</option>
            <option value="premium">Premium</option>
          </select>

          <label htmlFor="startDate">Fecha de inicio de membresía</label>
          <input id="startDate" name="startDate" type="date" required />

          <label className="checkbox-label" htmlFor="isActive">
            <input id="isActive" name="isActive" type="checkbox" defaultChecked />
            Membresía activa
          </label>

          <button type="submit">Guardar perfil</button>
        </form>

        {user !== null && (
          <div aria-live="polite">
            <p><strong>Nombre:</strong> {user.name}</p>
            <p><strong>Edad:</strong> {user.age}</p>
            <p><strong>Nivel:</strong> {user.experienceLevel}</p>
            <p><strong>Membresía:</strong> {user.plan}</p>
            <p><strong>Fecha de inicio:</strong> {user.startDate}</p>
            <p><strong>Estado:</strong> {user.isActive ? 'Activa' : 'Inactiva'}</p>
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
              <label htmlFor="category">Categoría</label>
              <select id="category" name="category" value={category} onChange={changeCategory} required>
                <option value="">Selecciona una categoría</option>
                <option value="cardio">Cardio</option>
                <option value="strength">Fuerza</option>
                <option value="flexibility">Flexibilidad</option>
              </select>

              {category !== '' && (
                <>
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

                  <fieldset key={category}>
                    <legend>Detalles de {categoryNames[category]}</legend>
                    {category === 'cardio' && (
                      <>
                        <label htmlFor="distanceKm">Distancia (km)</label>
                        <input id="distanceKm" name="distanceKm" type="number" min="0.01" step="0.01" required />

                        <label htmlFor="heartRateZone">Zona de frecuencia cardíaca</label>
                        <select id="heartRateZone" name="heartRateZone" defaultValue="1">
                          <option value="1">Zona 1</option>
                          <option value="2">Zona 2</option>
                          <option value="3">Zona 3</option>
                          <option value="4">Zona 4</option>
                          <option value="5">Zona 5</option>
                        </select>
                      </>
                    )}
                    {category === 'strength' && (
                      <>
                        <label htmlFor="sets">Número de series</label>
                        <input id="sets" name="sets" type="number" min="1" step="1" required />

                        <label htmlFor="repetitions">Repeticiones por serie</label>
                        <input id="repetitions" name="repetitions" type="number" min="1" step="1" required />

                        <label htmlFor="weightKg">Peso (kg)</label>
                        <input id="weightKg" name="weightKg" type="number" min="0" step="0.01" required />
                      </>
                    )}
                    {category === 'flexibility' && (
                      <>
                        <label htmlFor="poses">Número de poses</label>
                        <input id="poses" name="poses" type="number" min="1" step="1" required />
                      </>
                    )}
                  </fieldset>

                  <button type="submit">Agregar ejercicio</button>
                </>
              )}
            </form>
          </section>

          <section>
            <h2>Catálogo de ejercicios</h2>
            <p>{user.routine.name}</p>
            {!hasExercises && <p>Todavía no hay ejercicios registrados.</p>}
            {categories.map((exerciseCategory: ExerciseCategory): JSX.Element => {
              const summary: CategorySummary = getCategorySummary(user.routine, exerciseCategory)

              return (
                <div className="category-group" key={exerciseCategory}>
                  <h3>{categoryNames[exerciseCategory]}</h3>
                  <p>
                    {summary.entries.length} {summary.entries.length === 1 ? 'ejercicio' : 'ejercicios'}
                    {' | '}{summary.totalMinutes} min | {summary.totalCalories.toFixed(2)} kcal
                  </p>
                  {summary.entries.length === 0 && <p>No hay ejercicios de esta categoría.</p>}
                  <ul className="exercise-list">
                    {summary.entries.map((entry: RoutineEntry): JSX.Element => (
                      <li key={entry.exercise.id}>
                        <strong>{entry.exercise.name}</strong> — {entry.day}
                        <p>
                          {describeExercise(entry.exercise)}
                          {' | '}{calculateCaloriePercentage(entry.exercise, totalCalories)}% del total
                        </p>
                      </li>
                    ))}
                  </ul>
                </div>
              )
            })}
            <p><strong>Total de ejercicios:</strong> {user.routine.entries.length}</p>
            <p><strong>Total:</strong> {totalCalories.toFixed(2)} kcal</p>
            <p><strong>Promedio por día entrenado:</strong> {dailyAverage.toFixed(2)} kcal</p>
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
                <strong>Más calorías:</strong> {mostCaloric.name} ({calculateCalories(mostCaloric).toFixed(2)} kcal,
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
