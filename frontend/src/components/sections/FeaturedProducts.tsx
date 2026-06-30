'use client'

import { motion } from 'framer-motion'
import ProductCard, { Product } from '@/components/ui/ProductCard'

const SAMPLE_PRODUCTS: Product[] = [
  {
    _id: '1',
    name: 'Silk Floral Midi Dress',
    brand: 'Zara',
    price: 2999,
    originalPrice: 4999,
    image: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=533&fit=crop',
    rating: 4.8,
    reviewCount: 234,
    isSale: true,
  },
  {
    _id: '2',
    name: 'Oversized Linen Blazer',
    brand: 'Mango',
    price: 3499,
    image: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=533&fit=crop',
    rating: 4.6,
    reviewCount: 89,
    isNew: true,
  },
  {
    _id: '3',
    name: 'Vintage Wash Denim Jacket',
    brand: 'Levi\'s',
    price: 1499,
    originalPrice: 2500,
    image: 'https://images.unsplash.com/photo-1601333144130-8cbb312386b6?w=400&h=533&fit=crop',
    rating: 4.9,
    reviewCount: 412,
    condition: 'A',
  },
  {
    _id: '4',
    name: 'Boho Maxi Skirt',
    brand: 'H&M',
    price: 1299,
    image: 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=533&fit=crop',
    rating: 4.5,
    reviewCount: 67,
    isNew: true,
  },
  {
    _id: '5',
    name: 'Floral Co-ord Set',
    brand: 'AND',
    price: 3299,
    originalPrice: 4800,
    image: 'https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=400&h=533&fit=crop',
    rating: 4.7,
    reviewCount: 156,
    isSale: true,
  },
  {
    _id: '6',
    name: 'Relaxed Linen Trousers',
    brand: 'Uniqlo',
    price: 1899,
    image: 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&h=533&fit=crop',
    rating: 4.4,
    reviewCount: 203,
    condition: 'B',
  },
  {
    _id: '7',
    name: 'Wrap Tie Crop Top',
    brand: 'Zara',
    price: 1199,
    originalPrice: 1999,
    image: 'https://images.unsplash.com/photo-1564584217132-2271feaeb3c5?w=400&h=533&fit=crop',
    rating: 4.6,
    reviewCount: 334,
    isSale: true,
  },
  {
    _id: '8',
    name: 'Minimal Ribbed Sweater',
    brand: 'COS',
    price: 2299,
    image: 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=533&fit=crop',
    rating: 4.8,
    reviewCount: 78,
    isNew: true,
  },
]

export default function FeaturedProducts() {
  return (
    <section className="py-20 bg-[#FAFAF8]">
      <div className="section-container">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <p className="text-xs uppercase tracking-[0.25em] text-[#C9A96E] font-medium mb-3">
            Curated For You
          </p>
          <h2 className="font-serif text-4xl font-bold text-[#0A0A0A] mb-4">
            Trending Now
          </h2>
          <p className="text-[#737370] max-w-md mx-auto">
            Handpicked pieces our AI thinks you'll love — based on what's trending this season.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {SAMPLE_PRODUCTS.map((product, index) => (
            <ProductCard
              key={product._id}
              product={product}
              index={index}
            />
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="text-center mt-12"
        >
          <button className="btn-secondary">
            View All Products
          </button>
        </motion.div>

      </div>
    </section>
  )
}