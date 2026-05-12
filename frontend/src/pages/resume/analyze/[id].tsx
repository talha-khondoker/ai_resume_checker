'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import api from '@/services/api';

export default function AnalyzePage() {
  const router = useRouter();
  const { id } = router.query;
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;

    const fetchAnalysis = async () => {
      setLoading(true);
      try {
        const response = await api.analyzeResume(Number(id));
        setAnalysis(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Analysis failed');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-2xl text-gray-600">Analyzing your resume...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-2xl text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Resume Analysis</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* ATS Score */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">ATS Score</h2>
            <div className="text-5xl font-bold text-blue-600 mb-2">
              {analysis?.ats_score?.toFixed(1) || 0}%
            </div>
            <p className="text-gray-600">Applicant Tracking System Compatibility</p>
          </div>

          {/* Resume Strength */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Resume Strength
            </h2>
            <div className="text-3xl font-bold text-green-600 capitalize">
              {analysis?.resume_strength || 'N/A'}
            </div>
          </div>
        </div>

        {/* Suggestions */}
        {analysis?.suggestions && analysis.suggestions.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Suggestions for Improvement
            </h2>
            <ul className="space-y-2">
              {analysis.suggestions.map((suggestion: string, idx: number) => (
                <li key={idx} className="flex items-start">
                  <span className="text-green-600 mr-3">✓</span>
                  <span className="text-gray-700">{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommended Roles */}
        {analysis?.recommended_roles && analysis.recommended_roles.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Recommended Job Roles
            </h2>
            <div className="flex flex-wrap gap-2">
              {analysis.recommended_roles.map((role: string, idx: number) => (
                <span
                  key={idx}
                  className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm"
                >
                  {role}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
