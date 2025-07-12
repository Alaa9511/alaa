# Replit.md

## Overview

This repository contains a Flask-based SEO analyzer web application specifically designed for "Lavish Perfumes". The application analyzes website URLs to extract SEO-relevant information including titles, descriptions, keywords, and meta data. It supports both Arabic and English content analysis, making it suitable for bilingual e-commerce websites.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: HTML5 with inline CSS and JavaScript
- **Language Support**: Arabic (RTL) and English
- **UI Framework**: Custom CSS with Font Awesome icons
- **Design Pattern**: Single-page application with AJAX interactions
- **Styling**: Modern gradient backgrounds with glassmorphism effects

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Architecture Pattern**: MVC (Model-View-Controller)
- **Request Handling**: RESTful API endpoints
- **Session Management**: Flask sessions with configurable secret key
- **Logging**: Python logging module for debugging

## Key Components

### Core Services
1. **Web Scraping Service**: Uses BeautifulSoup for HTML parsing and content extraction
2. **Keyword Analysis Engine**: NLTK-based text processing with multilingual support
3. **SEO Analyzer**: Extracts titles, descriptions, meta tags, and images
4. **Language Detection**: Separates Arabic and English keywords using Unicode ranges

### Main Application Files
- `app.py`: Core Flask application with SEO analysis logic
- `main.py`: Application entry point and server configuration
- `templates/index.html`: Frontend interface with bilingual support

### External Libraries
- **Flask**: Web framework
- **BeautifulSoup4**: HTML parsing
- **NLTK**: Natural language processing
- **Requests**: HTTP client for web scraping

## Data Flow

1. **User Input**: URL submission through web interface
2. **Request Processing**: Flask receives POST request with URL
3. **Content Retrieval**: Requests library fetches webpage content
4. **HTML Parsing**: BeautifulSoup extracts structured data
5. **Text Analysis**: NLTK processes content for keyword extraction
6. **Language Separation**: Unicode regex separates Arabic/English keywords
7. **Response Generation**: JSON response with analyzed data
8. **Frontend Display**: JavaScript renders results in the interface

## External Dependencies

### Python Packages
- `flask`: Web framework
- `requests`: HTTP library
- `beautifulsoup4`: HTML parsing
- `nltk`: Natural language toolkit
- `re`: Regular expressions (built-in)
- `collections.Counter`: Frequency counting (built-in)

### Frontend Dependencies
- Font Awesome 6.0.0 (CDN)

### NLTK Data
- Arabic and English stopwords datasets (downloaded at runtime)

## Deployment Strategy

### Environment Configuration
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 5000
- **Debug Mode**: Enabled for development
- **Session Secret**: Environment variable or default fallback

### Server Setup
- Flask development server for local development
- Environment variables for configuration
- Automatic NLTK data download on startup

### Error Handling
- Comprehensive logging for debugging
- Graceful fallbacks for missing NLTK data
- Exception handling in keyword extraction

### Security Considerations
- Configurable session secret
- Input validation through URL processing
- Timeout limits on external requests (10 seconds)

## Recent Updates (January 2025)

### Enhanced SEO Features
- **Meta Description Generator**: Automatically creates SEO-optimized product descriptions under 160 characters
- **Comprehensive Keyword System**: Implemented categorized keyword lists including:
  - Fragrance-specific terms (oriental, niche, EDP, top notes)
  - Marketing keywords (add to cart, discounts, shop now)
  - Local Saudi Arabia keywords (Riyadh, Jeddah, instant delivery)
  - Comparison keywords (inspired by, alternative perfume)
- **Advanced SEO Title Format**: Uses exact format "[Product Name] | from lavish | [attractive description]"
- **Re-analysis Feature**: Added button to regenerate results with different random keyword combinations
- **Improved Product Name Extraction**: Preserves original product name formatting from webpage titles

### User Interface Improvements
- Consistent "Copy" button naming across all sections
- Enhanced loading states and error handling
- Automatic product image display from og:image or first img tag
- Dual button system: "Re-analyze Product" and "New Search"

## Notes

The application is currently configured for development use with debug mode enabled. For production deployment, additional considerations would include:
- Production WSGI server (e.g., Gunicorn)
- Environment-specific configuration
- Enhanced error handling and validation
- Security headers and CORS policies
- Caching mechanisms for improved performance