import os
import sys
import requests
import time
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------
# 50 fashion products with rich text descriptions
# The description is what gets embedded — not just the name
# Richer description = better search results
# e.g. "Flowy chiffon midi dress perfect for beach weddings and summer events,
#        soft pastel tones, elegant silhouette" 
# will match "flowy dress for beach wedding" much better than just "Midi Dress"
# -----------------------------------------------------------------------
PRODUCTS = [
    {
        "name": "Silk Floral Midi Dress",
        "brand": "Zara",
        "price": 2999,
        "originalPrice": 4999,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=533&fit=crop",
        "rating": 4.8,
        "reviewCount": 234,
        "isSale": True,
        "description": "Elegant silk floral midi dress with delicate print, perfect for garden parties, beach weddings, and summer occasions. Flowy silhouette with feminine details.",
    },
    {
        "name": "Oversized Linen Blazer",
        "brand": "Mango",
        "price": 3499,
        "category": "outerwear",
        "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 89,
        "isNew": True,
        "description": "Relaxed oversized linen blazer in neutral tones. Minimalist office wear, smart casual workwear blazer that pairs with trousers or jeans.",
    },
    {
        "name": "Vintage Wash Denim Jacket",
        "brand": "Levis",
        "price": 1499,
        "originalPrice": 2500,
        "category": "outerwear",
        "image": "https://images.unsplash.com/photo-1601333144130-8cbb312386b6?w=400&h=533&fit=crop",
        "rating": 4.9,
        "reviewCount": 412,
        "condition": "A",
        "description": "Classic vintage wash denim jacket, retro 90s style, great for casual college outfits, streetwear layering, and everyday looks.",
    },
    {
        "name": "Boho Maxi Skirt",
        "brand": "H&M",
        "price": 1299,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 67,
        "isNew": True,
        "description": "Flowy bohemian maxi skirt with earthy tones and ethnic print. Perfect for beach vacations, festival outfits, and boho casual wear.",
    },
    {
        "name": "Floral Co-ord Set",
        "brand": "AND",
        "price": 3299,
        "originalPrice": 4800,
        "category": "sets",
        "image": "https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=400&h=533&fit=crop",
        "rating": 4.7,
        "reviewCount": 156,
        "isSale": True,
        "description": "Matching floral co-ord set with crop top and wide-leg pants. Trendy summer set perfect for brunch, parties, and Instagram-worthy outfits.",
    },
    {
        "name": "Relaxed Linen Trousers",
        "brand": "Uniqlo",
        "price": 1899,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&h=533&fit=crop",
        "rating": 4.4,
        "reviewCount": 203,
        "condition": "B",
        "description": "Breathable linen wide-leg trousers in neutral beige. Minimalist wardrobe staple, great for office, travel, and smart casual occasions.",
    },
    {
        "name": "Wrap Tie Crop Top",
        "brand": "Zara",
        "price": 1199,
        "originalPrice": 1999,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1564584217132-2271feaeb3c5?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 334,
        "isSale": True,
        "description": "Flirty wrap tie crop top in soft satin fabric. Perfect for date nights, parties, and pairing with high-waisted jeans or skirts.",
    },
    {
        "name": "Minimal Ribbed Sweater",
        "brand": "COS",
        "price": 2299,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=533&fit=crop",
        "rating": 4.8,
        "reviewCount": 78,
        "isNew": True,
        "description": "Clean minimal ribbed knit sweater in off-white. Capsule wardrobe essential, cozy and elegant for autumn and winter layering.",
    },
    {
        "name": "High-Waist Straight Jeans",
        "brand": "Levis",
        "price": 2799,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=533&fit=crop",
        "rating": 4.7,
        "reviewCount": 521,
        "description": "Classic high-waist straight-fit blue jeans. Wardrobe staple that pairs with everything — crop tops, blazers, or tucked-in shirts.",
    },
    {
        "name": "Satin Slip Dress",
        "brand": "Mango",
        "price": 2599,
        "originalPrice": 3800,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 189,
        "isSale": True,
        "description": "Elegant satin slip dress in champagne gold. Minimalist evening wear, cocktail parties, and date night outfit.",
    },
    {
        "name": "Flowy Chiffon Maxi Dress",
        "brand": "Fabindia",
        "price": 1799,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 143,
        "description": "Dreamy flowy chiffon maxi dress in pastel lavender. Perfect for beach weddings, destination events, and summer vacations.",
    },
    {
        "name": "Structured White Shirt",
        "brand": "Marks & Spencer",
        "price": 1599,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 298,
        "description": "Crisp structured white cotton shirt, perfect for office workwear, smart casual looks, and can be styled with jeans or trousers.",
    },
    {
        "name": "Pleated Mini Skirt",
        "brand": "Zara",
        "price": 1399,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400&h=533&fit=crop",
        "rating": 4.4,
        "reviewCount": 167,
        "isNew": True,
        "description": "Cute pleated mini skirt in camel brown. Y2K inspired, pairs with crop tops, oversized sweaters, and boots for college outfits.",
    },
    {
        "name": "Ethnic Printed Kurta",
        "brand": "Biba",
        "price": 1299,
        "category": "ethnic",
        "image": "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=533&fit=crop",
        "rating": 4.8,
        "reviewCount": 445,
        "description": "Vibrant ethnic printed straight kurta with intricate block prints. For festive occasions, traditional celebrations, and daily ethnic wear.",
    },
    {
        "name": "Knit Cardigan",
        "brand": "H&M",
        "price": 1699,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=533&fit=crop",
        "rating": 4.3,
        "reviewCount": 234,
        "description": "Cozy oversized knit cardigan in dusty rose. Perfect for autumn layering, casual college outfits, and loungewear styling.",
    },
    {
        "name": "Leather Crossbody Bag",
        "brand": "Charles & Keith",
        "price": 2199,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=533&fit=crop",
        "rating": 4.7,
        "reviewCount": 312,
        "description": "Compact leather crossbody bag in black. Versatile everyday bag that works with casual and formal outfits.",
    },
    {
        "name": "Wide Brim Sun Hat",
        "brand": "Accessorize",
        "price": 899,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1521369909029-2afed882baee?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 89,
        "description": "Chic wide brim straw sun hat, perfect for beach days, summer vacations, and outdoor brunches.",
    },
    {
        "name": "Strappy Block Heel Sandals",
        "brand": "Steve Madden",
        "price": 2899,
        "category": "footwear",
        "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=533&fit=crop",
        "rating": 4.4,
        "reviewCount": 178,
        "description": "Elegant strappy block heel sandals in nude. Comfortable and stylish for parties, dates, and semi-formal occasions.",
    },
    {
        "name": "Printed Palazzo Pants",
        "brand": "Global Desi",
        "price": 999,
        "originalPrice": 1799,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1516762689617-e1cffcef479d?w=400&h=533&fit=crop",
        "rating": 4.3,
        "reviewCount": 267,
        "isSale": True,
        "description": "Flowy printed palazzo pants with ethnic motifs. Comfortable Indo-western fusion wear for casual and festive occasions.",
    },
    {
        "name": "Cropped Denim Jacket",
        "brand": "Roadster",
        "price": 1799,
        "category": "outerwear",
        "image": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 389,
        "condition": "A",
        "description": "Cropped light wash denim jacket. 90s streetwear style, pairs with midi skirts, dresses, or high-waist jeans.",
    },
    {
        "name": "Off-Shoulder Ruffle Blouse",
        "brand": "Forever 21",
        "price": 899,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400&h=533&fit=crop",
        "rating": 4.2,
        "reviewCount": 145,
        "description": "Romantic off-shoulder ruffle blouse in white. Perfect for beach vacations, summer parties, and date night looks.",
    },
    {
        "name": "Embroidered Anarkali Suit",
        "brand": "W",
        "price": 3999,
        "originalPrice": 5999,
        "category": "ethnic",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400&h=533&fit=crop",
        "rating": 4.9,
        "reviewCount": 234,
        "isSale": True,
        "description": "Royal embroidered Anarkali suit with heavy embellishments. For weddings, festivals, engagement ceremonies, and special occasions.",
    },
    {
        "name": "Workout Leggings",
        "brand": "Decathlon",
        "price": 799,
        "category": "activewear",
        "image": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 567,
        "description": "High-performance stretchy workout leggings with moisture-wicking fabric. For gym, yoga, running, and active lifestyle.",
    },
    {
        "name": "Sports Bra",
        "brand": "Nike",
        "price": 1299,
        "category": "activewear",
        "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&h=533&fit=crop",
        "rating": 4.7,
        "reviewCount": 423,
        "description": "Supportive sports bra with breathable mesh panels. Ideal for high-intensity workouts, yoga sessions, and gym training.",
    },
    {
        "name": "Trench Coat",
        "brand": "Mango",
        "price": 5999,
        "originalPrice": 8999,
        "category": "outerwear",
        "image": "https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=400&h=533&fit=crop",
        "rating": 4.8,
        "reviewCount": 178,
        "isSale": True,
        "description": "Classic beige trench coat with belt. Timeless outerwear for rainy days, autumn, and smart casual or office looks.",
    },
    {
        "name": "Sequin Party Dress",
        "brand": "ASOS",
        "price": 3299,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 89,
        "isNew": True,
        "description": "Dazzling sequin mini dress for NYE parties, clubbing, bachelorette nights, and cocktail events. Glamorous and eye-catching.",
    },
    {
        "name": "Linen Co-ord Set",
        "brand": "Mulmul",
        "price": 2499,
        "category": "sets",
        "image": "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 134,
        "description": "Breezy linen co-ord set in ivory white. Effortless summer style for brunch dates, travel, and relaxed daytime occasions.",
    },
    {
        "name": "Floral Maxi Sundress",
        "brand": "Zara",
        "price": 2799,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400&h=533&fit=crop",
        "rating": 4.7,
        "reviewCount": 312,
        "description": "Vibrant floral maxi sundress for vacation, beach walks, and tropical holiday outfits. Light and comfortable.",
    },
    {
        "name": "Blazer Dress",
        "brand": "AND",
        "price": 3799,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 98,
        "isNew": True,
        "description": "Chic blazer dress for powerful office looks and workwear fashion. Professional yet stylish, perfect for business meetings.",
    },
    {
        "name": "Tie-Dye Oversized Tee",
        "brand": "H&M",
        "price": 699,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=400&h=533&fit=crop",
        "rating": 4.3,
        "reviewCount": 234,
        "description": "Fun tie-dye oversized t-shirt in pastel colors. Casual college outfit, weekend wear, and athleisure styling.",
    },
    {
        "name": "Gold Hoop Earrings",
        "brand": "Accessorize",
        "price": 599,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400&h=533&fit=crop",
        "rating": 4.7,
        "reviewCount": 456,
        "description": "Classic gold hoop earrings, medium size. Versatile jewelry that elevates any outfit from casual to formal.",
    },
    {
        "name": "Silk Scarf",
        "brand": "Zara",
        "price": 999,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 123,
        "description": "Luxurious printed silk scarf in multicolor. Style as headscarf, necktie, or bag accessory for chic fashion looks.",
    },
    {
        "name": "White Sneakers",
        "brand": "Adidas",
        "price": 3499,
        "category": "footwear",
        "image": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&h=533&fit=crop",
        "rating": 4.8,
        "reviewCount": 678,
        "description": "Clean white minimalist sneakers. Essential for streetwear, casual outfits, college looks, and everyday comfortable wear.",
    },
    {
        "name": "Ruched Bodycon Dress",
        "brand": "Shein",
        "price": 899,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=533&fit=crop",
        "rating": 4.2,
        "reviewCount": 345,
        "description": "Curve-hugging ruched bodycon dress in black. Perfect for nightouts, parties, and date nights where you want to dress up.",
    },
    {
        "name": "Pashmina Shawl",
        "brand": "Fabindia",
        "price": 1599,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400&h=533&fit=crop",
        "rating": 4.8,
        "reviewCount": 189,
        "description": "Soft pashmina wool shawl in classic checks. Warm and elegant for winters, ethnic occasions, and travel.",
    },
    {
        "name": "Denim Shorts",
        "brand": "Levis",
        "price": 1299,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f43?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 289,
        "description": "Classic cut-off denim shorts. Summer staple for beach days, casual outings, and festival fashion.",
    },
    {
        "name": "Puffer Jacket",
        "brand": "The North Face",
        "price": 6999,
        "category": "outerwear",
        "image": "https://images.unsplash.com/photo-1544923246-77307dd654cb?w=400&h=533&fit=crop",
        "rating": 4.9,
        "reviewCount": 234,
        "description": "Warm quilted puffer jacket for cold weather. Perfect for winter travel, hill stations, and outdoor activities.",
    },
    {
        "name": "Printed Wrap Dress",
        "brand": "Vero Moda",
        "price": 2199,
        "originalPrice": 3299,
        "category": "dresses",
        "image": "https://images.unsplash.com/photo-1572804013427-4d7ca7268217?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 167,
        "isSale": True,
        "description": "Flattering printed wrap dress that suits all body types. Elegant for work, brunches, and semi-formal events.",
    },
    {
        "name": "Crochet Beach Cover-Up",
        "brand": "H&M",
        "price": 1099,
        "category": "beachwear",
        "image": "https://images.unsplash.com/photo-1570976447640-ac859083963f?w=400&h=533&fit=crop",
        "rating": 4.4,
        "reviewCount": 98,
        "description": "Boho crochet beach cover-up dress. Perfect for beach vacations, poolside lounging, and tropical holidays.",
    },
    {
        "name": "Embellished Clutch",
        "brand": "Aldo",
        "price": 1799,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 145,
        "description": "Sparkling embellished clutch bag. Essential for weddings, parties, and formal evening events.",
    },
    {
        "name": "Yoga Pants",
        "brand": "Reebok",
        "price": 1599,
        "category": "activewear",
        "image": "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 312,
        "description": "Flexible high-waist yoga pants with 4-way stretch. For yoga, pilates, gym workouts, and comfortable daily wear.",
    },
    {
        "name": "Kurti with Palazzo",
        "brand": "Libas",
        "price": 1499,
        "category": "ethnic",
        "image": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 378,
        "description": "Comfortable kurti and palazzo set in cotton. Everyday ethnic wear for office, casual outings, and family gatherings.",
    },
    {
        "name": "Sling Bag",
        "brand": "Baggit",
        "price": 1299,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=533&fit=crop",
        "rating": 4.4,
        "reviewCount": 234,
        "description": "Compact vegan leather sling bag for daily use. Fits essentials, perfect for college, travel, and casual outings.",
    },
    {
        "name": "Flared Trousers",
        "brand": "Zara",
        "price": 2499,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 156,
        "isNew": True,
        "description": "Retro flared trousers in earthy brown. 70s inspired boho fashion, pairs with fitted tops and platform shoes.",
    },
    {
        "name": "Sheer Printed Saree",
        "brand": "Nalli",
        "price": 4999,
        "category": "ethnic",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400&h=533&fit=crop",
        "rating": 4.9,
        "reviewCount": 267,
        "description": "Elegant sheer georgette printed saree with matching blouse. For weddings, festivals, and traditional celebrations.",
    },
    {
        "name": "Chunky Knit Sweater",
        "brand": "Marks & Spencer",
        "price": 2799,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 189,
        "description": "Cozy chunky knit oversized sweater in camel. Winter wardrobe staple for cold days, hill station trips, and layered looks.",
    },
    {
        "name": "Slip-On Loafers",
        "brand": "Clarks",
        "price": 2999,
        "category": "footwear",
        "image": "https://images.unsplash.com/photo-1533681904393-9ab6eee7e408?w=400&h=533&fit=crop",
        "rating": 4.6,
        "reviewCount": 198,
        "description": "Classic leather slip-on loafers in tan brown. Versatile footwear for office, college, and smart casual occasions.",
    },
    {
        "name": "Strapless Tube Top",
        "brand": "Mango",
        "price": 899,
        "category": "tops",
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400&h=533&fit=crop",
        "rating": 4.3,
        "reviewCount": 123,
        "description": "Sleek strapless tube top in black satin. Pairs with high-waist pants or skirts for a chic night-out look.",
    },
    {
        "name": "Beaded Necklace Set",
        "brand": "Accessorize",
        "price": 799,
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=533&fit=crop",
        "rating": 4.5,
        "reviewCount": 167,
        "description": "Layered beaded necklace set in pastel colors. Boho jewelry for casual styling, beach looks, and festival fashion.",
    },
    {
        "name": "Cargo Pants",
        "brand": "Roadster",
        "price": 1799,
        "category": "bottoms",
        "image": "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?w=400&h=533&fit=crop",
        "rating": 4.4,
        "reviewCount": 289,
        "isNew": True,
        "description": "Trendy utility cargo pants with multiple pockets. Y2K streetwear style, perfect for casual college outfits and urban fashion.",
    },
]


