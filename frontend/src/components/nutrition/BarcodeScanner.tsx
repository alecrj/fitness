import React, { useState, useRef } from 'react';
import { useNutrition } from '../../contexts/NutritionContext';

interface BarcodeScannerProps {
  onScanComplete: (foodItem: any) => void;
  onCancel: () => void;
}

const BarcodeScanner: React.FC<BarcodeScannerProps> = ({ onScanComplete, onCancel }) => {
  const { lookupBarcode } = useNutrition();
  const [isScanning, setIsScanning] = useState(false);
  const [manualCode, setManualCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Start camera for barcode scanning
  const startScanning = async () => {
    setError(null);
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        });
        
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          setIsScanning(true);
          // In a real implementation, we would use a barcode scanner library like quagga.js here
        }
      } else {
        setError('Camera access is not supported in your browser');
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      setError('Failed to access camera. Please check your permissions.');
    }
  };

  // Stop camera
  const stopScanning = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    
    setIsScanning(false);
  };

  // Handle manual barcode lookup
  const handleManualLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!manualCode.trim()) {
      setError('Please enter a barcode');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      const foodItem = await lookupBarcode(manualCode.trim());
      if (foodItem) {
        onScanComplete(foodItem);
      } else {
        setError('Food item not found for this barcode');
      }
    } catch (err) {
      console.error('Error looking up barcode:', err);
      setError('Failed to lookup barcode. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Clean up on unmount
  React.useEffect(() => {
    return () => {
      stopScanning();
    };
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-lg font-medium mb-4">Scan Barcode</h2>
      
      {isScanning ? (
        <div className="mb-4">
          <div className="relative w-full aspect-video bg-black rounded-lg overflow-hidden mb-3">
            <video 
              ref={videoRef} 
              className="absolute w-full h-full object-cover"
              autoPlay 
              playsInline
            />
            <div className="absolute inset-0 border-2 border-blue-500 z-10 pointer-events-none">
              <div className="absolute left-1/4 right-1/4 top-[45%] bottom-[55%] border-2 border-red-500" />
            </div>
          </div>
          <p className="text-sm text-gray-600 mb-3">
            Position the barcode within the red line and hold steady.
          </p>
          <button
            onClick={stopScanning}
            className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 rounded-md"
          >
            Cancel Scanning
          </button>
        </div>
      ) : (
        <div className="mb-4">
          <button
            onClick={startScanning}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md mb-4"
          >
            Start Camera Scanning
          </button>
          
          <div className="border-t border-b border-gray-200 py-4 my-4">
            <p className="text-center text-sm text-gray-600 mb-2">OR</p>
            <form onSubmit={handleManualLookup}>
              <div className="mb-3">
                <label htmlFor="barcode" className="block text-sm font-medium text-gray-700 mb-1">
                  Enter Barcode Manually
                </label>
                <input
                  type="text"
                  id="barcode"
                  value={manualCode}
                  onChange={(e) => setManualCode(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  placeholder="e.g., 123456789012"
                />
              </div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-md disabled:bg-green-400"
              >
                {isLoading ? 'Looking up...' : 'Lookup Barcode'}
              </button>
            </form>
          </div>
        </div>
      )}
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}
      
      <button
        onClick={onCancel}
        className="w-full border border-gray-300 text-gray-700 py-2 rounded-md"
      >
        Cancel
      </button>
      
      <div className="mt-4 text-sm text-gray-500">
        <p className="mb-1">Note:</p>
        <ul className="list-disc pl-5 space-y-1">
          <li>For best results, ensure good lighting</li>
          <li>Hold the camera steady</li>
          <li>Make sure the entire barcode is visible</li>
        </ul>
      </div>
    </div>
  );
};

export default BarcodeScanner;