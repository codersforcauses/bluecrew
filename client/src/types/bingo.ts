import type { ChallengeStatus, ChallengeType } from './challenge'

export interface BingoData {
  challenge_points: number
  bingo_row: -1 | 0 | 1 | 2 | 3
  bingo_col: -1 | 0 | 1 | 2 | 3
  bingo_diag: -1 | 0 | 3
  full_bingo: boolean
  bingo_points: number
}

export interface BingoTileProps {
  title: string
  type: ChallengeType
  selected: boolean
  status: ChallengeStatus
  isExploding: boolean
  isInBingo: boolean
  interactionAllowed: boolean
}

export type BingoType = 'row' | 'column' | 'diagonal' | 'full'
