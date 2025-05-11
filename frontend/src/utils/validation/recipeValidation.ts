import { RecipeFormData } from '../../types/recipe';

/**
 * Validates recipe form data and returns validation errors
 */
export const validateRecipeForm = (
  data: RecipeFormData
): Record<string, string> => {
  const errors: Record<string, string> = {};

  // Title validation
  if (!data.title.trim()) {
    errors.title = 'Recipe title is required';
  } else if (data.title.length > 100) {
    errors.title = 'Recipe title must be 100 characters or less';
  }

  // Description validation (optional)
  if (data.description && data.description.length > 500) {
    errors.description = 'Description must be 500 characters or less';
  }

  // Ingredients validation
  if (data.ingredients.length === 0) {
    errors.ingredients = 'At least one ingredient is required';
  } else if (data.ingredients.some(ing => !ing.trim())) {
    errors.ingredients = 'All ingredients must have content';
  }

  // Instructions validation
  if (data.instructions.length === 0) {
    errors.instructions = 'At least one instruction step is required';
  } else if (data.instructions.some(inst => !inst.trim())) {
    errors.instructions = 'All instruction steps must have content';
  }

  // Prep time validation (optional)
  if (data.prepTime !== undefined && data.prepTime < 0) {
    errors.prepTime = 'Prep time cannot be negative';
  }

  // Cook time validation (optional)
  if (data.cookTime !== undefined && data.cookTime < 0) {
    errors.cookTime = 'Cook time cannot be negative';
  }

  // Servings validation (optional)
  if (data.servings !== undefined && data.servings < 1) {
    errors.servings = 'Servings must be at least 1';
  }

  return errors;
};

/**
 * Validates recipe import URL
 */
export const validateRecipeUrl = (url: string): string | null => {
  if (!url.trim()) {
    return 'Recipe URL is required';
  }

  try {
    new URL(url);
    return null;
  } catch (error) {
    return 'Please enter a valid URL';
  }
};

/**
 * Checks if a recipe has unsaved changes compared to the original
 */
export const hasRecipeFormChanges = (
  original: RecipeFormData | null,
  current: RecipeFormData
): boolean => {
  if (!original) return true;

  // Basic comparison for primitive fields
  if (
    original.title !== current.title ||
    original.description !== current.description ||
    original.prepTime !== current.prepTime ||
    original.cookTime !== current.cookTime ||
    original.servings !== current.servings ||
    original.difficulty !== current.difficulty ||
    original.cuisine !== current.cuisine ||
    original.isPublic !== current.isPublic
  ) {
    return true;
  }

  // Check if ingredients array has changed
  if (original.ingredients.length !== current.ingredients.length) {
    return true;
  }
  for (let i = 0; i < original.ingredients.length; i++) {
    if (original.ingredients[i] !== current.ingredients[i]) {
      return true;
    }
  }

  // Check if instructions array has changed
  if (original.instructions.length !== current.instructions.length) {
    return true;
  }
  for (let i = 0; i < original.instructions.length; i++) {
    if (original.instructions[i] !== current.instructions[i]) {
      return true;
    }
  }

  // Check if tags array has changed
  const originalTags = original.tags || [];
  const currentTags = current.tags || [];
  if (originalTags.length !== currentTags.length) {
    return true;
  }
  for (let i = 0; i < originalTags.length; i++) {
    if (originalTags[i] !== currentTags[i]) {
      return true;
    }
  }

  // Check if image has changed
  if (!!current.image) {
    return true;
  }

  return false;
};