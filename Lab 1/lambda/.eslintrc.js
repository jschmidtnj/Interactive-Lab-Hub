module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: [
    '@typescript-eslint',
    'prefer-arrow',
    'import'
  ],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier/@typescript-eslint',
    'plugin:jsdoc/recommended',
    'plugin:prettier/recommended'
  ],
  env: {
    node: true
  },
  settings: {
    'import/parsers': {
      '@typescript-eslint/parser': ['.ts', '.tsx']
    },
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true
      },
    }
  },
  rules: {
    'prettier/prettier': ['error', { 'singleQuote': true }],
    'quotes': [2, 'single', { 'avoidEscape': true }],
    '@typescript-eslint/ban-ts-ignore': 'off',
    'semi': 'off',
    '@typescript-eslint/semi': ['error', 'always'],
    'no-control-regex': 'off',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        'argsIgnorePattern': '^_'
      }
    ],
    '@typescript-eslint/no-non-null-assertion': 'off',
    '@typescript-eslint/no-explicit-any': 'off',
    'no-async-promise-executor': 'off',
    'no-console': 'off',
    'no-debugger': 'error'
  },
};