def seed_database():
    print("Starting LUMIS database seed...")
    print(f"Total products to seed: {len(PRODUCTS)}")

    print("\nConnecting to MongoDB Atlas...")
    client = MongoClient(os.getenv('MONGODB_URI'), tlsCAFile=certifi.where())
    db = client['lumis']                   
    collection = db['products']           
   
    existing = collection.count_documents({})
    if existing > 0:
        print(f"Clearing {existing} existing products...")
        collection.delete_many({})
    
    print("\nRequesting embeddings from Flask server...")
    print("(Make sure your Python Flask server is running on port 8000!)")

    descriptions = [p['description'] for p in PRODUCTS]
    
    try:
        response = requests.post(
            'http://localhost:8000/embed-batch',
            json={'texts': descriptions},
            timeout=120
           )
        response.raise_for_status()
        
        embeddings = response.json()['embeddings']
        print(f"Got {len(embeddings)} embeddings, each with {len(embeddings[0])} dimensions")

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Flask server!")
        print("Please run 'python app.py' in another terminal first.")
        sys.exit(1)
        
    print("\nInserting products into MongoDB...")
    
    documents = []
    for i, product in enumerate(PRODUCTS):
        doc = {
            **product,          
            'embedding': embeddings[i],   
            'createdAt': time.time(),     
        }
        documents.append(doc)

    result = collection.insert_many(documents)
    print(f"Inserted {len(result.inserted_ids)} products successfully!")

    collection.create_index('category')
    collection.create_index('brand')
    print("Created indexes on 'category' and 'brand'")

    
    sample = collection.find_one({}, {'name': 1, 'brand': 1, 'embedding': 1})
    print(f"\nSample product: {sample['name']} by {sample['brand']}")
    print(f"Embedding preview: {sample['embedding'][:5]}... (showing first 5 of 384)")

    print("\nSeed complete!")
    print(f"Total products in database: {collection.count_documents({})}")
    print("\nNext step: Create the Vector Search index in MongoDB Atlas UI")
    
    client.close()


if __name__ == '__main__':
    seed_database()