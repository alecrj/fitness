// In jest.config.js
module.exports = {
    preset: 'react-scripts',
    transformIgnorePatterns: [
      '/node_modules/(?!(axios|@your-org/your-package)/)'
    ],
    moduleFileExtensions: ['ts', 'tsx', 'js', 'json'],
    transform: {
      '^.+\\.(ts|tsx)$': 'ts-jest',
      '^.+\\.(js|jsx)$': 'babel-jest'
    }
  };