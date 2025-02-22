// Type definitions for challenge-related data
export type ChallengeType = 'understand' | 'connect' | 'act'
export type ChallengeStatus = 'not started' | 'started' | 'completed' | 'bingo'

// Interface for challenge information
export interface ChallengeInfo {
  title: string
  points: number
  type: ChallengeType
  description: string
  status: ChallengeStatus
}
