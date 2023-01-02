# Django Shop

Django Shop is a web application that allows users to create their own online store and sell their products online. The application was built using the Django framework and utilizes a variety of features such as authentication, CRUD operations, and websockets.

## Getting Started

To get started with Django Shop, follow these steps:
#### Prerequisites

    Python 3.11
    Virtualenv (optional)

## Installing

Clone the repository:

`git clone https://github.com/oldhunterr/django-shop.git`

Navigate to the project directory:

`cd django-shop`

Create and activate a virtual environment (optional)

`virtualenv env`

Linux - Activate

`source env/bin/activate`

Windows - Activate

`env/Scripts/Activate`

Install the necessary packages:

`pip install -r requirements.txt`

Run the Django migrations:

`python manage.py migrate`

Run the development server:

`python manage.py runserver`

Open your web browser and navigate to http://localhost:8000 to view the application.

## Features
- User authentication and registration
- Product creation, updating and deleting by the owner
- Chat functionality between users on a product
- Realtime message updates using WebSockets
- Product search functionality
-  Responsive and user-friendly GUI using Bootstrap

## Usage

- Navigate to the home page and register or login to your account
- View all available products or add a new product from the dashboard
- View, update, or delete your products from the dashboard
- Click on a product to view the details and start a chat with the owner
- View all your chat rooms and messages in the chat rooms page
- Use the input field to send new messages in a chat room

### Contributing
------------
If you would like to contribute to Django Shop, please create a pull request with a detailed description of your changes.

### License

Django Shop is licensed under the MIT License.
