// Tipos para el perfil y la rutina.
export type ExperienceLevel = 'Principiante' | 'Intermedio' | 'Avanzado'

export type WeekDay =
  | 'Lunes'
  | 'Martes'
  | 'Miércoles'
  | 'Jueves'
  | 'Viernes'
  | 'Sábado'
  | 'Domingo'

export type Exercise = {
  name: string
  durationMinutes: number
  caloriesPerMinute: number
  distanceKm?: number
}

export type RoutineEntry = {
  day: WeekDay
  exercise: Exercise
}

export type WeeklyRoutine = {
  name: string
  entries: RoutineEntry[]
}

export type User = {
  name: string
  age: number
  experienceLevel: ExperienceLevel
  routine: WeeklyRoutine
}
