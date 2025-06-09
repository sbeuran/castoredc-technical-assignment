import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Fruits API Frontend',
  description: 'A frontend application for the Fruits API',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-[#0f1535]`}>
        <div className="min-h-screen">
          <nav className="bg-[#1a1f37] border-b border-gray-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="h-16 flex items-center">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">🍎</span>
                  <h1 className="text-lg font-bold text-white">
                    Fruits API
                  </h1>
                </div>
              </div>
            </div>
          </nav>
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              {children}
            </div>
          </main>
        </div>
        <Toaster 
          position="top-right"
          toastOptions={{
            style: {
              background: '#1a1f37',
              color: '#fff',
              border: '1px solid rgba(255,255,255,0.1)',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#4ade80',
                secondary: '#1a1f37',
              },
            },
            error: {
              duration: 4000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#1a1f37',
              },
            },
          }}
        />
      </body>
    </html>
  )
} 