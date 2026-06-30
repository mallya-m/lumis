'use client'

import { motion } from 'framer-motion'
import { Search, Camera, Sparkles } from 'lucide-react'

const features = [
  {
    icon: Search,
    title: 'Semantic Search',
    description: 'Describe it in plain English. Our AI understands meaning, not just keywords.',
  },
  {
    icon: Camera,
    title: 'AI Condition Grading',
    description: 'Upload a photo of secondhand clothing — get an instant grade, description & price.',
  },
  {
    icon: Sparkles,
    title: 'Personalized Discovery',
    description: 'The more you use LUMIS, the better it understands your style.',
  },
]

export default function FeatureBanner() {
  return (
    <section className="py-20 bg-[#0A0A0A]">
      <div className="section-container">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          {features.map((feature, i) => {
            const Icon = feature.icon
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
                className="text-center"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 bg-[#C9A96E]/15 rounded-2xl mb-4">
                  <Icon size={22} className="text-[#C9A96E]" />
                </div>
                <h3 className="font-serif text-xl font-semibold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-[#737370] text-sm leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}