import assert from 'node:assert/strict'
import { test } from 'node:test'
import type { Exercise, WeeklyRoutine } from '../src/types.ts'
import {
  calculateCalories,
  calculateCaloriePercentage,
  calculateDailyAverage,
  calculatePace,
  calculateTotalCalories,
  formatDuration,
  getLongestExercise,
  getMostCaloricExercise,
} from '../src/statistics.ts'

// Datos del ejemplo.
const running: Exercise = {
  name: 'Running', durationMinutes: 45, caloriesPerMinute: 10.4, distanceKm: 5.2,
}
const squats: Exercise = {
  name: 'Squats', durationMinutes: 30, caloriesPerMinute: 10,
}
const swimming: Exercise = {
  name: 'Swimming', durationMinutes: 60, caloriesPerMinute: 12, distanceKm: 9.6,
}
const routine: WeeklyRoutine = {
  name: 'Rutina de prueba',
  entries: [
    { day: 'Lunes', exercise: running },
    { day: 'Miércoles', exercise: squats },
    { day: 'Viernes', exercise: swimming },
  ],
}

test('Calcula las calorías y los ritmos del ejemplo', (): void => {
  assert.equal(calculateCalories(running), 468)
  assert.equal(calculateCalories(squats), 300)
  assert.equal(calculateCalories(swimming), 720)
  assert.equal(calculatePace(running), 8.65)
  assert.equal(calculatePace(squats), undefined)
  assert.equal(calculatePace(swimming), 6.25)
  assert.equal(calculateTotalCalories(routine), 1488)
})

test('Cuenta solamente los días entrenados', (): void => {
  assert.equal(calculateDailyAverage(routine), 496)

  const sameDayRoutine: WeeklyRoutine = {
    name: 'Dos días',
    entries: [
      { day: 'Lunes', exercise: running },
      { day: 'Lunes', exercise: squats },
      { day: 'Viernes', exercise: swimming },
    ],
  }

  assert.equal(calculateDailyAverage(sameDayRoutine), 744)
})

test('Formatea las duraciones', (): void => {
  assert.equal(formatDuration(135), '2h 15min')
  assert.equal(formatDuration(45), '45min')
  assert.equal(formatDuration(60), '1h')
  assert.equal(formatDuration(0), '0min')
})

test('Compara ejercicios y calcula porcentajes', (): void => {
  assert.equal(getLongestExercise(routine), swimming)
  assert.equal(getMostCaloricExercise(routine), swimming)
  assert.equal(calculateCaloriePercentage(running, 1488), 31)
  assert.equal(calculateCaloriePercentage(squats, 1488), 20)
  assert.equal(calculateCaloriePercentage(swimming, 1488), 48)
})

test('La mayor duración y las mayores calorías pueden ser de ejercicios distintos', (): void => {
  const walking: Exercise = {
    name: 'Walking', durationMinutes: 135, caloriesPerMinute: 1,
  }
  const updatedRoutine: WeeklyRoutine = {
    ...routine,
    entries: [...routine.entries, { day: 'Domingo', exercise: walking }],
  }

  assert.equal(getLongestExercise(updatedRoutine), walking)
  assert.equal(getMostCaloricExercise(updatedRoutine), swimming)
  assert.equal(calculateTotalCalories(updatedRoutine), 1623)
  assert.equal(calculateCaloriePercentage(swimming, 1623), 44)
})

test('Una rutina vacía no produce divisiones entre cero', (): void => {
  const emptyRoutine: WeeklyRoutine = { name: 'Vacía', entries: [] }

  assert.equal(calculateTotalCalories(emptyRoutine), 0)
  assert.equal(calculateDailyAverage(emptyRoutine), 0)
  assert.equal(getLongestExercise(emptyRoutine), undefined)
  assert.equal(getMostCaloricExercise(emptyRoutine), undefined)
  assert.equal(calculateCaloriePercentage(squats, 0), 0)
  assert.equal(calculatePace({ ...running, distanceKm: 0 }), undefined)
})

test('Los empates conservan el primer ejercicio registrado', (): void => {
  const tiedRoutine: WeeklyRoutine = {
    name: 'Empate',
    entries: [
      { day: 'Lunes', exercise: swimming },
      { day: 'Martes', exercise: { ...swimming, name: 'Otro ejercicio' } },
    ],
  }

  assert.equal(getLongestExercise(tiedRoutine), swimming)
  assert.equal(getMostCaloricExercise(tiedRoutine), swimming)
})
