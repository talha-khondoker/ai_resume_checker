'use client';

import { useState, useCallback } from 'react';
import { useRouter } from 'next/router';
import { useDropzone } from 'react-dropzone';
import api from '@/services/api';
import { useResumeStore } from '@/context/resumeStore';

export default function UploadPage() {
  const router = useRouter();
  const { addResume } = useResumeStore((state) => ({
    addResume: state.addResume,
  }));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) {
        setError('Please drop a valid PDF or DOCX file');
        return;
      }

      const file = acceptedFiles[0];

      // Validate file type
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(file.type)) {
        setError('Only PDF and DOCX files are supported');
        return;
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size exceeds 10MB limit');
        return;
      }

      setLoading(true);
      setError('');
      setUploadProgress(0);

      try {
        // Simulate upload progress
        const progressInterval = setInterval(() => {
          setUploadProgress((prev) => Math.min(prev + 10, 90));
        }, 200);

        const response = await api.uploadResume(file);

        clearInterval(progressInterval);
        setUploadProgress(100);

        // Add to store
        addResume(response.data);

        // Redirect to dashboard
        setTimeout(() => {
          router.push('/dashboard');
        }, 1000);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Upload failed');
      } finally {
        setLoading(false);
      }
    },
    [addResume, router]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
  });

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-2xl">
        <h1 className="text-3xl font-bold text-white mb-2 text-center">
          Upload Your Resume
        </h1>
        <p className="text-gray-100 text-center mb-8">
          Upload a PDF or DOCX file to get started with analysis
        </p>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-200 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
            isDragActive
              ? 'border-white bg-white/20'
              : 'border-white/30 hover:border-white/50'
          }`}
        >
          <input {...getInputProps()} />
          <div className="text-5xl mb-4">📄</div>
          {isDragActive ? (
            <p className="text-white text-lg font-semibold">
              Drop your resume here...
            </p>
          ) : (
            <>
              <p className="text-white text-lg font-semibold mb-2">
                Drag and drop your resume here
              </p>
              <p className="text-gray-200">or click to select a file</p>
              <p className="text-gray-300 text-sm mt-2">
                Supported formats: PDF, DOCX (Max 10MB)
              </p>
            </>
          )}
        </div>

        {uploadProgress > 0 && uploadProgress < 100 && (
          <div className="mt-6">
            <div className="w-full bg-white/20 rounded-full h-2">
              <div
                className="bg-white h-2 rounded-full transition-all"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <p className="text-white text-center mt-2">{uploadProgress}%</p>
          </div>
        )}

        {uploadProgress === 100 && (
          <div className="mt-6 text-center">
            <p className="text-green-300 text-lg font-semibold">
              Upload complete! Redirecting...
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
