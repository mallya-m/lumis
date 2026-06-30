'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ShoppingBag, Search, Heart, Menu, X } from 'lucide-react'
import { SignInButton, SignUpButton, UserButton, useAuth } from '@clerk/nextjs'

export default function Navbar() {
  const { isSignedIn, isLoaded } = useAuth()
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/search', label: 'Discover' },
    { href: '/sell', label: 'Sell' },
    { href: '/about', label: 'About' },
  ]

  return (
    <motion.nav
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      className={`
        fixed top-0 left-0 right-0 z-50
        transition-all duration-300
        ${scrolled
          ? 'bg-white/80 backdrop-blur-md border-b border-[#E5E5E0] shadow-sm'
          : 'bg-transparent'
        }
      `}
    >
      <div className="section-container">
        <div className="flex items-center justify-between h-16">

          <Link href="/">
            <span className="font-serif text-2xl font-bold text-[#C9A96E] tracking-widest">
              LUMIS
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm text-[#737370] hover:text-[#0A0A0A] transition-colors duration-200 font-medium tracking-wide"
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-3">

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 text-[#737370] hover:text-[#0A0A0A] transition-colors"
              aria-label="Search"
            >
              <Search size={20} />
            </motion.button>

            {isSignedIn && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-[#737370] hover:text-[#C9A96E] transition-colors"
                aria-label="Wishlist"
              >
                <Heart size={20} />
              </motion.button>
            )}

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 text-[#737370] hover:text-[#0A0A0A] transition-colors relative"
              aria-label="Cart"
            >
              <ShoppingBag size={20} />
              <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-[#C9A96E] text-white text-xs rounded-full flex items-center justify-center font-medium">
                0
              </span>
            </motion.button>

            {isLoaded && (
                !isSignedIn ? (
                    <SignInButton mode="modal">
                    <button className="hidden md:block btn-secondary text-sm py-1.5 px-4">
                        Sign In
                    </button>
                    </SignInButton>
                ) : (
                    <UserButton />
                )
            )}

            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => setMenuOpen(!menuOpen)}
              className="md:hidden p-2 text-[#737370]"
              aria-label="Toggle menu"
            >
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </motion.button>

          </div>
        </div>
      </div>

      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2, ease: 'easeInOut' }}
            className="md:hidden bg-white border-b border-[#E5E5E0] overflow-hidden"
          >
            <div className="section-container py-4 flex flex-col gap-4">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMenuOpen(false)}
                  className="text-sm text-[#737370] hover:text-[#0A0A0A] font-medium py-1"
                >
                  {link.label}
                </Link>
              ))}
              {!isSignedIn && (
                <div className="flex gap-3 pt-2">
                  <SignInButton mode="modal">
                    <button className="btn-secondary text-sm py-1.5 px-4">Sign In</button>
                  </SignInButton>
                  <SignUpButton mode="modal">
                    <button className="btn-primary text-sm py-1.5 px-4">Sign Up</button>
                  </SignUpButton>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  )
}