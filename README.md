# TechBlog-X

To use this project follow the steps below

## Getting Started

### Prerequisites

- Python 3.x
- Django
- XAMPP (for MySQL database)

### Installation

### 1. **Clone the Repository:**

   ```bash
   git clone https://github.com/bilaalk079/Blog-X
   ```
 Install the Requirements:
### 2. Access the directory 
```bash
   cd Blog-X
   cd myproject
```
### 3. Install the project dependencies listed in the requirements.txt file.
```bash
pip install -r requirements.txt
```
### 4. **Database Setup with XAMPP**

### 5. **Download and install XAMPP.**

### 6. Start XAMPP Services:

### 7. Start Apache and MySQL from the XAMPP Control Panel.

### 8. Create the Database:

   Open a web browser and go to http://localhost/phpmyadmin/.
   
   Create a new database named your-database-name.
   
### 9. Update Database Settings:

   Ensure the following settings in settings.py:
   ```bash
      DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your-database-name',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
### 10. Run Migrations:
```bash
python manage.py makemigrations
```

### 11. Apply the migrations to set up the database schema:
 ```bash
  python manage.py migrate
```
### 12. Run the Development Server:
```bash
python manage.py runserver
```
### 13. Access the Project:

Open a web browser and go to http://127.0.0.1:8000/ to access the project.
 you can customize 'your-database-name' into any name of your choice.
 #To Register an admin navigate to http://127.0.0.1:8000/regadmin
 #You will need to enter a token which is available in the settings.py file


   
 
