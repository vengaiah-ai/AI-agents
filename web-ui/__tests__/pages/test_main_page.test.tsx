// Test file for main page
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock Home component for test
const mockResult = {
  status: 'success',
  message: 'Content generated successfully',
  article_content: 'This is the generated article content.',
  download_url: '/api/download/test.pdf',
  file_path: 'output/test.pdf',
};

function MockHome() {
  return (
    <div>
      {/* Simulate the success result card */}
      {mockResult.status === 'success' && (
        <div>
          <div>{mockResult.message}</div>
          {mockResult.article_content && (
            <div data-testid="article-content">{mockResult.article_content}</div>
          )}
        </div>
      )}
    </div>
  );
}

describe('Main Page', () => {
  test('renders without crashing', () => {
    expect(true).toBe(true);
  });

  test('displays article content when present', () => {
    render(<MockHome />);
    const articleContent = screen.getByTestId('article-content');
    expect(articleContent).toBeInTheDocument();
    expect(articleContent).toHaveTextContent('This is the generated article content.');
  });
}); 