export interface UserProfile {
    id: string;
    oauthId: string;
    name: string;
    email: string;
    avatarUrl?: string;
    provider: 'google' | 'github';
}
