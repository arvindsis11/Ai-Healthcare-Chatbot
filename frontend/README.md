# AI Healthcare Assistant - Frontend

A modern, ChatGPT-like UI for the AI Healthcare Chatbot built with Next.js, React, and TailwindCSS.

## 🚀 Features

- **ChatGPT-like Interface**: Modern chat experience with message bubbles and smooth animations
- **Dark/Light Mode**: Toggle between themes with system preference detection
- **Typing Indicators**: Visual feedback when AI is generating responses
- **Symptom Suggestions**: Intelligent input suggestions for common symptoms and health questions
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Updates**: WebSocket-ready for streaming responses
- **Accessibility**: Built with accessibility best practices

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: TailwindCSS with custom design system
- **UI Components**: Shadcn/ui (Radix UI primitives)
- **Icons**: Lucide React
- **State Management**: React hooks
- **API**: RESTful API (WebSocket ready)

## 📦 Installation

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. **Set up environment variables:**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your API endpoints:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

4. **Run development server:**
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🏗️ Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles and CSS variables
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ChatWindow.tsx     # Main chat interface
│   ├── MessageBubble.tsx  # Individual message display
│   ├── InputBar.tsx       # Message input with suggestions
│   └── Sidebar.tsx        # Navigation and settings
├── lib/                   # Utility functions and types
│   ├── types.ts          # TypeScript interfaces
│   └── utils.ts          # Class name utilities
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # TailwindCSS configuration
├── tsconfig.json          # TypeScript configuration
└── README.md             # This file
```

## 🎨 Components

### ChatWindow
The main chat interface that orchestrates all other components. Handles:
- Message state management
- API communication
- Theme switching
- Responsive layout

### MessageBubble
Displays individual messages with:
- User/Assistant role differentiation
- Timestamps
- Typing animations
- Responsive design

### InputBar
Smart input component featuring:
- Auto-resizing textarea
- Symptom suggestions dropdown
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- Character counting
- Loading states

### Sidebar
Navigation and settings panel with:
- Quick action buttons
- Common symptoms grid
- Health topics navigation
- Session statistics
- Theme toggle
- Chat management (clear/export)

## 🎯 Key Features Implementation

### Symptom Suggestions
The input bar provides intelligent suggestions based on:
- Common symptoms
- Health questions
- Medical terminology
- User input matching

### Dark/Light Mode
- Automatic system preference detection
- Manual toggle in sidebar
- CSS custom properties for theming
- Smooth transitions

### Responsive Design
- Mobile-first approach
- Collapsible sidebar on mobile
- Touch-friendly interactions
- Optimized layouts for all screen sizes

### Accessibility
- Semantic HTML
- Keyboard navigation
- Screen reader support
- High contrast ratios
- Focus management

## 🔌 API Integration

### REST API Endpoints
```typescript
// Send message
POST /api/chat
{
  "message": "I have a headache"
}

// Response
{
  "message": "Based on your symptoms...",
  "symptom_analysis": {
    "severity_score": 3,
    "risk_level": "low",
    "possible_conditions": ["Tension headache", "Migraine"],
    "urgency_recommendation": "Rest and hydrate..."
  }
}
```

### WebSocket (Future)
```typescript
// Streaming responses
const ws = new WebSocket('ws://localhost:8000/chat')
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // Handle streaming chunks
}
```

## 🎨 Customization

### Theme Colors
Modify `app/globals.css` to customize the color scheme:

```css
:root {
  --primary: 221.2 83.2% 53.3%;
  --background: 0 0% 100%;
  /* ... other variables */
}
```

### Component Styling
All components use TailwindCSS classes and can be customized by:
- Modifying class names
- Adding custom CSS
- Extending the design system

## 🚀 Deployment

### Build for Production
```bash
npm run build
npm start
```

### Environment Variables for Production
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_WS_URL=wss://your-api-domain.com
```

### Docker (Optional)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🤝 Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test components on multiple screen sizes
4. Ensure accessibility compliance
5. Update documentation for new features

## 📄 License

This project is part of the AI Healthcare Assistant system. See the main project README for license information.

## ⚕️ Medical Disclaimer

This interface is designed for the AI Healthcare Assistant, which provides general health information only. Always consult healthcare professionals for medical advice, diagnosis, or treatment.