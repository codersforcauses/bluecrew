export interface User {
    userId: number; 
    userName: string; 
    firstName: string; 
    lastName: string; 
    bio: string; 
    totalPoints: number; 
    email: string; 
    visibility: 0 | 1 | 2; 
    avatar: 0 | 1 | 2 | 3 | 4 | 5;
  }