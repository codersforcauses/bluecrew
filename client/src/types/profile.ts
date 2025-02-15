export interface Challenge {
  title: string
  description: string
  type: 'Connect' | 'Understand' | 'Act'
  points: number
  image: string | null
  startDate: string
  finishDate: string | null
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
