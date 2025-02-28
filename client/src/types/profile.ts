export interface Challenge {
  title: string
  description: string
  type: 'Connect' | 'Understand' | 'Act'
  points: number
  image: string | null
  startDate: string
  finishDate?: string
  imageDescription?: string
  completed: boolean
}

export interface UserProfile {
  avatar: number
  username: string
  firstName: string
  lastName: string
  bio: string
  totalPoints: number
}
