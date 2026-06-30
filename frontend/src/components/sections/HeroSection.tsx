'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Sparkles, ArrowRight } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function HeroSection() {
  const [query, setQuery] = useState('')
  const [focused, setFocused] = useState(false)
  const router = useRouter()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    router.push(`/search?q=${encodeURIComponent(query)}`)
  }

  const suggestions = [
    'flowy dress for beach wedding',
    'minimalist work blazer',
    'vintage denim jacket',
    'boho maxi skirt',
  ]

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-32 overflow-hidden">

      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-[#FAFAF8]" />
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full bg-[#C9A96E]/10 blur-[80px]" />
        <div className="absolute top-20 -right-40 w-[500px] h-[500px] rounded-full bg-rose-100/60 blur-[100px]" />
        <div className="absolute -bottom-20 left-1/2 -translate-x-1/2 w-[800px] h-[300px] rounded-full bg-[#C9A96E]/5 blur-[60px]" />
      </div>

      <div className="section-container text-center relative z-10">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="inline-flex items-center gap-2 bg-[#C9A96E]/10 border border-[#C9A96E]/20 text-[#B8935A] text-sm font-medium px-4 py-2 rounded-full mt-4 mb-8"
        >
          <Sparkles size={14} />
          AI-Powered Fashion Discovery
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="font-serif text-5xl md:text-7xl font-bold text-[#0A0A0A] leading-tight mb-6"
        >
          Find it.{' '}
          <span className="text-[#C9A96E]">Flaunt it.</span>
          <br />
          Feel it.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-[#737370] text-lg md:text-xl max-w-xl mx-auto mb-10 leading-relaxed"
        >
          Describe what you're looking for in plain English.
          Our AI finds it — not by keywords, but by meaning.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="max-w-2xl mx-auto mb-6"
        >
          <motion.div
            animate={{
              boxShadow: focused
                ? '0 0 0 3px rgba(201, 169, 110, 0.25), 0 8px 40px rgba(0,0,0,0.08)'
                : '0 2px 20px rgba(0,0,0,0.06)',
            }}
            transition={{ duration: 0.2 }}
            className="relative bg-white rounded-2xl border border-[#E5E5E0] overflow-hidden"
          >
            <form onSubmit={handleSearch} className="flex items-center">

              <div className="pl-5 pr-3 text-[#C9A96E]">
                <Search size={22} />
              </div>

              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                placeholder="Try: flowy dress for a beach wedding..."
                className="flex-1 py-5 pr-4 text-base text-[#0A0A0A] placeholder:text-[#C4C4C0] bg-transparent outline-none"
              />

              <motion.button
                type="submit"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="m-2 btn-primary text-sm px-6 py-3"
              >
                <span className="hidden sm:block">Search</span>
                <ArrowRight size={18} className="sm:hidden" />
              </motion.button>

            </form>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="flex flex-wrap justify-center gap-2 mb-16"
        >
          <span className="text-xs text-[#737370] flex items-center mr-1">Try:</span>
          {suggestions.map((s, i) => (
            <motion.button
              key={s}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.7 + i * 0.08 }}
              whileHover={{ scale: 1.03, backgroundColor: '#E8D5B0' }}
              onClick={() => setQuery(s)}
              className="text-xs bg-white border border-[#E5E5E0] text-[#737370] px-3 py-1.5 rounded-full cursor-pointer transition-colors hover:border-[#C9A96E] hover:text-[#B8935A]"
            >
              {s}
            </motion.button>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="flex flex-wrap justify-center gap-8 md:gap-16 pb-16"
        >
          {[
            { number: '10K+', label: 'Products' },
            { number: 'AI', label: 'Semantic Search' },
            { number: '4.9★', label: 'User Rating' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="font-serif text-2xl font-bold text-[#0A0A0A]">{stat.number}</div>
              <div className="text-xs text-[#737370] mt-1 tracking-wide uppercase">{stat.label}</div>
            </div>
          ))}
        </motion.div>

      </div>
    </section>
  )
}