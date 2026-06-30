import Navbar from '@/components/layout/Navbar'
import HeroSection from '@/components/sections/HeroSection'
import FeatureBanner from '@/components/sections/FeatureBanner'
import FeaturedProducts from '@/components/sections/FeaturedProducts'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <HeroSection />
      <FeatureBanner />
      <FeaturedProducts />
      <footer className="py-8 border-t border-[#E5E5E0] text-center text-xs text-[#737370]">
        © 2026 LUMIS — Fashion, Reimagined.
      </footer>
    </main>
  )
}