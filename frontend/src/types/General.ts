export interface PaginationParams {
    page?: number;   // Current page number (default 1)
    limit?: number;  // Items per page (default 10)
}

export interface PaginatedResponse<T> {
    items: T[];           // Array of items of type T
    total?: number;       // Total number of items (optional)
    page?: number;        // Current page (optional)
    limit?: number;       // Page size (optional)
    totalPages?: number;  // Total pages (optional)
}

export interface ApiResponse<T> {
    data: T;
    message?: string;     // Optional message from backend
    error?: string;       // Optional error message
}


export interface ApiError {
    message: string;
    status?: number;
    details?: any;       // Optional extra info
}
