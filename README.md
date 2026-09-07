<img width="1517" height="984" alt="tactical-legends badge" src="https://github.com/user-attachments/assets/f67d5892-1098-4b74-94b3-724b6e3b2bca" />


[![CI](https://github.com/jurgen-paul/tactical-legends/actions/workflows/ci.yml/badge.svg)](https://github.com/jurgen-paul/tactical-legends/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

# Tactical Legends

> A turn-based tactical strategy game template built with Unity / Godot / Unreal Engine (replace with the engine you used).

[![Tactical Legends banner — placeholder screenshot (Hero: Image 1 - mystical vault) ](https://via.placeholder.com/800x400)](https://play.google.com/store/apps/details?id=com.example.tacticallegends)

# Tactical Legends

Welcome to **Tactical Legends**, an open-source tactical strategy game focused on turn-based combat, deep squad customization, and replayable missions. Whether you’re a strategist, developer, or[...]

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Play Store Console — Store Listing & Release Checklist](#play-store-console)
- [Production page](docs/production-tactical-legend.md)
- [Preview page](docs/preview-tactical-legend-page.md)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## About

Tactical Legends delivers engaging tactical gameplay built with C++ and SDL2, designed for extensibility and cross-platform support. Plan your moves, outwit adaptive AI, and enjoy a game that grow[...]

## Features

- Turn-based tactical combat
- Modular codebase using CMake
- Cross-platform support (Windows, macOS, Linux)
- SDL2-powered graphics and audio
- Unit testing via CTest
- Deep squad customization and branching campaign (coming soon)

## Installation

### Prerequisites

- CMake >= 3.x
- g++ >= 9.0
- SDL2, SDL2_image, SDL2_mixer, SDL2_ttf

### Setup

```bash
sudo apt update
sudo apt install cmake g++ libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends
mkdir build
cmake -S. -B build
cmake --build build
```

## Usage

Run the game executable from the build directory:

```bash
./build/tactical_legends
```

## Play Store Console — Store Listing & Release Checklist

Use this checklist and the metadata templates below to prepare a Play Store release. Replace the placeholders with your real values (package name, URLs, images, email).

1) App identifiers
- Package name / App bundle ID: com.example.tacticallegends  <-- replace with your actual package name
- Version code / version name: e.g., 100 (versionCode), 1.0.0 (versionName)
- Build artifact: Upload Android App Bundle (.aab) built with targetSdkVersion >= 31

2) Store listing metadata (fill these in Play Console)
- App title: Tactical Legends — Rise of OISTARIAN
- Short description (max 80 chars): Turn-based tactical strategy with deep squad customization.
- Full description (max 4000 chars): Replace the paragraph below with game-specific marketing copy.

  Tactical Legends is a turn-based tactical strategy game where you command a squad of heroes across branching missions. Customize loadouts, exploit terrain, and outsmart adaptive AI opponents. Fe[...]

- What’s new / Release notes: Add release-specific notes here.

3) Store listing assets (required)
- High-res icon: 512x512 PNG
- Feature graphic: 1024x500 PNG (used on Play Store listing)
- Screenshots: Phone screenshots (minimum 2, recommended 4–8), 16:9 or 9:16 ratios, PNG/JPEG. Include at least one landscape and one portrait where appropriate.
- Promo video (optional): YouTube URL
- Privacy policy URL: https://yourdomain.com/privacy (required if app collects personal data)
- Contact email: privacy@yourdomain.com (required)

4) App content & policies
- Content rating questionnaire: complete honestly in Play Console
- Target audience and content: declare if intended for children
- Ads & in-app purchases: declare implementation
- Permissions: Only request runtime permissions you need (e.g., INTERNET, READ_EXTERNAL_STORAGE) and document reasons in the Play Console

5) Technical checklist
- Build App Bundle (.aab) and sign with Play App Signing
- Target Android API level required by Play Store (check current requirement)
- Verify AAB installs on supported devices/emulators
- Verify ProGuard/R8 rules and that native libraries are included
- Test in internal/closed testing tracks before production

6) Release tracks & testing
- Create an internal test track for quick verification
- Then a closed or open test track to test with a broader audience
- Prepare release notes for each track

