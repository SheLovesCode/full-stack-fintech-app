export interface ExistingPayout {
    id: string;
    userId: string;
    amount: number;
    currency: string;
    status: 'pending' | 'completed' | 'failed';
    createdAt: string;
}

export interface NewPayout {
    amount: number;
    currency: string;
    idempotencyKey?: string; // Optional to ensure idempotent creation
}
