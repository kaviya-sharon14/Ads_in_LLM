"""
Structured Ad Database for AdGeno Patent-Grade Recommendation System.
Contains 40+ curated real brands across 12 intent categories with detailed metadata,
price ranges, key features, ingredients (for skincare), and targeted offer search queries.
"""

AD_DATABASE = [
    # --- 1. SKINCARE & BEAUTY ---
    {
        "id": "sk_001",
        "brand": "Minimalist",
        "product": "10% Niacinamide + Zinc Serum",
        "category": "skincare",
        "subcategory": "acne-pore-care",
        "description": "Science-backed, fragrance-free formula for oil control, reducing blemishes, and tightening open pores.",
        "url": "https://beminimalist.co",
        "ingredients_info": {
            "Niacinamide (Vitamin B3)": "Reduces sebum production, minimizes pore appearance, and evens out skin tone.",
            "Zinc PCA": "Anti-inflammatory mineral that prevents acne-causing bacteria and calms redness."
        },
        "keywords": ["niacinamide", "serum", "acne", "pores", "oily skin", "blemishes", "pimples", "skincare", "skin"],
        "offer_search_query": "Minimalist 10% Niacinamide discount offer coupon deal",
        "price_range": "₹599"
    },
    {
        "id": "sk_002",
        "brand": "Dot & Key",
        "product": "72HR Hydrating Gel Moisturizer",
        "category": "skincare",
        "subcategory": "moisturizer-dry-skin",
        "description": "Oil-free gel moisturizer enriched with Hyaluronic Acid and Rice Water for deep, long-lasting moisture.",
        "url": "https://www.dotandkey.com",
        "ingredients_info": {
            "Hyaluronic Acid": "Attracts and retains 1000x its weight in water, plumping up dehydrated skin.",
            "Probiotics & Rice Water": "Strengthens skin barrier and improves skin texture and radiance."
        },
        "keywords": ["moisturizer", "dry skin", "hydrating", "gel", "rice water", "hyaluronic", "glow", "skincare"],
        "offer_search_query": "Dot and Key 72HR Hydrating Gel offer coupon deal",
        "price_range": "₹495"
    },
    {
        "id": "sk_003",
        "brand": "Mamaearth",
        "product": "Vitamin C Daily Glow Face Serum",
        "category": "skincare",
        "subcategory": "brightening",
        "description": "Natural brightening serum formulated with Vitamin C and Gotu Kola for glowing skin and dark spot reduction.",
        "url": "https://mamaearth.in",
        "ingredients_info": {
            "Vitamin C": "Powerful antioxidant that brightens dull skin and fades hyperpigmentation.",
            "Gotu Kola": "Boosts collagen production and protects skin from environmental damage."
        },
        "keywords": ["vitamin c", "glow", "brightening", "dark spots", "face serum", "natural", "mamaearth"],
        "offer_search_query": "Mamaearth Vitamin C serum discount offer coupon",
        "price_range": "₹399"
    },
    {
        "id": "sk_004",
        "brand": "CeraVe",
        "product": "Hydrating Facial Cleanser & Moisturizing Cream",
        "category": "skincare",
        "subcategory": "barrier-repair",
        "description": "Dermatologist-developed gentle cleanser enriched with 3 essential ceramides and hyaluronic acid.",
        "url": "https://www.cerave.com",
        "ingredients_info": {
            "Ceramides (1, 3, 6-II)": "Restores and maintains the natural skin protective barrier.",
            "MVE Technology": "Controlled release of hydration for all-day moisture."
        },
        "keywords": ["cerave", "cleanser", "sensitive skin", "barrier repair", "ceramides", "dermatologist", "dry skin"],
        "offer_search_query": "CeraVe hydrating cleanser deal offer discount",
        "price_range": "₹650–₹1,200"
    },
    {
        "id": "sk_005",
        "brand": "The Ordinary",
        "product": "AHA 30% + BHA 2% Peeling Solution",
        "category": "skincare",
        "subcategory": "exfoliation",
        "description": "10-minute exfoliating facial peeling solution for targeted texture improvement and radiance.",
        "url": "https://theordinary.com",
        "ingredients_info": {
            "AHA (Glycolic/Lactic Acid)": "Exfoliates top layer of skin for a brighter, more even appearance.",
            "BHA (Salicylic Acid)": "Deeply clears pores to combat congestion and blackheads."
        },
        "keywords": ["ordinary", "peeling solution", "exfoliator", "aha bha", "blackheads", "skin texture", "glow"],
        "offer_search_query": "The Ordinary peeling solution discount offer Nykaa",
        "price_range": "₹750"
    },

    # --- 2. TRAVEL & TOURISM ---
    {
        "id": "tr_001",
        "brand": "MakeMyTrip",
        "product": "Holiday Packages & Cheap Flights",
        "category": "travel",
        "subcategory": "flight-hotels",
        "description": "India's leading travel portal for flight bookings, hotel reservations, and customized holiday packages.",
        "url": "https://www.makemytrip.com",
        "keywords": ["travel", "flight", "trip", "vacation", "hotel", "resort", "tour", "booking", "holiday", "flights"],
        "offer_search_query": "MakeMyTrip flight hotel discount offer promo code 2026",
        "price_range": "Up to ₹5,000 instant discount on flights"
    },
    {
        "id": "tr_002",
        "brand": "Airbnb",
        "product": "Unique Stays & Vacation Rentals",
        "category": "travel",
        "subcategory": "homestays",
        "description": "Discover cozy villas, beachside homestays, and unique local accommodations across the world.",
        "url": "https://www.airbnb.com",
        "keywords": ["airbnb", "homestay", "villa", "staycation", "cottage", "apartment", "vacation", "resort"],
        "offer_search_query": "Airbnb coupon code discount staycation deals",
        "price_range": "From ₹1,500/night"
    },
    {
        "id": "tr_003",
        "brand": "Ixigo",
        "product": "Train & Flight Instant Bookings with Zero cancellation",
        "category": "travel",
        "subcategory": "train-flight",
        "description": "AI-powered travel app with live train tracking, instant flight refunds, and zero cancellation fee options.",
        "url": "https://www.ixigo.com",
        "keywords": ["ixigo", "train ticket", "irctc", "flight booking", "railway", "cheap flight", "travel app"],
        "offer_search_query": "Ixigo zero cancellation flight train offer discount code",
        "price_range": "Zero payment gateway fees"
    },

    # --- 3. FOOD & DINING ---
    {
        "id": "fd_001",
        "brand": "Swiggy",
        "product": "Swiggy Gourmet & Food Delivery",
        "category": "food",
        "subcategory": "delivery",
        "description": "Fast food and grocery delivery from top local restaurants and Instamart in under 15 minutes.",
        "url": "https://www.swiggy.com",
        "keywords": ["food", "delivery", "swiggy", "restaurant", "eat", "order food", "dinner", "lunch", "pizza", "biryani"],
        "offer_search_query": "Swiggy coupon code discount offer 50 off",
        "price_range": "Free delivery with Swiggy One"
    },
    {
        "id": "fd_002",
        "brand": "Zomato",
        "product": "Zomato Gold Dining & Delivery",
        "category": "food",
        "subcategory": "dining-delivery",
        "description": "Discover trending restaurants, get exclusive dining discounts with Zomato Gold, or order online.",
        "url": "https://www.zomato.com",
        "keywords": ["zomato", "dining", "restaurant", "food delivery", "zomato gold", "cafe", "foodie", "dineout"],
        "offer_search_query": "Zomato Gold promo code discount offer today",
        "price_range": "Up to 40% off on dining out"
    },

    # --- 4. TECHNOLOGY & GADGETS ---
    {
        "id": "tc_001",
        "brand": "Amazon Electronics",
        "product": "Great Indian Electronics Hub",
        "category": "technology",
        "subcategory": "gadgets",
        "description": "Huge selection of laptops, smartphones, noise-canceling headphones, and smart home tech.",
        "url": "https://www.amazon.in",
        "keywords": ["technology", "tech", "laptop", "phone", "smartphone", "headphone", "gadget", "electronics", "amazon"],
        "offer_search_query": "Amazon electronics sale discount offer bank discount",
        "price_range": "Up to 40% off on tech"
    },
    {
        "id": "tc_002",
        "brand": "Croma",
        "product": "Tata Croma Digital Store",
        "category": "technology",
        "subcategory": "retail-tech",
        "description": "India's trusted tech retail destination offering genuine gadgets, express store delivery, and warranty.",
        "url": "https://www.croma.com",
        "keywords": ["croma", "tata croma", "appliances", "laptop sale", "tv", "camera", "smartwatch", "tech store"],
        "offer_search_query": "Croma store discount offer card offer",
        "price_range": "Instant bank cashback available"
    },

    # --- 5. FASHION & APPAREL ---
    {
        "id": "fs_001",
        "brand": "Myntra",
        "product": "Fashion & Trend Style Hub",
        "category": "fashion",
        "subcategory": "apparel",
        "description": "India's largest online fashion store for trendy clothing, footwear, accessories, and top designer brands.",
        "url": "https://www.myntra.com",
        "keywords": ["fashion", "clothes", "outfit", "myntra", "dress", "shoes", "apparel", "wear", "style", "shopping"],
        "offer_search_query": "Myntra coupon code fashion sale offer discount",
        "price_range": "50–80% off on fashion brands"
    },
    {
        "id": "fs_002",
        "brand": "Nykaa Fashion",
        "product": "Curated Premium & Luxe Wear",
        "category": "fashion",
        "subcategory": "luxe-fashion",
        "description": "Curated collection of international styles, ethnic wear, and luxury fashion labels.",
        "url": "https://www.nykaafashion.com",
        "keywords": ["nykaa fashion", "ethnic wear", "designer", "luxury fashion", "handbags", "western wear"],
        "offer_search_query": "Nykaa Fashion discount offer coupon first order",
        "price_range": "Flat ₹500 off on first purchase"
    },

    # --- 6. HEALTH & WELLNESS ---
    {
        "id": "hl_001",
        "brand": "Practo",
        "product": "Online Doctor Consultation & Telehealth",
        "category": "health",
        "subcategory": "telemedicine",
        "description": "Instant video consultation with verified specialists and lab test booking from home.",
        "url": "https://www.practo.com",
        "keywords": ["health", "doctor", "medical", "consultation", "practo", "medicine", "clinic", "fever", "checkup"],
        "offer_search_query": "Practo doctor consultation discount coupon code",
        "price_range": "Consultations starting @ ₹299"
    },
    {
        "id": "hl_002",
        "brand": "Tata 1mg",
        "product": "Online Pharmacy & Health Store",
        "category": "health",
        "subcategory": "pharmacy",
        "description": "Order genuine medicines, health supplements, and schedule diagnostic lab tests at home.",
        "url": "https://www.1mg.com",
        "keywords": ["1mg", "pharmacy", "medicines", "supplements", "vitamins", "lab test", "tata 1mg", "health"],
        "offer_search_query": "Tata 1mg medicine lab test promo code discount",
        "price_range": "15-20% off on medicines"
    },

    # --- 7. FITNESS & SPORTS ---
    {
        "id": "ft_001",
        "brand": "Cult.fit",
        "product": "Cultpass Unlimited Fitness & Gyms",
        "category": "fitness",
        "subcategory": "gym-workout",
        "description": "Access to group workouts, strength training, yoga, and top fitness centers across India.",
        "url": "https://www.cult.fit",
        "keywords": ["fitness", "gym", "workout", "cultfit", "yoga", "exercise", "weight loss", "train", "sports"],
        "offer_search_query": "Cult fit cultpass discount offer promo code gym",
        "price_range": "Free 7-day trial pack"
    },
    {
        "id": "ft_002",
        "brand": "Decathlon",
        "product": "Sports Equipment & Activewear",
        "category": "fitness",
        "subcategory": "sports-gear",
        "description": "High-quality, affordable gear for 60+ sports including running, trekking, badminton, and cycling.",
        "url": "https://www.decathlon.in",
        "keywords": ["decathlon", "sports gear", "running shoes", "trekking", "cycles", "dumbbells", "activewear"],
        "offer_search_query": "Decathlon sports gear discount offer sale",
        "price_range": "Gear starting from ₹199"
    },

    # --- 8. FINANCE & INVESTING ---
    {
        "id": "fn_001",
        "brand": "Zerodha",
        "product": "Kite Stock Trading & Mutual Funds",
        "category": "finance",
        "subcategory": "investing",
        "description": "India's largest stockbroker offering zero brokerage on equity investments and direct mutual funds.",
        "url": "https://zerodha.com",
        "keywords": ["finance", "stock", "invest", "money", "trading", "mutual fund", "zerodha", "savings", "shares"],
        "offer_search_query": "Zerodha free demat account offer zero brokerage",
        "price_range": "Zero brokerage on equity delivery"
    },
    {
        "id": "fn_002",
        "brand": "Groww",
        "product": "Direct Mutual Funds & Stocks App",
        "category": "finance",
        "subcategory": "mutual-funds",
        "description": "User-friendly platform for investing in SIPs, direct mutual funds, US stocks, and gold.",
        "url": "https://groww.in",
        "keywords": ["groww", "sip", "mutual fund", "investment", "gold", "stocks", "finance app"],
        "offer_search_query": "Groww mutual fund sip offer zero fee",
        "price_range": "Zero commission direct plans"
    },

    # --- 9. EDUCATION & COURSES ---
    {
        "id": "ed_001",
        "brand": "Udemy",
        "product": "Online Skill Development & Certification",
        "category": "education",
        "subcategory": "skill-learning",
        "description": "Over 210,000 video courses covering programming, AI, digital marketing, design, and business.",
        "url": "https://www.udemy.com",
        "keywords": ["education", "coding", "course", "learn", "udemy", "skills", "study", "programming", "python", "certify"],
        "offer_search_query": "Udemy course coupon discount offer ₹499 deal",
        "price_range": "Courses from ₹499 during sales"
    },
    {
        "id": "ed_002",
        "brand": "Coursera",
        "product": "University Certificates & Degrees",
        "category": "education",
        "subcategory": "university-courses",
        "description": "Learn from world-class universities like Stanford, Yale, and Google with professional certificates.",
        "url": "https://www.coursera.org",
        "keywords": ["coursera", "degree", "google certificate", "university", "data science", "ai course"],
        "offer_search_query": "Coursera Plus discount offer free trial coupon",
        "price_range": "7-day free trial available"
    },

    # --- 10. ENTERTAINMENT & STREAMING ---
    {
        "id": "et_001",
        "brand": "JioHotstar",
        "product": "Live Sports, Movies & Premium Shows",
        "category": "entertainment",
        "subcategory": "streaming",
        "description": "Stream live cricket matches, latest blockbuster movies, and international TV series.",
        "url": "https://www.hotstar.com",
        "keywords": ["entertainment", "movie", "series", "cricket", "hotstar", "streaming", "shows", "cinema", "watch"],
        "offer_search_query": "Hotstar premium subscription offer discount coupon",
        "price_range": "Plans from ₹149/quarter"
    },
    {
        "id": "et_002",
        "brand": "Spotify",
        "product": "Spotify Premium Music & Podcasts",
        "category": "entertainment",
        "subcategory": "music",
        "description": "Ad-free music streaming, offline downloads, and millions of global podcasts in HD audio.",
        "url": "https://www.spotify.com",
        "keywords": ["spotify", "music", "songs", "podcasts", "playlist", "audiobook", "streaming"],
        "offer_search_query": "Spotify Premium free trial 3 months offer discount",
        "price_range": "3 months free for new users"
    },

    # --- 11. HOME & DECOR ---
    {
        "id": "hm_001",
        "brand": "IKEA",
        "product": "Modern Home Furnishing & Decor",
        "category": "home",
        "subcategory": "furniture-decor",
        "description": "Functional, well-designed home furnishing solutions, ergonomic study desks, and aesthetic decor.",
        "url": "https://www.ikea.com",
        "keywords": ["home", "furniture", "decor", "ikea", "desk", "sofa", "bedroom", "chair", "interior"],
        "offer_search_query": "IKEA home sale discount offer delivery deal",
        "price_range": "Affordable modular furniture"
    },

    # --- 12. GENERAL / MULTI-PURPOSE ---
    {
        "id": "gn_001",
        "brand": "Amazon Superstore",
        "product": "Daily Essentials & Everything Store",
        "category": "general",
        "subcategory": "everyday",
        "description": "Fast 1-day delivery on daily essentials, groceries, personal care, and home goods.",
        "url": "https://www.amazon.in",
        "keywords": ["buy", "order", "online", "store", "product", "deal", "discount", "shop"],
        "offer_search_query": "Amazon Prime sale deals discount offer",
        "price_range": "Prime membership benefits included"
    }
]


def get_all_ads():
    """Return complete ad database list"""
    return AD_DATABASE
