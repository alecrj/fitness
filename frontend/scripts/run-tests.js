// scripts/run-tests.js
const jest = require('jest');
const argv = process.argv.slice(2);

// Add default arguments
if (!argv.includes('--config')) {
  argv.push('--config', 'jest.config.js');
}

// Run tests with watch mode by default in development
if (process.env.NODE_ENV !== 'production' && 
    !argv.includes('--watchAll') && 
    !argv.includes('--ci') && 
    !argv.includes('--coverage')) {
  argv.push('--watchAll');
}

jest.run(argv);