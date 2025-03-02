// Type definitions for challenge-related data
export type ChallengeType = 'understand' | 'connect' | 'act'
export type ChallengeStatus = 'not started' | 'started' | 'completed'

// Interface for challenge information
export interface ChallengeInfo {
  title: string
  points: number
  type: ChallengeType
  description: string
  status: ChallengeStatus
}

export interface ChallengeInfoAPI {
  name: string
  points: number
  challenge_type: ChallengeType
  description: string
  status: ChallengeStatus
}
