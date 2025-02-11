import type { User } from '@/types/user'

interface Challenge {
  title: string
  description: string
  type: 'Connect' | 'Understand' | 'Act'
  points: number
  startDate: string
  finishDate?: string
  status: 'Complete' | 'In Progress'
}

interface MockUser extends User {
  challenges: Challenge[]
}

export const mockUsers: Record<string, MockUser> = {
  johndoe: {
    userId: 1,
    userName: 'johndoe',
    firstName: 'John',
    lastName: 'Doe',
    bio: 'Environmental enthusiast passionate about ocean conservation. 🌊',
    totalPoints: 3450,
    email: 'john.doe@example.com',
    visibility: 1,
    avatar: 1,
    isSuperuser: false,
    challenges: [
      {
        title: 'Beach Clean-up Champion',
        description: 'Lead a team of volunteers in cleaning up Ocean Beach',
        type: 'Act',
        points: 500,
        startDate: '27/11/2024 10:27pm',
        finishDate: '27/11/2024 11:27pm',
        status: 'Complete',
      },
      {
        title: 'Marine Life Documentation',
        description: 'Photograph and identify local marine species',
        type: 'Connect',
        points: 300,
        startDate: '28/11/2024 09:00am',
        finishDate: '28/11/2024 11:00am',
        status: 'Complete',
      },
      {
        title: 'Ocean Conservation Workshop',
        description: 'Participate in marine ecosystem workshop',
        type: 'Understand',
        points: 400,
        startDate: '29/11/2024 02:00pm',
        status: 'In Progress',
      },
    ],
  },
  marinebiologist: {
    userId: 2,
    userName: 'marinebiologist',
    firstName: 'Emma',
    lastName: 'Wilson',
    bio: 'Marine Biology PhD Student | Coral Reef Research 🐠',
    totalPoints: 4200,
    email: 'emma.wilson@example.com',
    visibility: 2,
    avatar: 2,
    isSuperuser: false,
    challenges: [
      {
        title: 'Coral Health Assessment',
        description: 'Conduct detailed survey of coral reef health',
        type: 'Connect',
        points: 600,
        startDate: '25/11/2024 08:00am',
        finishDate: '25/11/2024 02:00pm',
        status: 'Complete',
      },
      {
        title: 'Public Education Session',
        description: 'Host educational session about marine conservation',
        type: 'Act',
        points: 400,
        startDate: '26/11/2024 03:00pm',
        finishDate: '26/11/2024 05:00pm',
        status: 'Complete',
      },
      {
        title: 'Research Data Analysis',
        description: 'Analyze collected marine ecosystem data',
        type: 'Understand',
        points: 500,
        startDate: '29/11/2024 10:00am',
        status: 'In Progress',
      },
    ],
  },
}

export const defaultUserData: MockUser = {
  userId: 0,
  userName: 'Username',
  firstName: 'Firstname',
  lastName: 'Lastname',
  bio: 'This is a bio.',
  totalPoints: 0,
  email: '',
  visibility: 1,
  avatar: 0,
  isSuperuser: false,
  challenges: [],
}