7) Compliance
- Verify privacy policy covers data collection, analytics, advertising, and payment processing
- Ensure GDPR/CCPA compliance if applicable

Metadata JSON template (fill and paste into your release notes or internal docs):

```json
{
  "packageName": "com.example.tacticallegends",
  "title": "Tactical Legends — Rise of OISTARIAN",
  "shortDescription": "Turn-based tactical strategy with deep squad customization.",
  "fullDescription": "Tactical Legends is a turn-based tactical strategy game where you command a squad of heroes across branching missions...",
  "privacyPolicyUrl": "https://yourdomain.com/privacy",
  "contactEmail": "privacy@yourdomain.com",
  "featureGraphic": "assets/feature_graphic.png",
  "highResIcon": "assets/icon_512.png",
  "screenshots": ["assets/ss1.png","assets/ss2.png"]
}
```

Helpful commands

- Build Android AAB (example for Unity/Gradle):
  - Unity: File > Build Settings > Android > Build App Bundle
  - Gradle CLI: ./gradlew bundleRelease

- Verify AAB locally with bundletool and install on device:
```bash
bundletool build-apks --bundle=app.aab --output=app.apks --mode=universal
bundletool install-apks --apks=app.apks
```

Next steps
- Replace all placeholders above (package name, URLs, images, email) with your real values
- Add the Play Store assets to the repository under /store-assets/ (icons, feature graphic, screenshots)
- Build and upload your signed .aab in Play Console, set up testing tracks, and roll out

---

## Testing

Run all unit tests with:

```bash
cd build
ctest --output-on-failure
```
Project Overview: Tactical Legends – Rise of OISTARIAN
Tactical Legends is a cross-platform game designed for strategic depth and replayability. It features:
• 	Turn-based tactical combat with adaptive AI
• 	Modular codebase using CMake for easy extension
• 	Cross-platform support (Windows, macOS, Linux)
• 	SDL2-powered graphics and audio
• 	Deep squad customization and branching campaign structure

Tactical Legends Game Architecture Diagram
Diagram Highlights:
• 	Central Game Loop powered by SDL2
• 	Modular AI System with combat and stealth logic
• 	Campaign Manager for branching storylines
• 	Audio Manager for immersive sound design
• 	UI Layer built with Vue and C++
• 	Data Layer using Prisma and JSON configs
• 	Build & Deployment via CMake and YAML workflows
• 	Testing supported by CTest
<img width="1105" height="811" alt="tactical-legend architecture diagram (Image 2 - soldier as unit art)" src="https://github.com/user-attachments/assets/e6e160a1-1a7d-42f6-8991-63b6786e1112" />

## Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
<img width="950" height="657" alt="onboarding flow — tactical-legend (Image 3 - poster thumbnail)" src="https://github.com/user-attachments/assets/31835e2c-649f-4518-a8db-625105ac725b" />
The flow is split into two main tracks:
🔍 Discovery & Setup
• 	Discover the project on GitHub
• 	Read the README and contribution guidelines
• 	Set up the development environment (C++, SDL2, CMake)
• 	Explore the codebase (AI, UI, Campaign Manager)
• 	Pick an issue or feature to work on
🛠️ Contribution & Review
• 	Fork the repository and create a branch
• 	Develop and test changes locally
• 	Submit a pull request
• 	Participate in code review and make revisions
• 	Merge and celebrate your contribution 🎉
Each stage is represented with labeled boxes and directional arrows to show progression. It’s designed to be intuitive and beginner-friendly.
Click/open the card above to download the diagram.

To propose changes:
- Fork the repo
- Create a feature branch
- Submit a pull request
# Enhanced Stripe SaaS Subscription System

A production-ready, TypeScript-based SaaS subscription management system with Stripe integration.

## 🚀 Features

- **Secure Payment Processing** - Full Stripe integration with 3D Secure support
- **Subscription Management** - Create, update, and cancel subscriptions
- **Automatic Retries** - Smart payment retry logic for failed transactions
- **Webhook Handling** - Comprehensive event processing for subscription lifecycle
- **Email Notifications** - Automated customer notifications for all events
- **Rate Limiting** - Protection against abuse
- **TypeScript** - Full type safety across the application
- **Logging** - Structured logging with Winston
- **Error Handling** - Robust error handling and validation

