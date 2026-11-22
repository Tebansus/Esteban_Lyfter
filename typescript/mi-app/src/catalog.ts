import type { CategorySummary, Exercise, ExerciseCategory, WeeklyRoutine } from './types.ts'
import { calculateCalories, calculatePace, formatDuration } from './statistics.ts'

// Detalles de cada tipo de ejercicio.
export function describeExercise(exercise: Exercise): string {
  const duration: string = formatDuration(exercise.durationMinutes)
  const calories: string = `${calculateCalories(exercise).toFixed(2)} kcal`

  switch (exercise.category) {
    case 'cardio': {
      const pace: number | undefined = calculatePace(exercise)
      const paceText: string = pace === undefined ? '' : ` | Ritmo: ${pace.toFixed(2)} min/km`
      return `${duration} | ${exercise.distanceKm} km${paceText} | Zona ${exercise.heartRateZone} | ${calories}`
    }
    case 'strength':
      return `${duration} | ${exercise.sets} series x ${exercise.repetitions} reps | ${exercise.weightKg} kg | ${calories}`
    case 'flexibility':
      return `${duration} | ${exercise.poses} poses | ${calories}`
  }
}

// Agrupa los ejercicios y suma sus totales.
export function getCategorySummary(routine: WeeklyRoutine, category: ExerciseCategory): CategorySummary {
  const summary: CategorySummary = { entries: [], totalMinutes: 0, totalCalories: 0 }

  for (const entry of routine.entries) {
    if (entry.exercise.category === category) {
      summary.entries.push(entry)
      summary.totalMinutes += entry.exercise.durationMinutes
      summary.totalCalories += calculateCalories(entry.exercise)
    }
  }

  return summary
}
