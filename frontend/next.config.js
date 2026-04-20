/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // Local LLMs (LM Studio / Ollama) can take 60+ seconds to respond.
    // The default Node.js proxy timeout (~30s) would drop the connection
    // before the backend finishes. 180s gives ample headroom for slow hardware
    // while still surfacing genuine hangs within a reasonable time.
    proxyTimeout: 180_000,
  },
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig