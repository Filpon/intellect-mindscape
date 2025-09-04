export const evaluateTrigonometricFunction = (question: string) => {
  const [func, angle] = question.split(' ');
  const radians = (parseInt(angle) * Math.PI) / 180; // Convertion degrees to radians
  switch (func) {
    case 'sin':
      return Math.sin(radians);
    case 'cos':
      return Math.cos(radians);
    case 'tg':
      return Math.tan(radians);
    case 'ctg':
      return 1 / Math.tan(radians);
    default:
      return 'not exists';
  }
};
