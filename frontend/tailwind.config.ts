import type {Config} from 'tailwindcss';

const config : Config = {
    content:[
        './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
        './src/components/**/*.{js,ts,jsx,tsx,mdx}',
        './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme:{
        extend:{
            fontFamily: {
                sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
                serif: ['var(--font-playfair)', 'Georgia', 'serif'],
            },
             colors: {
                gold: {
                DEFAULT: '#C9A96E',  
                light: '#E8D5B0',    
                dark: '#B8935A',    
                },
                cream: '#FAFAF8',  
            },
            borderRadius: {
                '3xl': '1.5rem',   // for large cards
                '4xl': '2rem',     // for hero sections
            }
        },
    },
    plugins: [],
}
export default config