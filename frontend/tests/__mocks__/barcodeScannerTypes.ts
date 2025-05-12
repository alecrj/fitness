// tests/__mocks__/barcodeScannerTypes.ts

// FoodItem interface matching the actual app types
export interface FoodItem {
    id: string;
    userId: string;
    name: string;
    brand?: string;
    barcode?: string;
    fdcId?: string;
    serving_size: number;
    serving_unit: string;
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
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
    is_custom: boolean;
    is_favorite: boolean;
    created_at: Date;
    updated_at: Date;
  }
  
  // BarcodeScanner component props
  export interface BarcodeScannerProps {
    onFoodFound: (food: FoodItem) => void;
    className?: string;
  }
  
  // Barcode detection result type
  export interface BarcodeResult {
    codeResult: {
      code: string;
    };
  }
  
  // Camera stream type
  export interface CameraStream {
    width: number;
    height: number;
    facing?: 'user' | 'environment';
  }