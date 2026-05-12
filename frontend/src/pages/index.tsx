export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="text-white font-bold text-2xl">📄 AI Resume Analyzer</div>
          <div className="space-x-4">
            <a href="/auth/login" className="text-white hover:text-gray-100">
              Login
            </a>
            <a
              href="/auth/register"
              className="bg-white text-blue-600 px-6 py-2 rounded-lg hover:bg-gray-100 transition"
            >
              Sign Up
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center text-white">
        <h1 className="text-5xl font-bold mb-4">
          Optimize Your Resume with AI
        </h1>
        <p className="text-xl mb-8 text-gray-100">
          Get instant feedback, ATS score, and job matching analysis
        </p>
        <a
          href="/auth/register"
          className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Get Started Free
        </a>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: '⚡',
              title: 'ATS Score',
              description: 'Check your resume compatibility with Applicant Tracking Systems',
            },
            {
              icon: '🎯',
              title: 'Job Matching',
              description: 'Match your skills with job descriptions and find the perfect role',
            },
            {
              icon: '💡',
              title: 'Smart Suggestions',
              description: 'Get personalized recommendations to improve your resume',
            },
          ].map((feature, idx) => (
            <div
              key={idx}
              className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 text-white text-center hover:bg-white/20 transition"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-100">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black/20 backdrop-blur-md border-t border-white/20 py-8 text-center text-white">
        <p>&copy; 2024 AI Resume Analyzer. All rights reserved.</p>
      </footer>
    </main>
  );
}
