# Developer Documentation

## Tech Stack

**Frontend**

- Vue3 using the composition API.
- Vuetify.js, which is a UI Components Library for Vue
- TypeScript
- Vite
- Pinia for state management

**Backend**

- Django, using the Django REST Framework
- Postgresql for the database
- Nginx as a reverse proxy

**Linting and Formatting**

- flake8 on the backend
- ESLint for linting on the frontend
- Prettier for formatting on the frontend

**Other**

- Docker
- Poetry for python package management
- Mailgun for sending emails
- Cloudflare for providing a SSL cerficate and DDoS protection
- DockerHub, a container registry
- Vercel for hosting the frontend
- Digital Ocean for hosting the backend

## Backend

As mentioned above, the website uses a Django Backend. This section will go into some more details.

### Administration Commands

### Entity Relationship Diagram

```mermaid
erDiagram
    User {
        int user_id PK
        string username UK
        string email UK
        string password
        string first_name
        string last_name
        string bio
        int total_points
        datetime birthdate
        string visibility
        string gender_identity
        string indigenous_identity
        int avatar
        boolean is_active
    }

    Challenge {
        int id PK
        string name
        string description
        string challenge_type
        int points
        int total_completions
    }

    Friendship {
        int id PK
        int requester FK
        int receiver FK
        string status
    }

    BingoGrid {
        int grid_id PK
        int challenge_1 FK "14 foreign keys omitted for brevity"
        int challenge_16 FK
        boolean is_active
    }

    TileInteraction {
        int user_id FK
        int grid FK
        int position
        string description
        image image
        boolean completed
        boolean consent
        datetime date_started
        datetime date_completed
    }

    TileInteraction }o--|| User : "does"
    TileInteraction }o--|| BingoGrid : "for"
    BingoGrid }o--|| Challenge  : "includes"
    Friendship }o--|| User   : "receives"
    Friendship }o--|| User   : "requests"

```
