/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone',
  modularizeImports: {
    '@mui/icons-material': {
      transform: '@mui/icons-material/{{member}}',
    },
  },
  transpilePackages: ['@mui/material', '@mui/system', '@mui/icons-material'],
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'https://fruits-api-app.azurewebsites.net/api/v1',
  }
}

module.exports = nextConfig 