/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'export',
  distDir: 'out',
  modularizeImports: {
    '@mui/icons-material': {
      transform: '@mui/icons-material/{{member}}',
    },
  },
  transpilePackages: ['@mui/material', '@mui/system', '@mui/icons-material'],
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'https://fruits-api-app.azurewebsites.net/api/v1',
  },
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig 