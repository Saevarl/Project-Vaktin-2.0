export const gpuModelComparator = (modelA: string, modelB: string): number => {
  const extractNumber = (model: string): number => {
    // Extract numbers from the model string
    const matches = model.match(/\d+/g);
    if (matches && matches.length > 0) {
      return parseInt(matches.join(''), 10);
    }
    return 0;
  };

  const numA = extractNumber(modelA);
  const numB = extractNumber(modelB);

  // Compare extracted numbers
  return numB - numA; // For descending order
};
