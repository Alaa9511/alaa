import os
import logging
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import random
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "lavish-perfumes-seo-analyzer-secret")

# Download NLTK data on startup
try:
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('arabic') + stopwords.words('english'))
    app.logger.info("NLTK stopwords loaded successfully")
except Exception as e:
    app.logger.error(f"Error loading NLTK stopwords: {e}")
    stop_words = set()

def extract_keywords(words):
    """Extract and rank keywords from a list of words"""
    try:
        # Filter out stop words and URLs
        filtered = [w for w in words if w not in stop_words and not w.startswith('http') and len(w) > 2]
        
        # Count word frequencies
        counts = Counter(filtered)
        
        # Get most common words
        common = counts.most_common(100)
        
        return [w for w, _ in common]
    except Exception as e:
        app.logger.error(f"Error extracting keywords: {e}")
        return []

def generate_meta_description(product_name, original_desc, marketing_words, fragrance_words):
    """Generate SEO meta description under 160 characters"""
    try:
        # Extract brief product info
        brief_desc = original_desc[:50] if original_desc and original_desc != "لا يوجد وصف" else f"عطر {product_name}"
        
        # Combine elements
        marketing_part = " ".join(marketing_words[:2])  # Max 2 marketing words
        fragrance_part = " ".join(fragrance_words[:1])  # Max 1 fragrance word
        
        # Build description
        description = f"{brief_desc} - {fragrance_part}. {marketing_part}"
        
        # Ensure it's under 160 characters
        if len(description) > 160:
            description = description[:157] + "..."
            
        return description
    except Exception as e:
        app.logger.error(f"Error generating meta description: {e}")
        return f"عطر {product_name} - فخامة وثبات. تسوق الآن مع عروض خاصة من لافيش"

@app.route('/')
def home():
    """Main page with the SEO analyzer interface"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a product URL and extract SEO data"""
    return perform_analysis()

@app.route('/reanalyze', methods=['POST'])
def reanalyze():
    """Re-analyze the same URL with different random keywords"""
    return perform_analysis()

