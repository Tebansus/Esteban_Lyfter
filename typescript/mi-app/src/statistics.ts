import type { Exercise, WeekDay, WeeklyRoutine } from './types.ts'

// Calorías de un ejercicio.
export function calculateCalories(exercise: Exercise): number {
  return exercise.durationMinutes * exercise.caloriesPerMinute
}

// Ritmo en minutos por kilómetro.
export function calculatePace(exercise: Exercise): number | undefined {
  if (exercise.distanceKm === undefined || exercise.distanceKm <= 0) {
    return undefined
  }

  return Number((exercise.durationMinutes / exercise.distanceKm).toFixed(2))
}

// Calorías de toda la rutina.
export function calculateTotalCalories(routine: WeeklyRoutine): number {
  let total: number = 0

  for (const entry of routine.entries) {
    total += calculateCalories(entry.exercise)
  }

  return total
}

// Promedio de los días con ejercicio.
export function calculateDailyAverage(routine: WeeklyRoutine): number {
  const trainingDays: Set<WeekDay> = new Set<WeekDay>()

  for (const entry of routine.entries) {
    trainingDays.add(entry.day)
  }

  if (trainingDays.size === 0) {
    return 0
  }

  return calculateTotalCalories(routine) / trainingDays.size
}

// Duración con horas y minutos.
export function formatDuration(minutes: number): string {
  const hours: number = Math.floor(minutes / 60)
  const remainingMinutes: number = minutes % 60

  if (hours === 0) {
    return `${remainingMinutes}min`
  }

  if (remainingMinutes === 0) {
    return `${hours}h`
  }

  return `${hours}h ${remainingMinutes}min`
}

// Ejercicio con mayor duración.
export function getLongestExercise(routine: WeeklyRoutine): Exercise | undefined {
  let longest: Exercise | undefined

  for (const entry of routine.entries) {
    if (longest === undefined || entry.exercise.durationMinutes > longest.durationMinutes) {
      longest = entry.exercise
    }
  }

  return longest
}

// Ejercicio con más calorías.
export function getMostCaloricExercise(routine: WeeklyRoutine): Exercise | undefined {
  let mostCaloric: Exercise | undefined

  for (const entry of routine.entries) {
    if (
      mostCaloric === undefined ||
      calculateCalories(entry.exercise) > calculateCalories(mostCaloric)
    ) {
      mostCaloric = entry.exercise
    }
  }

  return mostCaloric
}

// Porcentaje de calorías de un ejercicio.
export function calculateCaloriePercentage(exercise: Exercise, total: number): number {
  if (total === 0) {
    return 0
  }

  return Math.round((calculateCalories(exercise) / total) * 100)
}
