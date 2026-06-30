'use client'

import { LazyMotion, domAnimation } from 'framer-motion'

export default function MotionWrapper({ children }: { children: React.ReactNode }) {
  return (
    <LazyMotion features={domAnimation}>
      {children}
    </LazyMotion>
  )
}