def perform_analysis():
    """Analyze a product URL and extract SEO data"""
    try:
        # Get URL from request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data['url']
        app.logger.info(f"Analyzing URL: {url}")
        
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = "لا يوجد عنوان"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        
        # Extract meta description
        description = "لا يوجد وصف"
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag and desc_tag.get('content'):
            description = desc_tag['content'].strip()
        
        # Extract product image
        image_url = ""
        # Try Open Graph image first
        og_img = soup.find('meta', property='og:image')
        if og_img and og_img.get('content'):
            image_url = og_img['content']
        else:
            # Fallback to first img tag
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']
                # Convert relative URLs to absolute
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url
                elif image_url.startswith('/'):
                    from urllib.parse import urljoin
                    image_url = urljoin(url, image_url)
        
        # Extract page text and process words
        text = soup.get_text(separator=' ')
        words = re.findall(r'\b[\w-]{3,}\b', text.lower())
        keywords = extract_keywords(words)
        
        # Separate Arabic and English keywords
        arabic_keywords = []
        english_keywords = []
        
        for word in keywords:
            if re.search(r'[\u0600-\u06FF]', word):  # Arabic characters
                arabic_keywords.append(word)
            elif word.isascii() and not re.search(r'[\u0600-\u06FF]', word):
                english_keywords.append(word)
        
        # Remove duplicates while preserving order
        arabic_keywords = list(dict.fromkeys(arabic_keywords))
        english_keywords = list(dict.fromkeys(english_keywords))
        
        # Comprehensive keyword lists for perfume SEO
        fragrance_keywords_arabic = [
            "عطر شرقي", "عطر نيش", "عطر نسائي", "عطر رجالي", "عطر فاخر", "عطر زهري",
            "عطر فواكه", "عطر قوي", "ثبات عالي", "نوتات علوية", "تركيبة فخمة",
            "رائحة دائمة", "تركيز EDP", "عطر راقي", "عطر منعش", "عطر كلاسيكي"
        ]
        
        marketing_keywords_arabic = [
            "أضف للسلة", "تسوق الآن", "خصومات", "عروض", "أسعار مناسبة", "شحن مجاني",
            "متجر سعودي", "عطور أصلية", "خصم اليوم", "أرخص العطور", "عروض خاصة",
            "تسوق", "شراء", "توصيل سريع"
        ]
        
        local_keywords_arabic = [
            "عطر في الرياض", "متجر عطور في السعودية", "عطور جدة", "توصيل فوري",
            "عطر فاخر في السعودية", "متجر عطور نيش أونلاين", "عطور الدمام",
            "عطور المدينة", "عطور مكة"
        ]
        
        comparison_keywords_arabic = [
            "عطر بديل", "مستوحى من", "مثل باكارا روج", "نفس رائحة ديور سوفاج",
            "مشابه لتوم فورد", "عطر بجودة نيش وسعر أقل", "بديل عطر", "رائحة مميزة"
        ]
        
        fragrance_keywords_english = [
            "oriental fragrance", "niche fragrance", "women's fragrance", "men's fragrance",
            "luxury fragrance", "floral fragrance", "fruit fragrance", "strong fragrance",
            "high stability", "top notes", "luxurious composition", "lasting aroma",
            "EDP concentration", "premium scent", "elegant perfume"
        ]
        
        marketing_keywords_english = [
            "add to cart", "shop now", "discounts", "offers", "favorable prices",
            "free shipping", "Saudi store", "original perfumes", "discount today",
            "cheapest perfumes", "special offers", "buy", "fast delivery"
        ]
        
        local_keywords_english = [
            "perfume in Riyadh", "perfume shop in Saudi Arabia", "Jeddah perfumes",
            "instant delivery", "luxury perfume in Saudi Arabia", "niche online perfume shop",
            "Dammam perfumes", "Medina perfumes", "Mecca perfumes"
        ]
        
        comparison_keywords_english = [
            "alternative perfume", "inspired by", "like Baccarat Rouge", "same smell of Dior Sauvage",
            "similar to Tom Ford", "perfume with niche quality and lower price", "dupe fragrance",
            "signature scent"
        ]
        
        # Randomly select keywords from different categories
        selected_fragrance_ar = random.sample(fragrance_keywords_arabic, min(4, len(fragrance_keywords_arabic)))
        selected_marketing_ar = random.sample(marketing_keywords_arabic, min(5, len(marketing_keywords_arabic)))
        selected_local_ar = random.sample(local_keywords_arabic, min(3, len(local_keywords_arabic)))
        selected_comparison_ar = random.sample(comparison_keywords_arabic, min(2, len(comparison_keywords_arabic)))
        
        selected_fragrance_en = random.sample(fragrance_keywords_english, min(4, len(fragrance_keywords_english)))
        selected_marketing_en = random.sample(marketing_keywords_english, min(5, len(marketing_keywords_english)))
        selected_local_en = random.sample(local_keywords_english, min(3, len(local_keywords_english)))
        selected_comparison_en = random.sample(comparison_keywords_english, min(2, len(comparison_keywords_english)))
        
        # Combine all keyword types
        all_arabic_keywords = (arabic_keywords[:10] + selected_fragrance_ar + 
                              selected_marketing_ar + selected_local_ar + selected_comparison_ar)
        all_english_keywords = (english_keywords[:10] + selected_fragrance_en + 
                               selected_marketing_en + selected_local_en + selected_comparison_en)
        
        # Shuffle and remove duplicates
        random.shuffle(all_arabic_keywords)
        random.shuffle(all_english_keywords)
        all_arabic_keywords = list(dict.fromkeys(all_arabic_keywords))
        all_english_keywords = list(dict.fromkeys(all_english_keywords))
        
        # Extract product name from URL slug (preserve exact URL format)
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        url_path = parsed_url.path
        
        # Extract product name from URL path like /products/so-scandal-edp-50ml-women
        if '/products/' in url_path:
            product_name = url_path.split('/products/')[-1]
            # Remove any trailing slashes
            product_name = product_name.rstrip('/')
        else:
            # Fallback to title if URL doesn't match expected pattern
            product_name = title if title and title != "لا يوجد عنوان" else "عطر"
            # Clean up common website suffixes but keep the actual product name intact
            if " | " in product_name:
                product_name = product_name.split(" | ")[0]
            if " - " in product_name:
                product_name = product_name.split(" - ")[0]
        
        # Arabic attractive descriptions for SEO titles
        arabic_attractive_descriptions = [
            "ثبات لا يقاوم ورائحة مميزة",
            "نوتات شرقية برائحة فخمة", 
            "رائحة رجالية طويلة الثبات",
            "ثبات طويل الأمد",
            "رائحتان لا تقاومان",
            "رائحة نيش فخمة",
            "سعر خاص وجودة عالية",
            "مناسب لكل الأوقات",
            "عطر فاخر بلمسة نيش",
            "رائحة أنيقة وثبات مميز"
        ]
        
        # English attractive descriptions for SEO titles  
        english_attractive_descriptions = [
            "irresistible persistence and fragrance",
            "oriental notes with luxurious scent",
            "long-lasting masculine scent", 
            "long lasting stability",
            "two irresistible smells",
            "luxurious niche scent",
            "special price and high quality",
            "suitable for all times",
            "luxury perfume with niche touch",
            "elegant scent with premium quality"
        ]
        
        # Extract gender from product description and URL
        def extract_gender_info(text, url_path):
            gender_ar = ""
            gender_en = ""
            
            # Check URL for gender indicators
            if "women" in url_path.lower():
                gender_ar = "نسائي"
                gender_en = "women"
            elif "men" in url_path.lower():
                gender_ar = "رجالي"
                gender_en = "men"
            else:
                # Check description text for gender keywords
                text_lower = text.lower()
                if any(word in text_lower for word in ["woman", "women", "female", "lady", "her", "she"]):
                    gender_ar = "نسائي"
                    gender_en = "women"
                elif any(word in text_lower for word in ["man", "men", "male", "gentleman", "his", "he"]):
                    gender_ar = "رجالي"
                    gender_en = "men"
                # Check for Arabic gender indicators
                elif any(word in text for word in ["نسائي", "نساء", "المرأة", "للنساء"]):
                    gender_ar = "نسائي"
                    gender_en = "women"
                elif any(word in text for word in ["رجالي", "رجال", "الرجل", "للرجال"]):
                    gender_ar = "رجالي"
                    gender_en = "men"
                    
            return gender_ar, gender_en
        
        # Extract gender information
        gender_ar, gender_en = extract_gender_info(description + " " + text, url_path)
        
        # Generate SEO titles with gender included: [Product name] | from lavish | [gender] [attractive description]
        selected_desc_ar = random.choice(arabic_attractive_descriptions)
        selected_desc_en = random.choice(english_attractive_descriptions)
        
        # Include gender in the attractive description if detected
        if gender_ar:
            arabic_seo_title = f"{product_name} | من لافيش | عطر {gender_ar} {selected_desc_ar}"
        else:
            arabic_seo_title = f"{product_name} | من لافيش | {selected_desc_ar}"
            
        if gender_en:
            english_seo_title = f"{product_name} | from lavish | {gender_en} perfume {selected_desc_en}"
        else:
            english_seo_title = f"{product_name} | from lavish | {selected_desc_en}"
        
        # Generate SEO meta description (max 160 characters)
        meta_description = generate_meta_description(product_name, description, selected_marketing_ar[:3], selected_fragrance_ar[:2])
        
        # Limit keywords length for meta tags
        arabic_keywords_str = '، '.join(all_arabic_keywords)[:200]
        english_keywords_str = ', '.join(all_english_keywords[:25])
        
        app.logger.info("Analysis completed successfully")
        
        return jsonify({
            "title": title,
            "description": description,
            "meta_description": meta_description,
            "arabic_keywords": arabic_keywords_str,
            "english_keywords": english_keywords_str,
            "arabic_seo_title": arabic_seo_title,
            "english_seo_title": english_seo_title,
            "image_url": image_url
        })
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request error: {e}")
        return jsonify({"error": f"فشل في تحميل الصفحة: {str(e)}"}), 400
    except Exception as e:
        app.logger.error(f"Analysis error: {e}")
        return jsonify({"error": f"خطأ في التحليل: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
