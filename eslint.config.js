import js from '@eslint/js';
import prettierConfig from 'eslint-config-prettier';
import prettier from 'eslint-plugin-prettier';
import globals from 'globals';

export default [
    js.configs.recommended,
    prettierConfig,
    {
        files: ['undetectable_bot/js/**/*.js'],
        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.es2021,
            },
        },
        plugins: {
            prettier,
        },
        rules: {
            'prettier/prettier': 'error',
            'no-unused-vars': 'warn',
        },
    },
]; 