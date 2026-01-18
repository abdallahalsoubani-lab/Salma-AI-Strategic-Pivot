/**
 * صفحة إدارة المستندات
 * Document Management Page
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Upload,
  FileText,
  File,
  Image,
  Table,
  Search,
  Trash2,
  Eye,
  RefreshCw,
  CheckCircle,
  XCircle,
  Clock,
  Loader2
} from 'lucide-react';
import { useDropzone } from 'react-dropzone';

interface Document {
  id: string;
  filename: string;
  type: string;
  size_bytes: number;
  status: string;
  page_count: number;
  chunk_count: number;
  language: string;
  uploaded_at: string;
}

const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setIsUploading(true);

    for (const file of acceptedFiles) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('/api/documents/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        });

        const data = await response.json();

        // Auto-process after upload
        await fetch(`/api/documents/${data.id}/process`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        // Refresh list
        fetchDocuments();
      } catch (error) {
        console.error('Upload error:', error);
      }
    }

    setIsUploading(false);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'image/*': ['.jpg', '.jpeg', '.png', '.tiff']
    }
  });

  const fetchDocuments = async () => {
    // Fetch documents from API
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    const response = await fetch('/api/documents/search', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: searchQuery })
    });

    const data = await response.json();
    setSearchResults(data.results);
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText className="w-5 h-5 text-red-500" />;
      case 'docx':
      case 'doc': return <FileText className="w-5 h-5 text-blue-500" />;
      case 'xlsx':
      case 'xls':
      case 'csv': return <Table className="w-5 h-5 text-green-500" />;
      case 'image': return <Image className="w-5 h-5 text-purple-500" />;
      default: return <File className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="flex items-center gap-1 text-green-600 bg-green-50 px-2 py-1 rounded-full text-xs">
            <CheckCircle className="w-3 h-3" />
            مكتمل
          </span>
        );
      case 'processing':
        return (
          <span className="flex items-center gap-1 text-blue-600 bg-blue-50 px-2 py-1 rounded-full text-xs">
            <Loader2 className="w-3 h-3 animate-spin" />
            قيد المعالجة
          </span>
        );
      case 'failed':
        return (
          <span className="flex items-center gap-1 text-red-600 bg-red-50 px-2 py-1 rounded-full text-xs">
            <XCircle className="w-3 h-3" />
            فشل
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1 text-gray-600 bg-gray-50 px-2 py-1 rounded-full text-xs">
            <Clock className="w-3 h-3" />
            بانتظار
          </span>
        );
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">المستندات</h1>
          <p className="text-gray-500">إدارة ومعالجة المستندات للبحث الذكي</p>
        </div>
      </div>

      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />

        {isUploading ? (
          <div className="flex flex-col items-center">
            <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
            <p className="text-gray-600">جاري رفع الملفات...</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <Upload className="w-12 h-12 text-gray-400 mb-4" />
            <p className="text-gray-600 mb-2">
              {isDragActive
                ? 'أفلت الملفات هنا...'
                : 'اسحب الملفات هنا أو انقر للاختيار'}
            </p>
            <p className="text-sm text-gray-400">
              PDF, Word, Excel, CSV, صور (حد أقصى 50MB)
            </p>
          </div>
        )}
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl p-4 border border-gray-200">
        <div className="flex items-center gap-4">
          <div className="relative flex-1">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="ابحث في محتوى المستندات..."
              className="w-full pr-10 pl-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            بحث
          </button>
        </div>

        {/* Search Results */}
        {searchResults.length > 0 && (
          <div className="mt-4 space-y-3">
            <h3 className="font-medium text-gray-700">نتائج البحث:</h3>
            {searchResults.map((result: any, idx) => (
              <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">{result.filename}</span>
                  <span className="text-sm text-gray-500">
                    تشابه: {(result.similarity * 100).toFixed(1)}%
                  </span>
                </div>
                <p className="text-sm text-gray-600">{result.content}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الملف</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">النوع</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الحجم</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الحالة</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الصفحات</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الأجزاء</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">التاريخ</th>
              <th className="px-6 py-4"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {documents.map((doc) => (
              <tr key={doc.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    {getFileIcon(doc.type)}
                    <span className="font-medium">{doc.filename}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">{doc.type.toUpperCase()}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{formatFileSize(doc.size_bytes)}</td>
                <td className="px-6 py-4">{getStatusBadge(doc.status)}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{doc.page_count || '-'}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{doc.chunk_count || '-'}</td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {new Date(doc.uploaded_at).toLocaleDateString('ar-SA')}
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <Eye className="w-4 h-4 text-gray-500" />
                    </button>
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Documents;