## 📋 Prerequisites

- Node.js 18+ 
- npm or yarn
- Stripe account
- PostgreSQL (or your preferred database)

## 🛠️ Installation

### Backend Setup

1. **Clone and install dependencies:**
```bash
cd backend
npm install
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

3. **Set up Stripe:**
   - Create a Stripe account at https://stripe.com
   - Get your API keys from the Stripe Dashboard
   - Create a product and price in Stripe
   - Set up webhook endpoint at `https://yourdomain.com/webhook`
   - Add webhook secret to `.env`

4. **Build and run:**
```bash
# Development
npm run dev

# Production build
npm run build
npm start
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure Stripe public key:**
   - Update `pk_test_YourPublicKey` in `App.jsx` with your actual public key
   - Update `priceId` with your Stripe price ID

3. **Run development server:**
```bash
npm run dev
```

## 🔧 Configuration

### Stripe Webhook Events

Configure your Stripe webhook to listen for these events:
- `invoice.payment_succeeded`
- `invoice.payment_failed`
- `customer.subscription.deleted`
- `customer.subscription.updated`
- `customer.subscription.trial_will_end`

### Database Schema

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  customer_id VARCHAR(255) UNIQUE NOT NULL,
  subscription_id VARCHAR(255),
  status VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_customer_id ON users(customer_id);
CREATE INDEX idx_subscription_id ON users(subscription_id);
```

## 📡 API Endpoints

### POST /create-subscription
Create a new subscription for a customer.

**Request Body:**
```json
{
  "email": "user@example.com",
  "priceId": "price_xxxxxxxxxxxxx",
  "trialDays": 14,
  "couponId": "coupon_xxxxx" // optional
}
```

**Response:**
```json
{
  "subscriptionId": "sub_xxxxxxxxxxxxx",
  "status": "trialing",
  "requiresAction": false
}
```

### POST /cancel-subscription
Cancel a subscription at period end.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

### POST /webhook
Stripe webhook endpoint (automatically called by Stripe).

### GET /health
Health check endpoint.

## 🧪 Testing

```bash
# Run tests
npm test

# Watch mode
npm run test:watch

# Test webhook locally with Stripe CLI
stripe listen --forward-to localhost:4242/webhook
```

## 🔒 Security Best Practices

1. **Never commit API keys** - Always use environment variables
2. **Validate webhook signatures** - Prevents fraudulent webhook calls
3. **Use HTTPS in production** - Required for Stripe webhooks
4. **Implement rate limiting** - Protect against abuse
5. **Sanitize user input** - Prevent injection attacks
6. **Keep dependencies updated** - Regular security patches

## 📊 Monitoring & Logging

Logs are structured and written to:
- `error.log` - Error-level logs only
- `combined.log` - All logs
- Console output - Development environment

Example log entry:
```json
{
  "level": "info",
  "message": "Subscription created: sub_xxxxxxxxxxxxx",
  "timestamp": "2025-11-29T12:00:00.000Z"
}
```

## 🚨 Error Handling

The system handles various error scenarios:

- **Invalid payment methods** - Returns clear error to user
- **Failed payments** - Automatic retry with customer notification
- **Webhook failures** - Logged and can be replayed from Stripe
- **3D Secure** - Automatic handling with client confirmation

## 📈 Scaling Considerations

1. **Database** - Replace in-memory storage with PostgreSQL/MongoDB
2. **Caching** - Add Redis for session management
3. **Queue System** - Use Bull/Bee-Queue for async tasks
4. **Load Balancing** - Deploy behind nginx or AWS ALB
5. **Monitoring** - Add Sentry or similar error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - feel free to use for commercial projects

## 🆘 Support

For issues and questions:
- Check the [Stripe documentation](https://stripe.com/docs)
- Review existing GitHub issues
- Create a new issue with reproduction steps

---

> _Note_: If you plan to contribute code, please also review the project's [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines and setup instructions.
