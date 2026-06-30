import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import './globals.css'
import { ClerkProvider } from '@clerk/nextjs'
import MotionWrapper from '@/components/ui/MotionWrapper'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const playfair = Playfair_Display({ 
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'LUMIS — Fashion, Reimagined',
  description: 'AI-powered semantic fashion search and secondhand clothing grader',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={`${inter.variable} ${playfair.variable} font-sans antialiased`}>
          <MotionWrapper>
            {children}
          </MotionWrapper>
        </body>
      </html>
    </ClerkProvider>
  )
}