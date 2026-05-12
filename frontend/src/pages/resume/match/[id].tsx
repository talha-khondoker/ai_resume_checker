'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import api from '@/services/api';

export default function MatchPage() {
  const router = useRouter();
  const { id } = router.query;
  const [jobDescription, setJobDescription] = useState('');
  const [match, setMatch] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleMatch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (jobDescription.length < 50) {
      setError('Job description must be at least 50 characters');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await api.matchWithJob(Number(id), jobDescription);
      setMatch(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Matching failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Match with Job</h1>

        {!match && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <form onSubmit={handleMatch}>
              <label className="block text-lg font-semibold text-gray-900 mb-4">
                Paste Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="Paste the job description here..."
              />
              <div className="mt-4 text-sm text-gray-600">
                Minimum 50 characters required
              </div>
              {error && (
                <div className="mt-4 bg-red-100 border border-red-400 text-red-700 p-3 rounded">
                  {error}
                </div>
              )}
              <button
                type="submit"
                disabled={loading}
                className="mt-6 w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze Match'}
              </button>
            </form>
          </div>
        )}

        {match && (
          <>
            {/* Match Score */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Match Score
                </h2>
                <div className="text-5xl font-bold text-blue-600 mb-2">
                  {match?.match_score?.toFixed(1) || 0}%
                </div>
              </div>
            </div>

            {/* Matching Skills */}
            {match?.matching_skills && match.matching_skills.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Your Matching Skills
                </h2>
                <div className="flex flex-wrap gap-2">
                  {match.matching_skills.map((skill: any, idx: number) => (
                    <span
                      key={idx}
                      className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm"
                    >
                      {skill.skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Missing Skills */}
            {match?.missing_skills && match.missing_skills.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Missing Skills
                </h2>
                <div className="flex flex-wrap gap-2">
                  {match.missing_skills.map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="bg-red-100 text-red-800 px-4 py-2 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {match?.recommendations && match.recommendations.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Recommendations
                </h2>
                <ul className="space-y-2">
                  {match.recommendations.map((rec: string, idx: number) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-blue-600 mr-3">→</span>
                      <span className="text-gray-700">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}
