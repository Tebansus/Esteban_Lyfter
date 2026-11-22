// Identificadores del sistema.
export type EntityId = string
export type ExerciseId = EntityId
export type UserId = EntityId
export type RoutineId = EntityId

// Opciones del perfil y los ejercicios.
export type ExperienceLevel = 'Principiante' | 'Intermedio' | 'Avanzado'
export type MembershipPlan = 'basic' | 'premium'
export type HeartRateZone = 1 | 2 | 3 | 4 | 5

export type WeekDay =
  | 'Lunes'
  | 'Martes'
  | 'Miércoles'
  | 'Jueves'
  | 'Viernes'
  | 'Sábado'
  | 'Domingo'

// Datos comunes de los ejercicios.
export type BaseExercise = {
  id: ExerciseId
  name: string
  durationMinutes: number
  caloriesPerMinute: number
}

// Datos de cada categoría.
export type CardioExercise = BaseExercise & {
  category: 'cardio'
  distanceKm: number
  heartRateZone: HeartRateZone
}

export type StrengthExercise = BaseExercise & {
  category: 'strength'
  sets: number
  repetitions: number
  weightKg: number
}

export type FlexibilityExercise = BaseExercise & {
  category: 'flexibility'
  poses: number
}

export type Exercise = CardioExercise | StrengthExercise | FlexibilityExercise
export type ExerciseCategory = Exercise['category']

export type RoutineEntry = {
  day: WeekDay
  exercise: Exercise
}

export type WeeklyRoutine = {
  id: RoutineId
  name: string
  entries: RoutineEntry[]
}

// Datos personales del usuario.
export type PersonalData = {
  id: UserId
  name: string
  age: number
  experienceLevel: ExperienceLevel
}

// Datos de la membresía.
export type MembershipData = {
  plan: MembershipPlan
  startDate: string
  isActive: boolean
}

// Perfil completo del usuario.
export type User = PersonalData & MembershipData & {
  routine: WeeklyRoutine
}

// Totales de una categoría.
export type CategorySummary = {
  entries: RoutineEntry[]
  totalMinutes: number
  totalCalories: number
}
