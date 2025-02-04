export interface User {
  userId: number
  userName: string
  firstName: string
  lastName: string
  bio: string
  totalPoints: number
  email: string
  visibility: 0 | 1 | 2
  avatar: 0 | 1 | 2 | 3 | 4 | 5
  isSuperuser: boolean
}

export interface UserRegistrationForm {
  username: string
  email: string
  firstName: string
  lastName: string
  dateOfBirth: string
  genderId: string
  indigenousTIS: string
  password: string
  confirmPassword: string
}

export interface UserRegistrationFormFields {
  formAttribute: keyof UserRegistrationForm
  fieldName: string
  fieldPlaceholder: string
  errorMessages: string
  fieldType: 'text' | 'email' | 'password' | 'date'
  dropDownItems?: string[]
}
