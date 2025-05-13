#!/bin/bash
echo "=== Removing conflicting type declarations ==="
rm -f src/types/firebase.d.ts

echo -e "\n=== TypeScript Errors ==="
npx tsc --noEmit --pretty

echo -e "\n=== ESLint Issues ==="
npx eslint src --ext .ts,.tsx --format compact

echo -e "\n=== Build Errors ==="
npm run build

echo -e "\n=== Dependency Issues ==="
npm ls

echo -e "\n=== Unused Dependencies ==="
npx depcheck

echo -e "\n=== Test Results ==="
npm test -- --passWithNoTests --watchAll=false

echo -e "\n=== Check Complete ==="