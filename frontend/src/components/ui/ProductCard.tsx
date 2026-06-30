'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Heart, ShoppingBag, Star } from 'lucide-react'
import Image from 'next/image'

export interface Product {
  _id: string
  name: string
  brand: string
  price: number
  originalPrice?: number
  image: string
  rating: number
  reviewCount: number
  condition?: string
  isNew?: boolean
  isSale?: boolean
}

interface ProductCardProps {
  product: Product
  index?: number
}

export default function ProductCard({ product, index = 0 }: ProductCardProps) {
  const [wishlisted, setWishlisted] = useState(false)
  const [added, setAdded] = useState(false)

  const handleAddToCart = () => {
    setAdded(true)
    setTimeout(() => setAdded(false), 1500)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.08, ease: 'easeOut' }}
      className="card group cursor-pointer"
    >

      <div className="relative aspect-[3/4] overflow-hidden bg-[#F5F5F3]">

        <Image
          src={product.image}
          alt={product.name}
          fill
          sizes="(max-width: 768px) 50vw, 25vw"
          className="object-cover transition-transform duration-500 group-hover:scale-105"
        />

        <div className="absolute top-3 left-3 flex flex-col gap-1">
          {product.isNew && (
            <span className="bg-[#0A0A0A] text-white text-[10px] font-medium px-2.5 py-1 rounded-full tracking-wider uppercase">
              New
            </span>
          )}
          {product.isSale && (
            <span className="bg-[#C9A96E] text-white text-[10px] font-medium px-2.5 py-1 rounded-full tracking-wider uppercase">
              Sale
            </span>
          )}
          {product.condition && (
            <span className={`text-white text-[10px] font-bold px-2.5 py-1 rounded-full
              ${product.condition === 'A' ? 'bg-green-600' : ''}
              ${product.condition === 'B' ? 'bg-blue-600' : ''}
              ${product.condition === 'C' ? 'bg-amber-500' : ''}
              ${product.condition === 'D' ? 'bg-red-600' : ''}
            `}>
              Grade {product.condition}
            </span>
          )}
        </div>

        <motion.button
          whileTap={{ scale: 0.85 }}
          onClick={(e) => {
            e.stopPropagation()
            setWishlisted(!wishlisted)
          }}
          className="absolute top-3 right-3 p-2 bg-white/90 backdrop-blur-sm rounded-full shadow-sm"
          aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
        >
          <motion.div
            animate={{
              scale: wishlisted ? [1, 1.3, 1] : 1,
            }}
            transition={{ duration: 0.3 }}
          >
            <Heart
              size={18}
              className={wishlisted ? 'fill-[#C9A96E] text-[#C9A96E]' : 'text-[#737370]'}
            />
          </motion.div>
        </motion.button>

        <div className="absolute bottom-0 left-0 right-0 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
          <motion.button
            whileTap={{ scale: 0.98 }}
            onClick={(e) => {
              e.stopPropagation()
              handleAddToCart()
            }}
            className={`w-full py-3 text-sm font-medium tracking-wide transition-colors duration-200
              ${added 
                ? 'bg-[#3B6D11] text-white' 
                : 'bg-[#0A0A0A] text-white hover:bg-[#C9A96E]'
              }
            `}
          >
            <span className="flex items-center justify-center gap-2">
              <ShoppingBag size={16} />
              {added ? 'Added!' : 'Add to Cart'}
            </span>
          </motion.button>
        </div>
      </div>

      <div className="p-4">

        <p className="text-xs text-[#737370] font-medium uppercase tracking-wider mb-1">
          {product.brand}
        </p>

        <h3 className="text-sm font-medium text-[#0A0A0A] mb-2 line-clamp-2 leading-snug">
          {product.name}
        </h3>

        <div className="flex items-center gap-1 mb-3">
          <Star size={12} className="fill-[#C9A96E] text-[#C9A96E]" />
          <span className="text-xs text-[#737370]">
            {product.rating} ({product.reviewCount})
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="font-semibold text-[#0A0A0A]">
            ₹{product.price.toLocaleString('en-IN')}
          </span>
          {product.originalPrice && (
            <span className="text-xs text-[#737370] line-through">
              ₹{product.originalPrice.toLocaleString('en-IN')}
            </span>
          )}
          {product.originalPrice && (
            <span className="text-xs text-[#3B6D11] font-medium">
              {Math.round((1 - product.price / product.originalPrice) * 100)}% off
            </span>
          )}
        </div>

      </div>
    </motion.div>
  )
}