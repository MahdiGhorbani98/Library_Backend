Active venv environment with: .\venv\Scripts\Activate.ps1 
Run project with: uvicorn app.main:app --reload

# * best sorting in CRUD operations:
 # GET all (read list)
 # GET specific (read detail)
 # POST (create)
 # PUT (update)
 # DELETE (remove)

# * why we don't use async in routes?
# Recommendation:
# If traffic is low/medium: Keep synchronous(easier, less complex)
# If you want async: Switch your database to async driver + update all endpoints

MEMBERS:
POST   /members/              - Create member (✓ exists)
GET    /members/              - List all members (✓ exists)
GET    /members/{id}          - Get specific member [NEW]
PUT    /members/{id}          - Update member (is_borrowing, email, username) [NEW]
DELETE /members/{id}          - Soft delete member (optional) [NEW]

BOOKS:
POST   /books/                - Add new book to library [NEW]
GET    /books/                - List books with filters (category, author, language, is_available) [NEW]
GET    /books/{id}            - Get specific book with authors & categories [NEW]
PUT    /books/{id}            - Update book (is_available, title, year, etc.) [NEW]
DELETE /books/{id}            - Soft delete book (optional) [NEW]

BORROWINGS:
POST   /borrowings/           - Create borrowing request (member borrows book) [NEW]
GET    /borrowings/           - List borrowings with filters (member_id, status, overdue) [NEW]
GET    /borrowings/{id}       - Get specific borrowing details [NEW]
PUT    /borrowings/{id}       - Update borrowing (return book, extend due_date, change status) [NEW]
DELETE /borrowings/{id}       - Cancel borrowing request (optional) [NEW]

AUTHORS & CATEGORIES:
POST   /authors/              - Create author [NEW]
GET    /authors/              - List all authors [NEW]

POST   /categories/           - Create category [NEW]
GET    /categories/           - List all categories [NEW]