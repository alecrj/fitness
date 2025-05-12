// tests/__mocks__/barcodeScannerTypes.ts
export interface FoodItem {
    id: string;
    userId: string;
    name: string;
    brand?: string;
    serving_size: number;
    serving_unit: string;
    is_custom: boolean;
    is_favorite: boolean;
    nutrition: {
      calories: number;
      protein: number;
      carbs: number;
      fat: number;
      fiber?: number;
      sugar?: number;
      sodium?: number;
      cholesterol?: number;
    };
    created_at: string;
    updated_at: string;
  }
  
  export interface BarcodeScannerProps {
    onFoodFound: (food: FoodItem) => void;
  }