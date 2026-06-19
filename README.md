# EcoWaste Management System

## Abstract
EcoWaste Management is a comprehensive, web-based platform designed to modernize and streamline urban waste collection and recycling processes. By bridging the gap between municipal administrators, collection staff, recycling centers, and everyday citizens, the system fosters a cleaner and more sustainable environment. It features real-time waste bin status tracking, on-demand pickup requests, issue reporting, and automated task assignments. The integrated dashboard ensures that all stakeholders have access to role-specific data and tools, ultimately optimizing resource allocation, reducing environmental hazards, and promoting community engagement in waste management.

## Features by Role

### 👩‍💼 Admin
- **Dashboard Overview:** Monitor total users, staff, registered bins, and pickup requests.
- **User & Staff Management:** Approve or reject staff registrations and view registered users.
- **Bin Management:** Add new waste bins to the system and track their fill levels and statuses.
- **Pickup Tasks:** View all citizen pickup requests and assign them to available staff members.
- **Notifications:** Broadcast announcements and alerts to all users, specific roles, or staff members.

### 👷 Staff (Waste Collectors)
- **Task Management:** View assigned collection tasks and update their statuses (e.g., collected, pending) along with notes.
- **Issue Reporting:** Quickly report damaged, overflowing, or malfunctioning bins encountered during routes.
- **Alerts:** Receive notifications from the admin regarding schedules or emergencies.

### ♻️ Recycling Center
- **Record Management:** Log and update the processing status of collected waste batches.
- **Capacity & Processing:** Track processed quantities and maintain detailed recycling records.
- **Alerts:** Stay informed with platform-wide or center-specific announcements.

### 👤 Citizen / User
- **Bin Locator:** View the location, waste type, capacity, and current fill status of all nearby bins.
- **Pickup Requests:** Schedule doorstep waste collection and track the history of previous requests.
- **Report Issues:** Notify authorities about damaged or overflowing public bins.
- **Notifications:** Receive updates on pickup schedules and general waste management alerts.

## Technology Stack
- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3 (Custom UI), Vanilla JavaScript
- **Database:** SQLite (Default for Django, easily upgradeable to PostgreSQL/MySQL)
- **Icons & Fonts:** FontAwesome, Google Fonts (Inter, Outfit)

## Installation and Setup

1. **Clone or Download the Repository**
   Ensure you are in the project's root directory.

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv env
   source env/Scripts/activate  # For Windows
   # or
   source env/bin/activate      # For macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install django
   # Add any other specific libraries you may have used
   ```

4. **Apply Database Migrations**
   ```bash
   cd waste
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## Future Enhancements
- IoT integration for automatic bin fill-level updates.
- GPS tracking for collection vehicles.
- Gamification/Reward system for citizens actively participating in recycling.
a