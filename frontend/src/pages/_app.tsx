import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Resume Analyzer',
  description: 'Analyze and optimize your resume with AI',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
