// Formatea un número como precio en colones costarricenses.
export const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CR', {
    style: 'currency',
    currency: 'CRC',
    minimumFractionDigits: 0
  }).format(price);
};
