'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import api from '@/services/api';
import { useAuthStore } from '@/context/authStore';
import { useResumeStore } from '@/context/resumeStore';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuthStore((state) => ({
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    logout: state.logout,
  }));
  const { resumes, setResumes, isLoading, setIsLoading } = useResumeStore(
    (state) => ({
      resumes: state.resumes,
      setResumes: state.setResumes,
      isLoading: state.isLoading,
      setIsLoading: state.setIsLoading,
    })
  );

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    const fetchResumes = async () => {
      setIsLoading(true);
      try {
        const data = await api.getResumeHistory();
        setResumes(data);
      } catch (error) {
        console.error('Failed to fetch resumes:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchResumes();
  }, [isAuthenticated, setResumes, setIsLoading, router]);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-blue-600">
            📄 AI Resume Analyzer
          </Link>
          <div className="flex items-center space-x-6">
            <span className="text-gray-700">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="text-gray-700 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Your Resumes</h1>
          <Link
            href="/resume/upload"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            + Upload Resume
          </Link>
        </div>

        {isLoading ? (
          <div className="text-center text-gray-500">Loading...</div>
        ) : resumes.length === 0 ? (
          <div className="bg-white rounded-lg p-8 text-center border-2 border-dashed border-gray-300">
            <p className="text-gray-500 mb-4">No resumes uploaded yet</p>
            <Link
              href="/resume/upload"
              className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Upload Your First Resume
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resumes.map((resume) => (
              <div
                key={resume.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition"
              >
                <h3 className="font-semibold text-lg mb-2">{resume.filename}</h3>
                <p className="text-gray-600 text-sm mb-2">
                  {new Date(resume.created_at).toLocaleDateString()}
                </p>
                {resume.ats_score && (
                  <p className="text-lg font-bold text-blue-600 mb-4">
                    ATS Score: {resume.ats_score.toFixed(1)}%
                  </p>
                )}
                <div className="space-y-2">
                  <Link
                    href={`/resume/analyze/${resume.id}`}
                    className="block w-full text-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
                  >
                    Analyze
                  </Link>
                  <Link
                    href={`/resume/match/${resume.id}`}
                    className="block w-full text-center bg-green-600 text-white py-2 rounded hover:bg-green-700 transition"
                  >
                    Match with Job
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
