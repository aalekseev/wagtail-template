module.exports = {
  mode: 'jit',
  content: [
    '/backend/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
