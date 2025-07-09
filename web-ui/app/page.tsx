'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Download, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

interface GenerationResult {
  status: string;
  message: string;
  download_url?: string;
  file_path?: string;
  article_content?: string; // Added for displaying article content
}

export default function Home() {
  const [topic, setTopic] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<GenerationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-content', {
        topic: topic.trim(),
        output_format: 'pdf'
      });

      setResult(response.data);
    } catch (_err: unknown) {
      // TypeScript: _err is unknown, so we need to type guard
      if (axios.isAxiosError(_err)) {
        setError(_err.response?.data?.detail || 'Failed to generate content. Please try again.');
      } else {
        setError('Failed to generate content. Please try again.');
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = async (downloadUrl: string) => {
    try {
      const response = await axios.get(`http://localhost:8000${downloadUrl}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'generated-content.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      setError('Failed to download file. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Content Generator
          </h1>
          <p className="text-lg text-gray-600">
            Generate high-quality articles and content using AI research and writing agents
          </p>
        </div>

        {/* Main Form */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Generate New Content
            </CardTitle>
            <CardDescription>
              Enter a topic and our AI agents will research and write comprehensive content for you.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                  Topic
                </label>
                <Textarea
                  id="topic"
                  placeholder="Enter your topic here (e.g., 'The Future of Artificial Intelligence', 'Climate Change Solutions', 'Digital Marketing Trends')"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="min-h-[100px]"
                  disabled={isGenerating}
                />
              </div>
              
              <Button 
                type="submit" 
                disabled={isGenerating || !topic.trim()}
                className="w-full"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Content...
                  </>
                ) : (
                  <>
                    <FileText className="mr-2 h-4 w-4" />
                    Generate Content
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Error Alert */}
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Success Result */}
        {result && result.status === 'success' && (
          <Card className="border-green-200 bg-green-50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-800">
                <CheckCircle className="h-5 w-5" />
                Content Generated Successfully!
              </CardTitle>
              <CardDescription className="text-green-700">
                {result.message}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {/* Display the article content if available */}
              {result.article_content && (
                <div className="mb-4 p-4 bg-white rounded shadow text-gray-800 whitespace-pre-line text-base font-serif">
                  {result.article_content}
                </div>
              )}
              <div className="flex items-center justify-between">
                <div className="text-sm text-green-700">
                  Your content has been generated and saved as a PDF file.
                </div>
                {result.download_url && (
                  <Button
                    onClick={() => handleDownload(result.download_url!)}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    <Download className="mr-2 h-4 w-4" />
                    Download PDF
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Instructions */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>How it works</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 text-sm text-gray-600">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-medium">
                  1
                </div>
                <div>
                  <strong>Research Phase:</strong> Our AI research agent gathers comprehensive information about your topic from reliable sources.
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-medium">
                  2
                </div>
                <div>
                  <strong>Writing Phase:</strong> Our AI writing agent creates well-structured, engaging content based on the research findings.
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-medium">
                  3
                </div>
                <div>
                  <strong>Output:</strong> The final content is formatted as a professional PDF document ready for download.
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}